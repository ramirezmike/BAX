import urllib2
from BeautifulSoup import BeautifulSoup

print "test"
page_results_increment_by_ten = 0
url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=22566&catalogId=10001&isbn=&author=&title=%22+%22&start=" + str(page_results_increment_by_ten)
req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
con = urllib2.urlopen( req )
print "url open"
stringURL = con.read()
con.close()

soup = BeautifulSoup(stringURL)
print "soup made"

#print soup

count = 0
for dd in soup.findAll("td"):
	for td in dd.findAll("td"):
		try:
			if 'TITLE:' in td.text:
				print "title found"
				print td.text
				count+=1
		except:
			print "no thread found"
print "this is the end"
print count
