import java.util.ArrayList;
import java.util.Scanner;

public class ProblemA {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int superN = sc.nextInt();
		while (superN > 0) {
			int cases = sc.nextInt();
			long total = 0;
			while (cases > 0) {
				ArrayList<ArrayList<Integer>> prizes = new ArrayList<ArrayList<Integer>>();
				int n = sc.nextInt();
				int m = sc.nextInt();
				while (n > 0) {

					int k = sc.nextInt();
					ArrayList<Integer> stickers = new ArrayList<Integer>();
					while (k > 0) {
						stickers.add(new Integer(sc.nextInt()));
						k--;
					}
					// Also add the cash value for the prize
					stickers.add(new Integer(sc.nextInt()));
					prizes.add(stickers);

					n--;
				}
				ArrayList<Integer> our_stickers = new ArrayList<Integer>();
				while (m > 0) {
					our_stickers.add(new Integer(sc.nextInt()));
					m--;
				}
				if (our_stickers.size() > 0) {
					for (ArrayList<Integer> prize : prizes) {
						int num_possible = our_stickers.get(prize.get(0) - 1);
						for (int i = 1; i < prize.size() - 1; i++) {
							if (our_stickers.get(prize.get(i) - 1) < num_possible) {
								num_possible = our_stickers
										.get(prize.get(i) - 1);
							}
						}
						total += num_possible * prize.get(prize.size() - 1);
					}
				}
				System.out.println(total);
				total = 0;
				cases--;
			}
			superN--;
		}
		
	}
}
