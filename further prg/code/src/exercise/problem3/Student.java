package exercise.problem3;

/**
 * Represents a Student entity.
 * Demonstrates proper OOP encapsulation using private attributes
 * and public accessor/mutator methods.
 */
public class Student {
    // Attributes are declared 'private' to ensure encapsulation (data hiding).
    // They cannot be accessed or modified directly from outside this class.
    private int id;
    private String name;
    private String major;

    // Default constructor
    public Student() {}

    // Parameterized constructor
    public Student(int id, String name, String major) {
        this.id = id;
        this.name = name;
        this.major = major;
    }

    // Public getters and setters provide controlled access from any package
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getMajor() {
        return major;
    }

    public void setMajor(String major) {
        this.major = major;
    }

    @Override
    public String toString() {
        return "Student{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", major='" + major + '\'' +
                '}';
    }
}

