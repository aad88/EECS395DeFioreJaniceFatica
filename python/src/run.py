
from amazonSearch import searchByKeyword
from amazonSearch import searchById

interest = "football"
items = searchById('B01MXLWO5D')
#items = searchByKeyword('star wars')
for item in items:
    print "Name: " + item['name']
    print "ASIN: " + item['id']
    print "URL: " + item['url']
    if item['price'] != None:
      print "Price: " + item['price']
    print ""
