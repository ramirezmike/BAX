from BeautifulSoup import BeautifulSoup
import urllib2
import re

url_text = "http://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn=9780073386690&field-publisher=&node=&field-p_n_condition-type=&field-feature_browse-bin=&field-subject=&field-language=&field-dateop=&field-datemod=&field-dateyear=&sort=relevanceexprank&Adv-Srch-Books-Submit.x=25&Adv-Srch-Books-Submit.y=8" 

req = urllib2.Request(url_text, headers={'User-Agent' : "Magic Browser"})
con = urllib2.urlopen( req )
stringURL = con.read()
con.close()

soup = BeautifulSoup(stringURL)

for div in soup.findAll("html"):
	regex = re.compile("Today")
	match = regex.search(div.text)
	match = match.group()
	print str(match)
