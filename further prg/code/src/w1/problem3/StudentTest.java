package w1.problem3;

/**
 * @author COSC2440 Teaching Team
 * @version 1.0
 */

public class StudentTest {
    public static void main(String[] args) {
        /*
          Create Student objects and access their attributes
         */
        Student stu1 = new Student("s123", "John Smith", "IT");
        System.out.println(stu1.getStudentId() + " "  + stu1.getFullName() + " " + stu1.getMajor());

        Student stu2 = new Student();
        stu2.setStudentId("s345");
        stu2.setFullName("Taylor Swift");
        stu2.setMajor("SE");
        // another way to print data
        System.out.printf("%s %s %s\n", stu2.getStudentId(), stu2.getFullName(), stu2.getMajor());
    }
}
