"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from minixsv import pyxsval
from genxmlif import GenXmlIfError
from models import Crisis, Person, Org, Li, Common, Relations, populate_li
from loadModels import validate, populate_crisis, populate_person, populate_org, populate_models, populate_common
from unloadModels import *
import xml.etree.ElementTree as ET
from django.test.client import Client
from views import passwordValidate
from getDbModel import getCrisis, getPerson, getOrg, getCrisisIDs, getOrgIDs, getPeopleIDs


#xsd = open('wcdb/WorldCrises.xsd.xml', 'r')
#psvi = pyxsval.parseAndValidate("wcdb/temp.xml", "wcdb/WorldCrises.xsd.xml",
#	xmlIfClass=pyxsval.XMLIF_ELEMENTTREE)

class ModelsCrisisTest(TestCase):

	"""
	Contains the unit tests for models.py, the file where we define our Django files. These unit 
	tests mostly test that the models' populate methods work.
	"""
#--------------------------------------------#
#-----Unit Tests for functions from models.py
#--------------------------------------------#



	#---------------------------------------#
	#-----test_li_populate

	def test_li_populate0(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp, "PER_MMORSI", "Videos")
		self.assertEqual(temp_li.href, "href_stuff")
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	def test_li_populate1(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.set("embed", "embed_stuff")
		temp.set("text", "text_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp, "PER_BRANDO", "Images")
		self.assertEqual(temp_li.model_id, "PER_BRANDO")
		self.assertEqual(temp_li.kind, "Images")
		self.assertEqual(temp_li.text, "text_stuff")
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	def test_li_populate2(self):
		temp      = ET.Element('li')
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp, "PER_SHANGU", "ExternalLinks")
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")
		self.assertEqual(temp_li.kind, "ExternalLinks")

	#---------------------------------------#
	#-----test_populate_li

	def test_populate_li0(self):
		li_string = "<Crisis ID=\"CRI_NSAWRT\" Name=\"NSAWiretapping\"><People><Person ID=\"PER_ESNWDN\"/></People><Organizations><Org ID=\"ORG_NSAAAA\"/></Organizations><WaysToHelp><li href = \"http://www.restorethefourth.net/protests/\">Restore The Fourth</li></WaysToHelp></Crisis>"
		e_root    = ET.fromstring(li_string)
		populate_li(e_root, "CRI_NSAWRT", "WaysToHelp")
		li_list = Li.objects.filter(model_id = "CRI_NSAWRT")
		self.assertEqual(li_list[0].href, "http://www.restorethefourth.net/protests/")

	def test_populate_li1(self):
		li_string = "<Crisis ID=\"CRI_NSAWRT\" Name=\"NSAWiretapping\"><People><Person ID=\"PER_ESNWDN\"/></People><Organizations><Org ID=\"ORG_NSAAAA\"/></Organizations><WaysToHelp><li href = \"http://www.restorethefourth.net/protests/\">Restore The Fourth</li></WaysToHelp></Crisis>"
		e_root    = ET.fromstring(li_string)
		populate_li(e_root, "CRI_NSAWRT", "WaysToHelp")
		li_list = Li.objects.filter(model_id = "CRI_NSAWRT")
		self.assertEqual(li_list[0].floating_text, "Restore The Fourth")

	def test_populate_li2(self):
		li_string = "<Crisis ID=\"CRI_JOEJOE\" Name=\"Joe Johnson's contract\"><People><Person ID=\"PER_JOEJOE\"/></People><Organizations><Org ID=\"ORG_BRKNET\"/></Organizations><WaysToHelp><li href = \"http://www.joejohnsonsucks.net/protests/\">Joe Johnson's contract probably violates the Geneva Convention</li></WaysToHelp></Crisis>"
		e_root    = ET.fromstring(li_string)
		populate_li(e_root, "CRI_JOEJOE", "WaysToHelp")
		li_list = Li.objects.filter(model_id = "CRI_JOEJOE")
		self.assertEqual(li_list[0].href, "http://www.joejohnsonsucks.net/protests/")
		self.assertEqual(li_list[0].floating_text, "Joe Johnson's contract probably violates the Geneva Convention")

	#---------------------------------------#
	#-----test_common_populate

	def test_common_populate0(self):
		temp_com   = Common()
		xml_string = "<Common><Citations><li>The Hindustan Times</li></Citations><ExternalLinks><li href=\"http://en.wikipedia.org/wiki/2013_North_India_floods\">Wikipedia</li></ExternalLinks><Images><li embed=\"http://timesofindia.indiatimes.com/photo/15357310.cms\" /></Images><Videos><li embed=\"//www.youtube.com/embed/qV3s7Sa6B6w\" /></Videos><Maps><li embed=\"https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed\" /></Maps><Feeds><li embed=\"[WHATEVER A FEED URL LOOKS LIKE]\" /></Feeds><Summary>Lorem ipsum...</Summary></Common>"
		e_root     = ET.fromstring(xml_string)
		temp       = Common()
		temp.populate(e_root, "CRI_JOEJOE")


		populate_li(e_root, "CRI_JOEJOE", "Feeds")
		li_list = Li.objects.filter(model_id = "CRI_JOEJOE")
		common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
						'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
						'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
						'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		for a in li_list :
			common_dict[a.kind].append(a)
		self.assertEqual(common_dict['Citations'][0].floating_text, "The Hindustan Times")

	def test_common_populate1(self):
		temp_com   = Common()
		xml_string = "<Common><Citations><li>The Hindustan Times</li></Citations><ExternalLinks><li href=\"http://en.wikipedia.org/wiki/2013_North_India_floods\">Wikipedia</li></ExternalLinks><Images><li embed=\"http://timesofindia.indiatimes.com/photo/15357310.cms\" /></Images><Videos><li embed=\"//www.youtube.com/embed/qV3s7Sa6B6w\" /></Videos><Maps><li embed=\"https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed\" /></Maps><Feeds><li embed=\"[WHATEVER A FEED URL LOOKS LIKE]\" /></Feeds><Summary>Lorem ipsum...</Summary></Common>"
		e_root     = ET.fromstring(xml_string)
		temp       = Common()
		temp.populate(e_root, "CRI_JOEJOE")


		populate_li(e_root, "CRI_JOEJOE", "Feeds")
		li_list = Li.objects.filter(model_id = "CRI_JOEJOE")
		common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
						'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
						'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
						'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		for a in li_list :
			common_dict[a.kind].append(a)
		self.assertEqual(common_dict['ExternalLinks'][0].href, "http://en.wikipedia.org/wiki/2013_North_India_floods")
	
	def test_common_populate2(self):
		temp_com   = Common()
		xml_string = "<Common><Citations><li>The Hindustan Times</li></Citations><ExternalLinks><li href=\"http://en.wikipedia.org/wiki/2013_North_India_floods\">Wikipedia</li></ExternalLinks><Images><li embed=\"http://timesofindia.indiatimes.com/photo/15357310.cms\" /></Images><Videos><li embed=\"//www.youtube.com/embed/qV3s7Sa6B6w\" /></Videos><Maps><li embed=\"https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed\" /></Maps><Feeds><li embed=\"[WHATEVER A FEED URL LOOKS LIKE]\" /></Feeds><Summary>Lorem ipsum...</Summary></Common>"
		e_root     = ET.fromstring(xml_string)
		temp       = Common()
		temp.populate(e_root, "CRI_JOEJOE")


		populate_li(e_root, "CRI_JOEJOE", "Feeds")
		li_list = Li.objects.filter(model_id = "CRI_JOEJOE")
		common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
						'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
						'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
						'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		for a in li_list :
			common_dict[a.kind].append(a)
		self.assertEqual(common_dict['Images'][0].embed, "http://timesofindia.indiatimes.com/photo/15357310.cms")
		self.assertEqual(common_dict['Videos'][0].embed, "//www.youtube.com/embed/qV3s7Sa6B6w")
		self.assertEqual(common_dict['Maps'][0].embed, "https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&sspn=3.2522150867582833,7.2072687770004205&t=m&q=uttarakhand&dg=opt&ie=UTF8&hq=&hnear=Uttarakhand,+India&ll=30.066753,79.0193&spn=2.77128,5.07019&z=8&output=embed")
		


	#---------------------------------------#
	#-----test_populate_common

	def test_populate_common0(self):
		temp_com   = Common()
		xml_string = "<Crisis ID=\"CRI_DTHNTE\" Name=\"People mysteriously dying\"><People><Person ID=\"PER_KIRAAA\"/></People><Organizations><Org ID=\"ORG_POLICE\"/></Organizations><Common><Citations><li>Kyoto News Network</li></Citations><ExternalLinks><li href=\"http://myanimelist.net/anime/1535/Death_Note\">Wikipedia</li></ExternalLinks><Images><li embed=\"http://i0.kym-cdn.com/photos/images/original/000/243/591/ef4.jpg\" /></Images><Videos><li embed=\"//www.youtube.com/embed/qV3s7Sa6B6w\" /></Videos><Maps><li embed=\"https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed\" /></Maps><Feeds><li embed=\"[WHATEVER A FEED URL LOOKS LIKE]\" /></Feeds><Summary>Lorem ipsum...</Summary></Common></Crisis>"
		e_root     = ET.fromstring(xml_string)
		temp_crisis = Crisis
		populate_common(e_root, "CRI_DTHNTE", temp_crisis)

		li_list = Li.objects.filter(model_id = "CRI_DTHNTE")
		common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
						'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
						'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
						'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		for a in li_list :
			common_dict[a.kind].append(a)
		self.assertEqual(common_dict['Citations'][0].floating_text, "Kyoto News Network")

	def test_populate_common1(self):
		temp_com   = Common()
		xml_string = "<Crisis ID=\"CRI_DTHNTE\" Name=\"People mysteriously dying\"><People><Person ID=\"PER_KIRAAA\"/></People><Organizations><Org ID=\"ORG_POLICE\"/></Organizations><Common><Citations><li>Kyoto News Network</li></Citations><ExternalLinks><li href=\"http://myanimelist.net/anime/1535/Death_Note\">Wikipedia</li></ExternalLinks><Images><li embed=\"http://i0.kym-cdn.com/photos/images/original/000/243/591/ef4.jpg\" /></Images><Videos><li embed=\"//www.youtube.com/embed/qV3s7Sa6B6w\" /></Videos><Maps><li embed=\"https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed\" /></Maps><Feeds><li embed=\"[WHATEVER A FEED URL LOOKS LIKE]\" /></Feeds><Summary>Lorem ipsum...</Summary></Common></Crisis>"
		e_root     = ET.fromstring(xml_string)
		temp_crisis = Crisis
		populate_common(e_root, "CRI_DTHNTE", temp_crisis)

		li_list = Li.objects.filter(model_id = "CRI_DTHNTE")
		common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
						'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
						'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
						'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		for a in li_list :
			common_dict[a.kind].append(a)
		self.assertEqual(common_dict['Images'][0].embed, "http://i0.kym-cdn.com/photos/images/original/000/243/591/ef4.jpg")

	def test_populate_common2(self):
		temp_com   = Common()
		xml_string = "<Crisis ID=\"CRI_DTHNTE\" Name=\"People mysteriously dying\"><People><Person ID=\"PER_KIRAAA\"/></People><Organizations><Org ID=\"ORG_POLICE\"/></Organizations><Common><Citations><li>Kyoto News Network</li></Citations><ExternalLinks><li href=\"http://myanimelist.net/anime/1535/Death_Note\">Wikipedia</li></ExternalLinks><Images><li embed=\"http://i0.kym-cdn.com/photos/images/original/000/243/591/ef4.jpg\" /></Images><Videos><li embed=\"//www.youtube.com/embed/PkXw1iBgzoY\" /></Videos><Maps><li embed=\"https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed\" /></Maps><Feeds><li embed=\"twitter.com/kiraisgod\" /></Feeds><Summary>Lorem ipsum...</Summary></Common></Crisis>"
		e_root     = ET.fromstring(xml_string)
		temp_crisis = Crisis
		populate_common(e_root, "CRI_DTHNTE", temp_crisis)

		li_list = Li.objects.filter(model_id = "CRI_DTHNTE")
		common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
						'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
						'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
						'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		for a in li_list :
			common_dict[a.kind].append(a)
		self.assertEqual(common_dict['ExternalLinks'][0].href, "http://myanimelist.net/anime/1535/Death_Note")
		self.assertEqual(common_dict['Videos'][0].embed, "//www.youtube.com/embed/PkXw1iBgzoY")
		self.assertEqual(common_dict['Feeds'][0].embed, "twitter.com/kiraisgod")



	#---------------------------------------#
	#-----test_relations_populate

	def test_relation_populate0(self):
		crisis_id = "CRI_BEEDIE"
		org_id = "ORG_NSAAAA"
		relations1 = Relations()
		relations1.populate(c_id = crisis_id, o_id = org_id)
		self.assertEqual(relations1.crisis_ID, crisis_id)
		self.assertEqual(relations1.org_ID, org_id)


	def test_relation_populate1(self):
		relations1 = Relations()
		relations1.populate(c_id = "CRI_UEGYPT", p_id = "PER_MMORSI", o_id = "ORG_EGYGOV")
		self.assertEqual(relations1.crisis_ID, "CRI_UEGYPT")
		self.assertEqual(relations1.org_ID, "ORG_EGYGOV")
		self.assertEqual(relations1.person_ID, "PER_MMORSI")


	def test_relation_populate2(self):
		relations1 = Relations()
		relations1.populate(c_id = "CRI_NSAWRT")
		self.assertEqual(relations1.crisis_ID, "CRI_NSAWRT")


class unloadModelsCrisisTest(TestCase):
	'''
	unloadModelsCrisisTest tests the functions unloadModels.py, which handles the export function.
	setUp() adds several Crisis, Person, and Org objects to the database for testing purposes.
	export_crisis(), export_person(), and export_org() get an object from the database and return a string with its information.
	export_xml() uses export_crisis(), export_person(), and export_org() to form an xml string
	clean_xml(), make_non_li_string(), make_li_string(), make_common_string() are auxiliary functions used for formatting.
	'''
	def setUp(self):
		self.crisis = Crisis.objects.create(crisis_ID='CRI_CRISIS', name='name',
			kind='kind', date='date', time='time', common_summary='summary')
		self.crisis2 = Crisis.objects.create(crisis_ID='CRI_CRITWO', name='',
			kind='', date='', time='', common_summary='')
		self.crisis3 = Crisis.objects.create(crisis_ID='CRI_CTHREE', name='name',
			kind='', date='date', time='', common_summary='summary')
		self.person = Person.objects.create(person_ID='PER_PERSON', name='name',
			kind='kind', location='location', common_summary='summary')
		self.person2 = Person.objects.create(person_ID='PER_PERTWO', name='',
			kind='', location='', common_summary='')
		self.person3 = Person.objects.create(person_ID='PER_PTHREE', name='name',
			kind='', location='location', common_summary='')
		self.org = Org.objects.create(org_ID='ORG_ORGORG', name='name',
			kind='kind', location='location', common_summary='summary')
		self.org2 = Org.objects.create(org_ID='ORG_ORGTWO', name='',
			kind='', location='', common_summary='')
		self.org3 = Org.objects.create(org_ID='ORG_OTHREE', name='name',
			kind='', location='', common_summary='summary')

# #---------------------------------------------------#
# #-----Unit Tests for functions from unloadModels.py
# #---------------------------------------------------#

# 	#---------------------------------------#
# 	#-----test_clean_xml (paranoid clean for things that are not li objects)
	
 	def test_clean_xml0(self):
 		dirt = "happy&go&lucky&&&go&happy"
 		dirt_to_clean = clean_xml(dirt)
 		standard_clean = "happy&amp;go&amp;lucky&amp;&amp;&amp;go&amp;happy"
 		self.assertEqual(dirt_to_clean, standard_clean)

 	def test_clean_xml1(self):
 		dirt = "randomdirtwithoutescape"
 		dirt_to_clean = clean_xml(dirt)
 		standard_clean = "randomdirtwithoutescape"
 		self.assertEqual(dirt_to_clean, standard_clean)

 	def test_clean_xml2(self):
 		dirt = "me&myself&i"
 		dirt_to_clean = clean_xml(dirt)
 		standard_clean = "me&amp;myself&amp;i"
 		self.assertEqual(dirt_to_clean, standard_clean)

# 	#---------------------------------------#
# 	#-----test_make_non_li_string

	def test_make_non_li_string0(self):
		tag = 'tag'
		clean_string = 'clean_string'
		non_li_string = make_non_li_string(clean_string, tag)
		self.assertEqual(non_li_string, "	<" + tag + ">" + clean_string + "</" + tag + ">\n")

	def test_make_non_li_string1(self):
		tag = 'tag'
		clean_string = 'clean_string'
		non_li_string = make_non_li_string(clean_string, tag)
		self.assertNotEqual(non_li_string, "	<" + tag + ">" + clean_string + "</" + tag + ">")

	def test_make_non_li_string2(self):
		tag = 'tag'
		clean_string = 'clean_string'
		non_li_string = make_non_li_string(tag, tag)
		self.assertEqual(non_li_string, "	<" + tag + ">" + tag + "</" + tag + ">\n")

	def test_make_non_li_string3(self):
		result = make_non_li_string("Test", "Summary")
		self.assertEqual(result, "\t<Summary>Test</Summary>\n")

# 	#---------------------------------------#
# 	#-----test_make_li_string

	def test_make_li_string0(self):
		li1 = Li()
		li1.href="http://"
		li1.embed=u'';
		li1.text=u'';
		li1.floating_text=u'';
		result = make_li_string([li1], "History")
		self.assertEqual(result, "\t<History>\n\t\t<li href=\"http://\"></li>\n\t</History>\n")

	def test_make_li_string1(self):
		result = make_li_string([], "History")
		self.assertEqual(result, "")

	def test_make_li_string2(self):
		li1 = Li()
		li1.href=u''
		li1.embed='youtube.com/embed';
		li1.text='img not found';
		li1.floating_text="Testing methods";
		result = make_li_string([li1], "Loc")
		self.assertEqual(result, "\t<Loc>\n\t\t<li embed=\"youtube.com/embed\" text=\"img not found\">Testing methods</li>\n\t</Loc>\n")

	def test_make_li_string3(self):
		li1 = Li()
		li1.href="http://www.google.com"
		li1.embed="youtube.com/embed";
		li1.text=u'';
		li1.floating_text=u'';
		result = make_li_string([li1], "ContactInfo")
		self.assertEqual(result, "\t<ContactInfo>\n\t\t<li href=\"http://www.google.com\" embed=\"youtube.com/embed\"></li>\n\t</ContactInfo>\n")

	def test_make_li_string4(self):
		li1 = Li()
		li1.href="http://www.google.com"
		li1.embed="youtube.com/embed";
		li1.text=u'';
		li1.floating_text=u'';
		result = make_li_string([li1], "ContactInfo", True)
		self.assertEqual(result, "\t\t<ContactInfo>\n\t\t\t<li href=\"http://www.google.com\" embed=\"youtube.com/embed\"></li>\n\t\t</ContactInfo>\n")

	def test_make_li_string5(self):
		li1 = Li()
		li1.href=u''
		li1.embed='youtube.com/embed';
		li1.text='img not found';
		li1.floating_text="Testing methods";
		result = make_li_string([li1], "Loc", True)
		self.assertEqual(result, "\t\t<Loc>\n\t\t\t<li embed=\"youtube.com/embed\" text=\"img not found\">Testing methods</li>\n\t\t</Loc>\n")

	def test_make_li_string6(self):
		result = make_li_string([], "History", True)
		self.assertEqual(result, "")

	def test_make_li_string7(self):
		li1 = Li()
		li1.href="http://"
		li1.embed=u'';
		li1.text=u'';
		li1.floating_text=u'';
		result = make_li_string([li1], "History", True)
		self.assertEqual(result, "\t\t<History>\n\t\t\t<li href=\"http://\"></li>\n\t\t</History>\n")

# 	#---------------------------------------#
# 	#-----test_make_common_string

	def test_make_common_string0(self):
		common_dict = getOrg('ORG_ORGORG')['common']
		common_string = make_common_string(common_dict)
		s = '\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n'
		self.assertEqual(common_string, s)

	def test_make_common_string1(self):
		common_dict = getPerson('PER_PERSON')['common']
		li1 = Li()
		li1.href = 'href'
		li1.model_id = 'PER_PERSON'
		li1.kind = 'ExternalLinks'
		common_dict[li1.kind] = [li1]
		common_string = make_common_string(common_dict)
		s = '\t<Common>\n\t\t<ExternalLinks>\n\t\t\t<li href="href"></li>\n\t\t</ExternalLinks>\n\t\t<Summary>summary</Summary>\n\t</Common>\n'
		self.assertEqual(common_string, s)

	def test_make_common_string2(self):
		common_dict = getCrisis('CRI_CRISIS')['common']
		li1 = Li()
		li1.embed = 'embed'
		li1.model_id = 'CRI_CRISIS'
		li1.kind = 'Images'
		common_dict[li1.kind] = [li1]
		common_string = make_common_string(common_dict)
		s = '\t<Common>\n\t\t<Images>\n\t\t\t<li embed="embed"></li>\n\t\t</Images>\n\t\t<Summary>summary</Summary>\n\t</Common>\n'
		self.assertEqual(common_string, s)

# 	#---------------------------------------#
# 	#-----test_export_crisis

	def test_export_crisis0(self):
		crisis_dict = getCrisis(self.crisis.crisis_ID)
		crisis_xml = export_crisis(crisis_dict, self.crisis.crisis_ID)
		s = '<Crisis ID="CRI_CRISIS" Name="name">\n\t<Kind>kind</Kind>\n\t<Date>date</Date>\n\t<Time>time</Time>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n'
		self.assertEqual(crisis_xml, s)

	def test_export_crisis1(self):
		cid = self.crisis2.crisis_ID
		crisis_dict = getCrisis(cid)
		crisis_xml = export_crisis(crisis_dict, cid)
		s = '<Crisis ID="CRI_CRITWO" Name="">\n</Crisis>\n\n'
		self.assertEqual(crisis_xml, s)

	def test_export_crisis2(self):
		cid = self.crisis3.crisis_ID
		crisis_dict = getCrisis(cid)
		crisis_xml = export_crisis(crisis_dict, cid)
		s = '<Crisis ID="CRI_CTHREE" Name="name">\n\t<Date>date</Date>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n'
		self.assertEqual(crisis_xml, s)


# 	#---------------------------------------#
# 	#-----test_export_person

	def test_export_person0(self):
		pid = self.person.person_ID
		person_dict = getPerson(pid)
		person_xml = export_person(person_dict, pid)
		s = '<Person ID="PER_PERSON" Name="name">\n\t<Kind>kind</Kind>\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Person>\n\n'
		self.assertEqual(person_xml, s)

	def test_export_person1(self):
		pid = self.person2.person_ID
		person_dict = getPerson(pid)
		person_xml = export_person(person_dict, pid)
		s = '<Person ID="PER_PERTWO" Name="">\n</Person>\n\n'
		self.assertEqual(person_xml, s)

	def test_export_person2(self):
		pid = self.person3.person_ID
		person_dict = getPerson(pid)
		person_xml = export_person(person_dict, pid)
		s = '<Person ID="PER_PTHREE" Name="name">\n\t<Location>location</Location>\n</Person>\n\n'
		self.assertEqual(person_xml, s)

# 	#---------------------------------------#
# 	#-----test_export_organization

	def test_export_org0(self):
		oid = self.org.org_ID
		org_dict = getOrg(oid)
		org_xml = export_organization(org_dict, oid)
		s = '<Organization ID="ORG_ORGORG" Name="name">\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n'
		self.assertEqual(org_xml, s)

	def test_export_org1(self):
		oid = self.org2.org_ID
		org_dict = getOrg(oid)
		org_xml = export_organization(org_dict, oid)
		s = '<Organization ID="ORG_ORGTWO" Name="">\n</Organization>\n\n'
		self.assertEqual(org_xml, s)

	def test_export_org2(self):
		oid = self.org3.org_ID
		org_dict = getOrg(oid)
		org_xml = export_organization(org_dict, oid)
		s = '<Organization ID="ORG_OTHREE" Name="name">\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n'
		self.assertEqual(org_xml, s)

# 	#---------------------------------------#
# 	#-----test_export_xml

	def test_export_xml0(self):
		xml_string = export_xml()
		s = '<WorldCrises>\n<Crisis ID="CRI_CRITWO" Name="">\n</Crisis>\n\n<Crisis ID="CRI_CRISIS" Name="name">\n\t<Kind>kind</Kind>\n\t<Date>date</Date>\n\t<Time>time</Time>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n<Crisis ID="CRI_CTHREE" Name="name">\n\t<Date>date</Date>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n<Person ID="PER_PERTWO" Name="">\n</Person>\n\n<Person ID="PER_PTHREE" Name="name">\n\t<Location>location</Location>\n</Person>\n\n<Person ID="PER_PERSON" Name="name">\n\t<Kind>kind</Kind>\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Person>\n\n<Organization ID="ORG_ORGTWO" Name="">\n</Organization>\n\n<Organization ID="ORG_ORGORG" Name="name">\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n<Organization ID="ORG_OTHREE" Name="name">\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n</WorldCrises>'
		self.assertEqual(xml_string, s)

	def test_export_xml1(self):
		Crisis.objects.create(crisis_ID='CRI_CRFOUR', name='name4',
			kind='kind', date='date', time='time', common_summary='summary')
		xml_string = export_xml()
		s = '<WorldCrises>\n<Crisis ID="CRI_CRITWO" Name="">\n</Crisis>\n\n<Crisis ID="CRI_CRISIS" Name="name">\n\t<Kind>kind</Kind>\n\t<Date>date</Date>\n\t<Time>time</Time>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n<Crisis ID="CRI_CTHREE" Name="name">\n\t<Date>date</Date>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n<Crisis ID="CRI_CRFOUR" Name="name4">\n\t<Kind>kind</Kind>\n\t<Date>date</Date>\n\t<Time>time</Time>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n<Person ID="PER_PERTWO" Name="">\n</Person>\n\n<Person ID="PER_PTHREE" Name="name">\n\t<Location>location</Location>\n</Person>\n\n<Person ID="PER_PERSON" Name="name">\n\t<Kind>kind</Kind>\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Person>\n\n<Organization ID="ORG_ORGTWO" Name="">\n</Organization>\n\n<Organization ID="ORG_ORGORG" Name="name">\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n<Organization ID="ORG_OTHREE" Name="name">\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n</WorldCrises>'
		self.assertEqual(xml_string, s)

	def test_export_xml2(self):
		Org.objects.create(org_ID='ORG_ORFOUR', name='name',
			kind='kind', location='location', common_summary='summary')
		xml_string = export_xml()
		s = '<WorldCrises>\n<Crisis ID="CRI_CRITWO" Name="">\n</Crisis>\n\n<Crisis ID="CRI_CRISIS" Name="name">\n\t<Kind>kind</Kind>\n\t<Date>date</Date>\n\t<Time>time</Time>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n<Crisis ID="CRI_CTHREE" Name="name">\n\t<Date>date</Date>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Crisis>\n\n<Person ID="PER_PERTWO" Name="">\n</Person>\n\n<Person ID="PER_PTHREE" Name="name">\n\t<Location>location</Location>\n</Person>\n\n<Person ID="PER_PERSON" Name="name">\n\t<Kind>kind</Kind>\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Person>\n\n<Organization ID="ORG_ORGTWO" Name="">\n</Organization>\n\n<Organization ID="ORG_ORGORG" Name="name">\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n<Organization ID="ORG_ORFOUR" Name="name">\n\t<Location>location</Location>\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n<Organization ID="ORG_OTHREE" Name="name">\n\t<Common>\n\t\t<Summary>summary</Summary>\n\t</Common>\n</Organization>\n\n</WorldCrises>'
		self.assertEqual(xml_string, s)


class loadModelsCrisisTest(TestCase):

# #------------------------------------------------#
# #-----Unit Tests for functions from loadModels.py
# #------------------------------------------------#
	"""
	Contains the unit tests for loadModels.py, the import facility.These unit tests mostly 
    confirm that models are properly populated and stored in the database.
	"""

	#---------------------------------------#
	#-----test_validate

	def test_validate0(self):
		f = open('wcdb/xml0.xml')
		self.assertEqual(type(f), file)
		self.assert_(validate(f) != False)

	def test_validate1(self):
		f = open('wcdb/xml1.xml')
		self.assertEqual(type(f), file)
		self.assert_(type(validate(f)) == str)

	def test_validate2(self):
		f = open('wcdb/xml2.xm')
		self.assertEqual(type(f), file)
		self.assertEqual(validate(f), False)

	#---------------------------------------#
	#-----test_populate_models

	def test_populate_models0(self) :
		crisis_string = "<WC><Crisis ID=\"CRI_NOTFOREXPORT\" Name=\"NOTFOREXPORT\"><People><Person ID=\"PER_NOTFOREXPORT\" /></People><Organizations><Org ID=\"ORG_NOTFOREXPORT\" /></Organizations><Kind>NOTFOREXPORT</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>random</li></Locations><HumanImpact><li>random</li></HumanImpact><EconomicImpact><li>random</li></EconomicImpact><ResourcesNeeded><li>random</li></ResourcesNeeded><WaysToHelp><li> href=\"http://random\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis>"
		person_string = "<Person ID=\"PER_HMUBAR\" Name=\"Hosni Mubarak\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person>"
		org_string = "<Organization ID=\"ORG_MUSBRO\" Name=\"The Muslim Brotherhood\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><People><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_MMORSI\" /></People><Kind>Islamic Movement</Kind><Location>Egypt</Location><Common></Common></Organization></WC>"
		xml_to_tree = crisis_string + person_string + org_string
		e_root = ET.fromstring(xml_to_tree)
		e_tree = ET.ElementTree(e_root)
		populate_models(e_tree)
		cri_dict = getCrisis("CRI_NOTFOREXPORT")
		self.assertEqual(cri_dict['name'], "NOTFOREXPORT")
		self.assertEqual(cri_dict['time'], "09:00:00+05:30")
		self.assertEqual(cri_dict['organizations'][0][0], 'ORG_NOTFOREXPORT')


	def test_populate_models1(self) :
		crisis_string = "<WC><Crisis ID=\"CRI_kindofrandom\" Name=\"kindofrandom\"><People><Person ID=\"PER_kindofrandom\" /></People><Organizations><Org ID=\"ORG_kindofrandom\" /></Organizations><Kind>kindofrandom</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>kindofrandom</li></Locations><HumanImpact><li>kindofrandom</li></HumanImpact><EconomicImpact><li>kindofrandom</li></EconomicImpact><ResourcesNeeded><li>kindofrandom</li></ResourcesNeeded><WaysToHelp><li> href=\"http://kindofrandom\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis>"
		person_string = "<Person ID=\"PER_ELBARA\" Name=\"Mohamed ElBaradei\"><Crises><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person>"
		org_string = "<Organization ID=\"ORG_LAKERS\" Name=\"Los Angeles Lakers\"><Crises><Crisis ID=\"CRI_DWIGHT\" /></Crises><People><Person ID=\"PER_DANTON\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /></People><Kind>Sports</Kind><Location>Los Angeles</Location><Common></Common></Organization></WC>"
		xml_to_tree = crisis_string + person_string + org_string
		e_root = ET.fromstring(xml_to_tree)
		e_tree = ET.ElementTree(e_root)
		populate_models(e_tree)
		per_dict = getPerson("PER_ELBARA")
		org_dict = getOrg("ORG_LAKERS")
		self.assertEqual(per_dict['name'], "Mohamed ElBaradei")
		self.assertEqual(per_dict['kind'], "Politician")
		self.assertEqual(per_dict['organizations'][0][0], 'ORG_EGYGOV')
		self.assertEqual(org_dict['name'], "Los Angeles Lakers")
		self.assertEqual(org_dict['location'], "Los Angeles")
		self.assertEqual(org_dict['crises'][0][0], 'CRI_DWIGHT')

	def test_populate_models2(self) :
		crisis_string = "<WC><Crisis ID=\"CRI_DWIGHT\" Name=\"Dwightmare\"><People><Person ID=\"PER_JIMBUS\" /></People><Organizations><Org ID=\"ORG_YESMEN\" /></Organizations><Kind>kindofrandom</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>Wherever the Rugrats lived</li></Locations><HumanImpact><li>kindofrandom</li></HumanImpact><EconomicImpact><li>kindofrandom</li></EconomicImpact><ResourcesNeeded><li>kindofrandom</li></ResourcesNeeded><WaysToHelp><li> href=\"http://kindofrandom\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis>"
		person_string = "<Person ID=\"PER_JIMBUS\" Name=\"Jim Buss\"><Crises><Crisis ID=\"CRI_STUPID\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_LAKERS\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Idiot</Kind><Location>Egypt</Location><Common></Common></Person>"
		org_string = "<Organization ID=\"ORG_KNICKS\" Name=\"New York Knicks\"><Crises><Crisis ID=\"CRI_TOOOLD\" /></Crises><People><Person ID=\"PER_DOLANPLS\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /></People><Kind>Sports</Kind><Location>New York</Location><Common></Common></Organization></WC>"
		xml_to_tree = crisis_string + person_string + org_string
		e_root = ET.fromstring(xml_to_tree)
		e_tree = ET.ElementTree(e_root)
		populate_models(e_tree)
		cri_dict = getCrisis("CRI_DWIGHT")
		per_dict = getPerson("PER_JIMBUS")
		org_dict = getOrg("ORG_KNICKS")
		self.assertEqual(cri_dict['name'], "Dwightmare")
		self.assertEqual(cri_dict['time'], "09:00:00+05:30")
		self.assertEqual(cri_dict['organizations'][0][0], 'ORG_YESMEN')
		self.assertEqual(per_dict['name'], "Jim Buss")
		self.assertEqual(per_dict['kind'], "Idiot")
		self.assertEqual(per_dict['organizations'][0][0], 'ORG_LAKERS')
		self.assertEqual(org_dict['name'], "New York Knicks")
		self.assertEqual(org_dict['location'], "New York")
		self.assertEqual(org_dict['crises'][0][0], 'CRI_TOOOLD')



	#---------------------------------------#
	#-----test_populate_crisis

	def test_populate_crisis0(self):
		xml_string = "<WC><Crisis ID=\"CRI_SIXCHR\" Name=\"FAKENAME\"><People><Person ID=\"PER_NOTFOREXPORT\" /></People><Organizations><Org ID=\"ORG_NOTFOREXPORT\" /></Organizations><Kind>NOTFOREXPORT</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>random</li></Locations><HumanImpact><li>random</li></HumanImpact><EconomicImpact><li>random</li></EconomicImpact><ResourcesNeeded><li>random</li></ResourcesNeeded><WaysToHelp><li> href=\"http://random\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis></WC>"
		root = ET.fromstring(xml_string)
		populate_crisis(root)
		cri_dict = getCrisis("CRI_SIXCHR")
		self.assertEqual(cri_dict['name'], "FAKENAME")

	def test_populate_crisis1(self):
		xml_string = "<WC><Crisis ID=\"CRI_kindofrandom\" Name=\"kindofrandom\"><People><Person ID=\"PER_kindofrandom\" /></People><Organizations><Org ID=\"ORG_kindofrandom\" /></Organizations><Kind>kindofrandom</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>kindofrandom</li></Locations><HumanImpact><li>kindofrandom</li></HumanImpact><EconomicImpact><li>kindofrandom</li></EconomicImpact><ResourcesNeeded><li>kindofrandom</li></ResourcesNeeded><WaysToHelp><li> href=\"http://kindofrandom\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis></WC>"
		root = ET.fromstring(xml_string)
		populate_crisis(root)
		cri_dict = getCrisis("CRI_kindofrandom")
		self.assertEqual(cri_dict['name'], "kindofrandom")
		self.assertEqual(cri_dict['date'], "2011-01-25")

	def test_populate_crisis2(self):
		xml_string = "<WC><Crisis ID=\"CRI_last_populate_crisis_to_check\" Name=\"last_populate_crisis_to_check\"><People><Person ID=\"PER_last_populate_crisis_to_check\" /></People><Organizations><Org ID=\"ORG_SAVIOR\" /></Organizations><Kind>Apocalyptic</Kind><Date>2000-01-20</Date><Time>09:00:00+05:30</Time><Locations><li>last_populate_crisis_to_check</li></Locations><HumanImpact><li>last_populate_crisis_to_check</li></HumanImpact><EconomicImpact><li>last_populate_crisis_to_check</li></EconomicImpact><ResourcesNeeded><li>last_populate_crisis_to_check</li></ResourcesNeeded><WaysToHelp><li> href=\"http://last_populate_crisis_to_check\"</li><li>last_populate_crisis_to_check</li></WaysToHelp><Common><Citations><li> href= last_populate_crisis_to_check</li></Citations><ExternalLinks><li> href=\"http:last_populate_crisis_to_check.html\"</li></ExternalLinks><Images><li> embed=\"http:last_populate_crisis_to_check.jpg\"</li></Images><Summary>last_populate_crisis_to_check</Summary></Common></Crisis></WC>"
		root = ET.fromstring(xml_string)
		populate_crisis(root)
		cri_dict = getCrisis("CRI_last_populate_crisis_to_check")
		self.assertEqual(cri_dict['name'], "last_populate_crisis_to_check")
		self.assertEqual(cri_dict['time'], "09:00:00+05:30")
		self.assertEqual(cri_dict['kind'], "Apocalyptic")
		self.assertEqual(cri_dict['date'], "2000-01-20")
		self.assertEqual(cri_dict['organizations'][0][0], 'ORG_SAVIOR')
	#---------------------------------------#
	#-----test_populate_person

	def test_populate_person0(self):
		xml_string = "<WC><Person ID=\"PER_HMUBAR\" Name=\"Hosni Mubarak\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		root = ET.fromstring(xml_string)
		populate_person(root)
		per_dict = getPerson("PER_HMUBAR")
		self.assertEqual(per_dict['name'], "Hosni Mubarak")
		self.assertEqual(per_dict['kind'], "Politician")
		self.assertEqual(per_dict['location'], "Egypt")

	def test_populate_person1(self):
		xml_string = "<WC><Person ID=\"PER_ELBARA\" Name=\"Mohamed ElBaradei\"><Crises><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		root = ET.fromstring(xml_string)
		populate_person(root)
		per_dict = getPerson("PER_ELBARA")
		self.assertEqual(per_dict['name'], "Mohamed ElBaradei")

	def test_populate_person2(self):
		xml_string = "<WC><Person ID=\"PER_YEEZUS\" Name=\"Kanye West\"><Crises><Crisis ID=\"CRI_YEEZUS\" /></Crises><Organizations><Org ID=\"ORG_GOODMU\" /><Org ID=\"ORG_HARDNI\" /></Organizations><Kind>Self-proclaimed demi-god</Kind><Location>Earf</Location><Common></Common></Person></WC>"
		root = ET.fromstring(xml_string)
		populate_person(root)
		per_dict = getPerson("PER_YEEZUS")
		self.assertEqual(per_dict['name'], "Kanye West")
		self.assertEqual(per_dict['kind'], "Self-proclaimed demi-god")
		self.assertEqual(per_dict['location'], "Earf")
		self.assertEqual(per_dict['organizations'][0][0], 'ORG_GOODMU')
	#---------------------------------------#
	#-----test_populate_org

	def test_populate_org0(self):
		xml_string = "<WC><Organization ID=\"ORG_MUSBRO\" Name=\"The Muslim Brotherhood\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><People><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_MMORSI\" /></People><Kind>Islamic Movement</Kind><Location>Egypt</Location><Common></Common></Organization></WC>"
		root = ET.fromstring(xml_string)
		populate_org(root)
		org_dict = getOrg("ORG_MUSBRO")
		self.assertEqual(org_dict['name'], "The Muslim Brotherhood")
		self.assertEqual(org_dict['kind'], "Islamic Movement")
		self.assertEqual(org_dict['location'], "Egypt")

	def test_populate_org1(self):
		xml_string = "<WC><Organization ID=\"ORG_random\" Name=\"random\"><Crises><Crisis ID=\"CRI_random\" /></Crises><People><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /></People><Kind>krandom</Kind><Location>anywhere</Location><Common></Common></Organization></WC>"
		root = ET.fromstring(xml_string)
		populate_org(root)
		org_dict = getOrg("ORG_random")
		self.assertEqual(org_dict['name'], "random")
		self.assertEqual(org_dict['kind'], "krandom")
		self.assertEqual(org_dict['location'], "anywhere")


	def test_populate_org2(self):
		xml_string = "<WC><Organization ID=\"ORG_RECONC\" Name=\"Recon Corps\"><Crises><Crisis ID=\"CRI_TITANS\" /></Crises><People><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /></People><Kind>Elite titan research group</Kind><Location>Outside the walls</Location><Common></Common></Organization></WC>"
		root = ET.fromstring(xml_string)
		populate_org(root)
		org_dict = getOrg("ORG_RECONC")
		self.assertEqual(org_dict['name'], "Recon Corps")
		self.assertEqual(org_dict['kind'], "Elite titan research group")
		self.assertEqual(org_dict['location'], "Outside the walls")
		self.assertEqual(org_dict['crises'][0][0], 'CRI_TITANS')


class viewsTest(TestCase):
	"""
	Contains the unit tests for the views.py file. Tests that views return a correct reponse.
	"""
#--------------------------------------------#
#-----Unit Tests for functions from views.py
#--------------------------------------------#

	#---------------------------------------#
	#-----test_crisisView
	#---------------------------------------#

	# tests that user can see our pages 
	def test_indexView(self):
		response = self.client.get("http://localhost:8000/")
		self.assertEqual(response.status_code, 200)

	def test_crisisView1(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_NSAWRT")
		self.assertEqual(response.status_code, 200)

	def test_crisisView2(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_BEEDIE")
		self.assertEqual(response.status_code, 200)

	def test_crisisView3(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_TXWDFR")
		self.assertEqual(response.status_code, 200)

	def test_crisisView4(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_BRZLPR")
		self.assertEqual(response.status_code, 200)

	def test_crisisView5(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_MEXDRG")
		self.assertEqual(response.status_code, 200)

	def test_crisisView6(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_LGBTRU")
		self.assertEqual(response.status_code, 200)

	def test_crisisView7(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_UEGYPT")
		self.assertEqual(response.status_code, 200)

	def test_crisisView8(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_FWATER")
		self.assertEqual(response.status_code, 200)

	def test_crisisView9(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_FOREST")
		self.assertEqual(response.status_code, 200)

	def test_crisisView10(self):
		response = self.client.get("http://localhost:8000/crisis/CRI_NUCDIS")
		self.assertEqual(response.status_code, 200)

	def test_orgsView1(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_UOCSCI")
		self.assertEqual(response.status_code, 200)

	def test_orgsView2(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_NSAAAA")
		self.assertEqual(response.status_code, 200)

	def test_orgsView3(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_FEMAAA")
		self.assertEqual(response.status_code, 200)

	def test_orgsView4(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_EPAAAA")
		self.assertEqual(response.status_code, 200)

	def test_orgsView5(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_MUSBRO")
		self.assertEqual(response.status_code, 200)

	def test_orgsView6(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_EGYGOV")
		self.assertEqual(response.status_code, 200)

	def test_orgsView7(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_IUCNAT")
		self.assertEqual(response.status_code, 200)

	def test_orgsView8(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_SINCAR")
		self.assertEqual(response.status_code, 200)

	def test_orgsView9(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_LOSZTA")
		self.assertEqual(response.status_code, 200)

	def test_orgsView10(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_MEXGOV")
		self.assertEqual(response.status_code, 200)

	def test_orgsView11(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_GAYRUS")
		self.assertEqual(response.status_code, 200)

	def test_orgsView12(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_BRAGOV")
		self.assertEqual(response.status_code, 200)

	def test_orgsView13(self):
		response = self.client.get("http://localhost:8000/orgs/ORG_WATERO")
		self.assertEqual(response.status_code, 200)

	def test_peopleView1(self):
		response = self.client.get("http://localhost:8000/people/PER_YYAMAD")
		self.assertEqual(response.status_code, 200)

	def test_peopleView2(self):
		response = self.client.get("http://localhost:8000/people/PER_HPASSS")
		self.assertEqual(response.status_code, 200)

	def test_peopleView3(self):
		response = self.client.get("http://localhost:8000/people/PER_TTHBLD")
		self.assertEqual(response.status_code, 200)

	def test_peopleView4(self):
		response = self.client.get("http://localhost:8000/people/PER_DLVRUS")
		self.assertEqual(response.status_code, 200)

	def test_peopleView5(self):
		response = self.client.get("http://localhost:8000/people/PER_ESNWDN")
		self.assertEqual(response.status_code, 200)

	def test_peopleView6(self):
		response = self.client.get("http://localhost:8000/people/PER_RFLCRR")
		self.assertEqual(response.status_code, 200)

	def test_peopleView7(self):
		response = self.client.get("http://localhost:8000/people/PER_GUZMAN")
		self.assertEqual(response.status_code, 200)

	def test_peopleView8(self):
		response = self.client.get("http://localhost:8000/people/PER_RPERRY")
		self.assertEqual(response.status_code, 200)

	def test_peopleView9(self):
		response = self.client.get("http://localhost:8000/people/PER_MMORSI")
		self.assertEqual(response.status_code, 200)

	def test_peopleView10(self):
		response = self.client.get("http://localhost:8000/people/PER_XNSHNG")
		self.assertEqual(response.status_code, 200)

	def test_peopleView11(self):
		response = self.client.get("http://localhost:8000/people/PER_NIKALX")
		self.assertEqual(response.status_code, 200)

	def test_peopleView12(self):
		response = self.client.get("http://localhost:8000/people/PER_MTTDMN")
		self.assertEqual(response.status_code, 200)

	"""
	Creates an infinite loop!
	def test_unittestView(self):
		response = self.client.get("http://localhost:8000/unittests/")
		self.assertEqual(response.status_code, 200)
	"""

	def test_importView1(self):
		response = self.client.get("http://localhost:8000/import/")
		self.assertEqual(response.status_code, 200)

	def test_importView2(self):
		c = Client()
		with open('wcdb/xml0.xml') as upload:
			response = self.client.post("http://localhost:8000/import/", {'password': "ateam", 'xmlvalue': upload}, follow = True)
			self.assertEqual(response.status_code, 200) # Redirect on form success

	def test_passwordValidate0(self):
		pw = "ateam"
		result = passwordValidate(pw)
		self.assert_(result)

	def test_passwordValidate1(self):
		pw = "someotherteam"
		result = passwordValidate(pw)
		self.assert_(not (result))

	def test_exportView(self):
		response = self.client.get("http://127.0.0.1:8000/export/")
		self.assertEqual(response.status_code, 200)


class getDdModelTest(TestCase):
	"""
	Contains the unit tests for getDbModel.py. The tests use import functions to save modelt to 
	the database, then check that the getDbModel functions properly retrieve information from 
	the database
	"""

# #--------------------------------------------#
# #-----Unit Tests for functions from getDbModel.py
# #--------------------------------------------#

# 	#---------------------------------------#
# 	#-----test_getCrisis
# 	#---------------------------------------#

	def test_getCrisis1(self):
		# create a person, crisis, and organization
		temp_crisis           = Crisis()
		#temp_relations        = []		# can't save a list to db table
		temp_crisis.crisis_ID = "CRI_NSAWRT"
		temp_crisis.name      = "NSA Wiretapping"
		temp_crisis.kind      = "Civil Liberties"
		temp_crisis.date      = "2013-06-06"

		# relations = [{'crisis_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.crisis_ID = "CRI_NSAWRT"
		relations1.person_ID = "PER_ESNWDN"
		relations1.org_ID = "ORG_NSAAAA"
		relations2 = Relations()
		relations2.crisis_ID = "CRI_NSAWRT"
		relations2.person_ID = "PER_PUTIN"
		relations2.org_ID = "RUSGOVT"
		#temp_relations.append(relations1)
		
		"""
		temp_relations[0].crisis_ID = "CRI_NSAWRT"
		temp_relations[0].person_ID = "PER_ESNWDN"
		temp_relations[0].org_ID = "ORG_NSAAAA"
		temp_relations[1].crisis_ID = "CRI_NSAWRT"
		temp_relations[1].person_ID = "PER_PUTIN"
		temp_relations[1].org_ID = "RUSGOVT"		
		"""
		#temp_crisis.organizations = ["ORG_NSAAAA", "RUSGOVT"]
		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.href = "linktosomething.com"
		li1.text = "some text"
		li1.kind = "Images"
		li1.model_id = "CRI_NSAWRT"

		relations1.save()
		relations2.save()
		li1.save()
		temp_crisis.save()

		crisis = getCrisis("CRI_NSAWRT")
		#print crisis

		self.assertEqual(temp_crisis.name, crisis.get('name'))
		self.assertEqual(temp_crisis.kind, crisis.get('kind'))
		self.assertEqual(temp_crisis.date, crisis.get('date'))
		self.assertEqual(relations1.person_ID, crisis.get('people')[0][0])
		self.assertEqual(relations1.org_ID, crisis.get('organizations')[0][0])
		self.assertEqual(relations2.person_ID, crisis.get('people')[1][0])
		self.assertEqual(relations2.org_ID, crisis.get('organizations')[1][0])
		self.assertEqual(li1.href, crisis.get('common').get('Images')[0].href)
		self.assertEqual(li1.text, crisis.get('common').get('Images')[0].text)
		self.assertEqual(li1.kind, crisis.get('common').get('Images')[0].kind)
		self.assertEqual(li1.model_id, crisis.get('common').get('Images')[0].model_id)


	def test_getCrisis2(self):
		# create a person, crisis, and organization
		temp_crisis           = Crisis()
		temp_crisis.crisis_ID = "CRI_BEEDIE"
		temp_crisis.name      = "Bee Colony Collapse Disorder"
		temp_crisis.kind      = "Environmental, Economical"
		temp_crisis.date      = "2005-01-01"

		# relations = [{'crisis_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.crisis_ID = "CRI_BEEDIE"
		relations1.person_ID = "PER_TTHBLD"
		relations1.org_ID = "ORG_EPAAAA"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.embed = "map"
		li1.text = "some text"
		li1.floating_text = "more text" 
		li1.kind = "Maps"
		li1.model_id = "CRI_BEEDIE"

		relations1.save()
		li1.save()
		temp_crisis.save()

		crisis = getCrisis("CRI_BEEDIE")
		 #print crisis

		self.assertEqual(temp_crisis.name, crisis.get('name'))
		self.assertEqual(temp_crisis.kind, crisis.get('kind'))
		self.assertEqual(temp_crisis.date, crisis.get('date'))
		self.assertEqual(relations1.person_ID, crisis.get('people')[0][0])
		self.assertEqual(relations1.org_ID, crisis.get('organizations')[0][0])
		self.assertEqual(li1.embed, crisis.get('common').get('Maps')[0].embed)
		self.assertEqual(li1.text, crisis.get('common').get('Maps')[0].text)
		self.assertEqual(li1.floating_text, crisis.get('common').get('Maps')[0].floating_text)
		self.assertEqual(li1.kind, crisis.get('common').get('Maps')[0].kind)
		self.assertEqual(li1.model_id, crisis.get('common').get('Maps')[0].model_id)


	def test_getCrisis3(self):
		# create a person, crisis, and organization
		temp_crisis           = Crisis()
		temp_crisis.crisis_ID = "CRI_TXWDFR"
		temp_crisis.name      = "Texas Wild Fires"
		temp_crisis.kind      = "Natural disaster"
		temp_crisis.date      = "2011-09-04"

		# relations = [{'crisis_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.crisis_ID = "CRI_TXWDFR"
		relations1.person_ID = "PER_RPERRY"
		relations1.org_ID = "ORG_FEMAAA"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.embed = "something"
		li1.floating_text = "text" 
		li1.kind = "Citations"
		li1.model_id = "CRI_TXWDFR"

		relations1.save()
		li1.save()
		temp_crisis.save()

		crisis = getCrisis("CRI_TXWDFR")
		#ExternalLinks crisis

		self.assertEqual(temp_crisis.name, crisis.get('name'))
		self.assertEqual(temp_crisis.kind, crisis.get('kind'))
		self.assertEqual(temp_crisis.date, crisis.get('date'))
		self.assertEqual(relations1.person_ID, crisis.get('people')[0][0])
		self.assertEqual(relations1.org_ID, crisis.get('organizations')[0][0])
		self.assertEqual(li1.embed, crisis.get('common').get('Citations')[0].embed)
		self.assertEqual(li1.text, crisis.get('common').get('Citations')[0].text)
		self.assertEqual(li1.floating_text, crisis.get('common').get('Citations')[0].floating_text)
		self.assertEqual(li1.kind, crisis.get('common').get('Citations')[0].kind)
		self.assertEqual(li1.model_id, crisis.get('common').get('Citations')[0].model_id)


# 	#---------------------------------------#
# 	#-----test_getOrg
# 	#---------------------------------------#

	def test_getOrg1(self):
		# create a person, crisis, and organization
		temp_org           = Org()
		temp_org.org_ID = "ORG_EPAAAA"
		temp_org.name      = "Environmental Protection Agency"
		temp_org.kind      = "Federal government agency"
		temp_org.location      = "1200 Pennsylvania Ave. NW Washington, DC 20460"

		# relations = [{'org_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.org_ID = "ORG_EPAAAA"
		relations1.person_ID = "PER_TTHBLD"
		relations1.crisis_ID = "CRI_BEEDIE"
		relations2 = Relations()
		relations2.org_ID = "ORG_EPAAAA"
		relations2.person_ID = "PER_RPERRY"
		relations2.crisis_ID = "CRI_TXWDFR"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.href = "linktosomething.com"
		li1.text = "some text"
		li1.kind = "Images"
		li1.model_id = "ORG_EPAAAA"

		relations1.save()
		relations2.save()
		li1.save()
		temp_org.save()

		org = getOrg("ORG_EPAAAA")
		#print org

		self.assertEqual(temp_org.name, org.get('name'))
		self.assertEqual(temp_org.kind, org.get('kind'))
		self.assertEqual(temp_org.location, org.get('location'))
		self.assertEqual(relations1.person_ID, org.get('people')[0][0])
		self.assertEqual(relations1.crisis_ID, org.get('crises')[0][0])
		self.assertEqual(relations2.person_ID, org.get('people')[1][0])
		self.assertEqual(relations2.crisis_ID, org.get('crises')[1][0])
		self.assertEqual(li1.href, org.get('common').get('Images')[0].href)
		self.assertEqual(li1.text, org.get('common').get('Images')[0].text)
		self.assertEqual(li1.kind, org.get('common').get('Images')[0].kind)
		self.assertEqual(li1.model_id, org.get('common').get('Images')[0].model_id)


	def test_getOrg2(self):
		# create a person, crisis, and organization
		temp_org           = Org()
		temp_org.org_ID = "ORG_NSAAAA"
		temp_org.name      = "National Security Agency"
		temp_org.kind      = "Government"
		temp_org.location      = "Fort Meade, Maryland"

		# relations = [{'org_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.org_ID = "ORG_NSAAAA"
		relations1.person_ID = "PER_ESNWDN"
		relations1.crisis_ID = "CRI_NSAWRT"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.href = "linktosomething.com"
		li1.text = "some text"
		li1.kind = "Images"
		li1.model_id = "ORG_NSAAAA"

		relations1.save()
		li1.save()
		temp_org.save()

		org = getOrg("ORG_NSAAAA")
		#print org

		self.assertEqual(temp_org.name, org.get('name'))
		self.assertEqual(temp_org.kind, org.get('kind'))
		self.assertEqual(temp_org.location, org.get('location'))
		self.assertEqual(relations1.person_ID, org.get('people')[0][0])
		self.assertEqual(relations1.crisis_ID, org.get('crises')[0][0])
		self.assertEqual(li1.href, org.get('common').get('Images')[0].href)
		self.assertEqual(li1.text, org.get('common').get('Images')[0].text)
		self.assertEqual(li1.kind, org.get('common').get('Images')[0].kind)
		self.assertEqual(li1.model_id, org.get('common').get('Images')[0].model_id)


	def test_getOrg3(self):
		# create a person, crisis, and organization
		temp_org           = Org()
		temp_org.org_ID = "ORG_MUSBRO"
		temp_org.name      = "The Muslim Brotherhood"
		temp_org.kind      = "Islamic Movement"
		temp_org.location      = "Egypt"

		# relations = [{'org_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.org_ID = "ORG_MUSBRO"
		relations1.person_ID = "PER_MMORSI"
		relations1.crisis_ID = "CRI_UEGYPT"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.href = "linktosomething.com"
		li1.text = "some text"
		li1.kind = "ExternalLinks"
		li1.model_id = "ORG_MUSBRO"

		relations1.save()
		li1.save()
		temp_org.save()

		org = getOrg("ORG_MUSBRO")
		#print org

		self.assertEqual(temp_org.name, org.get('name'))
		self.assertEqual(temp_org.kind, org.get('kind'))
		self.assertEqual(temp_org.location, org.get('location'))
		self.assertEqual(relations1.person_ID, org.get('people')[0][0])
		self.assertEqual(relations1.crisis_ID, org.get('crises')[0][0])
		self.assertEqual(li1.href, org.get('common').get('ExternalLinks')[0].href)
		self.assertEqual(li1.text, org.get('common').get('ExternalLinks')[0].text)
		self.assertEqual(li1.kind, org.get('common').get('ExternalLinks')[0].kind)
		self.assertEqual(li1.model_id, org.get('common').get('ExternalLinks')[0].model_id)


# 	#---------------------------------------#
# 	#-----test_getPerson
# 	#---------------------------------------#

	def test_getPerson1(self):
		# create a person, crisis, and organization
		temp_person           = Person()
		temp_person.person_ID = "PER_ESNWDN"
		temp_person.name      = "Edward Snowden"
		temp_person.kind      = "Whistleblower"
		temp_person.location  = "Moscow, Russia"

		# relations = [{'person_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.person_ID = "PER_ESNWDN"
		relations1.crisis_ID = "CRI_NSAWRT"
		relations1.org_ID = "ORG_NSAAAA"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.href = "linktosomething.com"
		li1.text = "some text"
		li1.kind = "Images"
		li1.model_id = "PER_ESNWDN"

		relations1.save()
		li1.save()
		temp_person.save()

		person = getPerson("PER_ESNWDN")
		#print person

		self.assertEqual(temp_person.name, person.get('name'))
		self.assertEqual(temp_person.kind, person.get('kind'))
		self.assertEqual(temp_person.location, person.get('location'))
		self.assertEqual(relations1.crisis_ID, person.get('crises')[0][0])
		self.assertEqual(relations1.org_ID, person.get('organizations')[0][0])
		self.assertEqual(li1.href, person.get('common').get('Images')[0].href)
		self.assertEqual(li1.text, person.get('common').get('Images')[0].text)
		self.assertEqual(li1.kind, person.get('common').get('Images')[0].kind)
		self.assertEqual(li1.model_id, person.get('common').get('Images')[0].model_id)


	def test_getPerson2(self):
		# create a person, crisis, and organization
		temp_person           = Person()
		temp_person.person_ID = "PER_RFLCRR"
		temp_person.name      = "Rafael Correa"
		temp_person.kind      = "President of the Republic of Ecuador"
		temp_person.location  = "Ecuador"

		# relations = [{'person_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.person_ID = "PER_RFLCRR"
		relations1.crisis_ID = "CRI_NSAWRT"
		relations1.org_ID = "ORG_NSAAAA"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.href = "linktosomething.com"
		li1.text = "some text"
		li1.kind = "Images"
		li1.model_id = "PER_RFLCRR"

		relations1.save()
		li1.save()
		temp_person.save()

		person = getPerson("PER_RFLCRR")
		#print person

		self.assertEqual(temp_person.name, person.get('name'))
		self.assertEqual(temp_person.kind, person.get('kind'))
		self.assertEqual(temp_person.location, person.get('location'))
		self.assertEqual(relations1.crisis_ID, person.get('crises')[0][0])
		self.assertEqual(relations1.org_ID, person.get('organizations')[0][0])
		self.assertEqual(li1.href, person.get('common').get('Images')[0].href)
		self.assertEqual(li1.text, person.get('common').get('Images')[0].text)
		self.assertEqual(li1.kind, person.get('common').get('Images')[0].kind)
		self.assertEqual(li1.model_id, person.get('common').get('Images')[0].model_id)


	def test_getPerson3(self):
		# create a person, crisis, and organization
		temp_person           = Person()
		temp_person.person_ID = "PER_GUZMAN"
		temp_person.name      = "Joaquin Guzman Loera"
		temp_person.kind      = "Drug Cartel Leader"
		temp_person.location  = "Mexico"

		# relations = [{'person_ID': "", 'person_ID': "", 'org_ID': ""}]
		relations1 = Relations()
		relations1.person_ID = "PER_GUZMAN"
		relations1.crisis_ID = "CRI_MEXDRG"
		relations1.org_ID = "ORG_SINCAR"

		temp_common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [],'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}
		li1 = Li()
		li1.href = "facebook.com"
		li1.floating_text = "some floating_text"
		li1.kind = "Feeds"
		li1.model_id = "PER_GUZMAN"

		relations1.save()
		li1.save()
		temp_person.save()

		person = getPerson("PER_GUZMAN")
		#print person

		self.assertEqual(temp_person.name, person.get('name'))
		self.assertEqual(temp_person.kind, person.get('kind'))
		self.assertEqual(temp_person.location, person.get('location'))
		self.assertEqual(relations1.crisis_ID, person.get('crises')[0][0])
		self.assertEqual(relations1.org_ID, person.get('organizations')[0][0])
		self.assertEqual(li1.href, person.get('common').get('Feeds')[0].href)
		self.assertEqual(li1.floating_text, person.get('common').get('Feeds')[0].floating_text)
		self.assertEqual(li1.kind, person.get('common').get('Feeds')[0].kind)
		self.assertEqual(li1.model_id, person.get('common').get('Feeds')[0].model_id)

# 	#---------------------------------------#
# 	#-----test_getCrisis
# 	#---------------------------------------#

	def test_getCrisisIDs1(self):
		temp_crisis1          = Crisis()
		temp_crisis1.crisis_ID = "CRI_NSAWRT"
		temp_crisis1.name      = "NSA Wiretapping"
		temp_crisis1.kind      = "Civil Liberties"
		temp_crisis1.date      = "2013-06-06"

		temp_crisis2          = Crisis()
		temp_crisis2.crisis_ID = "CRI_BEEDIE"
		temp_crisis2.name      = "Bee Colony Collapse Disorder"
		temp_crisis2.kind      = "Economical, Environmental"
		temp_crisis2.date      = "2006-01-01"

		temp_crisis3          = Crisis()
		temp_crisis3.crisis_ID = "CRI_TXWDFR"
		temp_crisis3.name      = "Texas Wild Fires"
		temp_crisis3.kind      = "Natural disaster"
		temp_crisis3.date      = "2011-09-04"

		temp_crisis1.save()
		temp_crisis2.save()
		temp_crisis3.save()

		ids = getCrisisIDs()
		# print "\n\n"
		# print ids
		# print ids.get('CRI_TXWDFR')

		self.assertEqual(temp_crisis1.name, ids.get('CRI_NSAWRT'))
		self.assertEqual(temp_crisis2.name, ids.get('CRI_BEEDIE'))
		self.assertEqual(temp_crisis3.name, ids.get('CRI_TXWDFR'))


	def test_getCrisisIDs2(self):
		temp_crisis1          = Crisis()
		temp_crisis1.crisis_ID = "CRI_BRZLPR"
		temp_crisis1.name      = "Brazilian Protests"
		temp_crisis1.kind      = "Socioeconomic Crisis"
		temp_crisis1.date      = "2013-06-17"

		temp_crisis2          = Crisis()
		temp_crisis2.crisis_ID = "CRI_MEXDRG"
		temp_crisis2.name      = "Mexican Drug Violence"
		temp_crisis2.kind      = "Violent Conflict"
		temp_crisis2.date      = "2006-01-01"

		temp_crisis3          = Crisis()
		temp_crisis3.crisis_ID = "CRI_LGBTRU"
		temp_crisis3.name      = "LGBT Issues in Russia"
		temp_crisis3.kind      = "Civil/Human Rights"
		temp_crisis3.date      = "Russia"

		temp_crisis1.save()
		temp_crisis2.save()
		temp_crisis3.save()

		ids = getCrisisIDs()
		# print "\n\n"
		# print ids
		# print ids.get('CRI_LGBTRU')

		self.assertEqual(temp_crisis1.name, ids.get('CRI_BRZLPR'))
		self.assertEqual(temp_crisis2.name, ids.get('CRI_MEXDRG'))
		self.assertEqual(temp_crisis3.name, ids.get('CRI_LGBTRU'))


	def test_getCrisisIDs3(self):
		temp_crisis1          = Crisis()
		temp_crisis1.crisis_ID = "CRI_FWATER"
		temp_crisis1.name      = "Fresh Water Scarcity"
		temp_crisis1.kind      = "Environmental"
		temp_crisis1.date      = "1970-01-01"

		temp_crisis1.save()

		ids = getCrisisIDs()
		# print "\n\n"
		# print ids
		# print ids.get('CRI_LGBTRU')

		self.assertEqual(temp_crisis1.name, ids.get('CRI_FWATER'))


# 	#---------------------------------------#
# 	#-----test_getPeopleIDs
# 	#---------------------------------------#

	def test_getPeopleIDs1(self):
		temp_person1           = Person()
		temp_person1.person_ID = "PER_TTHBLD"
		temp_person1.name      = "Tom Theobald"
		temp_person1.kind      = "Beekeeper"
		temp_person1.location  = "4802 Gatewood Dr, Colorado Springs, CO, USA"

		temp_person2           = Person()
		temp_person2.person_ID = "PER_DLVRUS"
		temp_person2.name      = "Dilma Vana Rousseff"
		temp_person2.kind      = "Politician"
		temp_person2.location  = "Rio de Janeiro"

		temp_person3           = Person()
		temp_person3.person_ID = "PER_ESNWDN"
		temp_person3.name      = "Edward Snowden"
		temp_person3.kind      = "Whistleblower"
		temp_person3.location  = "Moscow, Russia"

		temp_person1.save()
		temp_person2.save()
		temp_person3.save()

		ids = getPeopleIDs()

		self.assertEqual(temp_person1.name, ids.get('PER_TTHBLD'))
		self.assertEqual(temp_person2.name, ids.get('PER_DLVRUS'))
		self.assertEqual(temp_person3.name, ids.get('PER_ESNWDN'))


	def test_getPeopleIDs2(self):
		temp_person1           = Person()
		temp_person1.person_ID = "PER_YYAMAD"
		temp_person1.name      = "Yasuteru Yamad"
		temp_person1.kind      = "Proactive engineer"
		temp_person1.location  = "Japan"

		temp_person2           = Person()
		temp_person2.person_ID = "PER_HPASSS"
		temp_person2.name      = "Hildebrando Pascoal"
		temp_person2.kind      = "Former Politician"
		temp_person2.location  = "Rio de Janeiro"

		temp_person1.save()
		temp_person2.save()

		ids = getPeopleIDs()

		self.assertEqual(temp_person1.name, ids.get('PER_YYAMAD'))
		self.assertEqual(temp_person2.name, ids.get('PER_HPASSS'))


	def test_getPeopleIDs3(self):
		temp_person1           = Person()
		temp_person1.person_ID = "PER_XNSHNG"
		temp_person1.name      = "Zhang Xinsheng"
		temp_person1.kind      = "President of International Union for Conservation of Nature"
		temp_person1.location  = "China"

		temp_person1.save()

		ids = getPeopleIDs()

		self.assertEqual(temp_person1.name, ids.get('PER_XNSHNG'))


# 	#---------------------------------------#
# 	#-----test_getOrgIDs
# 	#---------------------------------------#

	def test_getOrgIDs1(self):
		temp_org1           = Org()
		temp_org1.org_ID    = "ORG_UOCSCI"
		temp_org1.name      = "The Union of Concerned Scientists"
		temp_org1.kind      = "Government Fund"
		temp_org1.location  = "USA"

		temp_org2           = Org()
		temp_org2.org_ID    = "ORG_NSAAAA"
		temp_org2.name      = "National Security Agency"
		temp_org2.kind      = "Government"
		temp_org2.location  = "Fort Meade, Maryland"

		temp_org3           = Org()
		temp_org3.org_ID    = "ORG_FEMAAA"
		temp_org3.name      = "Federal Emergency Management Service"
		temp_org3.kind      = "Government Organization"
		temp_org3.location  = "500 C Street SW, Washington, DC 20472"

		temp_org1.save()
		temp_org2.save()
		temp_org3.save()

		ids = getOrgIDs()

		self.assertEqual(temp_org1.name, ids.get('ORG_UOCSCI'))
		self.assertEqual(temp_org2.name, ids.get('ORG_NSAAAA'))
		self.assertEqual(temp_org3.name, ids.get('ORG_FEMAAA'))


	def test_getOrgIDs2(self):
		temp_org1           = Org()
		temp_org1.org_ID    = "ORG_GAYRUS"
		temp_org1.name      = "LGBT Human Rights Project GayRussia.Ru"
		temp_org1.kind      = "Activist Group"
		temp_org1.location  = "Russia"

		temp_org2           = Org()
		temp_org2.org_ID    = "ORG_WATERO"
		temp_org2.name      = "Water.org"
		temp_org2.kind      = "Nonprofit Developmental Aid Organization"
		temp_org2.location  = "United States"

		temp_org1.save()
		temp_org2.save()

		ids = getOrgIDs()

		self.assertEqual(temp_org1.name, ids.get('ORG_GAYRUS'))
		self.assertEqual(temp_org2.name, ids.get('ORG_WATERO'))


	def test_getOrgIDs3(self):
		temp_org1           = Org()
		temp_org1.org_ID    = "ORG_LOSZTA"
		temp_org1.name      = "Los Zetas Cartel"
		temp_org1.kind      = "Drug Cartel"
		temp_org1.location  = "Mexico"

		temp_org1.save()

		ids = getOrgIDs()

		self.assertEqual(temp_org1.name, ids.get('ORG_LOSZTA'))

