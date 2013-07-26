import sys
import os
import datetime, json
from os.path import join
from subprocess import call, Popen, PIPE

from crisis_app import views
from views import make_parent, add_child, make_json, parse, querify, \
	mark_urls, youtube_to_embed

from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import models
from minixsv.pyxsval import parseAndValidateXmlInputString

from crisis_app.converters import to_xml, to_db
from crisis_app.models import Event, Organization, Person, Embed
from crisis_app.management.commands.validate import XSD

XML_FIXTURE_PATH = 'crisis_app/fixtures/xml'
XML = dict((f.split('.')[0], open(join(XML_FIXTURE_PATH, f)).read().strip())
	for f in os.listdir(XML_FIXTURE_PATH))

class UsefulTestCase(TestCase):

	def _clear_db(self):
		management.call_command('flush', load_initial_data=False,
				interactive=False)

	def _reset_db(self):
		management.call_command('flush', interactive=False)


class ToJsonTestCase(TestCase):

	def test_make_parent_1(self):
		p = make_parent("test", "color")
		self.assertEqual(p['id'], "test")
		self.assertEqual(p['data']['$color'], "color")

	def test_make_parent_2(self):
		p = make_parent(1, "color")
		self.assertEqual(p['id'], 1)
		self.assertEqual(p['data']['$color'], "color")
		
	def test_make_parent_3(self):
		p = make_parent((1, 2), [1, 2, 3])
		self.assertEqual(p['id'], (1, 2))
		self.assertEqual(p['data']['$color'], [1, 2, 3])		

	def test_add_child_1(self):
		p = make_parent("test", "color")
		add_child(p, 'child', 'color', 0, [], 'desc')
		self.assertEqual(p['children'][0]['id'], 'child')
		self.assertEqual(p['children'][0]['data']['$color'], 'color')
		self.assertEqual(p['children'][0]['data']['$area'], 0)
		self.assertEqual(p['children'][0]['data']['popularity'], 0)
		self.assertEqual(p['children'][0]['data']['image'], 'None')
		self.assertEqual(p['children'][0]['data']['description'], 'desc')

	def test_add_child_2(self):
		p = make_parent("test", "color")
		add_child(p, 'child', 'color', 0, [], 'desc')
		add_child(p, 'child', 'color', 0, [1, 2, 3], 'desc')
		self.assertEqual(p['children'][1]['id'], 'child')
		self.assertEqual(p['children'][1]['data']['$color'], 'color')
		self.assertEqual(p['children'][1]['data']['$area'], 0)
		self.assertEqual(p['children'][1]['data']['popularity'], 0)
		self.assertEqual(p['children'][1]['data']['image'], '1')
		self.assertEqual(p['children'][1]['data']['description'], 'desc')

	def test_make_json_1(self):
		j = make_json(3)
		p = json.loads(j)
		self.assertEqual(p["id"], "Crisis")
		self.assertEqual(p['children'][0]['id'], "Events")
		self.assertEqual(p['children'][1]['id'], "People")
		self.assertEqual(p['children'][2]['id'], "Organizations")

class ToXmlTestCase(TestCase):
	fixtures = ['test_data.json']

	def test_export(self):
		# just a sanity check to make sure we're working w/ the correct data
		self.assertEqual(len(Event.objects.all()), 1)

		# the real test
		self.assertEqual(to_xml.convert().strip(), XML['initial_data'])

	def test_export_validation(self):
		xml = to_xml.convert()
		ret = parseAndValidateXmlInputString(inputText=xml, xsdText=XSD)
		self.assertTrue(not not ret)

class ToDbTestCase(UsefulTestCase):

	def test_import(self):
		self._clear_db()
		self.assertEqual(len(Event.objects.all()), 0)
		to_db.convert(XML['initial_data'])
		events = Event.objects.all()
		people = Person.objects.all()
		orgs = Organization.objects.all()

		self.assertEqual(len(events), 1)
		self.assertEqual(len(events[0].organization_set.all()), 1)
		self.assertEqual(len(events[0].person_set.all()), 1)
		self.assertEqual(len(events[0].embed_set.all()), 8)

		self.assertEqual(len(people), 1)
		self.assertEqual(len(people[0].event.all()), 1)
		self.assertEqual(len(people[0].organization_set.all()), 1)
		self.assertEqual(len(people[0].embed_set.all()), 10)

		self.assertEqual(len(orgs), 1)
		self.assertEqual(len(orgs[0].event.all()), 1)
		self.assertEqual(len(orgs[0].person.all()), 1)
		self.assertEqual(len(orgs[0].embed_set.all()), 10)

		self._reset_db()

class ImportExportTest(UsefulTestCase):
	PWD = '123'

	def setUp(self):
		self._clear_db()
		self.xml = open(join(XML_FIXTURE_PATH, 'initial_data.xml'))
		self.user = User.objects.create_user('admin', 'dont@talk.to.me',
				self.PWD)

	def tearDown(self):
		self.client.logout()
		self.user.delete()
		self.xml.close()
		self._reset_db()

	def test_xml_redirect_to_login(self):
		response = self.client.get('/upload_xml')
		self.assertEqual(response.status_code, 302)

	def test_xml_submission(self):
		self.client.login(username=self.user.username, password=self.PWD)
		response = self.client.get('/upload_xml')
		self.assertEqual(response.status_code, 200)

		response = self.client.post('/upload_xml', {
			'xml': self.xml,
			'Submit': 'Submit'
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], 'http://testserver/xml')

		response = self.client.get('/xml')
		try:
			self.assertEqual(response.content.strip(),
				XML['initial_data'].strip())
		except AssertionError as e:
			# write the wrong file out to disk for inspection from the cmd line
			open('invalid_response.xml', 'w').write(response.content)
			raise e
			
class RegexTestCase(UsefulTestCase):
	def test_youtube_working_embed(self):
		testString_1 = youtube_to_embed("http://www.youtube.com/watch?v=RUKsyA_z7n8","youtube_1")
		testString_2 = youtube_to_embed("http://www.youtube.com/watch?v=nBzHCVv5GeQ","youtube_2")
		testString_3 = youtube_to_embed("http://www.youtube.com/watch?v=5gg1hkd5wnI","youtube_3")

		assert testString_1 == '<iframe width="560" height="315" src="http://www.youtube.com/embed/RUKsyA_z7n8" frameborder="0" name="youtube_1?wmode=opaque" allowfullscreen></iframe>'

		assert testString_2 == '<iframe width="560" height="315" src="http://www.youtube.com/embed/nBzHCVv5GeQ" frameborder="0" name="youtube_2?wmode=opaque" allowfullscreen></iframe>'

		assert testString_3 == '<iframe width="560" height="315" src="http://www.youtube.com/embed/5gg1hkd5wnI" frameborder="0" name="youtube_3?wmode=opaque" allowfullscreen></iframe>'

	def test_youtube_semiWorking_embed(self):
		testString_1 = youtube_to_embed("http://vimeo.com/13595568","youtube_1")
		testString_2 = youtube_to_embed("http://vimeo.com/1532967","youtube_2")
		testString_3 = youtube_to_embed("http://www.youtube.com/vatican","youtube_3")

		assert testString_1 == '<a href="http://vimeo.com/13595568">youtube_1 (Vimeo)</a><br />'

		assert testString_2 == '<a href="http://vimeo.com/1532967">youtube_2 (Vimeo)</a><br />'

		assert testString_3 == '<a href="http://www.youtube.com/vatican">youtube_3 (Youtube)</a><br />'

	def test_youtube_notWorking_embed(self):
		testString_1 = youtube_to_embed("http://youtu.be/_iNBKlBcXkY","youtube_1")
		testString_2 = youtube_to_embed("http://commons.wikimedia.org/wiki/Obama_Administration_weekly_video_addresses","youtube_2")
		testString_3 = youtube_to_embed("http://www.tepco.co.jp/en/news/library/movie-01e.html","youtube_3")

		assert testString_1 == '<a href="http://youtu.be/_iNBKlBcXkY">youtube_1</a><br />'

		assert testString_2 == '<a href="http://commons.wikimedia.org/wiki/Obama_Administration_weekly_video_addresses">youtube_2</a><br />'

		assert testString_3 == '<a href="http://www.tepco.co.jp/en/news/library/movie-01e.html">youtube_3</a><br />'

	def test_markurls(self):
		testString_1 = mark_urls('tapkorea@gmail.com')
		testString_2 = mark_urls('http://www.valvesoftware.com/')
		testString_3 = mark_urls('URL: http://www.dfps.state.tx.us/child_protection/ address: 701 W. 51st St. Austin, Texas 78751 Phone: (512) 438-4800')
		testString_4 = mark_urls('FLDS.org')
		testString_5 = mark_urls('Phone: 1-800-FOR-KIDS')
		testString_6 = mark_urls('Phone: 720-898-5900 URL: http://www.communityfirstfoundation.org/index.cfm Address: 6870 West 52nd Avenue, Suite 103 Arvada, Colorado 80002')
		testString_7 = mark_urls('The Salvation Army National Headquarters 615 Slaters Lane P.O. Box 269 Alexandria, VA 22313')
		testString_8 = mark_urls('http://www.oref.org.il/International/14-en/PAKAR.aspx')
		testString_9 = mark_urls('(405) 235-3313')
		testString_10 = mark_urls('http://www.redcross.org/contact-us/general-inquiry')

		assert testString_1 == '<a href="mailto:tapkorea@gmail.com" target="_blank">tapkorea@gmail.com<span></span></a>'

		assert testString_2 == '<a href="http://www.valvesoftware.com/" target="_blank">http://www.valvesoftware.com/<span></span></a>'

		assert testString_3 == 'URL: <a href="http://www.dfps.state.tx.us/child_protection/" target="_blank">http://www.dfps.state.tx.us/child_protection/<span></span></a> address: 701 W. 51st St. Austin, Texas 78751 Phone: (512) 438-4800'

		assert testString_4 == '<a href="http://FLDS.org" target="_blank">FLDS.org<span></span></a>'

		assert testString_5 == 'Phone: 1-800-FOR-KIDS'

		assert testString_6 == 'Phone: 720-898-5900 URL: <a href="http://www.communityfirstfoundation.org/index.cfm" target="_blank">http://www.communityfirstfoundation.org/index.cfm<span></span></a> Address: 6870 West 52nd Avenue, Suite 103 Arvada, Colorado 80002'

		assert testString_7 == 'The Salvation Army National Headquarters 615 Slaters Lane P.O. Box 269 Alexandria, VA 22313'

		assert testString_8 == '<a href="http://www.oref.org.il/International/14-en/PAKAR.aspx" target="_blank">http://www.oref.org.il/International/14-en/PAKAR.aspx<span></span></a>'

		assert testString_9 == '(405) 235-3313'

		assert testString_10 == '<a href="http://www.redcross.org/contact-us/general-inquiry" target="_blank">http://www.redcross.org/contact-us/general-inquiry<span></span></a>'


class ParseQuerifyTest(TestCase):
	fixtures = ['test_data.json']

	def test_parse_1(self):
		inp = "\"Barack Obama\" US President"
		out = parse(inp)
		self.assertEqual(out[0], "Barack Obama")
		self.assertEqual(out[1], "US")
		self.assertEqual(out[2], "President")

	def test_parse_2(self):
		self.assertEqual(parse("\"Barack Obama\" US President")[0], "Barack Obama")
		self.assertEqual(parse("\"Barack Obama\" US President")[1], "US")
		self.assertEqual(parse("\"Barack Obama\" US President")[2], "President")

	def test_parse_3(self):
		out = parse("\"Barack Obama\" US President")
		assert type(out) is list

	def test_parse_4(self):
		out = parse("\"Barack Obama\" US President")
		self.assertEqual(len(out), 3)

	def test_parse_5(self):
		out = parse("\"Barack Obama\" US President")
		assert type(out[0]) is str
		assert type(out[1]) is str
		assert type(out[2]) is str

	def test_querify_1(self):
		inp = parse("\"Barack Obama\" US President")
		assert type(querify(inp, ["column1", "column2", "column3"])) is models.query_utils.Q

	def test_querify_2(self):
		inp = parse("\"Barack Obama\" US Pres POTUS")
		self.assertEqual(len(querify(inp, ["column1", "column2", "column3"])),4) #len should be the number of things being parsed

	def test_db_query(self):
		inp = parse("Sandy")
		quer = querify(inp,["id","name","kind"])
		self.assertEqual(str(Event.objects.filter(quer)),"[<Event: Hurricane Sandy>]")
