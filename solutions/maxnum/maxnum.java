import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int len = Integer.parseInt(scan.nextLine());
        int max_ind = 0;
        String[] nums = new String[len];
        int[] int_nums = new int[len];

        nums = scan.nextLine().split("\\s+");
        for (int i = 0; i < len; i++) {
            int_nums[i] = Integer.parseInt(nums[i]);
        }
        for (int i = 0; i < len; i++) {
            if (int_nums[i] > int_nums[max_ind]) max_ind = i;
        }
        System.out.println(int_nums[max_ind]);
    }
}
