#!/usr/bin/python
from amazonproduct import API
from amazonproduct import AWSError
from multiprocessing import Semaphore
from time import sleep
#from sys import argv

api = API(locale='us')
#last_time = 0
sem = Semaphore()
# this semaphore is used due to Amazon's throttling. We are allowed exactly one Amazon query per second, so this is used to prevent sending queries too quickly

#takes in a string keyword, and has the potential for a minimum and maximum price requirement
#returns a list of dictionaries, where each dictionary represents a product
def searchByKeyword(keyword, minPrice = -1, maxPrice = -1):
    items = None
    try:
        sem.acquire()
        sleep(1)
        if (minPrice == -1):
            items = api.item_search('All', Keywords=keyword, ResponseGroup='Medium')
        else:
            items = api.item_search('All', Keywords=keyword, MinimumPrice=minPrice, MaximumPrice=maxPrice, ResponseGroup='Medium')
    except AWSError as e:
        sem.release()
        print 'Amazon complained about request'
        print e.code
        print e.msg
        return None
    sem.release()
    results = []
    count = 0
    for result in items:
        #create temp dictionary to add to results list
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
        # limit to three results
        if count == 3:
            break
    return results

#similar should always be false when method is called from an outside source, used to get similar products by id in order to reuse code
#takes in a string id that is a product's ASIN (Amazon ID)
#returns a list of dictionaries, where each dictionary represents one product
def searchById(id, similar = False):
    items = None
    sem.acquire()
    sleep(1)
    try:
        items = api.item_lookup(ItemId=id, ResponseGroup='Medium,Similarities')
    except AWSError as e:
        sem.release()
        print 'Amazon complained about request'
        print e.code
        print e.msg
        return None
    sem.release()
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
    #get two similar products to return along with the original
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
