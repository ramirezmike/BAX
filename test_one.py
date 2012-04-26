import urllib2
import re
import time
from BeautifulSoup import BeautifulSoup

SCHOOL = "santafe"
page_results_increment_by_ten = 0
Book_Array = []
Extra_Books_Array = []

class BookInfo:
	pass


def ifBookIsOnBuyBack(book):
	url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=22566&catalogId=10001&isbn=" + str(book.ISBN) + "&author=&title=&x=44&y=20"
	request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	print "Pause to Maintain Connection..."
	time.sleep(3)
	connection = urllib2.urlopen( request )
	stringURL = connection.read()
	connection.close()	

	soup = BeautifulSoup(stringURL)

	for div in soup.findAll("div"):
		if book.title in div.text:
			print "Match Found"
			return True
		else:
			print "."
	return False



def getBookTitles(page_results_increment_by_ten,SCHOOL):
	total_books = 0
	title_array = []
	while (True):
#	while (page_results_increment_by_ten < 50):
			url = "http://" + SCHOOL + ".bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=22566&catalogId=10001&isbn=&author=&title=%22+%22&start=" + str(page_results_increment_by_ten)

			req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
			print "Pause to Maintain Connection... Total Book Titles Collected: " + str(total_books)
			time.sleep(3)
			con = urllib2.urlopen( req )
			print "URL Open"
			stringURL = con.read()
			con.close()

			soup = BeautifulSoup(stringURL)
			print "Soup Made"

			#print soup

			count = 0
			for dd in soup.findAll("td"):
				for td in dd.findAll("td"):
					try:
						if 'TITLE:' in td.text:
							print "Title Found: ",
							temp_string = td.text.replace("TITLE:","")
							print temp_string 
							title_array.append(temp_string)
							count+=1
							total_books+=1
					except:
						print "No Title in 'td'"

			page_results_increment_by_ten += 10
			if (count < 10):
				break

	print "Total Books Found: " + str(total_books)
	return title_array

def getCourseFromSoup(soup):
	try:
		for div in soup.findAll("div"):
			if "Course" in div.text:
				regex = re.compile("[\d]Course.+Select")
				match = regex.search(div.text)
				match = re.sub("[\d]Course:", "", match.group())
				course = str(match).replace("Select","")
				return course 
		
	except:
		print "Course Error"
		emptyString = "NONE"
		return str(emptyString) 

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
		emptyString = "No Edition"
		return str(emptyString)

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
		emptyString = "NONE"
		return str(emptyString) 

def getUsedPriceFromSoup(soup):
	try:
		for tr in soup.findAll("tr"):
			if "Used" in tr.text:
				for td in tr.findAll("td"):
					if "$" in td.text:
						usedPrice = str(td.text)
						return usedPrice
	except:
		print "Used Price ERROR"
		emptyString = "NONE"
		return str(emptyString)

def getNewPriceFromSoup(soup):
	try:
		for tr in soup.findAll("tr"):
			if "New" in tr.text:
				for td in tr.findAll("td"):
					if "$" in td.text:
						newPrice = str(td.text)
						return newPrice
	except:
		print "New Price ERROR"
		emptyString = "NONE"
		return str(emptyString)

def getBookInfoFromPage(link):
	url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/" + link
	request_url = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	print "Pause to Maintain Connection"
	time.sleep(3)
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

	book = BookInfo()
	book.usedPrice = usedPrice
	book.newPrice = newPrice
	book.ISBN = ISBN
	book.edition = str(edition)
	book.course = course
	
	print "Book Info Successfully Stored"
	return book

def getPriceLinkFromLink(link):
	url = "http://santafe.bncollege.com" + link
	request_url = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	print "Pause to Maintain Connection"
	time.sleep(3)
	connection = urllib2.urlopen( request_url )
	print "Opening Book Page"	
	stringURL = connection.read()
	connection.close()

	soup = BeautifulSoup(stringURL)
	print "Book Page Soup Made"

	for img in soup.findAll("img"):
		try:
			if "image1" in img.get('name'):
				print "IMG Tag Found"
				price_link = str(img.get("onclick"))
				price_link = price_link.replace("refreshTBDisplay('","")
				price_link = price_link.replace("');","")
				print "URL for Prices: " + price_link
				return price_link
		except:
			print "."
	return


def printBook(book,number):
	try:
		print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
		print str(number).rjust(3," "),
		print book.title.ljust(50," "), 
		print book.ISBN.ljust(15," ") + book.edition.ljust(8," ") + book.course.ljust(30," ") + book.usedPrice.ljust(8," ") + book.newPrice.ljust(8," ")	
	except:
		print "Error on " + book.title
		print book.ISBN
		print book.edition
		print book.course
		print book.usedPrice
		print book.newPrice

def searchWithTitles(title_array,bookarray,extrabooksarray):
	#for title in title_array:
		title = title_array[21]
		title_url = str(title).replace("&amp;","%26")	
		title_url = title_url.replace(" ","+")
		title_url = title_url.replace(":","%3A")
		title_url = title_url.replace("/","%2F")
		url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/ProductSearchCommand?storeId=22566&catalogId=10001&langId=-1&extSearchEnabled=G+&displayImage=Y+&search=" + title_url
		print "Generated Search URL: " + url
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		print "Connecting.. this can sometimes take a bit"
		con = urllib2.urlopen( req )
		print "Opening Search Page"
		stringURL = con.read()
		con.close()

		soup = BeautifulSoup(stringURL)
		print "Search Soup Made"
		for td in soup.findAll("td"):
			try:
				if str(title) in td.text:
					regex = re.compile("DESCRIPTION.+AUTHOR")
					match = regex.search(td.text)
					match = re.sub("DESCRIPTION:", "", match.group())
					titleOfBookInLoop = str(match).replace("AUTHOR","")
					print "TITLE OF BOOK IN LOOP: " + titleOfBookInLoop

					for link in td.findAll("a"):
						if "TextbookDetailView" in link.get('href'):
							print "Book Link Found"
							link = str(link.get('href')).replace("&amp;","&")
#							link = link.replace(" ","+")
#							link = link.replace(":","%3A")
#							link = link.replace("/","%2F")
							print link
							priceLink = getPriceLinkFromLink(link)	
							book = getBookInfoFromPage(priceLink) 
							book.title = str(titleOfBookInLoop).replace("&amp;","&")
							if (title == titleOfBookInLoop):
								if (ifBookIsOnBuyBack(book)):
									print "Book Added to Book Array"
									bookarray.append(book)
								
								else:
									print "Book Added to Extra Book Array"
									extrabooksarray.append(book)
							else:
								print "Book Added to Extra Book Array"
								extrabooksarray.append(book)
			except:
				print "Title Not Found in 'td' SKIPPING"
		
#	return bookarray
		return bookarray



titleArray = getBookTitles(page_results_increment_by_ten,SCHOOL)
Book_Array = searchWithTitles(titleArray,Book_Array,Extra_Books_Array)
bookNumber = 0
extraBookNumber = 0
print "\n\n"
print "\n\n"


print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
print "#".rjust(3," ") + "Title".rjust(6," ") + "ISBN".rjust(50," ") + "Edn.".rjust(15," ") + "Course".rjust(10," ") + "Used".rjust(28," ") + "New".rjust(7," ")

for book in Book_Array:
	bookNumber+=1
	printBook(book,bookNumber)
print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------"
print "Number of Books: " + str(len(Book_Array))
print "\n\n"
print "---------------------------------------------------------------------------------EXTRA BOOKS---------------------------------------------------------------------"
print "#".rjust(3," ") + "Title".rjust(6," ") + "ISBN".rjust(50," ") + "Edn.".rjust(15," ") + "Course".rjust(10," ") + "Used".rjust(28," ") + "New".rjust(7," ")
for book in Extra_Books_Array:
	extraBookNumber+=1
	printBook(book,extraBookNumber)	
print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------"
print "Number of Books: " + str(len(Extra_Books_Array))
print "----------------------------------------------this is the end----------------------------------------------------------------------------------------------------"
