package exercise.problem3;

/**
 * Tests the Student class from within the SAME package (exercise.problem3).
 */
public class StudentTest {
    public static void main(String[] args) {
        System.out.println("=== StudentTest (Same Package: exercise.problem3) ===");

        // 1. Instantiation using parameterized constructor
        Student s1 = new Student(101, "Alice Smith", "Computer Science");

        // 2. Instantiation using default constructor
        Student s2 = new Student();

        // 3. Modifying attributes via public setter methods
        s2.setId(102);
        s2.setName("Bob Johnson");
        s2.setMajor("Information Technology");

        // 4. Accessing attributes via public getter methods
        System.out.println("Student 1 Details:");
        System.out.println("ID: " + s1.getId());
        System.out.println("Name: " + s1.getName());
        System.out.println("Major: " + s1.getMajor());

        System.out.println("\nModifying Student 1's major...");
        s1.setMajor("Software Engineering");
        System.out.println("Updated Major: " + s1.getMajor());

        System.out.println("\nStudent 2 Details:");
        System.out.println(s2);
    }
}

