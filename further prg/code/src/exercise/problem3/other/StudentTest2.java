package exercise.problem3.other;

// Must import Student because it resides in a different package (exercise.problem3)
import exercise.problem3.Student;

/**
 * Tests the Student class from a DIFFERENT package (exercise.problem3.other).
 */
public class StudentTest2 {
    public static void main(String[] args) {
        System.out.println("=== StudentTest2 (Different Package: exercise.problem3.other) ===");

        // 1. Instantiating a Student object across package boundaries
        Student s3 = new Student(201, "Charlie Brown", "Data Science");

        // 2. Accessing attributes via public getter methods
        System.out.println("Initial Student 3 Details:");
        System.out.println("ID: " + s3.getId());
        System.out.println("Name: " + s3.getName());
        System.out.println("Major: " + s3.getMajor());

        // 3. Modifying attributes via public setter methods
        System.out.println("\nModifying attributes using setters...");
        s3.setName("Charlie B. Brown");
        s3.setMajor("Cybersecurity");

        // 4. Accessing updated attributes
        System.out.println("Updated Student 3 Details:");
        System.out.println(s3);
    }
}

