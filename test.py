from BeautifulSoup import BeautifulSoup


go to santafe.bncollege.com

"click get cash"

in title search '" "'
	will result in pages of results
for each result in results
	save title to a variable
	search for title on website
		if title returns multiple results
			check titles and copy results
			copy result to array that is exact match
			make note of multiple results for search
	click "select"
	copy Course letters and numbers to a variable and ISBN
	copy Edition and published year
	copy used and new prices
	save all to object of book and place in new array

go to amazon.com

for each object in array
	search by object.ISBN
	its ALWAYS the first result
	copy and add the price listed from amazon: (new and used)
	

copy all information into spreadsheet || print out data in terminal in readible format


Script 2
	for each object in array
		search book
		copy changed prices
		save prices over amazon variables (new and used)
		update spreadsheet


