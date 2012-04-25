import urllib2
from BeautifulSoup import BeautifulSoup

SCHOOL = "santafe"
page_results_increment_by_ten = 0

def getBookTitles(page_results_increment_by_ten,SCHOOL):
	total_books = 0
	title_array = []
	#while (True):
	while (page_results_increment_by_ten < 10):
			url = "http://" + SCHOOL + ".bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=22566&catalogId=10001&isbn=&author=&title=%22+%22&start=" + str(page_results_increment_by_ten)

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
							temp_string = td.text.replace("TITLE:","")
							print temp_string 
							title_array.append(temp_string)
							count+=1
							total_books+=1
					except:
						print "no thread found"

			page_results_increment_by_ten += 10
			if (count < 10):
				break
			print count

	print "total books equals:" + str(total_books)
	return title_array


def searchWithTitles(title_array):
#	for title in title_array:
		title = title_array[0]
		print str(title)	
		url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/ProductSearchCommand?storeId=22566&catalogId=10001&langId=-1&extSearchEnabled=G+&displayImage=Y+&search=" + str(title)
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		con = urllib2.urlopen( req )
		print "Opening Search Page"
		stringURL = con.read()
		con.close()

		soup = BeautifulSoup(stringURL)
		print "Search soup made"
		for td in soup.findAll("td"):
			try:
				if str(title) in td.text:
					print "Title found" 
					print str(title)
					for link in td.findAll("a"):
						if "TextbookDetailView" in link.get('href'):
							print "link found"
							print str(link.get('href')).replace("&amp;","&")
			except:
				print "title not found"
		
#	return
		return



titleArray = getBookTitles(page_results_increment_by_ten,SCHOOL)
print titleArray
searchWithTitles(titleArray)
print "----------------------------------------------this is the end-------------------------------------------------------"
