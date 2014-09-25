package week3


object rationals {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(56); 

var s = Set(1, 2, 3);System.out.println("""s  : scala.collection.immutable.Set[Int] = """ + $show(s ));$skip(14); 
var t = s + 4;System.out.println("""t  : scala.collection.immutable.Set[Int] = """ + $show(t ));$skip(14); 
var x = s | t;System.out.println("""x  : scala.collection.immutable.Set[Int] = """ + $show(x ))}


}
