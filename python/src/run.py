
from amazon import searchByKeyword
from amazon import searchById

interest = "football"
items = searchById('0439064872')
for item in items:
    print "Name: " + item['name']
    print "ASIN: " + item['id']
    print "URL: " + item['url']
    if item['price'] != None:
      print "Price: " + item['price']
    print ""
