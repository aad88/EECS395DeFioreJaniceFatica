
from amazon import searchByKeyword
from amazon import searchById

interest = "football"
items = searchByKeyword(interest, 1000, 2000)
for item in items:
    print "Name: " + item['Name']
    print "URL: " + item['URL']
    print "Price: " + item['Price']
    print ""
