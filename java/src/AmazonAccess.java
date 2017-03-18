//package com.amazon.advertising.api.access;

import java.util.*;
import javax.xml.parsers.*;
import org.w3c.dom.Document;
import org.w3c.dom.Node;

public class AmazonAccess{
    private static final String AWS_ACCESS_KEY_ID = "";
    private static final String AWS_SECRET_KEY = "";
    private static final String ENDPOINT = "webservices.amazon.com";

    public static List<String> search(Set<String> terms){
        return AmazonAccess.search(terms, -1.0, -1.0);
    }

    public static List<String> search(Set<String> terms, double lowPrice, double highPrice){
        SignedRequestsHelper helper;
        try{
          helper = SignedRequestsHelper.getInstance(ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY);
        }
        catch(Exception e){
          e.printStackTrace();
          return null;
        }

        String requestUrl = null;

        Map<String, String> params = new HashMap<String, String>();
        List<String> output = new ArrayList<String>();
        
        if(highPrice < lowPrice && highPrice != -1.0){
          lowPrice = -1.0;
        }

        params.put("Service", "AWSECommerceService");
        params.put("Operation", "ItemSearch");
        params.put("AWSAccessKeyID", "");
        params.put("AssociateTag", "");
        params.put("SearchIndex", "All");
        params.put("ResponseGroup", "Images,ItemAttributes,Offers");
        if(lowPrice >= 0){
          String minPrice = "";
          minPrice += lowPrice;
          int minDec = minPrice.indexOf(".");
          if(minDec != -1){
            minPrice = minPrice.substring(0, minDec) + minPrice.substring(minDec + 1, minPrice.length());
          }
          params.put("MinimumPrice", minPrice);
        }
        if(highPrice > 0){
          String maxPrice = "";
          maxPrice += highPrice;
          int maxDec = maxPrice.indexOf(".");
          if(maxDec != -1){
            maxPrice = maxPrice.substring(0, maxDec) + maxPrice.substring(maxDec + 1, maxPrice.length());
          }
          params.put("MaximumPrice", maxPrice);
        }
        

        for(String keyword : terms){
          params.remove("Keywords");
          params.put("Keywords", keyword);

          requestUrl = helper.sign(params);
          output.add(requestUrl);
        }
        return output;
    }
}