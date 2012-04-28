from decimal import *
from BeautifulSoup import BeautifulSoup
import urllib2
import re


def getPrices(URL):
	request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
	connection = urllib2.urlopen( req )
	stringURL = connection.read()
	connection.close()
	
	soup = BeautifulSoup(stringURL)
	print "Price Soup Made"
	prices = [];
	for link in soup.findAll("a"):
		try:
			if "$" in link.text:
				prices.append(link.text)
		except:
			print "derp"
	print prices
	if (len(prices) == 4):
		prices.remove(prices[3])
		prices.remove(prices[1])
		usedPrice = prices[1]
		newPrice = prices[0]
	elif (len(prices) > 1):
		usedPrice = str(prices[0]).replace("$","")	
		newPrice = 0 
		for price in prices:
			price = str(price).replace("$","")
			if (Decimal(price) > Decimal(newPrice)):
				print str(price) + " is >= " + str(newPrice)
				newPrice = price
			if (Decimal(price) < Decimal(usedPrice)):
				print price + " is <= " + str(newPrice)
				usedPrice = price
		
	array = []
	array.append(newPrice)
	array.append(usedPrice)
	return array




print "Trying.."
ISBN = "9780205648467"
url_text = "http://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn=" + ISBN + "&field-publisher=&node=&field-p_n_condition-type=&field-feature_browse-bin=&field-subject=&field-language=&field-dateop=&field-datemod=&field-dateyear=&sort=relevanceexprank&Adv-Srch-Books-Submit.x=37&Adv-Srch-Books-Submit.y=14"

req = urllib2.Request(url_text, headers={'User-Agent' : "Magic Browser"})
con = urllib2.urlopen( req )
stringURL = con.read()
con.close()

soup = BeautifulSoup(stringURL)
print url_text
for link in soup.findAll("a"):
	#if "today's moral issues" in link.text:		
		#regex = re.compile("Today")
		#match = regex.search(div.text)
		#match = match.group()
		#print str(match)
	#	print link.text
		if "http://www.amazon.com/" in link.get("href"):
			print link.get("href")
			array = getPrices(link.get("href"))
			break
		else:
			print "."
print array
