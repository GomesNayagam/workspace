package week2
//curry
object exercise2 {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(72); 
	
	def cube(x: Int) = x * x * x;System.out.println("""cube: (x: Int)Int""");$skip(175); 
	
	def sum(f: Int => Int)(a:Int, b:Int)(c:Int): Int = {

	def sumF(x:Int, y:Int): Int = {
		f(x) + f(y)
	}
	
	def sumC(x:Int): Int = {
	
	x+1
	
	}
	
	sumC( sumF(a,b)+c )
	
	};System.out.println("""sum: (f: Int => Int)(a: Int, b: Int)(c: Int)Int""");$skip(57); 

//below is called currying

  def s = sum(cube)(1,2)(3);System.out.println("""s: => Int""");$skip(7); val res$0 = 
  
  s;System.out.println("""res0: Int = """ + $show(res$0))}

}
