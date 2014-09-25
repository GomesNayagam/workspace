package week1
object session {

	def sqrt(x: Double) = {

  def abs(y: Double) = if (y < 0) -y else y

	def sqrtIter(guess: Double): Double =
		if (isGoodEnough(guess)) guess
		else sqrtIter(improve(guess))
		
	def isGoodEnough(guess: Double): Boolean =
		abs(guess * guess- x) / x < 0.001
		
	def improve(guess: Double): Double =
		(guess + x / guess) / 2

	sqrtIter(1)

  }                                               //> sqrt: (x: Double)Double
  
  sqrt(25)                                        //> res0: Double = 5.000023178253949

}