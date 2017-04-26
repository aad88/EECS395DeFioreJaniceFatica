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
      items = api.item_search('All', Keywords=keyword, MinimumPrice=minPrice, MaximumPrice = maxPrice, ResponseGroup='Medium')
  except AWSError as e:
    print 'Amazon complained about request'
    print e.code
    print e.msg
    return None
  results = []
  for result in items:
    obj = {}
    obj['Name'] = result.ItemAttributes.Title
    obj['URL'] = result.DetailPageURL
    obj['Price'] = result.ItemAttributes.ListPrice.FormattedPrice
    obj['ImageURL'] = result.SmallImage.URL
    obj['ImageHeight'] = result.SmallImage.Height
    obj['ImageWidth'] = result.SmallImage.Width
    results.append(obj)
  return results

def searchById(id):
  items = None
  try:
    items = api.item_search(id, ResponseGroup='Medium')
  except AWSError as e:
    print 'Amazon complained about request'
    print e.code
    print e.msg
  results = []
  for result in items:
    obj = {}
    obj['Name'] = result.ItemAttributes.Title
    obj['URL'] = result.DetailPageURL
    obj['Price'] = result.ItemAttributes.ListPrice.FormattedPrice
    obj['ImageURL'] = result.SmallImage.URL
    obj['ImageHeight'] = result.SmallImage.Height
    obj['ImageWidth'] = result.SmallImage.Width
    results.append(obj)
  return results
