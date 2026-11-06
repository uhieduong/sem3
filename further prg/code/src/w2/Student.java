package w2;

/**
 * Abstract base class representing a Student.
 */
public abstract class Student {
    private String id;
    private String name;
    private String major;

    public Student() {
        this("Default", "Default", "Default");
    }

    public Student(String id, String name, String major) {
        this.id = id;
        this.name = name;
        this.major = major;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
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
        return String.format("Student [ID: %s, Name: %s, Major: %s]", id, name, major);
    }
}

