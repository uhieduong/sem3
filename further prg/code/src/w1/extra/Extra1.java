package w1.extra;

import java.util.Arrays;
import java.util.Scanner;

public class Extra1 {

    /*
       Write a program that get three integers from the user and then prints them out in ascending order.
     */
    public static void exercise1(){
        int [] arr = new int[3];
        System.out.println("Please type three integer:");
        // Get 3 input from users and store in an array
        Scanner sc = new Scanner(System.in);
        for(int i = 0; i < 3; i++){
            arr[i] = sc.nextInt();
        }
        // Display the inputted values
        System.out.println("The input array: ");
        for(int i = 0; i < 3; i++){
            System.out.print(arr[i] + " ");
        }
        // Sort the array using Java Collections Framework
        Arrays.sort(arr);
        System.out.println();
        // Display the sorted array
        System.out.println("Ascending order: ");
        for(int i = 0; i < 3; i++){
            System.out.print(arr[i] + " ");
        }

    }

    /*
       Write a program that repeatedly prompts the user to enter a positive integer and checks
       whether the number is divisible by both 5 and 6, or neither of them, or just one of them.
       The program ends when the user enters a negative integer or zero.
     */
    public static void exercise2(){
        int num;
        Scanner sc = new Scanner(System.in);
        // Keep prompting until when the user enters a negative integer or zero
        while (true) {
            System.out.print("Enter a positive integer: ");
            num = sc.nextInt();
            if (num <= 0) break; // End the program
            // Check whether the number is divisible by both first. Why? (You should be able to answer this)
            if (num % 5 == 0 && num % 6 == 0){
                System.out.println(num + " is divisible by both 5 and 6");
            }
            else if (num % 5 == 0 || num % 6 == 0){
                System.out.println(num + " is divisible by either 5 or 6, but not both");
            }
            else {
                System.out.println(num + " is neither divisible by 5 or 6");
            }
        }
        System.out.println("Goodbye!");
    }

    /*
       Write a program that displays all the numbers from 100 to 200, ten numbers per line,
       that are divisible by 5 or 6, but not both. Numbers are separated by exactly one space.
     */
    public static void exercise3(){
        // Use a counter to keep track the numbers in one line
        int count = 0;
        for (int i = 100; i < 200; i++){
            // Skip the number that is divisible by both 5 and 6
            if (i % 5 == 0 && i % 6 == 0){
                continue;
            }
            if (i % 5 == 0 || i % 6 == 0){
                System.out.print(i + " ");
                count++;
            }
            // Move to the next line when 10 numbers is already printed, and reset the counter
            if (count == 10 ){
                System.out.println();
                count = 0;
            }
        }
    }

    /*
       Write a program that uses a suitable loop to display a conversion table nicely,
       knowing that 1 mile is 1.609 kilometers.
     */
    public static void exercise4(){
        System.out.println("Miles \t\t Kilometers");
        for(int i = 1; i < 10; i++){
            double kilometer = i * 1.61;
            System.out.printf(" %n %d \t\t\t %.2f", i, kilometer);
        }

        System.out.println();

        System.out.println("Kilometers \t Miles");
        for(int j = 20; j <= 65; j = j + 5){
            double miles = j * 0.62137119;
            System.out.printf(" %n %d \t\t %.2f", j, miles);
        }
    }

    /*
       Write a program that prompts the user to enter an integer from 1 to 15 and displays a pyramid.
     */
    public static void exercise5(){
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the number of lines (between 1-15): ");
        int lines = sc.nextInt();
        // Input validation
        while (lines < 1 || lines > 15) {
            System.out.print("Enter the number of lines (between 1-15): ");
            lines = sc.nextInt();
        }

        System.out.println();

        for (int i = 1; i <= lines; i++){ // Main loop to keep track the lines
            for (int j = 1; j <= (lines - i) * 2; j++){ // Print out the spaces
                System.out.print(" ");
            }
            for (int k = i; k >= 1; k--){ // Print out the left half
                System.out.print(" " + k);
            }
            for (int l = 2; l <= i; l++){ // Print out the right half
                System.out.print(" " + l);
            }
            System.out.println();
        }
    }

    /*
       Write a program that prompts the user to enter the center coordinates and
       radius-es of two circles and determines whether the second circle is inside
       the first or overlaps with the first.
     */
    public static void exercise6(){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter circle 1's coordinates and radius: ");
        double x1 , y1 , rad1;
        x1 = scanner.nextDouble();
        y1 = scanner.nextDouble();
        rad1 = scanner.nextDouble();

        System.out.println("Enter circle 2's coordinates and radius:");
        double x2 , y2 , rad2;
        x2 = scanner.nextDouble();
        y2 = scanner.nextDouble();
        rad2 = scanner.nextDouble();

        double distance = Math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
        if (distance <= Math.abs(rad1 - rad2)){
            System.out.println("Circle 2 is inside circle 1");
        }
        else if (distance <= rad1 + rad2){
            System.out.println("Circle 2 overlaps circle 1");
        }
        else {
            System.out.println("Outside");
        }
    }

    public static void main(String args[]){
//        exercise1();
//        exercise2();
//        exercise3();
//        exercise4();
//        exercise5();
        exercise6();
    }
}
