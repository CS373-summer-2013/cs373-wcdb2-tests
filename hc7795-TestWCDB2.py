#!/usr/bin/env python
"""
tests.py

To test the program:
	% python testWCDB2.py
"""


"""
Import.
"""

# ElementTree XML parsing.
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

# minixsv XML validation and parsing.
from minixsv import pyxsval
from genxmlif import GenXmlIfError

# Setup Django environment.
from django.core.management import setup_environ
import settings
setup_environ(settings)

# Django code.
from django.db import models
from wcdb.models import Person, Organization, Crisis

# xmlParser code.
from xmlParser import elementTreeToModels

# Misc.
import logging
import StringIO
import unittest


class testWCDB2(unittest.TestCase):
  
	def testelementTreeToModels_01(self):
		testXML = """
		<WorldCrises>
			<Crisis ID="CRI_HURIKE" Name="Hurricane Ike">
				<People>
					<Person ID="PER_RENPRE" />
				</People>
				<Organizations>
					<Org ID="ORG_FEDEMA" />
				</Organizations>
				<Kind>Natural Disaster</Kind>
				<Date>2008-09-01</Date>
				<Locations>
					<li>Turks and Caicos, Bahamas, Haiti, Dominican Republic, Cuba, Florida Keys, Mississippi, Louisiana, Texas, Mississippi Valley, Ohio Valley, Great Lakes region, Eastern Canada</li>
				</Locations>
				<HumanImpact>
					<li>Fatalities: 103 direct, 92 indirect</li>
				</HumanImpact>
				<EconomicImpact>
					<li>37.5 billion (2008 USD)</li>
				</EconomicImpact>
				<Common>
					<ExternalLinks>
						  <li href="https://en.wikipedia.org/wiki/Hurricane_Ike">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/c1/Hurricane_Ike_off_the_Lesser_Antilles.jpg" />
					</Images>
				</Common>
			</Crisis>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[0][0].id == "CRI_HURIKE" )
		self.assert_( models[0][0].name == "Hurricane Ike" )
		self.assert_( models[0][0].kind == "Natural Disaster" )
		self.assert_( models[0][0].date == "2008-09-01" )
		self.assert_( models[0][0].location == "['Turks and Caicos, Bahamas, Haiti, Dominican Republic, Cuba, Florida Keys, Mississippi, Louisiana, Texas, Mississippi Valley, Ohio Valley, Great Lakes region, Eastern Canada']" )
		self.assert_( models[0][0].humanImpact == "['Fatalities: 103 direct, 92 indirect']" )
		self.assert_( models[0][0].economicImpact == "['37.5 billion (2008 USD)']" )
		self.assert_( models[0][0].people == "['PER_RENPRE']" )
		self.assert_( models[0][0].organizations == "['ORG_FEDEMA']" )
		self.assert_( models[0][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Hurricane_Ike")
		self.assert_( models[0][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[0][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/c/c1/Hurricane_Ike_off_the_Lesser_Antilles.jpg")
		
		
	def testelementTreeToModels_02(self):
		testXML = """
		<WorldCrises>
			<Person ID="PER_BRAMAN" Name="Bradley Manning">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
				</Crises>
				<Organizations>
					<Org ID="ORG_IAVETA" />
				</Organizations>
				<Kind>Private First Class</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Bradley_Manning">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg" />
					 </Images>
				</Common>
			</Person>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)
		
		self.assert_( models[1][0].id == "PER_BRAMAN" )
		self.assert_( models[1][0].name == "Bradley Manning" )
		self.assert_( models[1][0].crises == "['CRI_BAGAIR']" )
		self.assert_( models[1][0].organizations == "['ORG_IAVETA']" )
		self.assert_( models[1][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Bradley_Manning")
		self.assert_( models[1][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg")
		
	def testelementTreeToModels_03(self):
		testXML = """
		<WorldCrises>
			<Organization ID="ORG_AQAEDA" Name="al-Qaeda">
				<Crises>
					<Crisis ID="CRI_IRAQWR" />
					<Crisis ID="CRI_NINEOO" />
				 </Crises>
				 <People>
					<Person ID="PER_OSAMAB" />
				  </People>
				  <Kind>Terrorist</Kind>
				  <Location>World Wide</Location>
				  <History>
					  <li>Founded in 1988</li>
				  </History>
				  <Common>
					  <ExternalLinks>
						  <li href="https://en.wikipedia.org/wiki/Al_Queda">Wikipedia</li>
					  </ExternalLinks>
				  </Common>
			</Organization>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)
		self.assert_( models[2][0].id == "ORG_AQAEDA" )
		self.assert_( models[2][0].name == "al-Qaeda" )
		self.assert_( models[2][0].kind == "Terrorist" )
		self.assert_( models[2][0].location == "World Wide" )
		self.assert_( str(models[2][0].history) == "['Founded in 1988']" )
		self.assert_( models[2][0].crises == "['CRI_IRAQWR', 'CRI_NINEOO']" )
		self.assert_( models[2][0].people == "['PER_OSAMAB']" )
		self.assert_( models[2][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Al_Queda")
		self.assert_( models[2][0].common.externalLinks.all()[0].content == "Wikipedia")
		
	def testelementTreeToModels_04(self):
		testXML = """
		<WorldCrises>
			<Crisis ID="CRI_SWNFLU" Name="Influenza A virus subtype H1N1">
				<People>
					<Person ID="PER_BROBMA" />
					<Person ID="PER_GHARTL" />
				</People>
				<Organizations>
					<Org ID="ORG_WHLORG" />
					<Org ID="ORG_CFDCAP" />
					<Org ID="ORG_REDCRS" />
				</Organizations>
				<Kind>Pandemic</Kind>
				<Date>2009-10-01</Date>
				<Locations>
					<li>World Wide</li>
				</Locations>
				<HumanImpact>
					<li>caused severe illness in 3 to 5 million people</li>
					<li>250,000 to 500,000 deaths worldwide</li>
				</HumanImpact>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/2009_flu_pandemic">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/f/f0/H1N1_influenza_virus.jpg" />
					</Images>
				</Common>
			</Crisis>
			<Crisis ID="CRI_EXXONV" Name="Exxon Valdez Oil Spill">
				<People>
					<Person ID="PER_BUSDAD" />
				</People>
				<Organizations>
					<Org ID="ORG_OILREC" />
				</Organizations>
				<Kind>Oil Spill</Kind>
				<Date>1989-03-24</Date>
				<Locations>
					<li>Prince William Sound, Alaska</li>
				</Locations>
				<HumanImpact>
					<li>devastated fishing industry</li>
				</HumanImpact>
				<EconomicImpact>
					<li>$3.8 billion in clean cup costs, fines, compensation</li>
				</EconomicImpact>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Exxon_Valdez_oil_spill">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/6/66/Exval.jpeg" />
					</Images>
				</Common>
			</Crisis>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[0][0].id == "CRI_SWNFLU" )
		self.assert_( models[0][0].name == "Influenza A virus subtype H1N1" )
		self.assert_( models[0][0].kind == "Pandemic" )
		self.assert_( models[0][0].date == "2009-10-01" )
		self.assert_( models[0][0].location == "['World Wide']" )
		self.assert_( models[0][0].humanImpact == "['caused severe illness in 3 to 5 million people', '250,000 to 500,000 deaths worldwide']" )
		self.assert_( models[0][0].people == "['PER_BROBMA', 'PER_GHARTL']" )
		self.assert_( models[0][0].organizations == "['ORG_WHLORG', 'ORG_CFDCAP', 'ORG_REDCRS']" )
		self.assert_( models[0][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/2009_flu_pandemic")
		self.assert_( models[0][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[0][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/f/f0/H1N1_influenza_virus.jpg")
		
		self.assert_( models[0][1].id == "CRI_EXXONV" )
		self.assert_( models[0][1].name == "Exxon Valdez Oil Spill" )
		self.assert_( models[0][1].kind == "Oil Spill" )
		self.assert_( models[0][1].date == "1989-03-24" )
		self.assert_( models[0][1].location == "['Prince William Sound, Alaska']" )
		self.assert_( models[0][1].humanImpact == "['devastated fishing industry']" )
		self.assert_( models[0][1].economicImpact == "['$3.8 billion in clean cup costs, fines, compensation']" )
		self.assert_( models[0][1].people == "['PER_BUSDAD']" )
		self.assert_( models[0][1].organizations == "['ORG_OILREC']" )
		self.assert_( models[0][1].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Exxon_Valdez_oil_spill")
		self.assert_( models[0][1].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[0][1].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/6/66/Exval.jpeg")
		
		
		
	def testelementTreeToModels_05(self):
		testXML = """
		<WorldCrises>
			<Person ID="PER_SADHUS" Name="Saddam Hussein">
				<Crises>
					<Crisis ID="CRI_IRAQWR" />
				</Crises>
				<Kind>President of Iraq</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Saddam_Hussein">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/f/f1/Iraq%2C_Saddam_Hussein_%28222%29.jpg" />
					</Images>
				</Common>
			</Person>

			<Person ID="PER_OSAMAB" Name="Osama Bin Laden">
				<Crises>
					<Crisis ID="CRI_NINEOO" />
				</Crises>
				<Organizations>
					<Org ID="ORG_AQAEDA" />
				</Organizations>
				<Kind>Founder of al-Qaeda</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Osama_Bin_Laden">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg" />
					</Images>
				</Common>
			</Person>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[1][0].id == "PER_SADHUS" )
		self.assert_( models[1][0].name == "Saddam Hussein" )
		self.assert_( models[1][0].kind == "President of Iraq" )
		self.assert_( models[1][0].crises == "['CRI_IRAQWR']")
		self.assert_( models[1][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Saddam_Hussein")
		self.assert_( models[1][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/f/f1/Iraq%2C_Saddam_Hussein_%28222%29.jpg")
		
		self.assert_( models[1][1].id == "PER_OSAMAB" )
		self.assert_( models[1][1].name == "Osama Bin Laden" )
		self.assert_( models[1][1].kind == "Founder of al-Qaeda" )
		self.assert_( models[1][1].crises == "['CRI_NINEOO']")
		self.assert_( models[1][1].organizations == "['ORG_AQAEDA']" )
		self.assert_( models[1][1].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Osama_Bin_Laden")
		self.assert_( models[1][1].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][1].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg")
	
	def testelementTreeToModels_06(self):
		testXML = """
		<WorldCrises>
			<Organization ID="ORG_WIKLKS" Name="Wikileaks">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
				</Crises>
				<People>
					<Person ID="PER_JULASS" />
				</People>
				<Kind>Nonprofit document archive and disclosure</Kind>
				<Location>Online</Location>
				<History>
					<li>Launched in 2006</li>
				</History>
				<ContactInfo>
					<li>IRC: http://chat.wikileaks.org/</li>
				</ContactInfo>
				<Common>
					<ExternalLinks>
						<li href="http://wikileaks.org/">Official Website</li>
					</ExternalLinks>
					<Images>
						<li  embed="http://wikileaks.org/IMG/wlogo.png" />
					</Images>
				</Common>
			</Organization>
			<Organization ID="ORG_AQAEDA" Name="al-Qaeda">
				<Crises>
					<Crisis ID="CRI_IRAQWR" />
					<Crisis ID="CRI_NINEOO" />
				</Crises>
				<People>
					<Person ID="PER_OSAMAB" />
				</People>
				<Kind>Terrorist</Kind>
				<Location>World Wide</Location>
				<History>
					<li>Founded in 1988</li>
				</History>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Al_Queda">Wikipedia</li>
					</ExternalLinks>
				</Common>
			</Organization>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[2][0].id == "ORG_WIKLKS" )
		self.assert_( models[2][0].name == "Wikileaks" )
		self.assert_( models[2][0].kind == "Nonprofit document archive and disclosure" )
		self.assert_( models[2][0].location == "Online")
		self.assert_( models[2][0].crises == "['CRI_BAGAIR']")
		self.assert_( models[2][0].people == "['PER_JULASS']")
		self.assert_( models[2][0].common.externalLinks.all()[0].href == "http://wikileaks.org/")
		self.assert_( models[2][0].common.externalLinks.all()[0].content == "Official Website")
		self.assert_( models[2][0].common.images.all()[0].embed == "http://wikileaks.org/IMG/wlogo.png")
		
		self.assert_( models[2][1].id == "ORG_AQAEDA" )
		self.assert_( models[2][1].name == "al-Qaeda" )
		self.assert_( models[2][1].kind == "Terrorist" )
		self.assert_( models[2][1].crises == "['CRI_IRAQWR', 'CRI_NINEOO']")
		self.assert_( str(models[2][1].history) == "['Founded in 1988']")
		self.assert_( models[2][1].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Al_Queda")
		self.assert_( models[2][1].common.externalLinks.all()[0].content == "Wikipedia")
	
	
	
		
print "testWCDB2.py"
unittest.main()
print "Done."
	
