import java.util.Scanner;

public class ReadInput {
   public static void main(String[] args) {
      // Prints whatever was in the input file
       Scanner sc = new Scanner(System.in);
       while(sc.hasNext()){
	   System.out.println(sc.nextLine());
       }
   }
}
