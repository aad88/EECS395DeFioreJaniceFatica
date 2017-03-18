
import java.util.*;
public class AmazonTest{
  public static void main(String[] args){
    Set<String> terms = new HashSet<String>();
    terms.add("football");
    terms.add("pokemon ruby");
    terms.add("soccer");

    List<String> noPriceUrls = AmazonAccess.search(terms);
    List<String> priceUrls = AmazonAccess.search(terms, 0.00, 30.00);

    for(String url : noPriceUrls){
      System.out.println(url);
    }
    System.out.println();
    for(String url : priceUrls){
      System.out.println(url);
    }
  }
}