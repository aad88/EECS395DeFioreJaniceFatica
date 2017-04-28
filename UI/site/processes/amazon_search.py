#!/usr/bin/python
from amazonproduct import API
from amazonproduct import AWSError
#from sys import argv

api = API(locale='us')

def searchByKeyword(keyword, minPrice = -1, maxPrice = -1):
  items = None
  try:
    if (minPrice == -1):
      items = api.item_search('All', Keywords=keyword, ResponseGroup='Medium')
    else:
      items = api.item_search('All', Keywords=keyword, MinimumPrice=minPrice, MaximumPrice=maxPrice, ResponseGroup='Medium')
  except AWSError as e:
    print 'Amazon complained about request'
    print e.code
    print e.msg
    return None
  results = []
  count = 0
  for result in items:
    obj = {}
    obj['id'] = result.ASIN
    obj['name'] = result.ItemAttributes.Title
    obj['url'] = result.DetailPageURL
    try:
      obj['price'] = result.ItemAttributes.ListPrice.FormattedPrice
    except:
      obj['price'] = None
    obj['imageurl'] = result.SmallImage.URL
    obj['imageheight'] = result.SmallImage.Height
    obj['imagewidth'] = result.SmallImage.Width
    results.append(obj)
    count += 1
    if count == 3:
        break
  return results

def searchById(id, similar = False):
    items = None
    try:
        items = api.item_lookup(ItemId=id, ResponseGroup='Medium,Similarities')
    except AWSError as e:
        print 'Amazon complained about request'
        print e.code
        print e.msg
    results = []
    result = items.Items.Item
    obj = {}
    obj['id'] = id
    obj['name'] = result.ItemAttributes.Title
    obj['url'] = result.DetailPageURL
    try:
      obj['price'] = result.ItemAttributes.ListPrice.FormattedPrice
    except:
      obj['price'] = None
    obj['imageurl'] = result.SmallImage.URL
    obj['imageheight'] = result.SmallImage.Height
    obj['imagewidth'] = result.SmallImage.Width
    results.append(obj)
    if not similar:
        similar_products = result.SimilarProducts
        count = 0
        for prod in similar_products:
            obj = {}
            new_id = prod.SimilarProduct.ASIN
            results.append(searchById(new_id, True))
            count += 1
            if count == 2:
                break
    return results
