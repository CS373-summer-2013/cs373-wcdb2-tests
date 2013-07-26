"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# ---------
# imports
# ---------
from django.test import TestCase
from xml_import_export import verifyXML, saveModels, exportModels
import os
import xml.etree.ElementTree as ET
from genxmlif import GenXmlIfError
from minixsv import pyxsval
from wcdb_app.models import Person, Crisis, Org, List, Common
from StringIO import StringIO
import settings

# ------------
# SimpleTest
# ------------
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

# -----------------
# xml_file_as_str
# -----------------
def xml_file_as_str(path):
    xml = ""
    f = open(path, 'r')
    for l in f:
        xml += l
    return xml

# ---------
# XMLTest
# ---------
class XMLTest(TestCase):
    
    def test_xml_import(self):
        path = os.getcwd() + "/wcdb_app/WorldCrises.xml"
        result = verifyXML(xml_file_as_str(path))
        self.assertEqual(type(result[0]), ET.Element) 

    def test_xml_import_fails(self):
        path = os.getcwd() + "/wcdb_app/BadXML.xml"
        result = verifyXML(xml_file_as_str(path))
        self.assertEqual(result[0], None)

    def test_xml_import_generated(self):
        path = os.getcwd() + "/wcdb_app/GeneratedWCDB.xml"
        result = verifyXML(xml_file_as_str(path))
        self.assertEqual(type(result[0]), ET.Element) 

    def test_save_models(self):
        path = os.getcwd() + "/wcdb_app/WorldCrises.xml"
        root = verifyXML(xml_file_as_str(path))
        saveModels(root[0])
        p = Person.objects.get(xml_id='PER_MNSNGH')
        c = Crisis.objects.get(xml_id='CRI_NRINFL')
        self.assertEqual(p.name, 'Manmohan Singh')
        self.assertEqual(c.kind, 'Natural Disaster')
        exportModels()

    def test_save_models_common(self):
        path = os.getcwd() + "/wcdb_app/WorldCrises.xml"
        root = verifyXML(xml_file_as_str(path))
        saveModels(root[0])
        c = Crisis.objects.get(xml_id='CRI_NRINFL')
        self.assertTrue('Lorem ipsum...' in c.common.summary)

    def test_export_models_generated(self):
        path = os.getcwd() + "/wcdb_app/GeneratedWCDB.xml"
        root = verifyXML(xml_file_as_str(path))
        saveModels(root[0])
        export = exportModels()
        result = verifyXML(export)
        self.assertEqual(type(result[0]), ET.Element)

    def test_export_models(self):
        path = os.getcwd() + "/wcdb_app/WorldCrises.xml"
        root = verifyXML(xml_file_as_str(path))
        saveModels(root[0])
        export = exportModels()
        result = verifyXML(export)
        self.assertEqual(type(result[0]), ET.Element)
    
#----------
#View Tests
#----------

    def test_view_home_1(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_home_2(self):
        response = self.client.get("/")
        self.assertEqual(len(response.templates), 2)

    def test_view_home_3(self):
        response = self.client.get("/")
        self.assertEqual(response.templates[0].name, 'home.html')


    def test_crises_index_1(self):
        response = self.client.get("/crises/index/")
        self.assertEqual(response.status_code, 200)

    def test_crises_index_2(self):
        response = self.client.get("/crises/index/")
        self.assertEqual(len(response.templates), 2)

    def test_crises_index_3(self):
        response = self.client.get("/crises/index/")
        self.assertEqual(response.templates[0].name, 'dynamic_pages/crises_index.html')


    def test_orgs_index_1(self):
        response = self.client.get("/orgs/index/")
        self.assertEqual(response.status_code, 200)

    def test_orgs_index_2(self):
        response = self.client.get("/orgs/index/")
        self.assertEqual(len(response.templates), 2)

    def test_orgs_index_3(self):
        response = self.client.get("/orgs/index/")
        self.assertEqual(response.templates[0].name, 'dynamic_pages/orgs_index.html')


    def test_people_index_1(self):
        response = self.client.get("/people/index/")
        self.assertEqual(response.status_code, 200)

    def test_people_index_2(self):
        response = self.client.get("/people/index/")
        self.assertEqual(len(response.templates), 2)

    def test_people_index_3(self):
        response = self.client.get("/people/index/")
        self.assertEqual(response.templates[0].name, 'dynamic_pages/people_index.html')


    def test_crises_detail_1(self):
        response = self.client.get("/crises/error/NotACrisis/")
	self.assertEqual(response.templates[0].name, 'error_pages/crisis.html')

    def test_crises_detail_2(self):
        response = self.client.get("/crises/2010%20Haiti%20Earthquake/")
	self.assertEqual(response.status_code, 302)

    def test_crises_detail_3(self):
        response = self.client.get("/crises/2010%20Haiti%20Earthquake/")
	self.assertEqual(len(response.templates), 0)


    def test_orgs_detail_1(self):
        response = self.client.get("/orgs/error/NotAnOrg/")
	self.assertEqual(response.templates[0].name, 'error_pages/org.html')

    def test_orgs_detail_2(self):
        response = self.client.get("/orgs/Federal%20Emergency%20Management%20Agency/")
	self.assertEqual(response.status_code, 302)

    def test_orgs_detail_3(self):
        response = self.client.get("/orgs/Federal%20Emergency%20Management%20Agency/")
	self.assertEqual(len(response.templates), 0)


    def test_people_detail_1(self):
        response = self.client.get("/people/error/NotAPerson/")
	self.assertEqual(response.templates[0].name, 'error_pages/person.html')

    def test_people_detail_2(self):
        response = self.client.get("/people/Barack%20Obama/")
	self.assertEqual(response.status_code, 302)

    def test_people_detail_3(self):
        response = self.client.get("/people/Barack%20Obama/")
	self.assertEqual(len(response.templates), 0)

    #-----------
    #Model Tests
    #-----------


    def test_list(self):
        ls = List(href = "asdf", embed = "qwer", text = "more text")
        ls.save()
        self.assertEquals(ls.href, "asdf")
        self.assertEquals(ls.embed, "qwer")
        self.assertEquals(ls.text, "more text")

    def test_common(self):
        cn = Common(summary = "Short summary")
        self.assertEquals(cn.summary, "Short summary")

    def test_person(self):
        per = Person(xml_id = "TES_QQQQQQ", name = "Charlie", kind = "Deadbeat", location = "Colorado")
        per.save()
        self.assertEquals(per.xml_id, "TES_QQQQQQ")
        self.assertEquals(per.name, "Charlie")
        self.assertEquals(per.kind, "Deadbeat")
        self.assertEquals(per.location, "Colorado")
       # self.assertEquals(ls.common, None)

    def test_org(self):
        org = Org(xml_id="123456", kind="kind", name="org", location="loc")
        org.save()
        self.assertEqual(org.xml_id, "123456")
        self.assertEqual(org.kind, "kind")
        self.assertEqual(org.name, "org")
        self.assertEqual(org.location, "loc")

    def test_crisis(self):
        cri = Crisis(xml_id="123456", kind="kind", name="name", time="time")
        cri.save()
        self.assertEqual(cri.xml_id, "123456")
        self.assertEqual(cri.kind, "kind")
        self.assertEqual(cri.name, "name")
        self.assertEqual(cri.time, "time")

    def test_list_fail(self):
        try:
            ls = List()
            self.assert_(False)
        except:
            self.assert_(True)

    def test_common_fail(self):
        try:
            cm = Common()
            self.assert_(False)
        except:
            self.assert_(True)

    
    def test_person_fail(self):
        try:
            per = Person(name="name")
            self.assert_(False)
        except:
            self.assert_(True)

    def test_org_fail(self):
        try:
            org = Org(xml_id="98412478092384092834")
            self.assert_(False)
        except:
            self.assert_(True)

    def test_crsis_fail(self):
        try:
            crisis = Crisis(kind="helloworld")
            self.assert_(False)
        except:
            self.assert_(True)

    def test_list_fail_2(self):
        try:
            ls = List(href=False)
            self.assert_(False)
        except:
            self.assert_(True)

    def test_common_fail_2(self):
        try:
            common = Common(citations=None, images='')
            self.assert_(False)
        except:
            self.assert_(True)

    def test_person_fail_2(self):
        try:
            person = Person(xml_id="123456", kind="kind", name="org", location="loc")
            self.assert_(False)
        except:
            self.assert_(True)

    def test_org_fail_2(self):
        try:
            org = Org(xml_id="123456", kind="kind", name="name", time="time")
            self.assert_(False)
        except:
            self.assert_(True)

    def test_crisis_fail_2(self):
        try:
            crisis = Crisis(xml_id="123456", kind="kind", name="name")
            self.assert_(False)
        except:
            self.assert_(True)

    """
    def test_xml_view_4(self):
        self.client.login(username = "django_unchained", password = "du1342AY!")
        response = self.client.post("/technical/xml/")
        self.assertHTMLEqual(response.content, "<html><body><h1>No file uploaded</h1></body></html>")

    def test_xml_view_5(self):
        self.client.login(username = "django_unchained", password = "du1342AY!")
        with open("WorldCrises.xml") as f:
          response = self.client.post("/technical/xml/", { 'name': 'xml_file', 'attachment': f })

          contents = ''
          for l in f:
              contents += l
          self.assertEquals(response.content, l)

    def test_xml_view_6(self):
        self.client.login(username = "django_unchained", password = "du1342AY!")
        with open("WorldCrises.xml") as f:
          response = self.client.post("/technical/xml/", { 'name': 'file', 'attachment': f })
          self.assertHTMLEqual(response.content, "<html><body><h1>Missing file 'xml_file'</h1></body></html>")
    """




    """
    def test_xml_import_1(self):
      self.client.login(username = "django_unchained", password = "du1342AY!")
      f = StringIO()
      f.write("lkjsadklfjweakraf")
      response = self.client.post("/technical/xml/import", { 'name': 'file', 'attachment': f })
      self.assertEquals(response.status_code, 500)

    def test_xml_import_2(self):
      self.client.login(username = "django_unchained", password = "du1342AY!")
      with open("WorldCrises.xml") as f:
        response = self.client.post("/technical/xml/import", { 'name': 'xml_file', 'attachment': f })
        self.assertEquals(response.status_code, 200)

    def test_xml_import_3(self):
        self.client.login(username = "django_unchained", password = "du1342AY!")
        response = self.client.get("/technical/xml/import")
        self.asserEquals(response.templates[0].name, "technical/import_xml.html")
    """
