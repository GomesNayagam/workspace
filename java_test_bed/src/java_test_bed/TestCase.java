package java_test_bed;

import scala.collection.immutable.*;


public class TestCase {

    public static void main(String[] args) {
        HashSet<String> set2 = new HashSet<String>();

        HashSet<String> set4 = set2.$plus("test");

        System.out.println(set2.size());
        System.out.println(set4.size());


    }
}