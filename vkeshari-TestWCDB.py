"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
import xml.etree.ElementTree as ET
from ModelFactory import create_crisis_element, create_org_element, create_person_element, read_wcdb_model, read_list_content, read_common_content
from XMLUtility import print_rec_xml, initialize_pages, parse_models, parse_xml, process_xml, read_and_validate_xml
from crises.models import WCDBElement, Crisis, Organization, Person, ListType, LI, R_Crisis_Person, R_Crisis_Org, R_Org_Person
from genxmlif import GenXmlIfError
from minixsv import pyxsval
from django.test.simple import DjangoTestSuiteRunner
from django.test import Client
from django.test import TestCase


####
####Begin blackbox tests
####

class TestViews(TestCase) :
	@classmethod
	def setUpClass(cls) :
		client = Client()
		with open('WCDB_tmp.xml') as fp:
			response = client.post('/import/', {'password': 'baddatamining', 'docfile':fp})

	def setUp(self):
		self.client = Client()

	def test_import (self) :
		with open('WCDB_tmp.xml') as fp:
			response = self.client.post('/import/')
		self.assertEqual(response.status_code, 200)

	def test_index (self) :
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTrue("Ambareesha Nittala" in response.content)
		self.assertTrue("Brandon Fairchild" in response.content)
		self.assertTrue("Chris Coney" in response.content)
		self.assertTrue("Roberto Weller" in response.content)
		self.assertTrue("Rogelio Sanchez" in response.content)
		self.assertTrue("Vineet Keshari" in response.content)

	def test_crisis (self) :
		response = self.client.get('/crises/CRI_UEGYPT/')
		self.assertTrue("Summary" in response.content)
		self.assertTrue("Human Impact" in response.content)
		self.assertTrue("As many as 846 deaths and over 6000 injuries." in response.content)
		self.assertTrue("Economic Impact" in response.content)
		self.assertTrue("ion in lost foreign currency and gold reserv" in response.content)
		self.assertTrue("Ways to Help:" in response.content)
		self.assertTrue("Help in Egypt" in response.content)
		self.assertTrue("Resources Needed" in response.content)
		self.assertTrue("Economist, social reformers, stable goverm" in response.content)
		self.assertTrue("Feeds" in response.content)
		self.assertTrue("External Link" in response.content)
		self.assertTrue("Wikipedia article" in response.content)
		self.assertTrue("Citations" in response.content)
		self.assertTrue("rt.com" in response.content)

	def test_org (self) :
		response = self.client.get('/crises/ORG_PMRLFD/')
		self.assertTrue("Governement Fund" in response.content)
		self.assertTrue("In pursuance of an appea" in response.content)
		self.assertTrue("India" in response.content)
		self.assertTrue("2013 Northern India Floods" in response.content)
		self.assertTrue("Manmohan Singh" in response.content)
		self.assertTrue("<img src=http://photogallery.indiatimes.com/news/india/rescue-relief-uttarakhand/photo/20713370/Army-men-unload-relief-material-from-an-IAF-MI-26-helicopter-at-Gauchar-district-Chamoli-in-Uttarakhand-.jpg alt=" in response.content)

	def test_people  (self) :
		response = self.client.get('/crises/PER_GEDAPE/')
		self.assertTrue("Former Director CIA" in response.content)
		self.assertTrue("None" in response.content)
		self.assertTrue("Los Angeles, CA" in response.content)
		self.assertTrue("US Drone Attacks in Pakistan" in response.content)
		self.assertTrue("Central Intelligence Agency" in response.content)
		self.assertTrue("img src=http://msnbcmedia.msn.com/j/MSNBC/Components/Photo/_new/121109-david-petraeus-wife-1258p.380;380;7;70;0.jpg" in response.content)		

####
####Begin whitebox tests
####
class TestXMLUtility (unittest.TestCase) :
	def test_process_xml_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		# model = process_xml(testXMLFile)
		# assert(len(model["crises"])==1)
		# assert(type(model["crises"]["CRI_NRINFL"]) is Crisis)
		# assert(len(model["people"])==1)
		# assert(type(model["people"]["PER_MNSNGH"]) is Person)
		# assert(len(model["orgs"])==1)
		# assert(type(model["orgs"]["ORG_PMRLFD"]) is Organization)

	def test_process_xml_2(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_bad_root.xml"
			model = process_xml(testXMLFile)	
			assert(False)
		except :
			assert(True)

	def test_process_xml_3(self) :
		try :
			testXMLFile = ""
			model = process_xml(testXMLFile)	
			assert(False)
		except :
			assert(True)

	def test_initialize_pages_1(self) :
		all_models = initialize_pages()
		assert("crises" in all_models)
		assert("list_types" in all_models)
		assert("orgs" in all_models)
		assert("list_types" in all_models)
		assert("list_elements" in all_models)

	def test_read_and_validate_xml_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		model = read_and_validate_xml(testXMLFile)
		assert (model is not None)

	def test_read_and_validate_xml_2(self) :
		testXMLFile = "crises/test_data/WorldCrises_bad_root.xml"
		try :
			model = read_and_validate_xml(testXMLFile)
			assert(False)
		except :
			assert(True)

	def test_read_and_validate_xml_3(self) :
		testXMLFile = "crises/test_data/WorldCrises_bad_id.xml"
		try :
			model = read_and_validate_xml(testXMLFile)
			assert(False)
		except :
			assert(True)	

	def test_parse_xml_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		xml = read_and_validate_xml(testXMLFile)
		model = parse_xml (xml)
		assert(len(model["crises"])==1)
		assert(type(model["crises"]["CRI_NRINFL"]) is Crisis)
		assert(len(model["people"])==1)
		assert(type(model["people"]["PER_MNSNGH"]) is Person)
		assert(len(model["orgs"])==1)
		assert(type(model["orgs"]["ORG_PMRLFD"]) is Organization)

	def test_parse_xml_2(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_bad_root.xml"
			xml = read_and_validate_xml(testXMLFile)
			model = parse_xml (xml)	
			assert(False)
		except :
			assert(True)

	def test_parse_xml_3(self) :
		try :
			testXMLFile = ""
			xml = read_and_validate_xml(testXMLFile)
			model = parse_xml (xml)		
			assert(False)
		except :
			assert(True)

	def test_print_rec_xml_1(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_good.xml"
			xml = read_and_validate_xml(testXMLFile)
			#print_rec_xml(xml, 0)
			assert(True)
		except :
			assert(False)

	def test_parse_models_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		root = read_and_validate_xml (testXMLFile)
		model = initialize_pages ()
		parse_models (root, model)
		assert(len(model["crises"])==1)
		assert(type(model["crises"]["CRI_NRINFL"]) is Crisis)
		assert(len(model["people"])==1)
		assert(type(model["people"]["PER_MNSNGH"]) is Person)
		assert(len(model["orgs"])==1)
		assert(type(model["orgs"]["ORG_PMRLFD"]) is Organization)

	def test_parse_models_2(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_good.xml"
			root = read_and_validate_xml (testXMLFile)
			model = initialize_pages ()
			parse_models (root, model)
			assert(False)
		except :
			assert(True)

	def test_parse_models_3(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_good.xml"
			root = read_and_validate_xml (testXMLFile)
			model = initialize_pages ()
			parse_models (root, model)	
			assert(False)
		except :
			assert(True)

		

class TestModelFactoryUtility (unittest.TestCase) :
	def test_create_crisis_element_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		root = read_and_validate_xml (testXMLFile)
		model = create_crisis_element (root[0])		
		assert(model[0] == "CRI_NRINFL")
		assert(type(model[1]) is Crisis)

	def test_create_crisis_element_2(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_bad_crisis.xml"
			root = read_and_validate_xml (testXMLFile)
			model = create_crisis_element (root[0])		
			assert(False)
		except :
			assert(True)

	def test_create_org_element_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		root = read_and_validate_xml (testXMLFile)
		model = create_org_element (root[2])		
		assert(model[0] == "ORG_PMRLFD")
		assert(type(model[1]) is Organization)

	def test_create_org_element_2(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_bad_org.xml"
			root = read_and_validate_xml (testXMLFile)
			model = create_org_element (root[2])		
			assert(False)
		except :
			assert(True)

	def test_create_person_element_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		root = read_and_validate_xml (testXMLFile)
		model = create_person_element (root[1])		
		assert(model[0] == "PER_MNSNGH")
		assert(type(model[1]) is Person)

	def test_create_person_element_2(self) :
		try :
			testXMLFile = "crises/test_data/WorldCrises_bad_person.xml"
			root = read_and_validate_xml (testXMLFile)
			model = create_person_element (root[1])		
			assert(False)
		except :
			assert(True)

	def test_read_common_content_1(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		root = read_and_validate_xml (testXMLFile)
		common = root[0].find('Common')
		a = []
		b = []
		read_common_content ("ORG_PMRLFD", common, a, b)
		assert (len(a) > 0)
		assert (len(b) > 0)

	def test_read_common_content_2(self) :
		testXMLFile = "crises/test_data/WorldCrises_good.xml"
		root = read_and_validate_xml (testXMLFile)
		common = root[0].find('NotCommon')
		a = []
		b = []
		try :
			read_common_content ("ORG_PMRLFD", common, a, b)
			assert(False)
		except :
			assert(True)