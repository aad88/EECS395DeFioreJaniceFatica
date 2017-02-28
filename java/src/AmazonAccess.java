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

    public static void search(Set<String> terms, double lowPrice, double highPrice){
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

        params.put("Service", "AWSECommerceService");
        params.put("Operation", "ItemSearch");
        params.put("AWSAccessKeyID", "");
        params.put("AssociateTag", "");
        params.put("SearchIndex", "All");
        params.put("ResponseGroup", "Images,ItemAttributes,Offers");

        for(String keyword : terms){
          params.remove("Keywords");
          params.put("Keywords", keyword);

          requestUrl = helper.sign(params);
          //use url to access amazon

          //process returned xml or html
        }
    }
}