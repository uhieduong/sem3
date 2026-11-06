package w1.problem3;

/**
 * @author COSC2440 Teaching Team
 * @version 1.0
 */

public class Student {
    private String studentId;
    private String fullName;
    private String major;

    public  Student() {
        this.studentId = "Default";
        this.fullName = "Default";
        this.major = "Default";
    }

    public Student(String studentId, String fullName, String major) {
        this.studentId = studentId;
        this.fullName = fullName;
        this.major = major;
    }

    // Getter and setter methods
    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getMajor() {
        return major;
    }

    public void setMajor(String major) {
        this.major = major;
    }
}
