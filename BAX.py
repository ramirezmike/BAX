from decimal import *
import urllib2
import re
import time
from BeautifulSoup import BeautifulSoup
import socket

# CLASS DECLARATIONS
class BookInfo:
	pass

# GENERAL
def getSoup(URL):
	while (True):
		try:
			req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
			print "Pause to Maintain Connection..." 
			time.sleep(3)
			con = urllib2.urlopen(req, None, 5.0 )
			print "URL Open: " + URL
			stringURL = con.read()
			con.close()
			break
		except urllib2.URLError, e:
			print "Connection ERROR. Retrying.."
		except socket.timeout, e:
			print "Socket Timeout. Retrying.."


	soup = BeautifulSoup(stringURL)
	print "Soup Made"
	return soup

def is_number(testNumber):
    try:
        float(testNumber)
        return True
    except ValueError:
        return False

# PRINTING DATA
def printBook(book,number):
	print "-" * 181
	print str(number).rjust(3," "),
	try:
		print book.title.ljust(50," "), 
		print book.ISBN.ljust(15," ") + book.edition.ljust(8," ") + book.course.ljust(30," ") + "|".ljust(5," "),
		print book.usedPrice.ljust(8," ") + book.newPrice.ljust(10," ") + "$" + book.amzNew.ljust(8," ") + "$" + book.amzUsd.ljust(6," ")	

	except:
		print "Error on " + book.title
		print book.ISBN
		print book.edition
		print book.course
		print book.usedPrice
		print book.newPrice
		print book.amzNew
		print book.amzUsd
	return

def displayResults(bookArray):
	bookNumber = 0
	print "\n" * 4
	print "-" * 181
	print "#".rjust(3," ") + "Title".rjust(6," ") + "ISBN".rjust(50," ") + "Edn.".rjust(15," ") + "Course".rjust(10," "), 
	print "Used".rjust(33," ") + "New".rjust(7," ") + "AmzN".rjust(11," ") + "AmzU".rjust(9," ")

	for book in bookArray:
		bookNumber+=1
		printBook(book,bookNumber)
	print "-" * 181
	print "Number of Books: " + str(len(bookArray))
	return

# EXPORTING TO EXCEL
def createExcel(array, fileName):
	excelText = ""
	for book in array:
		try:
			excelText = excelText + addToExcelText(book)
			print "Text added to Excel String"
		except:
			print "Excel Text ERRROR"
			continue
	exportToExcel(fileName,excelText)
	print "Excel sheet written"
	return

def addToExcelText(book):
	text = "\n" + book.title + "\t\t" + book.ISBN + "\t" + book.course + "\t" + book.edition + "\t" + book.usedPrice + "\t" + book.newPrice + "\t" + book.amzNew + "\t" + book.amzUsd
	return text


def exportToExcel(school,text):
	fileTitle = school + ".xls"
	fileContent = open(fileTitle,"w")
	fileContent.write(text)
	fileContent.close()
	return

# BNCOLLEGE 
def getSchoolID(school):
	url = "http://" + school + ".bncollege.com"
	while (True):
		print url
		soup = getSoup(url)
		for link in soup.findAll("a"):
			if "storeId" in link.get("href"):
				regex = re.compile("storeId=.+&")
				match = regex.search(link.get("href"))
				match = re.sub("storeId=","", match.group())
				schoolId = str(match).replace("&","")
		try:
			return schoolId
		except:
			print "Redirecting.."
		regex = re.compile('URL=.+"')
		match = regex.search(str(soup))
		match = re.sub('URL="',"",match.group())
		match = match.replace('"',"")
		match = match.replace("&amp;","&")
		url = "http://" + school + ".bncollege.com/" + match


def getBookTitles(page_results_increment_by_ten,SCHOOL,schoolId):
	total_books = 0
	title_array = []
	temp_array = []
	while (True):
	#while (page_results_increment_by_ten < 10):
		url = "http://" + SCHOOL + ".bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=" + schoolId + "&catalogId=10001&isbn=&author=&title=%22+%22&start=" + str(page_results_increment_by_ten)

		print "Total Book Titles Collected: " + str(total_books)

		soup = getSoup(url)

		count = 0
		previous_array = temp_array 
		temp_array = []
		
		for dd in soup.findAll("td"):
			for td in dd.findAll("td"):
				try:
					if 'TITLE:' in td.text:
						print "Title Found: ",
						temp_string = td.text.replace("TITLE:","")
						print temp_string 
						temp_array.append(temp_string)
						count+=1
						total_books+=1
				except:
					print "No Title in 'td'"

		page_results_increment_by_ten += 10
		
		if (temp_array == previous_array):
			break
		for string in temp_array:
			title_array.append(string)	
		if (count < 10):
			break

	print "Total Books Found: " + str(total_books)
	return title_array

def searchWithTitles(title_array,bookarray,extrabooksarray,school,schoolId):
	bookCount = 0
#		bookCount = 0
	for title in title_array:
#		title = title_array[0]
		bookCount += 1
		print "Book number " + str(bookCount) + " of " + str(len(title_array))

		title_url = str(title).replace("&amp;","%26")	
		title_url = title_url.replace(" ","+")
		title_url = title_url.replace(":","%3A")
		title_url = title_url.replace("/","%2F")

		url = "http://" + school + ".bncollege.com/webapp/wcs/stores/servlet/ProductSearchCommand?storeId=" + str(schoolId) + "&catalogId=10001&langId=-1&extSearchEnabled=G+&displayImage=Y+&search=" + title_url
		print "Generated Search URL: " + url

		soup = getSoup(url)
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
							print link
							priceLink = getPriceLinkFromLink(link,school)	
							book = getBookInfoFromPage(priceLink,school) 
							book.title = str(titleOfBookInLoop).replace("&amp;","&")
							if (title == titleOfBookInLoop):
								if (ifBookIsOnBuyBack(book,school,schoolId)):
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
		
	return bookarray
#		return bookarray

def ifBookIsOnBuyBack(book, school,schoolId):
	url = "http://" + school + ".bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=" + schoolId + "&catalogId=10001&isbn=" + str(book.ISBN) + "&author=&title=&x=44&y=20"
	soup = getSoup(url)

	for div in soup.findAll("div"):
		if book.title in div.text:
			print "Match Found"
			return True
		else:
			print "."
	return False

def getBookInfoFromPage(link,school):
	url = "http://" + school + ".bncollege.com/webapp/wcs/stores/servlet/" + link
	soup = getSoup(url)	
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

def getPriceLinkFromLink(link,school):
	url = "http://" + school + ".bncollege.com" + link
	soup = getSoup(url)
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

# AMAZON
def storeAmazonInfo(array):
	for book in array:
		soup = getAmazonLink(book.ISBN)
		if (soup):
			priceArray = getAmazonPrices(soup)
			book.amzNew = priceArray[0]
			book.amzUsd = priceArray[1]
		else:
			book.amzNew = ""
			book.amzUsd = ""
	return

def getAmazonLink(ISBN):
	print "Connecting to Amazon.."
        print ISBN
	if (ISBN):
		url_text = "http://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn=" + ISBN + "&field-publisher=&node=&field-p_n_condition-type=&field-feature_browse-bin=&field-subject=&field-language=&field-dateop=&field-datemod=&field-dateyear=&sort=relevanceexprank&Adv-Srch-Books-Submit.x=37&Adv-Srch-Books-Submit.y=14"	

		soup = getSoup(url_text)
		
		for link in soup.findAll("a"):
			if "http://www.amazon.com/" in link.get("href"):
				print "Amazon Book Link: " + link.get("href")
				return soup
		
	print "Book Not Found on Amazon Website.."
	return


def getAmazonPrices(soup):
	print "Price Soup Made"
	prices = []
	foundPricesArray = []

	for link in soup.findAll("a"):
		try:
			if "$" in link.text:
				price_test = link.text.replace("$","")
				if (is_number(price_test)):
					prices.append(link.text)
		except:
			print "Amazon Money ERROR"
	print prices
		
	newPrice = "None"
	usedPrice = "None"

	if (len(prices) == 4):
		prices.remove(prices[3])
		prices.remove(prices[1])
		usedPrice = str(prices[1]).replace("$","")
		newPrice = str(prices[0]).replace("$","")

	elif (len(prices) > 1):
		usedPrice = str(prices[0]).replace("$","")
		newPrice = 0
		for price in prices:
			price = str(price).replace("$","")

			if (Decimal(price) > Decimal(newPrice)):
				print str(price) + " is > " + str(newPrice)
				newPrice = price
			if (Decimal(price) < Decimal(usedPrice)):
				print price + " is <= " + str(newPrice)
				usedPrice = price
	
	foundPricesArray.append(newPrice)
	foundPricesArray.append(usedPrice)
	return foundPricesArray 

# SOUP FUNCTIONS
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
						print usedPrice
						return usedPrice
		emptyString = "NONE"
		return str(emptyString)
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
						print newPrice
						return newPrice
		emptyString = "NONE"
		return str(emptyString)
	except:
		print "New Price ERROR"
		emptyString = "NONE"
		return str(emptyString)

pause_script = ""
while (pause_script != "q"):
	page_results_increment_by_ten = 0
	Book_Array = []
	Extra_Books_Array = []

	SCHOOL = raw_input("School:")
	excelFileName = raw_input("Enter name you wish to use for the exported excel file: ")

	startTime = time.time()

	schoolId = getSchoolID(SCHOOL) 
	titleArray = getBookTitles(page_results_increment_by_ten,SCHOOL,schoolId)
	Book_Array = searchWithTitles(titleArray,Book_Array,Extra_Books_Array,SCHOOL,schoolId)

	storeAmazonInfo(Book_Array)
	for book in Extra_Books_Array:
		print book.ISBN
	storeAmazonInfo(Extra_Books_Array)

	displayResults(Book_Array)
	displayResults(Extra_Books_Array)


	createExcel(Book_Array,excelFileName)

	elapsedTime = time.time() - startTime
	print "Elapsed Time: " + str(elapsedTime) + "(s)"

	pause_script = raw_input("Enter 'q' to quit, or enter anything else to restart the script: ")
