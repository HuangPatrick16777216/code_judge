import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String[] input = scan.nextLine().split("\\s+");
        float pos, target, step, range;
        int steps = 0;

        pos = Integer.parseInt(input[0]);
        target = Integer.parseInt(input[1]);
        step = Integer.parseInt(input[2]);
        range = Integer.parseInt(input[3]);

        while (true) {
            float dist = pos-target;
            if (dist < 0) dist *= -1;
            if (dist <= range) {
                System.out.println(steps);
                break;
            }
            if (pos < target) {
                while (pos < target-range) {
                    pos += step;
                    steps++;
                }
            } else {
                while (pos > target+range) {
                    pos -= step;
                    steps++;
                }
            }
            step /= 2;
        }
    }
}
