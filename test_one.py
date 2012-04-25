import urllib2
import re
import time
from BeautifulSoup import BeautifulSoup

SCHOOL = "santafe"
page_results_increment_by_ten = 0

class BookInfo:
	pass

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

def getCourseFromSoup(soup):
	try:
		for div in soup.findAll("div"):
			if "Course" in div.text:
				print div.text
				regex = re.compile("[\d]Course.+Select")
				match = regex.search(div.text)
				match = re.sub("[\d]Course:", "", match.group())
				course = str(match).replace("Select","")
				return course 
		
	except:
		print "Course Error"
		return

def getEditionFromSoup(soup):
	try:
		for div in soup.findAll("div"):
			if "Edition" in div.text:
				regex = re.compile("Edition.+Publisher")
				match = regex.search(div.text)
				match = match.group()
				match = str(match).replace("Edition","")
				match = str(match).replace("Publisher","")
				edition = str(match)
				return edition 
	except:
		print "Edition ERROR"
		return

def getISBNFromSoup(soup):
	try:
		for div in soup.findAll("div"):
			if "ISBN" in div.text:
				regex = re.compile("ISBN...[\d]+") 
				match = regex.findall(div.text)
				match = re.sub("\D", "", str(match))
				ISBN = str(match)	
				return ISBN
	except:
		print "ISBN ERROR"
	return

def getUsedPriceFromSoup(soup):
	for tr in soup.findAll("tr"):
		if "Used" in tr.text:
			for td in tr.findAll("td"):
				if "$" in td.text:
					usedPrice = str(td.text)
					return usedPrice

def getNewPriceFromSoup(soup):
	for tr in soup.findAll("tr"):
		if "New" in tr.text:
			for td in tr.findAll("td"):
				if "$" in td.text:
					newPrice = str(td.text)
	return newPrice

def getBookInfoFromPage(link):
	url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/" + link
	request_url = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	connection = urllib2.urlopen( request_url )
	print "Opening Price Page"
	stringURL = connection.read()
	connection.close()

	soup = BeautifulSoup(stringURL)
	print "Price Page Soup Made"

	usedPrice = getUsedPriceFromSoup(soup)	
	newPrice = getNewPriceFromSoup(soup)
	ISBN = getISBNFromSoup(soup)
	edition = getEditionFromSoup(soup)
	course = getCourseFromSoup(soup)
	print "Used: " + usedPrice
	print "New: " + newPrice
	print "ISBN: " + ISBN
	print "Edition: " + edition
	print "Course: " + course

	book = BookInfo()
	book.usedPrice = usedPrice
	book.newPrice = newPrice
	book.ISBN = ISBN
	book.edition = edition
	book.course = course
	
	return book

def getPriceLinkFromLink(link):
	url = "http://santafe.bncollege.com" + link
	request_url = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	connection = urllib2.urlopen( request_url )
	print "Opening Book Page"	
	stringURL = connection.read()
	connection.close()

	soup = BeautifulSoup(stringURL)
	print "Book Page Soup Made"

	for img in soup.findAll("img"):
		try:
			if "image1" in img.get('name'):
				print "IMAGE FOUND"
				price_link = str(img.get("onclick"))
				print price_link
				price_link = price_link.replace("refreshTBDisplay('","")
				price_link = price_link.replace("');","")
				print price_link
				return getBookInfoFromPage(price_link)
				
				break
		except:
			print "."
	return


def printBook(book):
	print book.title +  "    " + book.ISBN + "     " + book.edition + "     " + book.course + "      " + book.usedPrice + "     " + book.newPrice	

def searchWithTitles(title_array):
	#for title in title_array:
		title = title_array[4]
		time.sleep(20)
		title_url = str(title).replace("&amp;","%26")	
		title_url = title_url.replace(" ","+")
		title_url = title_url.replace(":","%3A")
		title_url = title_url.replace("/","%2F")
		print title_url
		url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/ProductSearchCommand?storeId=22566&catalogId=10001&langId=-1&extSearchEnabled=G+&displayImage=Y+&search=" + title_url
		print url
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		con = urllib2.urlopen( req )
		print "Opening Search Page"
		stringURL = con.read()
		con.close()

		soup = BeautifulSoup(stringURL)
		print "Search soup made"
#		print soup
		for td in soup.findAll("td"):
			try:
				print "In soup"
				if str(title) in td.text:
					print "Title found" 
					print str(title)
					for link in td.findAll("a"):
						if "TextbookDetailView" in link.get('href'):
							print "link found"
							link = str(link.get('href')).replace("&amp;","&")
							print link
							book = getPriceLinkFromLink(link)	
							book.title = title
							printBook(book)
			except:
				print "title not found"
		
#	return
		return



titleArray = getBookTitles(page_results_increment_by_ten,SCHOOL)
print titleArray
searchWithTitles(titleArray)
print "----------------------------------------------this is the end-------------------------------------------------------"
