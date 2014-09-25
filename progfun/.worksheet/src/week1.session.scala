package week1
object session {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(375); 

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

  };System.out.println("""sqrt: (x: Double)Double""");$skip(14); val res$0 = 
  
  sqrt(25);System.out.println("""res0: Double = """ + $show(res$0))}

}
