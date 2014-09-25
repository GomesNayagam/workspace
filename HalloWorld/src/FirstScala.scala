object FirstScala {

 def capitalizeAll(args: String*) = {
  args.map { arg =>
    arg.capitalize
  }
}
    
  def main(args: Array[String]): Unit = {
    
    val calc = new Calculator("HP")
    
    println("Test")
    
      println(calc.color)
      println(calc.add(2,3))
  }
  
}

trait Ops{
  val add: String
  val sub: String
}

trait SciOps{
  val div: String
  val mul: String
}

class Calculator (brand: String) extends Ops with SciOps {
    
  val color:String = if (brand == "TI"){"blue"}else if(brand == "HP"){"black"}else{"white"}
  
  val add = "+"
  val sub = "-"
  val div = "/"
  val mul = "*"
    
  
  def add(m:Int,n:Int): Int = m+n
}

object addone extends Function1[Int, Int] {
  def apply(m: Int): Int = m+1
}

//The above is called function as objects,  Function1 takes one argument and return one, it is like .net Action<T>, so you can call it as addone(2) thats it. this applicable for Class also.
// so you would call it like val a = new Addone() and a(1)
//extends Function1[Int, Int] is extends (Int => Int) can be written liek this also, since it is anonymous 

object addone1 extends (Int => Int) {
 def apply(m: Int): Int = m+1
}









