"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# -------
# imports
# -------

import sys
import StringIO
import unittest
import datetime

import xml.etree.ElementTree as ET

from models import Crisis, Person, Organization

#from importXML import make_common, eval_crises, eval_people, eval_organizations, listings, import_xml_solve

import importXML as ixml

#from exportXML import eval_links, eval_textfield, eval_common, eval_crises, eval_organizations, eval_people, export_xml_solve 

import exportXML as exml

from django.db import models


"""
To test the program:
	(In 'WCDB2/cs373-wcdb/wcdb' folder ) :
	python manage.py test db_app <-- Tests only 'tests' in this file

	python manage.py test <-- Tests all tests on test suite, takes longer

	DO NOT USE THESE LEGACY TEST COMMANDS:
	#% python tests.py >& tests.py.out
	#% chmod ugo+x tests.py
	#% tests.py >& tests.py.out
"""

from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner

class DjangoCrisesTests(TestCase): 

	#def test_basic_addition(self):
	#    """
	#    Tests that 1 + 1 always equals 2.
	#    """
	#    self.assertEqual(1 + 1, 2)

	#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	# Unit Testing all methods in importXML.py first 
	#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        

	# -----------
	# make_common
	# -----------
	
	# Evaluate one tag
	def test_make_common_1 (self) :
		elem = ET.fromstring("<Common><Citations /></Common>");
		m = Crisis(name = "TEST", wcdb_id = "CRI_TESTIN")
		ixml.make_common(elem, m)
		self.assert_(m.citations == "")
   
	# Evaluate two tags
	def test_make_common_2 (self) :
		elem = ET.fromstring("<Common><Citations /><ExternalLinks /></Common>");
		m = Crisis(name = "TEST", wcdb_id = "CRI_TESTIN")
		ixml.make_common(elem, m)
		self.assert_(m.citations == "")
		self.assert_(m.extLinks == "")

	# Evaluate 3 tags
	def test_make_common_3 (self) :
		elem = ET.fromstring("<Common><ExternalLinks /></Common>");
		m = Crisis(name = "TEST", wcdb_id = "CRI_TESTIN")
		ixml.make_common(elem, m)
		self.assert_(m.extLinks == "")

	# Evaluate all tags
	def test_make_common_4 (self) :
		elem = ET.fromstring("<Common><Citations /><ExternalLinks /><Images /><Videos /><Maps /><Feeds /><Summary /></Common>");
		m = Crisis(name = "TEST", wcdb_id = "CRI_TESTIN")
		ixml.make_common(elem, m)
		self.assert_(m.citations == "")
		self.assert_(m.extLinks == "")
		self.assert_(m.images == "")
		self.assert_(m.videos == "")
		self.assert_(m.maps == "")
		self.assert_(m.feeds == "")
		self.assert_(m.summary == "")


	# -----------
	# eval_crises
	# -----------

	# evaluate empty 'crises' input. To test it I had to create some data for it
	# in the method above.
	def test_eval_crises_1 (self) :
		elem = ET.fromstring('<w><Crisis ID="CRI_KATRIN" Name="Katrina"><People><Person ID="PER_GWBUSH" /><Person ID="PER_KATBLA" /></People><Organizations><Org ID="ORG_FEMAAA" /></Organizations><Kind>Natural Disaster</Kind><Date>2005-07-29</Date><Time>09:45:00</Time><Locations><li>New Orleans, Louisiana</li></Locations><HumanImpact><li>Over 1800 Deaths</li></HumanImpact><EconomicImpact><li>Over $100 billion worth of damage</li></EconomicImpact><ResourcesNeeded><li>Early in September, Congress authorized a total of $62.3 billion in aid for victims. Additionally, President Bush enlisted the help of former presidents Bill Clinton and George H.W. Bush to raise additional voluntary contributions, much as they did after the 2004 Indian Ocean earthquake and tsunami.</li></ResourcesNeeded><Common><Citations><li>Wikipedia</li><li>Youtube</li><li>BBC news</li><li>Web in general</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/Hurricane_Katrina">Wikipedia</li></ExternalLinks><Images><li href="http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg">Katrina NOAA.gov</li><li href="http://www.hurricanekatrina.com/images/hurricane-katrina-levees.jpg">Katrina breaking through New Orleans Leeves</li><li href="http://mediamythalert.files.wordpress.com/2011/05/new-orleans-flooding.jpg">New Orleans Flooding</li><li href="http://dart.arc.nasa.gov/katrina/CATF3/images/2067.jpg">Floded House</li><li href="http://jameswagner.com/mt_archives/superdomebody.jpg">Floating body</li><li href="http://affrodite.net/wp-content/uploads/2009/08/Hurricane_Katrina-15.jpg">Superdome used as shelter</li><li href="http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg">View of the Hurricane in action</li></Images><Videos><li href="http://www.youtube.com/watch?v=s76Qn7bpCsQ">Extreme video coverage</li><li href="http://video.nationalgeographic.com/video/environment/environment-natural-disasters/hurricanes/katrina/">Hurricane Katrina Day by Day</li><li href="http://www.history.com/topics/hurricane-katrina/videos#hurricane-katrina">Video from History channel</li><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=AUTcrC1ciXE">Shocking images</li><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=LmSjW7C16T8">Video from inside a house</li></Videos><Maps><li href="https://maps.google.com/maps?q=New+Orleans+area+affected+by+Hurricane+Katrina&amp;hl=en&amp;sll=29.950175,-90.071411&amp;sspn=2.303546,1.590271&amp;t=h&amp;gl=us&amp;hq=area+affected+by+Hurricane+Katrina&amp;hnear=New+Orleans,+Orleans,+Louisiana&amp;z=10">New Orleans map</li></Maps><Feeds><li href="https://www.facebook.com/notes/firehouse-subs/it-all-began-with-hurricane-katrina/10150108753635141">It all began with Hurricane Katrina</li><li href="https://www.facebook.com/pages/Hurricane-Katrina-Dogs/115239633713">Hurricane Katrina Dogs</li></Feeds><Summary></Summary></Common></Crisis></w>');

		ixml.eval_crises(elem.findall('Crisis'))

		# Pull the data from the database and check they are as expected
		assert(Crisis.objects.all() != None)
		for c in Crisis.objects.all() :
			assert(Crisis.objects.all() != None)
			self.assert_(c.kind=="Natural Disaster")        
			self.assert_(c.date==datetime.datetime(2005,07,29,9,45,00))
			self.assert_(c.locations=="New Orleans, Louisiana\n")
			self.assert_(c.humanImpact=="Over 1800 Deaths\n")
			self.assert_(c.economicImpact=="Over $100 billion worth of damage\n")
			self.assert_(c.resources=="Early in September, Congress authorized a total of $62.3 billion in aid for victims. Additionally, President Bush enlisted the help of former presidents Bill Clinton and George H.W. Bush to raise additional voluntary contributions, much as they did after the 2004 Indian Ocean earthquake and tsunami.\n")


	# Test with missing Crisis ID and name
	def test_eval_crises_2 (self) :
		elem = ET.fromstring('<w><Crisis ID="" Name=""><People><Person ID="PER_GWBUSH" /><Person ID="PER_KATBLA" /></People><Organizations><Org ID="ORG_FEMAAA" /></Organizations><Kind>Natural Disaster</Kind><Date>2005-07-29</Date><Time>09:45:00</Time><Locations><li>New Orleans, Louisiana</li></Locations><HumanImpact><li>Over 1800 Deaths</li></HumanImpact><EconomicImpact><li>Over $100 billion worth of damage</li></EconomicImpact><ResourcesNeeded><li>Early in September, Congress authorized a total of $62.3 billion in aid for victims. Additionally, President Bush enlisted the help of former presidents Bill Clinton and George H.W. Bush to raise additional voluntary contributions, much as they did after the 2004 Indian Ocean earthquake and tsunami.</li></ResourcesNeeded><Common><Citations><li>Wikipedia</li><li>Youtube</li><li>BBC news</li><li>Web in general</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/Hurricane_Katrina">Wikipedia</li></ExternalLinks><Images><li href="http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg">Katrina NOAA.gov</li><li href="http://www.hurricanekatrina.com/images/hurricane-katrina-levees.jpg">Katrina breaking through New Orleans Leeves</li><li href="http://mediamythalert.files.wordpress.com/2011/05/new-orleans-flooding.jpg">New Orleans Flooding</li><li href="http://dart.arc.nasa.gov/katrina/CATF3/images/2067.jpg">Floded House</li><li href="http://jameswagner.com/mt_archives/superdomebody.jpg">Floating body</li><li href="http://affrodite.net/wp-content/uploads/2009/08/Hurricane_Katrina-15.jpg">Superdome used as shelter</li><li href="http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg">View of the Hurricane in action</li></Images><Videos><li href="http://www.youtube.com/watch?v=s76Qn7bpCsQ">Extreme video coverage</li><li href="http://video.nationalgeographic.com/video/environment/environment-natural-disasters/hurricanes/katrina/">Hurricane Katrina Day by Day</li><li href="http://www.history.com/topics/hurricane-katrina/videos#hurricane-katrina">Video from History channel</li><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=AUTcrC1ciXE">Shocking images</li><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=LmSjW7C16T8">Video from inside a house</li></Videos><Maps><li href="https://maps.google.com/maps?q=New+Orleans+area+affected+by+Hurricane+Katrina&amp;hl=en&amp;sll=29.950175,-90.071411&amp;sspn=2.303546,1.590271&amp;t=h&amp;gl=us&amp;hq=area+affected+by+Hurricane+Katrina&amp;hnear=New+Orleans,+Orleans,+Louisiana&amp;z=10">New Orleans map</li></Maps><Feeds><li href="https://www.facebook.com/notes/firehouse-subs/it-all-began-with-hurricane-katrina/10150108753635141">It all began with Hurricane Katrina</li><li href="https://www.facebook.com/pages/Hurricane-Katrina-Dogs/115239633713">Hurricane Katrina Dogs</li></Feeds><Summary></Summary></Common></Crisis></w>');

		ixml.eval_crises(elem.findall('Crisis'))

		# Pull the data from the database and check they are as expected
		assert(Crisis.objects.all() != None)
		for c in Crisis.objects.all() :
			assert(Crisis.objects.all() != None)
			self.assert_(c.kind=="Natural Disaster")        
			self.assert_(c.date==datetime.datetime(2005,07,29,9,45,00))
			self.assert_(c.locations=="New Orleans, Louisiana\n")
			self.assert_(c.humanImpact=="Over 1800 Deaths\n")
			self.assert_(c.economicImpact=="Over $100 billion worth of damage\n")
			self.assert_(c.resources=="Early in September, Congress authorized a total of $62.3 billion in aid for victims. Additionally, President Bush enlisted the help of former presidents Bill Clinton and George H.W. Bush to raise additional voluntary contributions, much as they did after the 2004 Indian Ocean earthquake and tsunami.\n")
	

	# Test a non-existing crisis    
	def test_eval_crises_3 (self) :
		elem = ET.fromstring('<w><Crisis ID="CRI_DNEXIS" Name="DoesNotExist"><People><Person ID="" /><Person ID="PER_KATBLA" /></People><Organizations><Org ID="ORG_FEMAAA" /></Organizations><Kind>DNE</Kind><Date>2005-07-29</Date><Time>09:45:00</Time><Locations><li>DNE</li></Locations><HumanImpact><li>DNE</li></HumanImpact><EconomicImpact><li>DNE</li></EconomicImpact><ResourcesNeeded><li>DNE</li></ResourcesNeeded><Common><Citations><li>Wikipedia</li><li>DNE</li><li>DNE</li><li>DNE</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/Hurricane_Katrina">Wikipedia</li></ExternalLinks><Images><li href="http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg">Katrina NOAA.gov</li><li href="http://www.hurricanekatrina.com/images/hurricane-katrina-levees.jpg">Katrina breaking through New Orleans Leeves</li><li href="http://mediamythalert.files.wordpress.com/2011/05/new-orleans-flooding.jpg">New Orleans Flooding</li><li href="http://dart.arc.nasa.gov/katrina/CATF3/images/2067.jpg">Floded House</li><li href="http://jameswagner.com/mt_archives/superdomebody.jpg">Floating body</li><li href="http://affrodite.net/wp-content/uploads/2009/08/Hurricane_Katrina-15.jpg">Superdome used as shelter</li><li href="http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg">View of the Hurricane in action</li></Images><Videos><li href="http://www.youtube.com/watch?v=s76Qn7bpCsQ">Extreme video coverage</li><li href="http://video.nationalgeographic.com/video/environment/environment-natural-disasters/hurricanes/katrina/">Hurricane Katrina Day by Day</li><li href="http://www.history.com/topics/hurricane-katrina/videos#hurricane-katrina">Video from History channel</li><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=AUTcrC1ciXE">Shocking images</li><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=LmSjW7C16T8">Video from inside a house</li></Videos><Maps><li href="https://maps.google.com/maps?q=New+Orleans+area+affected+by+Hurricane+Katrina&amp;hl=en&amp;sll=29.950175,-90.071411&amp;sspn=2.303546,1.590271&amp;t=h&amp;gl=us&amp;hq=area+affected+by+Hurricane+Katrina&amp;hnear=New+Orleans,+Orleans,+Louisiana&amp;z=10">New Orleans map</li></Maps><Feeds><li href="https://www.facebook.com/notes/firehouse-subs/it-all-began-with-hurricane-katrina/10150108753635141">It all began with Hurricane Katrina</li><li href="https://www.facebook.com/pages/Hurricane-Katrina-Dogs/115239633713">Hurricane Katrina Dogs</li></Feeds><Summary></Summary></Common></Crisis></w>');

		ixml.eval_crises(elem.findall('Crisis'))

		# Pull the data from the database and check they are as expected
		assert(Crisis.objects.all() != None)
		for c in Crisis.objects.all() :
			assert(Crisis.objects.all() != None)
			self.assert_(c.kind=="DNE")        
			self.assert_(c.date==datetime.datetime(2005,07,29,9,45,00))
			self.assert_(c.locations=="DNE\n")
			self.assert_(c.humanImpact=="DNE\n")
			self.assert_(c.economicImpact=="DNE\n")
			self.assert_(c.resources=="DNE\n")



	def test_xml_solve_1 (self) :
		data = '<WorldCrises><!-- Example Crisis element --><Crisis ID="CRI_NRINFL" Name="2013 Northern India Floods"><People><Person ID="PER_MNSNGH" /></People><Organizations><Org ID="ORG_PMRLFD" /></Organizations><Kind>Natural Disaster</Kind><Date>2013-06-14</Date><Time>09:00:00</Time><Locations><li>Uttarakhand, India</li><li>Himachal Pradesh, India</li><li>Nepal</li></Locations><HumanImpact><li>More than 1000 dead.</li><li>Over 70000 stranded.</li><li>Over 100000 more evacuated.</li></HumanImpact><EconomicImpact><li>Ongoing large-scale crisis, impact has not been evaluated as of July 5th 2013.</li><li>Estimates over 500 Billion INR (10 Billion USD)</li></EconomicImpact><ResourcesNeeded><li>Prime Minister of India undertook an aerial survey of the affected areas and announced 1,000 crore (US$170 million) aid package for disaster relief efforts in the state.</li><li>The Indian Army and the National Disaster Response Force were deployed to evacuate stranded people on June 15th 2013.</li><li>The Indian Airforce has flown hundreds of sorties every day to airdrop food and fuel for trapped villages.</li></ResourcesNeeded><WaysToHelp><!-- Put text with optional hyperlinks here --><li href="http://google.org/personfinder/2013-uttrakhand-floods/">Google Person Finder</li><li href="https://pmnrf.gov.in/">Donate to Prime Ministers Relief Fund</li><li>Like a page on Facebook</li></WaysToHelp><Common><Citations><!-- Put text with optional hyperlinks here --><li>The Hindustan Times</li><li>The Times of India</li></Citations><ExternalLinks><!-- Put text with compulsory hyperlinks here --><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><!-- hrefs optional in the following depending on how you want them to behave on your site --><Images><!-- Put full URLs to images here, display them on your site in your own cool way --><li embed="http://images.jagran.com/ukhand-ss-02-07-13.jpg" text="This is the alt element of the image." /><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Videos><!-- Put youtube link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by youtube) --><!-- Embed example for your site: <iframe width="420" height="315" src="[THIS LINK]" frameborder="0" allowfullscreen></iframe> --><li embed="//www.youtube.com/embed/qV3s7Sa6B6w" /></Videos><Maps><!-- Put google maps link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by google maps) --><!-- Embed example for your site: <iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="[THIS LINK]"></iframe> --><li embed="https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed" /></Maps><Feeds><!-- Put feed URL here and embed on your site in your own cool way--><li embed="[WHATEVER A FEED URL LOOKS LIKE]" /></Feeds><!-- Optional summary field for extra random data --><Summary>Lorem ipsum...</Summary></Common></Crisis><!-- Example Person element --><Person ID="PER_MNSNGH" Name="Manmohan Singh"><Crises><Crisis ID="CRI_NRINFL" /></Crises><Organizations><Org ID="ORG_PMRLFD" /></Organizations><Kind>Politician</Kind><Location>India</Location><!-- See Crisis element above for examples of everything under <Common> --></Person><!-- Example Organization element --><Organization ID="ORG_PMRLFD" Name="Prime Ministers Relief Fund"><Crises><Crisis ID="CRI_NRINFL" /></Crises><People><Person ID="PER_MNSNGH" /></People><Kind>Governement Fund</Kind><Location>India</Location><History><li>Founded in 1948.</li></History><ContactInfo><li>Phone: (+91) 1-800-DONTKNOW</li><li>Email: donot@email.me</li></ContactInfo><!-- See Crisis element above for examples of everything under <Common> --></Organization></WorldCrises>'
		ixml.import_xml_solve(data)
		for c in Crisis.objects.all():
			self.assert_(c.name == "2013 Northern India Floods") 
			self.assert_(c.wcdb_id == "CRI_NRINFL") 
			self.assert_(c.kind=="Natural Disaster")
			self.assert_(c.date == datetime.datetime(2013, 6,14,9,0,0))      

		for p in Person.objects.all():
			self.assert_(p.name == "Manmohan Singh")
			self.assert_(p.wcdb_id == "PER_MNSNGH")             
			self.assert_(p.kind=="Politician") 

		for o in Organization.objects.all():
			self.assert_(o.name == "Prime Ministers Relief Fund")
			self.assert_(o.wcdb_id == "ORG_PMRLFD") 
			self.assert_(o.kind=="Governement Fund") 



	def test_xml_solve_2 (self) :
		data = '<WorldCrises><!-- Example Crisis element --><Crisis ID="CRI_NRINFL" Name="2013 Northern India Floods"><People><Person ID="PER_MNSNGH" /></People><Organizations><Org ID="ORG_PMRLFD" /></Organizations><Kind>Natural Disaster</Kind><Date>2013-06-14</Date><Time>09:00:00</Time><Locations><li>Uttarakhand, India</li><li>Himachal Pradesh, India</li><li>Nepal</li></Locations><HumanImpact><li>More than 1000 dead.</li><li>Over 70000 stranded.</li><li>Over 100000 more evacuated.</li></HumanImpact><EconomicImpact><li>Ongoing large-scale crisis, impact has not been evaluated as of July 5th 2013.</li><li>Estimates over 500 Billion INR (10 Billion USD)</li></EconomicImpact><ResourcesNeeded><li>Prime Minister of India undertook an aerial survey of the affected areas and announced 1,000 crore (US$170 million) aid package for disaster relief efforts in the state.</li><li>The Indian Army and the National Disaster Response Force were deployed to evacuate stranded people on June 15th 2013.</li><li>The Indian Airforce has flown hundreds of sorties every day to airdrop food and fuel for trapped villages.</li></ResourcesNeeded><WaysToHelp><!-- Put text with optional hyperlinks here --><li href="http://google.org/personfinder/2013-uttrakhand-floods/">Google Person Finder</li><li href="https://pmnrf.gov.in/">Donate to Prime Ministers Relief Fund</li><li>Like a page on Facebook</li></WaysToHelp><Common><Citations><!-- Put text with optional hyperlinks here --><li>The Hindustan Times</li><li>The Times of India</li></Citations><ExternalLinks><!-- Put text with compulsory hyperlinks here --><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><!-- hrefs optional in the following depending on how you want them to behave on your site --><Images><!-- Put full URLs to images here, display them on your site in your own cool way --><li embed="http://images.jagran.com/ukhand-ss-02-07-13.jpg" text="This is the alt element of the image." /><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Videos><!-- Put youtube link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by youtube) --><!-- Embed example for your site: <iframe width="420" height="315" src="[THIS LINK]" frameborder="0" allowfullscreen></iframe> --><li embed="//www.youtube.com/embed/qV3s7Sa6B6w" /></Videos><Maps><!-- Put google maps link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by google maps) --><!-- Embed example for your site: <iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="[THIS LINK]"></iframe> --><li embed="https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed" /></Maps><Feeds><!-- Put feed URL here and embed on your site in your own cool way--><li embed="[WHATEVER A FEED URL LOOKS LIKE]" /></Feeds><!-- Optional summary field for extra random data --><Summary>Lorem ipsum...</Summary></Common></Crisis><!-- Example Person element --><Person ID="PER_MNSNGH" Name="Manmohan Singh"><Crises><Crisis ID="CRI_NRINFL" /></Crises><Organizations><Org ID="ORG_PMRLFD" /></Organizations><Kind>Politician</Kind><Location>India</Location><!-- See Crisis element above for examples of everything under <Common> --></Person><!-- Example Organization element --><Organization ID="ORG_PMRLFD" Name="Prime Ministers Relief Fund"><Crises><Crisis ID="CRI_NRINFL" /></Crises><People><Person ID="PER_MNSNGH" /></People><Kind>Governement Fund</Kind><Location>India</Location><History><li>Founded in 1948.</li></History><ContactInfo><li>Phone: (+91) 1-800-DONTKNOW</li><li>Email: donot@email.me</li></ContactInfo><!-- See Crisis element above for examples of everything under <Common> --></Organization></WorldCrises>'
		ixml.import_xml_solve(data)
		for c in Crisis.objects.all():
			list_people = Person.objects.all()
			list_people[0].wcdb_id == "PER_MNSNGH"
			list_people[0].name == "Manmohan Singh"
			list_people[0].kind == "Politician"

			list_orgs = Organization.objects.all()
			list_orgs[0].wcdb_id == "ORG_PMRLFD"
			list_orgs[0].name == "Prime Ministers Relief Fund"
			list_orgs[0].kind == "Governement Fund"

		for p in Person.objects.all():
			list_crisis = Crisis.objects.all()
			list_crisis[0].wcdb_id == "PER_MNSNGH"
			list_crisis[0].name == "Manmohan Singh"
			list_crisis[0].kind == "Politician"

			list_orgs = Organization.objects.all()
			list_orgs[0].wcdb_id == "ORG_PMRLFD"
			list_orgs[0].name == "Prime Ministers Relief Fund"
			list_orgs[0].kind == "Governement Fund"

		for o in Organization.objects.all():
			list_crisis = Crisis.objects.all()
			list_crisis[0].wcdb_id == "PER_MNSNGH"
			list_crisis[0].name == "Manmohan Singh"
			list_crisis[0].kind == "Politician"

			list_people = Person.objects.all()
			list_people[0].wcdb_id == "PER_MNSNGH"
			list_people[0].name == "Manmohan Singh"
			list_people[0].kind == "Politician"

	def test_xml_solve_3 (self) :
		data = '<WorldCrises><!-- Example Crisis element --><Crisis ID="CRI_NRINFL" Name="2013 Northern India Floods"><People><Person ID="PER_MNSNGH" /></People><Organizations><Org ID="ORG_PMRLFD" /></Organizations><Kind>Natural Disaster</Kind><Date>2013-06-14</Date><Time>09:00:00</Time><Locations><li>Uttarakhand, India</li><li>Himachal Pradesh, India</li><li>Nepal</li></Locations><HumanImpact><li>More than 1000 dead.</li><li>Over 70000 stranded.</li><li>Over 100000 more evacuated.</li></HumanImpact><EconomicImpact><li>Ongoing large-scale crisis, impact has not been evaluated as of July 5th 2013.</li><li>Estimates over 500 Billion INR (10 Billion USD)</li></EconomicImpact><ResourcesNeeded><li>Prime Minister of India undertook an aerial survey of the affected areas and announced 1,000 crore (US$170 million) aid package for disaster relief efforts in the state.</li><li>The Indian Army and the National Disaster Response Force were deployed to evacuate stranded people on June 15th 2013.</li><li>The Indian Airforce has flown hundreds of sorties every day to airdrop food and fuel for trapped villages.</li></ResourcesNeeded><WaysToHelp><!-- Put text with optional hyperlinks here --><li href="http://google.org/personfinder/2013-uttrakhand-floods/">Google Person Finder</li><li href="https://pmnrf.gov.in/">Donate to Prime Ministers Relief Fund</li><li>Like a page on Facebook</li></WaysToHelp><Common><Citations><!-- Put text with optional hyperlinks here --><li>The Hindustan Times</li><li>The Times of India</li></Citations><ExternalLinks><!-- Put text with compulsory hyperlinks here --><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><!-- hrefs optional in the following depending on how you want them to behave on your site --><Images><!-- Put full URLs to images here, display them on your site in your own cool way --><li embed="http://images.jagran.com/ukhand-ss-02-07-13.jpg" text="This is the alt element of the image." /><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Videos><!-- Put youtube link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by youtube) --><!-- Embed example for your site: <iframe width="420" height="315" src="[THIS LINK]" frameborder="0" allowfullscreen></iframe> --><li embed="//www.youtube.com/embed/qV3s7Sa6B6w" /></Videos><Maps><!-- Put google maps link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by google maps) --><!-- Embed example for your site: <iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="[THIS LINK]"></iframe> --><li embed="https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed" /></Maps><Feeds><!-- Put feed URL here and embed on your site in your own cool way--><li embed="[WHATEVER A FEED URL LOOKS LIKE]" /></Feeds><!-- Optional summary field for extra random data --><Summary>Lorem ipsum...</Summary></Common></Crisis><!-- Example Person element --><Person ID="PER_MNSNGH" Name="Manmohan Singh"><Crises><Crisis ID="CRI_NRINFL" /></Crises><Organizations><Org ID="ORG_PMRLFD" /></Organizations><Kind>Politician</Kind><Location>India</Location><!-- See Crisis element above for examples of everything under <Common> --></Person><!-- Example Organization element --><Organization ID="ORG_PMRLFD" Name="Prime Ministers Relief Fund"><Crises><Crisis ID="CRI_NRINFL" /></Crises><People><Person ID="PER_MNSNGH" /></People><Kind>Governement Fund</Kind><Location>India</Location><History><li>Founded in 1948.</li></History><ContactInfo><li>Phone: (+91) 1-800-DONTKNOW</li><li>Email: donot@email.me</li></ContactInfo><!-- See Crisis element above for examples of everything under <Common> --></Organization></WorldCrises>'
		ixml.import_xml_solve(data)
		assert(Crisis.objects.all() != None and Person.objects.all() != None and Organization.objects.all() != None)

	# ------------------
	# eval_organizations
	# ------------------
	def test_eval_organizations_1 (self) :
		elem = ET.fromstring('<w><Organization ID="ORG_PMRLFD" Name="Prime Ministers Relief Fund"><Crises><Crisis ID="CRI_NRINFL" /></Crises><People><Person ID="PER_MNSNGH" /></People><Kind>Governement Fund</Kind><Location>India</Location><History><li>Founded in 1948.</li></History><ContactInfo><li>Phone: (+91) 1-800-DONTKNOW</li><li>Email: donot@email.me</li></ContactInfo><!-- See Crisis element above for examples of everything under <Common> --></Organization></w>')
		ixml.eval_organizations(elem.findall('Organization'))
		for o in Organization.objects.all() :
			self.assert_(o.wcdb_id == "ORG_PMRLFD")
			self.assert_(o.name == "Prime Ministers Relief Fund")
			self.assert_(o.kind == "Governement Fund")
			self.assert_(o.location == "India")
			self.assert_(o.history == "Founded in 1948.\n")
			self.assert_(o.contact == "Phone: (+91) 1-800-DONTKNOW\nEmail: donot@email.me\n")

	def test_eval_organizations_2 (self) :
		elem = ET.fromstring('<w><Organization ID="ORG_PMRLFD" Name="Prime Ministers Relief Fund"><Crises><Crisis ID="CRI_NRINFL" /></Crises><People><Person ID="PER_MNSNGH" /></People><Kind>Governement Fund</Kind><Location>India</Location><History><li>Founded in 1948.</li></History><ContactInfo><li>this</li><li>is</li><li>a</li><li>test</li><li>Phone: (+91) 1-800-DONTKNOW</li><li>Email: donot@email.me</li></ContactInfo><!-- See Crisis element above for examples of everything under <Common> --></Organization></w>')
		ixml.eval_organizations(elem.findall('Organization'))
		for o in Organization.objects.all() :
			self.assert_(o.wcdb_id == "ORG_PMRLFD")
			self.assert_(o.name == "Prime Ministers Relief Fund")
			self.assert_(o.kind == "Governement Fund")
			self.assert_(o.location == "India")
			self.assert_(o.history == "Founded in 1948.\n")
			self.assert_(o.contact == "this\nis\na\ntest\nPhone: (+91) 1-800-DONTKNOW\nEmail: donot@email.me\n")

	def test_eval_organizations_3 (self) :
		elem = ET.fromstring('<w><Organization ID="ORG_PMRLFD" Name="Prime Ministers Relief Fund"><Crises><Crisis ID="CRI_NRINFL" /></Crises><People><Person ID="PER_MNSNGH" /></People></Organization></w>')
		ixml.eval_organizations(elem.findall('Organization'))
		for o in Organization.objects.all() :
			self.assert_(o.wcdb_id == "ORG_PMRLFD")
			self.assert_(o.name == "Prime Ministers Relief Fund")


	# --------
	# listings
	# --------
	def test_listings_1 (self) :
		elem = ET.fromstring('<w><Images><li href="http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg">Katrina NOAA.gov</li><li href="http://www.hurricanekatrina.com/images/hurricane-katrina-levees.jpg">Katrina breaking through New Orleans Leeves</li><li href="http://mediamythalert.files.wordpress.com/2011/05/new-orleans-flooding.jpg">New Orleans Flooding</li><li href="http://dart.arc.nasa.gov/katrina/CATF3/images/2067.jpg">Floded House</li><li href="http://jameswagner.com/mt_archives/superdomebody.jpg">Floating body</li><li href="http://affrodite.net/wp-content/uploads/2009/08/Hurricane_Katrina-15.jpg">Superdome used as shelter</li><li href="http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg">View of the Hurricane in action</li>  </Images></w>')
		x = ixml.listings(elem.find('Images'))
		assert(x == '<a href="http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg">Katrina NOAA.gov</a>\n<a href="http://www.hurricanekatrina.com/images/hurricane-katrina-levees.jpg">Katrina breaking through New Orleans Leeves</a>\n<a href="http://mediamythalert.files.wordpress.com/2011/05/new-orleans-flooding.jpg">New Orleans Flooding</a>\n<a href="http://dart.arc.nasa.gov/katrina/CATF3/images/2067.jpg">Floded House</a>\n<a href="http://jameswagner.com/mt_archives/superdomebody.jpg">Floating body</a>\n<a href="http://affrodite.net/wp-content/uploads/2009/08/Hurricane_Katrina-15.jpg">Superdome used as shelter</a>\n<a href="http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg">View of the Hurricane in action</a>\n')
		
	def test_listings_2 (self) :
		elem = ET.fromstring('<w><Videos><li href="http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg">Katrina NOAA.gov</li><li href="http://www.hurricanekatrina.com/images/hurricane-katrina-levees.jpg">Katrina breaking through New Orleans Leeves</li><li href="http://mediamythalert.files.wordpress.com/2011/05/new-orleans-flooding.jpg">New Orleans Flooding</li><li href="http://dart.arc.nasa.gov/katrina/CATF3/images/2067.jpg">Floded House</li><li href="http://jameswagner.com/mt_archives/superdomebody.jpg">Floating body</li><li href="http://affrodite.net/wp-content/uploads/2009/08/Hurricane_Katrina-15.jpg">Superdome used as shelter</li><li href="http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg">View of the Hurricane in action</li>  </Videos></w>')
		x = ixml.listings(elem.find('Videos'))
		assert(x == '<a href="http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg">Katrina NOAA.gov</a>\n<a href="http://www.hurricanekatrina.com/images/hurricane-katrina-levees.jpg">Katrina breaking through New Orleans Leeves</a>\n<a href="http://mediamythalert.files.wordpress.com/2011/05/new-orleans-flooding.jpg">New Orleans Flooding</a>\n<a href="http://dart.arc.nasa.gov/katrina/CATF3/images/2067.jpg">Floded House</a>\n<a href="http://jameswagner.com/mt_archives/superdomebody.jpg">Floating body</a>\n<a href="http://affrodite.net/wp-content/uploads/2009/08/Hurricane_Katrina-15.jpg">Superdome used as shelter</a>\n<a href="http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg">View of the Hurricane in action</a>\n')

	def test_listings_3 (self) :
		elem = ET.fromstring('<w><Videos><li>raw text</li></Videos></w>')
		x = ixml.listings(elem.find('Videos'))
		assert(x == 'raw text\n')


	# -----------
	# eval_people
	# -----------    

	# an empty 'people' request


	def test_eval_people_1 (self) :
		elem = ET.fromstring('<w><Person ID="PER_TONYHA" Name="Tony Hayward"><Crises><Crisis ID="CRI_BPOILS" /></Crises><Organizations><Org ID="ORG_BPETRO" /></Organizations><Kind>Natural Disaster</Kind><Location>Gulf of Mexico</Location><Common>  <Citations><li>Wikipedia</li><li>Youtube</li><li>Twitter</li><li>Web in general</li>  </Citations>  <ExternalLinks><li href="http://en.wikipedia.org/wiki/Tony_Hayward">Tony Hayward</li>  </ExternalLinks>  <Images><li href="http://i.telegraph.co.uk/multimedia/archive/00879/money-graphics-2007_879614a.jpg">Tony Hayward Steps up to the BP Plate</li><li href="http://i.telegraph.co.uk/multimedia/archive/01650/hay_1650628c.jpg">Tony Hayward</li>  </Images>  <Videos><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=_AwD_7yNzKo">BP Tony Hayward Sorry Ad Original Version Exclusive</li>  </Videos>  <Maps><li href="http://www.4hotels.co.uk/uk/images/england-kent.gif">Tony Hayward from Kent, UK</li><li href="http://asset3.cbsistatic.com/cnwk.1d/i/tim//2010/06/03/Home_BP_oil_spill_map_June_2.jpg">BP Oil Spill Area Affected</li>  </Maps>  <Feeds><li href="https://twitter.com/bpcaresUK">Tony Hayward @bpcaresUK</li>  </Feeds>  <Summary></Summary></Common>  </Person></w>');
		ixml.eval_people(elem.findall('Person'))
		
		# Pull the data from the database and check they are as expected
		for p in Person.objects.all() :
			self.assert_(p.wcdb_id == "PER_TONYHA")
			self.assert_(p.name == "Tony Hayward")
			self.assert_(p.kind == "Natural Disaster")
			self.assert_(p.location == "Gulf of Mexico")
			

	# Evaluate one person
	def test_eval_people_2 (self) :
		elem = ET.fromstring('<w><Person ID="PER_TONYHA" Name="Tony Hayward"><Crises><Crisis ID="CRI_BPOILS" /></Crises><Organizations><Org ID="ORG_BPETRO" /></Organizations><Kind>Natural Disaster</Kind><Location>Gulf of Mexico</Location><Common>  <Citations><li>Wikipedia</li><li>Youtube</li><li>Twitter</li><li>Web in general</li>  </Citations>  <ExternalLinks><li href="http://en.wikipedia.org/wiki/Tony_Hayward">Tony Hayward</li>  </ExternalLinks>  <Images><li href="http://i.telegraph.co.uk/multimedia/archive/00879/money-graphics-2007_879614a.jpg">Tony Hayward Steps up to the BP Plate</li><li href="http://i.telegraph.co.uk/multimedia/archive/01650/hay_1650628c.jpg">Tony Hayward</li>  </Images>  <Videos><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=_AwD_7yNzKo">BP Tony Hayward Sorry Ad Original Version Exclusive</li>  </Videos>  <Maps><li href="http://www.4hotels.co.uk/uk/images/england-kent.gif">Tony Hayward from Kent, UK</li><li href="http://asset3.cbsistatic.com/cnwk.1d/i/tim//2010/06/03/Home_BP_oil_spill_map_June_2.jpg">BP Oil Spill Area Affected</li>  </Maps>  <Feeds><li href="https://twitter.com/bpcaresUK">Tony Hayward @bpcaresUK</li>  </Feeds>  <Summary></Summary></Common>  </Person><Person ID="PER_TEST" Name="TEST"><Crises><Crisis ID="CRI_BPOILS" /></Crises><Organizations><Org ID="ORG_BPETRO" /></Organizations><Kind>TEST</Kind><Location>TEST</Location><Common>  <Citations><li>Wikipedia</li><li>Youtube</li><li>Twitter</li><li>Web in general</li>  </Citations>  <ExternalLinks><li href="http://en.wikipedia.org/wiki/Tony_Hayward">Tony Hayward</li>  </ExternalLinks>  <Images><li href="http://i.telegraph.co.uk/multimedia/archive/00879/money-graphics-2007_879614a.jpg">Tony Hayward Steps up to the BP Plate</li><li href="http://i.telegraph.co.uk/multimedia/archive/01650/hay_1650628c.jpg">Tony Hayward</li>  </Images>  <Videos><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=_AwD_7yNzKo">BP Tony Hayward Sorry Ad Original Version Exclusive</li>  </Videos>  <Maps><li href="http://www.4hotels.co.uk/uk/images/england-kent.gif">Tony Hayward from Kent, UK</li><li href="http://asset3.cbsistatic.com/cnwk.1d/i/tim//2010/06/03/Home_BP_oil_spill_map_June_2.jpg">BP Oil Spill Area Affected</li>  </Maps>  <Feeds><li href="https://twitter.com/bpcaresUK">Tony Hayward @bpcaresUK</li>  </Feeds>  <Summary></Summary></Common>  </Person></w>');
		ixml.eval_people(elem.findall('Person'))
		
		# Pull the data from the database and check they are as expected
		list_people = Person.objects.all()
		self.assert_(list_people[0].wcdb_id == "PER_TONYHA")
		self.assert_(list_people[0].name == "Tony Hayward")
		self.assert_(list_people[0].kind == "Natural Disaster")
		self.assert_(list_people[0].location == "Gulf of Mexico")
		self.assert_(list_people[1].wcdb_id == "PER_TEST")
		self.assert_(list_people[1].name == "TEST")
		self.assert_(list_people[1].kind == "TEST")
		self.assert_(list_people[1].location == "TEST")

	# Evaluate two people
	def test_eval_people_3 (self) :
		elem = ET.fromstring('<w><Person ID="DNE" Name="DNE"><Crises><Crisis ID="CRI_BPOILS" /></Crises><Organizations><Org ID="ORG_BPETRO" /></Organizations><Kind>DNE</Kind><Location>DNE</Location><Common>  <Citations><li>Wikipedia</li><li>Youtube</li><li>Twitter</li><li>Web in general</li>  </Citations>  <ExternalLinks><li href="http://en.wikipedia.org/wiki/Tony_Hayward">Tony Hayward</li>  </ExternalLinks>  <Images><li href="http://i.telegraph.co.uk/multimedia/archive/00879/money-graphics-2007_879614a.jpg">Tony Hayward Steps up to the BP Plate</li><li href="http://i.telegraph.co.uk/multimedia/archive/01650/hay_1650628c.jpg">Tony Hayward</li>  </Images>  <Videos><li href="http://www.youtube.com/watch?feature=player_detailpage&amp;v=_AwD_7yNzKo">BP Tony Hayward Sorry Ad Original Version Exclusive</li>  </Videos>  <Maps><li href="http://www.4hotels.co.uk/uk/images/england-kent.gif">Tony Hayward from Kent, UK</li><li href="http://asset3.cbsistatic.com/cnwk.1d/i/tim//2010/06/03/Home_BP_oil_spill_map_June_2.jpg">BP Oil Spill Area Affected</li>  </Maps>  <Feeds><li href="https://twitter.com/bpcaresUK">Tony Hayward @bpcaresUK</li>  </Feeds>  <Summary></Summary></Common>  </Person></w>');
		ixml.eval_people(elem.findall('Person'))
		
		# Pull the data from the database and check they are as expected
		for p in Person.objects.all() :
			self.assert_(p.wcdb_id == "DNE")
			self.assert_(p.name == "DNE")
			self.assert_(p.kind == "DNE")
			self.assert_(p.location == "DNE")


	

	#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	# Unit Testing methods in exportXML.py
	#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 


	"""
	eval_links(str_field, node, common)
	eval_common(m, main)
	eval_crises(crisis, root)
	eval_organizations(org, root)
	eval_people(people, root)
	export_xml_solve(c, o, p)
	"""
	

	#------------
	# eval_links
	#------------
	def test_eval_links_1(self):
		common = ET.fromstring('<Common />')
		links = ["<li href=\"http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg\">Katrina NOAA.gov</li>",
		"<li href=\"http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg\">View of the Hurricane in action</li>"]
		node = ET.fromstring("<ExternalLinks />")
		exml.eval_links(links, node, common)
		self.assert_(ET.tostring(common) == ("<Common><ExternalLinks><li href=\"http://www.katrina.noaa.gov/images/katrina-08-28-2005.jpg\">Katrina NOAA.gov</li><li href=\"http://www.mthurricane.com/Hurricane_Katrina/Hurricane_Katrina_Index_02.jpg\">View of the Hurricane in action</li></ExternalLinks></Common>"))

	def test_eval_links_2(self):
		common = ET.fromstring('<Common />')
		links = ["Wikipedia","Youtube","Fox news","Web in general"]
		node = ET.fromstring("<ExternalLinks />")
		exml.eval_links(links, node, common)
		self.assert_((ET.tostring(common) == ("<Common><ExternalLinks><li>Wikipedia</li><li>Youtube</li><li>Fox news</li><li>Web in general</li></ExternalLinks></Common>")))

	def test_eval_links_3(self):
		common = ET.fromstring('<Common />')
		links = ["<li embed=\"http://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Sandy_Oct_25_2012_0400Z.JPG/546px-Sandy_Oct_25_2012_0400Z.JPG\" text=\"Satellite photo of hurricane Sandy\"/>" , "<li embed=\"http://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/HurricaneSANDYCheltenham.jpg/220px-HurricaneSANDYCheltenham.jpg\" text=\"Damage to neighborhood caused by Hurricane Sandy\"/>" , "<li embed=\"http://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Sandy_Poweroutage_1.jpg/220px-Sandy_Poweroutage_1.jpg\" text=\"Manhattan power outage caused by Hurricane Sandy\"/>"]
		node = ET.fromstring("<ExternalLinks />")
		exml.eval_links(links, node, common)
		self.assert_((ET.tostring(common) == ('<Common><ExternalLinks><li embed=\"http://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Sandy_Oct_25_2012_0400Z.JPG/546px-Sandy_Oct_25_2012_0400Z.JPG\" text=\"Satellite photo of hurricane Sandy\" /><li embed=\"http://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/HurricaneSANDYCheltenham.jpg/220px-HurricaneSANDYCheltenham.jpg\" text=\"Damage to neighborhood caused by Hurricane Sandy\" /><li embed=\"http://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Sandy_Poweroutage_1.jpg/220px-Sandy_Poweroutage_1.jpg\" text=\"Manhattan power outage caused by Hurricane Sandy\" /></ExternalLinks></Common>')))


	
	#------------
	# eval_common
	#------------  
	
	# test empty Crisis model 
	def test_eval_common_1(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = (datetime.datetime(2000,1,1,1,1,1))
		crisis.kind = "N/A"
		crisis.locations = "N/A\n"
		crisis.citations = "N/A\n"
		crisis.extLinks = "N/A\n"
		crisis.images = "N/A\n"
		crisis.videos = "N/A\n"
		crisis.maps = "N/A\n"
		crisis.feeds = "N/A\n"
		crisis.summary = "N/A"
		crisis.save()
		main_ = ET.fromstring('<Crisis />')  # Create empty Element Tree to store result
		exml.eval_common (crisis, main_)
		assert(ET.tostring(main_) == '<Crisis><Common><Citations><li>N/A</li></Citations><ExternalLinks><li>N/A</li></ExternalLinks><Images><li>N/A</li></Images><Videos><li>N/A</li></Videos><Maps><li>N/A</li></Maps><Feeds><li>N/A</li></Feeds><Summary>N/A</Summary></Common></Crisis>')
	

	# Test a valid Crisis model
	def test_eval_common_2(self):
		crisis = Crisis(name = "Katrina", wcdb_id = "CRI_KATRIN")
		crisis.date = (datetime.datetime(2005,07,29,9,45,00))
		crisis.kind = "Natural Disaster"
		crisis.locations = "New Orleans, Louisiana\n"
		crisis.citations = "Wikipedia, Youtube, BBC news, Web in general\n"
		crisis.extLinks = "Wikipedia\n"
		crisis.images = "Katrina NOAA.gov, Katrina breaking through New Orlean\'s Leeves, New Orleans Flooding, Floded House, Floating body, Superdome used as shelter, View of the Hurricane in action\n"
		crisis.videos = "Extreme video coverage, Hurricane Katrina Day by Day, Video from History channel, Shocking images, Video from inside a house\n"
		crisis.maps = "New Orleans google map\n"
		crisis.feeds = "It all began with Hurricane Katrina, Hurricane Katrina Dogs\n"
		crisis.summary = "No summary"
		crisis.save()
		main_ = ET.fromstring('<Crisis />')  # Create empty Element Tree to store result
		exml.eval_common (crisis, main_)
		assert(ET.tostring(main_) == "<Crisis><Common><Citations><li>Wikipedia, Youtube, BBC news, Web in general</li></Citations><ExternalLinks><li>Wikipedia</li></ExternalLinks><Images><li>Katrina NOAA.gov, Katrina breaking through New Orlean's Leeves, New Orleans Flooding, Floded House, Floating body, Superdome used as shelter, View of the Hurricane in action</li></Images><Videos><li>Extreme video coverage, Hurricane Katrina Day by Day, Video from History channel, Shocking images, Video from inside a house</li></Videos><Maps><li>New Orleans google map</li></Maps><Feeds><li>It all began with Hurricane Katrina, Hurricane Katrina Dogs</li></Feeds><Summary>No summary</Summary></Common></Crisis>")

	
	# Test an invalid Crisis model
	def test_eval_common_3(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = (datetime.datetime(2000,1,1,1,1,1))
		crisis.kind = "TestKind"
		crisis.locations = "Location\n"
		crisis.citations = "Wikipedia Youtube BBC news Web in general\n"
		crisis.extLinks = "Wikipedia link\n"
		crisis.images = "jpg images\n"
		crisis.videos = "youtube videos\n"
		crisis.maps = "google maps\n"
		crisis.feeds = "news feeds\n"
		crisis.summary = "no summary"
		crisis.save()
		main_ = ET.fromstring('<Crisis />')  # Create empty Element Tree to store result
		exml.eval_common (crisis, main_)
		assert(ET.tostring(main_) == '<Crisis><Common><Citations><li>Wikipedia Youtube BBC news Web in general</li></Citations><ExternalLinks><li>Wikipedia link</li></ExternalLinks><Images><li>jpg images</li></Images><Videos><li>youtube videos</li></Videos><Maps><li>google maps</li></Maps><Feeds><li>news feeds</li></Feeds><Summary>no summary</Summary></Common></Crisis>')
	

	#------------
	# eval_crises
	#------------

	# Test a 'dummy' crisis
	def test_eval_crises_1(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = datetime.datetime(2000,1,1,1,1,1)
		crisis.kind = "TestKind"
		#crisis.locations = "Location\n"
		crisis.save()
		root = ET.fromstring("<w></w>")
		exml.eval_crises(Crisis, root)        
		assert(ET.tostring(root) == '<w><Crisis ID="CRI_TESTIN" Name="Test"><Kind>TestKind</Kind><Date>2000-01-01</Date><Time>01:01:01</Time></Crisis></w>')

	# Test one valid crisis
	def test_eval_crises_2(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = datetime.datetime(2000,1,1,1,1,1)
		crisis.kind = "TestKind"
		#crisis.locations = "Location\n"
		crisis.save()
		crisis2 = Crisis(name = "Test2", wcdb_id = "CRI_2TESTN")
		crisis2.date = datetime.datetime(2222,1,1,1,1,1)
		crisis2.kind = "TestKind2"
		crisis2.save()
		root = ET.fromstring("<w></w>")
		exml.eval_crises(Crisis, root)      
		assert(ET.tostring(root) == '<w><Crisis ID="CRI_TESTIN" Name="Test"><Kind>TestKind</Kind><Date>2000-01-01</Date><Time>01:01:01</Time></Crisis><Crisis ID="CRI_2TESTN" Name="Test2"><Kind>TestKind2</Kind><Date>2222-01-01</Date><Time>01:01:01</Time></Crisis></w>')
	  

	# Test an invalid crisis  (no information other than date)
	def test_eval_crises_3(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = datetime.datetime(2000,1,1,1,1,1)
		#crisis.locations = "Location\n"
		crisis.save()
		root = ET.fromstring("<w></w>")
		exml.eval_crises(Crisis, root)  
		assert(ET.tostring(root) == '<w><Crisis ID="CRI_TESTIN" Name="Test"><Date>2000-01-01</Date><Time>01:01:01</Time></Crisis></w>')
 

	#-------------------------
	# eval_organizations (org, root)
	#-------------------------

	# Test an empty organizations set
	def test_eval_organizations_1(self):
		root = ET.fromstring('<w></w>')
		assert(Organization != None)
		exml.eval_organizations (Organization, root)
		for o in root :
			assert(root != None)
			assert(False)
			

		org = Organization(name = "Test", wcdb_id = "ORG_TESTIN")
		org.kind = "TestKind"
		#org.locations = "Location\n"
		org.save()
		root = ET.fromstring("<w></w>")
		exml.eval_organizations(Organization, root)     
		assert(ET.tostring(root) == '<w><Organization ID="ORG_TESTIN" Name="Test" /></w>')

			

	# Test a valid organizations set
	def test_eval_organizations_2(self):
		org = Organization(name = "Test", wcdb_id = "ORG_TESTIN")
		org.kind = "TestKind"
		org.save()
		#org.locations = "Location\n"
		org2 = Organization(name = "Test2", wcdb_id = "ORG_2TESTN")
		org2.kind = "TestKind2"
		org2.save()
		root = ET.fromstring("<w></w>")
		exml.eval_organizations(Organization, root) 
		assert(ET.tostring(root) == '<w><Organization ID="ORG_TESTIN" Name="Test" /><Organization ID="ORG_2TESTN" Name="Test2" /></w>')

	# Test an invalid organizations set (no kind)
	def test_eval_organizations_3(self):
		org = Organization(name = "Test", wcdb_id = "ORG_TESTIN")
		#org.locations = "Location\n"
		org.save()
		root = ET.fromstring("<w></w>")
		exml.eval_organizations(Organization, root)  
		assert(ET.tostring(root) == '<w><Organization ID="ORG_TESTIN" Name="Test" /></w>')
	#------------
	# eval_people
	#------------

	# Test an empty people set
	def test_eval_people_1(self):
		per = Person(name = "Test", wcdb_id = "PER_TESTIN")
		per.kind = "TestKind"
		per.save()
		#per.locations = "Location\n"
		root = ET.fromstring('<w></w>')
		exml.eval_people(Person, root) 
		assert(ET.tostring(root) == '<w><Person ID="PER_TESTIN" Name="Test"><Kind>TestKind</Kind></Person></w>')

	# Test a valid people set
	def test_eval_people_2(self):
		per = Person(name = "Test", wcdb_id = "PER_TESTIN")
		per.kind = "TestKind"
		per.save()
		#per.locations = "Location\n"
		per2 = Person(name = "Test2", wcdb_id = "PER_2TESTN")
		per2.kind = "TestKind2"
		per2.save()
		root = ET.fromstring('<w></w>')
		exml.eval_people(Person, root) 
		assert(ET.tostring(root) == '<w><Person ID="PER_TESTIN" Name="Test"><Kind>TestKind</Kind></Person><Person ID="PER_2TESTN" Name="Test2"><Kind>TestKind2</Kind></Person></w>')

	# Test an invalid people set (no information)
	def test_eval_people_3(self):
		per = Person(name = "Test", wcdb_id = "PER_TESTIN")
		per.save()
		#per.locations = "Location\n"
		root = ET.fromstring('<w></w>')
		exml.eval_people(Person, root)
		assert(ET.tostring(root) == '<w><Person ID="PER_TESTIN" Name="Test" /></w>')

	#-----------------
	# export_xml_solve
	#-----------------
	def test_export_xml_solve_1(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = datetime.datetime(2000,1,1,1,1,1)
		crisis.kind = "TestKind"
		crisis.save()

		per = Person(name = "Test", wcdb_id = "PER_TESTIN")
		per.kind = "TestKind"
		per.save()

		org = Organization(name = "Test", wcdb_id = "ORG_TESTIN")
		org.kind = "TestKind"
		org.save()

		s = exml.export_xml_solve(Crisis, Organization, Person)
		self.assert_(s == "<WorldCrises><Crisis ID=\"CRI_TESTIN\" Name=\"Test\"><Kind>TestKind</Kind><Date>2000-01-01</Date><Time>01:01:01</Time></Crisis><Person ID=\"PER_TESTIN\" Name=\"Test\"><Kind>TestKind</Kind></Person><Organization ID=\"ORG_TESTIN\" Name=\"Test\" /></WorldCrises>")

		

	# Test a valid export_xml_solve set
	def test_export_xml_solve_2(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = datetime.datetime(2000,1,1,1,1,1)
		crisis.kind = "TestKind"
		crisis.save()
		crisis2 = Crisis(name = "Test2", wcdb_id = "CRI_2TESTN")
		crisis2.date = datetime.datetime(2222,1,1,1,1,1)
		crisis2.kind = "TestKind2"
		crisis2.save()

		per = Person(name = "Test", wcdb_id = "PER_TESTIN")
		per.kind = "TestKind"
		per.save()
		per2 = Person(name = "Test2", wcdb_id = "PER_2TESTN")
		per2.kind = "TestKind2"
		per2.save()

		org = Organization(name = "Test", wcdb_id = "ORG_TESTIN")
		org.kind = "TestKind"
		org.save()
		org2 = Organization(name = "Test2", wcdb_id = "ORG_2TESTN")
		org2.kind = "TestKind2"
		org2.save()

		s = exml.export_xml_solve(Crisis, Organization, Person)
		self.assert_(s == '<WorldCrises><Crisis ID="CRI_TESTIN" Name="Test"><Kind>TestKind</Kind><Date>2000-01-01</Date><Time>01:01:01</Time></Crisis><Crisis ID="CRI_2TESTN" Name="Test2"><Kind>TestKind2</Kind><Date>2222-01-01</Date><Time>01:01:01</Time></Crisis><Person ID="PER_TESTIN" Name="Test"><Kind>TestKind</Kind></Person><Person ID="PER_2TESTN" Name="Test2"><Kind>TestKind2</Kind></Person><Organization ID="ORG_TESTIN" Name="Test" /><Organization ID="ORG_2TESTN" Name="Test2" /></WorldCrises>')

	# Test an invalid export_xml_solve set
	def test_export_xml_solve_3(self):
		crisis = Crisis(name = "Test", wcdb_id = "CRI_TESTIN")
		crisis.date = datetime.datetime(2000,1,1,1,1,1)
		crisis.save()

		per = Person(name = "Test", wcdb_id = "PER_TESTIN")
		per.save()

		org = Organization(name = "Test", wcdb_id = "ORG_TESTIN")
		org.save()

		s = exml.export_xml_solve(Crisis, Organization, Person)
		self.assert_(s == '<WorldCrises><Crisis ID="CRI_TESTIN" Name="Test"><Date>2000-01-01</Date><Time>01:01:01</Time></Crisis><Person ID="PER_TESTIN" Name="Test" /><Organization ID="ORG_TESTIN" Name="Test" /></WorldCrises>')
