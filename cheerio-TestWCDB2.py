"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
import sys
import StringIO
from django.test.simple import DjangoTestSuiteRunner
from django.http import HttpResponse
from django.conf import settings
from wcdb_export import xml_mods2etree, xml_etree2xml
from wcdb_import import xml_validate, xml_reader, xml_etree2mods 
from models import People, Crises, Organizations, List_Item
import xml.etree.ElementTree as ET
import unittest
from types import *

class SimpleTest(unittest.TestCase):

	# ------------
	# xml_validate
	# ------------

	def test_xml_validate_1(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		self.assertEqual(xml_validate(xml_file, xml_schema), True)
			
	def test_xml_validate_2(self) :
		xml_file   = open('wcdb/WCDB2Fail.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		self.assertEqual(xml_validate(xml_file, xml_schema), False)
	
	def test_xml_validate_3(self) :
		try :
			xml_file   = open('wcdb/models.py', 'r')
			xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
			self.assertEqual(xml_validate(xml_file, xml_schema), False)
			assert(False)
		except Exception :
			assert(True)
			
	
	# ----------
	# xml_reader
	# ----------

	def test_xml_reader_1(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))

	def test_xml_reader_2(self) :
		xml_file   = open('wcdb/WCDB2Fail.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertTrue(et, 1)	
	
	def test_xml_reader_3(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		
		crisis_cnt = 0
		person_cnt = 0
		org_cnt    = 0
		for child in list(et.getroot()) :
			if child.tag == "Crisis" :
				crisis_cnt += 1
			elif child.tag == "Organization" :
				org_cnt += 1
			elif child.tag == "Person" :
				person_cnt += 1

		self.assertEqual(crisis_cnt, 10)
		self.assertEqual(person_cnt, 11)
		self.assertEqual(org_cnt,    11)


	# --------------
	# xml_etree2mods
	# --------------
        


	def test_etree2mods_1(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		self.assertTrue(len(People.objects.all()) > 0)
		self.assertTrue(len(Crises.objects.all()) > 0)
		self.assertTrue(len(Organizations.objects.all()) > 0)
		self.assertTrue(len(List_Item.objects.all()) > 0)
		
	def test_etree2mods_2(self) :
		our_ids = [ 'CRI_CHINAD', 'CRI_SCMARI', 'CRI_NKCONF', 'CRI_FINCRI', 'CRI_HUMTRA',
					'CRI_EGYPTR', 'CRI_AIDSHI', 'CRI_AZWILD', 'CRI_LRACON', 'CRI_OSLOSH',
					'PER_MMORSI', 'PER_LALOCA', 'PER_GASPAR', 'PER_CYLUNG', 'PER_JKERRY',
					'PER_BROBMA', 'PER_MAGICJ', 'PER_COPETE', 'PER_VPUTIN', 'PER_JEABEL', 'PER_JONGUN',
					'ORG_MAMFDN', 'ORG_FIREDP', 'ORG_PARIBS', 'ORG_ASEANA', 'ORG_POLARS',
					'ORG_IMFUND', 'ORG_UNINAT', 'ORG_RIBBON', 'ORG_SALARM', 'ORG_WHORGN', 'ORG_CHILDR']
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		people = People.objects.all()

		for p in people :
			self.assertEqual(p.idref in our_ids, True)		
	
	def test_etree2mods_3(self) :
		our_ids = [ 'CRI_CHINAD', 'CRI_SCMARI', 'CRI_NKCONF', 'CRI_FINCRI', 'CRI_HUMTRA',
					'CRI_EGYPTR', 'CRI_AIDSHI', 'CRI_AZWILD', 'CRI_LRACON', 'CRI_OSLOSH',
					'PER_MMORSI', 'PER_LALOCA', 'PER_GASPAR', 'PER_CYLUNG', 'PER_JKERRY',
					'PER_BROBMA', 'PER_MAGICJ', 'PER_COPETE', 'PER_VPUTIN', 'PER_JEABEL', 'PER_JONGUN',
					'ORG_MAMFDN', 'ORG_FIREDP', 'ORG_PARIBS', 'ORG_ASEANA', 'ORG_POLARS',
					'ORG_IMFUND', 'ORG_UNINAT', 'ORG_RIBBON', 'ORG_SALARM', 'ORG_WHORGN', 'ORG_CHILDR']
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		orgs = Organizations.objects.all()

		for o in orgs :
			self.assertEqual(o.idref in our_ids, True)		
	
	def test_etree2mods_4(self) :
		our_ids = [ 'CRI_CHINAD', 'CRI_SCMARI', 'CRI_NKCONF', 'CRI_FINCRI', 'CRI_HUMTRA',
					'CRI_EGYPTR', 'CRI_AIDSHI', 'CRI_AZWILD', 'CRI_LRACON', 'CRI_OSLOSH',
					'PER_MMORSI', 'PER_LALOCA', 'PER_GASPAR', 'PER_CYLUNG', 'PER_JKERRY',
					'PER_BROBMA', 'PER_MAGICJ', 'PER_COPETE', 'PER_VPUTIN', 'PER_JEABEL', 'PER_JONGUN',
					'ORG_MAMFDN', 'ORG_FIREDP', 'ORG_PARIBS', 'ORG_ASEANA', 'ORG_POLARS',
					'ORG_IMFUND', 'ORG_UNINAT', 'ORG_RIBBON', 'ORG_SALARM', 'ORG_WHORGN', 'ORG_CHILDR']
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		crises = Crises.objects.all()

		for c in crises :
			self.assertEqual(c.idref in our_ids, True)		
	
	# ------
	# models
	# ------
	
	def test_tables_exist(self) :
		self.assertTrue(len(People.objects.all()) > 0)
		self.assertTrue(len(Crises.objects.all()) > 0)
		self.assertTrue(len(Organizations.objects.all()) > 0)
		self.assertTrue(len(List_Item.objects.all()) > 0)

	# -------------
	# xml_etree2xml
	# -------------

	def test_xml_etree2xml_1(self) :
		et = xml_mods2etree()
		xml_text = xml_etree2xml(et)
		self.assertEqual(type(xml_text) is UnicodeType, True)
	
	def test_xml_etree2xml_2(self) :
		root = ET.Element("Tag1")
		sub = ET.Element("Tag2")
		root.append(sub)
		et = ET.ElementTree(root)

		output = "<Tag1>\n\t<Tag2></Tag2 >\n</Tag1 >"
		
		xml_text = xml_etree2xml(et)
		self.assertEqual(xml_text == output, True)
	
	# --------------
	# xml_mods2etree
	# --------------

	def test_xml_mods2etree_1(self):
		et = xml_mods2etree()
		root = et.getroot()
		self.assertEqual(type(et), type(ET.ElementTree('')))
		self.assertEqual(root.tag, 'WorldCrises')


		for child in list(root) :
			valid = child.tag == "Crisis" or child.tag == "Organization" or child.tag == "Person"
			self.assertEqual(valid, True)

	def test_xml_mods2etree_2(self):
		et = xml_mods2etree()
		root = et.getroot()
		self.assertEqual(type(et), type(ET.ElementTree('')))
		self.assertEqual(root.tag, 'WorldCrises')
		crisis_cnt = 0
		person_cnt = 0
		org_cnt    = 0
		for child in list(root) :
			if child.tag == "Crisis" :
				crisis_cnt += 1
			elif child.tag == "Organization" :
				org_cnt += 1
			elif child.tag == "Person" :
				person_cnt += 1

		self.assertEqual(crisis_cnt, 10)
		self.assertEqual(person_cnt, 11)
		self.assertEqual(org_cnt,    11)

	def test_xml_mods2etree_3(self):
		p = People(idref="PER_TCANNO", name="Taylor Cannon", kind="badass")
		p.save()
		et = xml_mods2etree()
		root = et.getroot()
		self.assertEqual(type(et), type(ET.ElementTree('')))
		self.assertEqual(root.tag, 'WorldCrises')
		crisis_cnt = 0
		person_cnt = 0
		org_cnt    = 0
		for child in list(root) :
			if child.tag == "Crisis" :
				crisis_cnt += 1
			elif child.tag == "Organization" :
				org_cnt += 1
			elif child.tag == "Person" :
				person_cnt += 1

		self.assertEqual(crisis_cnt, 10)
		self.assertEqual(person_cnt, 11)
		self.assertEqual(org_cnt,    11)

def do_test():
	return 'nope'
	settings.RUNNING_OFF_TEST_DB = True
	result = StringIO.StringIO('')
	suite = unittest.TestLoader().loadTestsFromTestCase(SimpleTest)
	unittest.TextTestRunner(stream=result,verbosity=0).run(suite)
	return result.getvalue()
