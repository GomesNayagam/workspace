package week2
//curry
object exercise2 {
	
	def cube(x: Int) = x * x * x              //> cube: (x: Int)Int
	
	def sum(f: Int => Int)(a:Int, b:Int)(c:Int): Int = {

	def sumF(x:Int, y:Int): Int = {
		f(x) + f(y)
	}
	
	def sumC(x:Int): Int = {
	
	x+1
	
	}
	
	sumC( sumF(a,b)+c )
	
	}                                         //> sum: (f: Int => Int)(a: Int, b: Int)(c: Int)Int

//below is called currying

  def s = sum(cube)(1,2)(3)                       //> s: => Int
  
  s                                               //> res0: Int = 13

}