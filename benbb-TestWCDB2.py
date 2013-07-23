"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

We will definitely want to add many many more tests, but for now, 3 per
function will have to do.


"""
# --- imports ---
import StringIO
import xml.etree.ElementTree as et
from django.test import TestCase
from django.db.models.base import ObjectDoesNotExist
import crises.models as cm
from scripts.importScript import *
from scripts.export import *

class Empty:
    pass

NIFCrisis = """
    <Crisis ID="CRI_AURSHO" Name="2013 Northern India Floods">
        <Kind>Natural Disaster</Kind>
        <Date>2013-06-14</Date>
        <Time>09:00:00</Time>
        <Common>
            <Citations>
                <li>The Hindustan Times</li>
                <li>The Times of India</li>
            </Citations>
            <ExternalLinks>
                <li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li>
            </ExternalLinks>
            <Images>
                <li embed="http://images.jagran.com/ukhand-ss-02-07-13.jpg" text="This is the alt element of the image."/>
                <li embed="http://timesofindia.indiatimes.com/photo/15357310.cms"/>
            </Images>
            <Videos>
                <li embed="//www.youtube.com/embed/qV3s7Sa6B6w"/>
            </Videos>
            <Maps>
                <li embed="[fake]"/>
            </Maps>
            <Feeds>
                <li embed="[WHATEVER A FEED URL LOOKS LIKE]"/>
            </Feeds>
            <Summary>Lorem ipsum...</Summary>
        </Common>
    </Crisis>
"""

CFFOrg = """
    <Organization ID="ORG_COFIFO" Name="The Community First Foundation">
        <Crises>
            <Crisis ID="CRI_AURSHO"/>
        </Crises>
        <Kind>Charity</Kind>
        <Location>United States</Location>
        <History>
            <li>This is a story all about how...</li>
        </History>
    </Organization>
"""

JEHPerson = """
    <Person ID="PER_JAEAHO" Name="James Eagen Holmes">
        <Crises>
            <Crisis ID="CRI_AURSHO"/>
        </Crises>
        <Organizations>
            <Org ID="ORG_COFIFO" />
        </Organizations>
        <Kind>Mass Murderer</Kind>
        <Location>Aurora, CO, USA</Location>
        <Common>
            <Summary>I have nothing nice to say about this man.</Summary>
        </Common>
    </Person>
"""

TestFile = "<WorldCrises>"+"\n"+ NIFCrisis +"\n"+ JEHPerson+"\n" +CFFOrg +"\n" + "</WorldCrises>"

class TestImportScript(TestCase):
    # TODO must make sure to make proper XML strings for these
    def test_parsevalidate_01(TestCase):
        assert validateXML(TestFile)
        
    def test_parsevalidate_02(TestCase):
        assert not validateXML(NIFCrisis)
        
    def test_parsevalidate_03(TestCase):
        testXML = StringIO.StringIO("<Dragon><Cooly></Cooly></Dragon>")
        assert not validateXML(testXML)
        
    def test_parseXML_01(self):
        testXML = StringIO.StringIO("<Dragon></Dragon>")
        try:
            root = parseXML(testXML)
            assert(False)
        except Exception:
            pass

    def test_parseXML_02(TestCase):
        testXML = StringIO.StringIO(TestFile)
        root = None
        try:
            parseXML(testXML)
            assert(False)
        except Exception:
            pass

    def test_parseXML_03(TestCase):
        testXML = StringIO.StringIO(TestFile)
        try:
            parseXML(testXML)
            assert(False)
        except Exception:
            pass

    def test_parseCrisis_01(TestCase):
        testElement = et.fromstring(NIFCrisis)
        testDict = {}
        testCrisis = parseCrisis(testElement)
        try:
            testCrisisCopy = cm.Crisis.objects.get(id="CRI_AURSHO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testCrisis == testCrisisCopy)
        assert(testCrisis.name == "2013 Northern India Floods")

    def test_parseCrisis_02(TestCase):
        try:
            while True:
                testCrisisCopy = cm.Crisis.objects.get(id="CRI_AURSHO")
                testCrisisCopy.delete()
                assert(False)
        except ObjectDoesNotExist:
            pass
        
    def test_parseCrisis_03(TestCase):
        testElement = et.fromstring(NIFCrisis)
        testDict = {}
        testCrisis = parseCrisis(testElement)
        try:
            testCrisisCopy = cm.Crisis.objects.get(id="CRI_AURSH")
            assert(False)
        except ObjectDoesNotExist:
            pass
        
    def test_parseOrganization_01(TestCase):
        testElement = et.fromstring(CFFOrg)
        testDict = {}
        testOrg = parseOrganization(testElement)
        try:
            testOrgCopy = cm.Organization.objects.get(id="ORG_COFIFO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testOrg == testOrgCopy)
        assert(testOrg.kind == "Charity")
        
    def test_parseOrganization_02(TestCase):
        testElement = et.fromstring(CFFOrg)
        testDict = {"ORG_COFIFO" : parseOrganization(testElement)}
        try:
            testOrgCopy = cm.Organization.objects.get(id="ORG_COFIFO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testDict["ORG_COFIFO"] == testOrgCopy)
        
    def test_parseOrganization_03(TestCase):
        testElement = et.fromstring(CFFOrg)
        testDict = {}
        testOrg = parseOrganization(testElement)
        try:
            while True:
                testOrg.delete()
                testOrgCopy = cm.Organization.objects.get(id="CRI_COFIFO")
                assert(False)
        except ObjectDoesNotExist:
            pass
        
    def test_parsePerson_01(TestCase):
        testElement = et.fromstring(JEHPerson)
        testDict = {}
        testPer = parsePerson(testElement)
        try:
            testPerCopy = cm.Person.objects.get(id="PER_JAEAHO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testPer == testPerCopy)
        assert(testPer.kind == "Mass Murderer")
        
    def test_parsePerson_02(TestCase):
        testElement = et.fromstring(JEHPerson)
        testDict = {"PER_JAEAHO" : parsePerson(testElement)}
        try:
            testPerCopy = cm.Person.objects.get(id="PER_JAEAHO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testDict["PER_JAEAHO"] == testPerCopy)
        
    def test_parsePerson_03(TestCase):
        testElement = et.fromstring(JEHPerson)
        testDict = {}
        testPer = parsePerson(testElement)
        try:
            testPer.delete()
            testPerCopy = cm.Person.objects.get(id="PER_JAEAHO")
            assert(False)
        except ObjectDoesNotExist:
            pass


class TestExportScript(TestCase):
    #this test should fail if anything else fails
    def test_common_export(TestCase):
        owner = Empty()
        common = cm.Common()
        data = cm.CommonListType()
        data.href = "BOX"
        data.altText = "ALTERNATIVE MUSIC"
        data.embed = "EMBER"
        data.text = "HIDEY HO"
        
        common.save()
        data.owner_id = common.id
        owner.common_id = common.id
        
        data.save()
        
        test = et.Element("Test")
        
        createCommonNode(owner,test)
        assert(len(test.getchildren()) > 0)
        assert(test[0].tag == "Common")
        assert(test[0][0].tag == "ExternalLinks")
        assert(test[0][0][0].attrib["href"] == "BOX")
        assert(test[0][0][0].attrib["text"] == "ALTERNATIVE MUSIC")
        assert(test[0][0][0].attrib["embed"] == "EMBER")
        assert(test[0][0][0].text == "HIDEY HO")
        
    def test_crisis_export(TestCase):
        testElement = et.fromstring(NIFCrisis)
        testModel = parseCrisis(testElement)
        node = createCrisisElement(testModel)
        assert(testModel.id == node.attrib["ID"])
        assert(testModel.kind == node.find("Kind").text)
        assert(testModel.date.strftime("%Y-%m-%d") == node.find("Date").text)
        assert(testModel.time.strftime("%H:%M:%S") == node.find("Time").text)
        assert(testModel.name == node.attrib["Name"])
        
    def test_person_export(TestCase):
        testElement = et.fromstring(JEHPerson)
        testModel = parsePerson(testElement)
        node = createPersonElement(testModel)
        assert(testModel.id == node.attrib["ID"])
        assert(testModel.kind == node.find("Kind").text)
        assert(testModel.location == node.find("Location").text)
        assert(testModel.name == node.attrib["Name"])
    
    def test_org_export(TestCase):
        testElement = et.fromstring(CFFOrg)
        testModel = parseOrganization(testElement)
        node = createOrganizationElement(testModel)
        assert(testModel.id == node.attrib["ID"])
        assert(testModel.kind == node.find("Kind").text)
        assert(testModel.location == node.find("Location").text)
        assert(testModel.name == node.attrib["Name"])
        
    
    def test_everything(TestCase):
        testXML = StringIO.StringIO(TestFile)
        
        parse = parseXML(testXML)
        root = et.fromstring(TestFile)

        assert(et.tostring(parse) == et.tostring(root))
        
        xmlToModels(parse)
        node = exportXML()
        
        assert(validateXML(et.tostring(node)))
                
        root_iter = root.iter()
        node_iter = node.iter()
        done = [False, False]
        prevValA = root_iter.next()
        
        while not done[0] or not done[1]:
            valA = prevValA
            valToUse = prevValA
            valB = None
            
            try:
                valB = node_iter.next()
            except:
                done[1] = True
            
            try:
                if valB is not None and valB.tag == valA.tag:
                    valA = root_iter.next()
                else:
                    valA = None
            except:
                done[0] = True
            
            #print valB, valA if valA is None else valToUse

            if valA is not None:
                prevValA = valA
                
            #Asserts to make sure the tags being compared are the exact same
            if valA is not None:
                assert(valToUse.tag == valB.tag)
                if "ID" in valToUse.attrib:
                    assert(valToUse.attrib["ID"] == valB.attrib["ID"])
                if "Name" in valToUse.attrib:
                    assert(valToUse.attrib["Name"] == valB.attrib["Name"])
                if "href" in valToUse.attrib:
                    assert(valToUse.attrib["href"] == valB.attrib["href"])
                if "embed" in valToUse.attrib:
                    assert(valToUse.attrib["embed"] == valB.attrib["embed"])
                if "text" in valToUse.attrib:
                    assert(valToUse.attrib["text"] == valB.attrib["text"])
                if valToUse.text is not None and valToUse.text.strip() != "":
                    assert(valToUse.text == valB.text)
                
                
        """
        for root_child in root.iter():
            rootList += (root_child,)
        print nodeList
        print rootList
        """

