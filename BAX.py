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
def makeProfit(usedPrice,amzPrice):
	usedPrice = str(usedPrice).replace("$","")
	amzPrice = str(amzPrice).replace("$","")

	if (is_number(usedPrice) & is_number(amzPrice)):
		usedPrice = decFormat(usedPrice)/2
		amzPrice = decFormat(amzPrice) + 8
		profit = usedPrice / amzPrice
		return profit
	else:
		return "NONE"

def makeCost(price):
	price = str(price).replace("$","")
	if (is_number(price)):
		cost = decFormat(price) + 8
		return cost
	else:
		return "NONE"

def makeRevenue(price):
	price = str(price).replace("$","")
	if (is_number(price)):
		revenue = decFormat(price)/2
		return revenue
	else:
		return "NONE"

def decFormat(number):
	number = str(number).replace("$","")
	if (is_number(number)):
		number = Decimal(number)
		return number 
	else:
		return ""

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
		except socket.error, e:
			print "Socket Error: Connection Reset By Peer. Retrying.."


	soup = BeautifulSoup(stringURL)
	print "Soup Made"
	return soup

def is_number(testNumber):
    try:
        float(testNumber)
        return True
    except ValueError:
        return False

def getRetryTitleArray(retryarray):
	titleArray = []
	for book in retryarray:
		titleArray.append(str(book.title))
	return titleArray

def makeShortTitles(bookArray):
	print "Making Short Book Titles..."
	for book in bookArray:
		while (len((book.title).split()) > 1):
			string = re.sub("[^A-Za-z\d]"," ", book.title)	
			string = string.split()
			string.remove(string[len(string)/2])
			string = " ".join(string)
			book.title = string

	
# PRINTING DATA
def printBook(book,number):
	print "-" * 181
	print str(number).rjust(3," "),
	try:
		print book.tempTitle.ljust(50," "), 
		print book.ISBN.ljust(15," ") + book.edition.ljust(8," ") + book.course.ljust(30," ") + "|".ljust(5," "),
		print book.usedPrice.ljust(8," ") + book.newPrice.ljust(10," ") + "$" + book.amzNew.ljust(8," ") + "$" + book.amzUsd.ljust(6," ")	

	except:
		print "Error on " + book.tempTitle
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
	revenue = (makeRevenue(book.usedPrice))
	cost = (makeCost(book.amzUsd))
	profitRatio = (makeProfit(book.usedPrice,book.amzUsd))
	text = "\n" + book.tempTitle + "\t" + book.ISBN + "\t" + book.course + "\t" + book.edition + "\t" + book.usedPrice + "\t" + book.newPrice + "\t" + book.amzNew + "\t" + book.amzUsd + "\t" + str(revenue) + "\t" + str(cost) + "\t" + str(profitRatio)
	return text


def exportToExcel(school,text):
	fileTitle = school + ".xls"
	fileContent = open(fileTitle,"w")
	fileContent.write(text)
	fileContent.close()
	return

# BNCOLLEGE 
def checkForJavascriptBug(string):
    if (string == "JAVASCRIPT:WEB WARRIOR SERIES"):
        print "Book title had javascript; fixed."
        string = "JAVASCRIPT"
    return string

def removeDuplicateBooks(bookArray,retryArray):
	tempArray = bookArray
	for book in tempArray:
		for retryBook in retryArray:
			if (book.tempTitle == retryBook.tempTitle):
				bookArray.remove(book)

def makeBooksFromTitleArray(titleArray):
	booksWithTitles = []
	for title in titleArray:
		book = BookInfo()
		book.title = title
		book.tempTitle = title
		book.usedPrice = "NONE"
		book.newPrice = "NONE"
		book.ISBN = "NONE"
		book.edition = "NONE"
		book.course = "NONE"
		booksWithTitles.append(book)
	return booksWithTitles
		

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
#	while (page_results_increment_by_ten < 10):
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
						temp_string = checkForJavascriptBug(temp_string) 
						if((temp_string in title_array) == False):
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

def searchWithTitles(title_array,bookarray,extrabooksarray,retryarray,school,schoolId):
	bookCount = 0
#		bookCount = 0
	for bookFromArray in title_array:
#		bookFromArray = title_array[10]
		bookCount += 1
		print "Book number " + str(bookCount) + " of " + str(len(title_array))

		title_url = str(bookFromArray.title).replace("&amp;","%26")	
		title_url = title_url.replace(" ","+")
		title_url = title_url.replace(":","%3A")
		title_url = title_url.replace("/","%2F")

		url = "http://" + school + ".bncollege.com/webapp/wcs/stores/servlet/ProductSearchCommand?storeId=" + str(schoolId) + "&catalogId=10001&langId=-1&extSearchEnabled=G+&displayImage=Y+&search=" + title_url
		print "Generated Search URL: " + url

		soup = getSoup(url)
		print "Search Soup Made"
		for td in soup.findAll("td"):
			try:
				if ((str(bookFromArray.title) in td.text) | (str(bookFromArray.tempTitle) in td.text)):
					regex = re.compile("DESCRIPTION.+AUTHOR")
					match = regex.search(td.text)
					match = re.sub("DESCRIPTION:", "", match.group())
					titleOfBookInLoop = str(match).replace("AUTHOR","")

					if (bookFromArray.tempTitle == titleOfBookInLoop):
						print "TITLE OF BOOK IN LOOP: " + titleOfBookInLoop

						for link in td.findAll("a"):
							if "TextbookDetailView" in link.get('href'):
								print "Book Link Found"
								link = str(link.get('href')).replace("&amp;","&")
								print link
								priceLink = getPriceLinkFromLink(link,school)	
								if (priceLink):
									bookFromArray = getBookInfoFromPage(priceLink,school,bookFromArray) 
									if (bookFromArray.ISBN == "NONE"):
										retryarray.append(bookFromArray)
										print "Book Added to Retry Array"
									elif (bookFromArray.tempTitle == titleOfBookInLoop):
										if (ifBookIsOnBuyBack(bookFromArray,school,schoolId) == False):
											print "Book Added to Extra Book Array"
											extrabooksarray.append(bookFromArray)
											
									else:
										print "Book Successfully Stored"
								else:
									print "Book Price Page Not Found... Getting ISBN"
									bookPageURL = "http://" + school + ".bncollege.com" + link
									bookInfoSoup = getSoup(bookPageURL)
									bookFromArray.ISBN = getISBNFromSoup(bookInfoSoup)
									print "ISBN Saved"
					else:
						print "Wrong book.."
				else:
					print "."
			except:
				print "Regex Error?"
		if (bookFromArray.ISBN == "NONE"):
			print "Book added to Retry Array"
			retryarray.append(bookFromArray)
		
#	return title_array 
#		return title_array 

def ifBookIsOnBuyBack(book, school,schoolId):
	url = "http://" + school + ".bncollege.com/webapp/wcs/stores/servlet/BuyBackSearchCommand?extBuyBackSearchEnabled=Y&displayImage=N+&langId=-1&storeId=" + schoolId + "&catalogId=10001&isbn=" + str(book.ISBN) + "&author=&title=&x=44&y=20"
	soup = getSoup(url)
	#print soup
	print "Buyback check: " + book.title + ": " + url
	if " " in book.title:
		regex = re.compile(" .+")
		matchSpace = regex.search(book.title)
		if (matchSpace):
			shortTitle = str(book.title).replace(matchSpace.group(),"")
	if "." in book.title:
		regex = re.compile("\..+")
		matchPeriod = regex.search(shortTitle)
		if (matchPeriod):
			matchPeriod = matchPeriod.group()
			periodTitle = str(shortTitle).replace(matchPeriod,"")

	for div in soup.findAll("div"):
		if book.title in div.text:
			print "Match Found"
			return True
		elif book.title.replace("&","&amp;") in div.text:
			print "Match Found"
			return True
		elif (shortTitle):
			if shortTitle in div.text:
				print "Match Found"
				return True
			elif shortTitle.replace("&","&amp;") in div.text:
				print "Match Found"
				return True
		elif (periodTitle):
			if periodTitle in div.text:
				print "Match Found"
				return True
		else:
			print "."
	return False

def getBookInfoFromPage(link,school,book):
	url = "http://" + school + ".bncollege.com/webapp/wcs/stores/servlet/" + link
	soup = getSoup(url)	
	print "Book info page: " + url
	print "Price Page Soup Made"

	if (checkBookTitle(soup,book)):
		for i in range(0,2):
			if (book.usedPrice == "NONE"):	
				book.usedPrice = str(getUsedPriceFromSoup(soup))
			if (book.newPrice == "NONE"):	
				book.newPrice = str(getNewPriceFromSoup(soup))
			if (book.ISBN == "NONE"):	
				book.ISBN = str(getISBNFromSoup(soup))
			if (book.edition == "NONE"):	
				book.edition = str(getEditionFromSoup(soup))
			if (book.course == "NONE"):	
				book.course = str(getCourseFromSoup(soup))
			print "Book Info Stored"
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
				if "Add2" in price_link:
					print "Add2 found"
				else:
					return price_link
			else:
				print "."
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
		
		emptyString = "NONE"
		return str(emptyString)
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
		emptyString = "NONE"
		return str(emptyString)
	except:
		print "Edition ERROR"
		emptyString = "NONE"
		return str(emptyString)

def checkBookTitle(soup,book):
        try:    
                for img in soup.findAll("img"):
                        if (img.get("title")):
                                if (str(book.tempTitle).replace("&amp;","&") == img.get("title")):
                                        print "Title Check Success"          
                                        return True           
                        else:                                  
                                 print "."              
		return False
                                   
        except:  
                 print "TITLE ERROR"
				
def getISBNFromSoup(soup):
	try:
		for div in soup.findAll("div"):
			if "ISBN" in div.text:
				regex = re.compile("ISBN...[\d]+") 
				match = regex.findall(div.text)
				match = re.sub("\D", "", str(match))
				ISBN = str(match)	
				return ISBN
		emptyString = "NONE"
		return str(emptyString)
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


# start of script. Create schedule of schools

pause_script = ""
while (pause_script != "q"):
	Schools = []
	Excel_Names = []

	numberOfSchools = raw_input("How many schools will be scraped: ")
	for i in range(0,int(numberOfSchools)):
		schoolName = raw_input("Name of School Number " + str(i) + ": ")
		Schools.append(schoolName)	
		excelFileName = raw_input("Enter name you wish to use for this school's exported excel file: ")
		Excel_Names.append(excelFileName)
		print "School " + schoolName + " saved."
		
	i = 0
	for school in Schools: 
		print school + " will be saved as " + Excel_Names[i] 
		i+=1
	schoolSelection = 0
	for school in Schools:
			page_results_increment_by_ten = 0
			Book_Array = []
			Extra_Books_Array = []
			Retry_Array = []

			SCHOOL = Schools[schoolSelection]
			excelFileName = Excel_Names[schoolSelection]

			startTime = time.time()

			schoolId = getSchoolID(SCHOOL) 
			titleArray = getBookTitles(page_results_increment_by_ten,SCHOOL,schoolId)
			booksWithTitles = makeBooksFromTitleArray(titleArray)
			searchWithTitles(booksWithTitles,Book_Array,Extra_Books_Array,Retry_Array,SCHOOL,schoolId)


		#	removeDuplicateBooks(booksWithTitles,Retry_Array)
			for i in range(0,2):
				print "RETRYING..."
				Retry_Array = set(Retry_Array)
				retryTitles = []
				makeShortTitles(Retry_Array)
				searchWithTitles(Retry_Array,Book_Array,Extra_Books_Array,retryTitles,SCHOOL,schoolId)
				for book in Retry_Array:
					booksWithTitles.append(book)
					print "Added " + book.tempTitle + " to booksWithTitles"
				Retry_Array = retryTitles

			booksWithTitles = set(booksWithTitles)
			retryTitles = set(retryTitles)
			
			for book in booksWithTitles:
				book.title = book.tempTitle
				print book.title

			storeAmazonInfo(booksWithTitles)
			storeAmazonInfo(Extra_Books_Array)
			storeAmazonInfo(retryTitles)

			displayResults(booksWithTitles)
			displayResults(Extra_Books_Array)

			displayResults(retryTitles)


			createExcel(booksWithTitles,excelFileName)

			elapsedTime = time.time() - startTime
			print "Elapsed Time: " + str(elapsedTime) + "(s)"
			schoolSelection += 1
	pause_script = raw_input("Enter 'q' to quit, or enter anything else to restart the script: ")
