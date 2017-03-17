package com.amazon.advertising.api.access;

import java.util.*;
import java.xml.parsers.*;
import org.w3c.dom.Document;
import org.w3c.dom.Node;

public class AmazonAccess{
    private static final String AWS_ACCESS_KEY_ID = "";
    private static final String AWS_SECRET_KEY = "";
    private static final String ENDPOINT = "webservices.amazon.com";

    public static void search(Set<String> terms){
        AmazonAccess.search(terms, 0.0, Double.MAX_VALUE);
    }

    public static List<String> search(Set<String> terms, double lowPrice, double highPrice){
        SignedRequestsHelper helper;
        try{
          helper = SignedRequestsHelper.getInstance(ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY);
        }
        catch(Exception e){
          e.printStackTrace();
          return;
        }

        String requestUrl = null;

        Map<String, String> params = new HashMap<String, String>();
        List<String> output = new ArrayList<String>();

        String minPrice = "";
        String maxPrice = "";
        minPrice += lowPrice;
        maxPrice += highPrice;
        int minDec = minPrice.indexOf(".");
        int maxDec = maxPrice.indexOf(".");
        if(minDec != -1){
          minPrice = minPrice.substring(0, minDec) + minPrice.substring(minDec + 1, minPrice.length());
        }
        if(maxDec != -1){
          maxPrice = maxPrice.substring(0, maxDec) + maxPrice.substring(maxDec + 1, maxPrice.length());
        }

        params.put("Service", "AWSECommerceService");
        params.put("Operation", "ItemSearch");
        params.put("AWSAccessKeyID", "");
        params.put("AssociateTag", "");
        params.put("SearchIndex", "All");
        params.put("ResponseGroup", "Images,ItemAttributes,Offers");
        params.put("MinimumPrice", minPrice);
        params.put("MaximumPrice", maxPrice);

        for(String keyword : terms){
          params.remove("Keywords");
          params.put("Keywords", keyword);

          requestUrl = helper.sign(params);
          output.add(requestUrl);
        }
        return output;
    }
}