package w1.extra;

import java.util.*;

public class Extra2 {
    /*
       Write a program that prompts the user to enter a year
       and a string of three characters for a month name (with the first letter in uppercase)
       then displays the number of days in the month.
       If the user enters an invalid value for year or month, print out a helpful error message.
     */
    public static void q1(){
        int day = 0;
        Scanner input = new Scanner(System.in);

        System.out.print("Enter a year: ");
        int year = input.nextInt();
        input.nextLine();

        System.out.print("Enter a month: ");
        String month = input.nextLine();

        if (year < 0)
            System.out.println("\nInvalid year.");

        switch (month) {
            case "Jan":
            case "Mar":
            case "May":
            case "Jul":
            case "Aug":
            case "Oct":
            case "Dec":
                day = 31;
                break;
            case "Apr":
            case "Jun":
            case "Sep":
            case "Nov":
                day = 30;
                break;
            case "Feb":
                if (isLeapYear(year))
                    day = 29;
                else
                    day = 28;
                break;
            default:
                System.out.println("\nInvalid month.");
        }

        if (year > 0 && day != 0)
            System.out.printf("\n%s %d has %d days.\n", month, year, day);
    }

    public static boolean isLeapYear(int year) {
        if (year % 400 == 0)
            return true;

        if (year % 100 == 0)
            return false;

        if (year % 4 == 0)
            return true;

        return false;
    }

    /*
       Write a program that prompts the user to enter three cities and display them in ascending order.
     */
    public static void q2(){
        Scanner input = new Scanner(System.in);
        ArrayList<String> cities = new ArrayList<>();
        //LinkedList<String> cities = new LinkedList<>();

        System.out.print("Enter the first city: ");
        cities.add(input.nextLine());

        System.out.print("Enter the second city: ");
        cities.add(input.nextLine());

        System.out.print("Enter the third city: ");
        cities.add(input.nextLine());

        Collections.sort(cities);

        System.out.print("\nThe three cities in alphabetical order are");
        for (String city : cities) {
            System.out.print(" " + city);
        }
        System.out.print(".\n");
    }

    /*
       Write a method that takes a string and returns its reverse.
       For example, if the given string is "Good day" then the method returns "yad dooG".
     */
    public static void q3() {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter a string: ");

        String s = input.nextLine(), reversedString = "";

        for (int i = s.length() - 1; i >= 0; --i)
            reversedString += s.charAt(i);

        System.out.println("Reverse string: " + reversedString);
    }

    /*
       A palindrome is a string that reads the same backward as forward when ignoring punctuations, blanks and case difference.
       For example, "madam", "Hannah", "Step on no pets", "Was it a car or a cat I saw?", "A man, a plan, a canal, Panama!" are all palindromes.
       Write a method that checks if a given string is a palindrome or not. Hint: Use the method in the last exercise.
     */
    public static void q4(String dummy){
        String stringToCheck = dummy;
        String palindromeString = "";
        // initialize a stack
        Stack<Character> stack = new Stack<Character>();
        // iterate over the string
        for (int i = 0; i < stringToCheck.length(); i++) {
            char character = stringToCheck.charAt(i);
            stack.push(character);
        }
        // iterate over the stack till it is empty
        while (!stack.isEmpty()) {
            // add the character at the top to a string
            palindromeString = palindromeString + stack.pop();
        }
        // compare original and reversed strings
        if (stringToCheck.equals(palindromeString)) {
            System.out.println("String is palindrome");
        } else {
            System.out.println("String is not palindrome");
        }
    }

    /*
       Write a program that determines if a list is already sorted in increasing order.
       The program should prompt the user to enter a list and displays whether the list is sorted in ascending order or not.
       Note that the first number in the input indicates the number of the elements in the list.
       The program exits when the first number is 0.
     */
    public static void q5(){
        Scanner input = new Scanner(System.in);

        System.out.print("Enter list: ");

        int length = input.nextInt();
        if (length > 0) {
            boolean isSorted = true;
            int currentNumber = input.nextInt();

            for (int i = 1; i < length; ++i) {
                int tempNumber = input.nextInt();

                if (currentNumber <= tempNumber) {
                    currentNumber = tempNumber;
                } else {
                    isSorted = false;
                    break;
                }
            }

            if (isSorted) {
                System.out.println("The list is already sorted.");
            } else {
                System.out.println("The list is not sorted.");
            }
        }
    }

    /*
       Write a program that generates 100 random integers between 0 and 9 then displays the count for each number.
     */
    public static void q6() {
        int min = 0;
        int max = 9;
        int range = max - min + 1;
        int[] numbers = new int[max + 1];

        for (int i = 0; i < 100; ++i) {
            int rand = (int) (Math.random() * range) + min;
            numbers[rand] += 1;
        }

        for (int i = min; i <= max; ++i) {
            if (numbers[i] > 0)
                System.out.println(i + ": " + numbers[i]);
        }
    }

    /*
       Write a program that reads an unspecified number of scores in one input
       and determines how many scores are above or equal to the average and how many scores are below the average.
     */
    public static void q7() {
        System.out.print("Enter scores: ");
        Scanner readLine = new Scanner(System.in);

        if (readLine.hasNextLine()) {
            String line = readLine.nextLine();
            Scanner input = new Scanner(line);

            ArrayList<Integer> numbers = new ArrayList<>();

            double average;
            double sum = 0;

            int length = 0;
            int numOfAbove = 0;
            int numOfBelow = 0;

            while (input.hasNextInt()) {
                int number = input.nextInt();
                numbers.add(number);
                sum += number;
                ++length;
            }

            average = sum / length;

            for (int number : numbers) {
                if (number >= average)
                    ++numOfAbove;
                else
                    ++numOfBelow;
            }

            System.out.println("\nAverage: " + average);
            System.out.println("Above: " + numOfAbove);
            System.out.println("Below: " + numOfBelow);
        }
    }


    /*
       Write a program that reads in ten integers between 1 and 100 then displays the number
       of  distinct  integers  and  the  distinct  integers  separated  by  exactly  one  space
       (i.e.,  if  a number appears multiple times, it is displayed only once)
     */
    public static void q8() {
        HashSet<Integer> set = new HashSet<Integer>();
        System.out.print("Enter ten numbers: ");
        Scanner input = new Scanner(System.in);
        for (int i = 0; i < 10; i++) {
            set.add(input.nextInt());
        }
        System.out.println("The number of distinct number is: " + set.size());
        System.out.print("The distinct numbers are: ");
        for (int number: set) {
            System.out.print(number + " ");
        }
    }

    /*
       Write a program that reads a list of integers between 1 and 100
       then counts the occurrences of each.
       Assume that the user always input value integers and the input always ends with 0.
       Note that if a number occurs more than one time, the plural word "times" is used in the output.
     */
    public static void q9() {
        System.out.print("Enter the integers between 1 and 100: ");
        Scanner input = new Scanner(System.in);
        int[] numbers = new int[101];

        while (input.hasNextInt()) {
            int number = input.nextInt();

            if (number == 0)
                break;

            numbers[number] += 1;
        }

        for (int i = 1; i < 101; ++i) {
            if (numbers[i] > 0) {
                System.out.print(i + " occurs " + numbers[i] + " time");

                if (numbers[i] > 1)
                    System.out.print("s");

                System.out.print("\n");
            }
        }
    }
    public static void main(String args[]) {
        //q1();
        //q2();
        //q3();
        //q4();
        //q5();
        //q6();
        //q7();
        //q8();
        q9();
    }
}
