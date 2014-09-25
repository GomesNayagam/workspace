class Companion {
  def hello() { println("Hello (class)") } // [1]
}
object Companion {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(139); 
  def hallo() { println("Hallo (object)") };System.out.println("""hallo: ()Unit""");$skip(51);  // [2]
  def hello() { println("Hello (object)") } // [3];System.out.println("""hello: ()Unit""")}
}

// File TestCompanion.java
public class TestCompanion {
    public static void main(String[] args) {
        new Companion().hello(); // [1]
        Companion.hallo();  // [2] (static)
        Companion$.MODULE$.hello();  // [3] (hidden static)
    }
}
