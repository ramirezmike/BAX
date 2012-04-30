from decimal import *
import urllib2
import re
import time
from BeautifulSoup import BeautifulSoup
import socket

SCHOOL = "santafe"
page_results_increment_by_ten = 0
Book_Array = []
Extra_Books_Array = []

class BookInfo:
	pass


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

def addToExcelText(book):
	text = "\n" + book.title + "\t\t" + book.ISBN + "\t" + book.course + "\t" + book.edition + "\t" + book.usedPrice + "\t" + book.newPrice + "\t" + book.amzNew + "\t" + book.amzUsd
	return text

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def exportToExcel(school,text):
	fileTitle = school + ".xls"
	fileContent = open(fileTitle,"w")
	fileContent.write(text)
	fileContent.close()

def ifBookIsOnBuyBack(book):
	url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=22566&catalogId=10001&isbn=" + str(book.ISBN) + "&author=&title=&x=44&y=20"
	soup = getSoup(url)

	for div in soup.findAll("div"):
		if book.title in div.text:
			print "Match Found"
			return True
		else:
			print "."
	return False

def getAmazonLink(ISBN):
	print "Connecting to Amazon.."
        print ISBN
	url_text = "http://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn=" + ISBN + "&field-publisher=&node=&field-p_n_condition-type=&field-feature_browse-bin=&field-subject=&field-language=&field-dateop=&field-datemod=&field-dateyear=&sort=relevanceexprank&Adv-Srch-Books-Submit.x=37&Adv-Srch-Books-Submit.y=14"	
	soup = getSoup(url_text)
	
	for link in soup.findAll("a"):
		if "http://www.amazon.com/" in link.get("href"):
			print "Amazon Book Link: " + link.get("href")
			#return link.get("href")
			#return stringURL
			return soup
		
	print "Book Not Found on Amazon Website.."
	return


def getAmazonPrices(soup):
	#request = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
	#connection = urllib2.urlopen( req )
	#stringURL = connection.read()
	#connection.close()

	#soup = BeautifulSoup(stringURL)
	
	print "Price Soup Made"
	prices = []

	for link in soup.findAll("a"):
		try:
			if "$" in link.text:
				price_test = link.text.replace("$","")
				if (is_number(price_test)):
					prices.append(link.text)
		except:
			print "No Money Found"
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
	
	foundPricesArray = []
	foundPricesArray.append(newPrice)
	foundPricesArray.append(usedPrice)
	return foundPricesArray 

def getBookTitles(page_results_increment_by_ten,SCHOOL):
	total_books = 0
	title_array = []
	temp_array = []
	while (True):
	#while (page_results_increment_by_ten < 10):
			url = "http://" + SCHOOL + ".bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=22566&catalogId=10001&isbn=&author=&title=%22+%22&start=" + str(page_results_increment_by_ten)

			print "Total Book Titles Collected: " + str(total_books)

			soup = getSoup(url)

			#print soup

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
	print title_array
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

def getBookInfoFromPage(link):
	url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/" + link
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

def getPriceLinkFromLink(link):
	url = "http://santafe.bncollege.com" + link
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


def printBook(book,number):
	try:
		print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
		print str(number).rjust(3," "),
		print book.title.ljust(50," "), 
		print book.ISBN.ljust(15," ") + book.edition.ljust(8," ") + book.course.ljust(30," ") + "|".ljust(5," ") + book.usedPrice.ljust(8," ") + book.newPrice.ljust(10," ") + "$" + book.amzNew.ljust(8," ") + "$" + book.amzUsd.ljust(6," ")	

	except:
		print "Error on " + book.title
		print book.ISBN
		print book.edition
		print book.course
		print book.usedPrice
		print book.newPrice
		print book.amzNew
		print book.amzUsd


def searchWithTitles(title_array,bookarray,extrabooksarray):
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
		url = "http://santafe.bncollege.com/webapp/wcs/stores/servlet/ProductSearchCommand?storeId=22566&catalogId=10001&langId=-1&extSearchEnabled=G+&displayImage=Y+&search=" + title_url
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
		
	return bookarray
	#	return bookarray


startTime = time.time()
print "Start Time: " + str(startTime)

titleArray = getBookTitles(page_results_increment_by_ten,SCHOOL)
Book_Array = searchWithTitles(titleArray,Book_Array,Extra_Books_Array)

for book in Book_Array:
	amazonSoup = getAmazonLink(book.ISBN)
	if (amazonSoup):
		priceArray = getAmazonPrices(amazonSoup)
		book.amzNew = priceArray[0]
		book.amzUsd = priceArray[1]
	else:
		book.amzNew = ""
		book.amzUsd = ""

for book in Extra_Books_Array:
	extraAmazonSoup = getAmazonLink(book.ISBN)
	if (extraAmazonSoup):
		priceArray = getAmazonPrices(extraAmazonSoup)
		book.amzNew = priceArray[0]
		book.amzUsd = priceArray[1]
	else:
		book.amzNew = ""
		book.amzUsd = ""
	


bookNumber = 0
extraBookNumber = 0
print "\n\n"
print "\n\n"


print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
print "#".rjust(3," ") + "Title".rjust(6," ") + "ISBN".rjust(50," ") + "Edn.".rjust(15," ") + "Course".rjust(10," ") + "Used".rjust(33," ") + "New".rjust(7," ") + "AmzN".rjust(11," ") + "AmzU".rjust(9," ")

for book in Book_Array:
	bookNumber+=1
	printBook(book,bookNumber)
for book in Extra_Books_Array:
	bookNumber+=1
	printBook(book,bookNumber)
print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------"
print "Number of Books: " + str(len(Book_Array))
print "\n\n"
print "---------------------------------------------------------------------------------EXTRA BOOKS---------------------------------------------------------------------"
print "#".rjust(3," ") + "Title".rjust(6," ") + "ISBN".rjust(50," ") + "Edn.".rjust(15," ") + "Course".rjust(10," ") + "Used".rjust(33," ") + "New".rjust(7," ") + "AmzN".rjust(11," ") + "AmzU".rjust(7," ")
for book in Extra_Books_Array:
	extraBookNumber+=1
	printBook(book,extraBookNumber)	
print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------"
print "Number of Books: " + str(len(Extra_Books_Array))
print "----------------------------------------------this is the end----------------------------------------------------------------------------------------------------"

excelText = ""
for book in Book_Array:
	try:
		excelText = excelText + addToExcelText(book)
		print "Text added to Excel String"
	except:
		print "Excel Text ERRROR"
		continue
exportToExcel(SCHOOL,excelText)
print "Excel sheet written"

elapsedTime = time.time() - startTime
print "Elapsed Time: " + str(elapsedTime)
