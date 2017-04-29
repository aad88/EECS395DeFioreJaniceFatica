
from amazon_search import searchById, searchByKeyword

id = 'B01MXLWO5D'

results = searchById(id)
for item in results:
    print 'Name: ' + item['name']
    print 'URL: ' + item['url']
    print 'Price: ' + item['price']
    print 'Image URL: ' + item['imageurl']
    print 'Image Height: ', item['imageheight']
    print 'Image Width: ', item['imagewidth']
    print ''
results2 = searchByKeyword('pots')
for item in results2:
    print 'Name: ' + item['name']
    print 'URL: ' + item['url']
    print 'Price: ' + item['price']
    print 'Image URL: ' + item['imageurl']
    print 'Image Height: ', item['imageheight']
    print 'Image Width: ', item['imagewidth']
    print ''
