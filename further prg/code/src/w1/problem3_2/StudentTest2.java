package w1.problem3_2;

import w1.problem3.Student;

/**
 * @author COSC2440 Teaching Team
 * @version 1.0
 */

public class StudentTest2 {
    public static void main(String[] args) {
        /*
          Create Student objects and access their attributes
         */
        Student stu1 = new Student("s123", "John Smith", "IT");
        /*
          To access Student class in this package,
          either use its fully-qualified name (name with the prefix package name),
          or "import" it first, then use it as it is in the same package
         */
        // w1.problem3.Student stu = new w1.problem3.Student();
        System.out.println(stu1.getStudentId() + " "  + stu1.getFullName() + " " + stu1.getMajor());

        Student stu2 = new Student();
        /*
          From Java 10, if the type of a variable can be determined automatically,
          you can use "var" to declare its type. For example
          var stu = new Student();
         */
        stu2.setStudentId("s345");
        stu2.setFullName("Taylor Swift");
        stu2.setMajor("SE");
        // another way to print data
        System.out.printf("%s %s %s\n", stu2.getStudentId(), stu2.getFullName(), stu2.getMajor());
    }
}

