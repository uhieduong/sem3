package exercise.problem4;

import exercise.problem3.Student;

/**
 * Represents a Full-Time Student at the university.
 * According to specifications, only full-time students can optionally
 * join one research project as a member.
 */
public class FullTimeStudent extends Student {
    private Project project;

    /**
     * Default constructor.
     */
    public FullTimeStudent() {
        super();
    }

    /**
     * Constructs a FullTimeStudent with the specified ID, name, and major.
     *
     * @param id    the student ID
     * @param name  the student's full name
     * @param major the student's major
     */
    public FullTimeStudent(int id, String name, String major) {
        super(id, name, major);
    }

    /**
     * Optionally joins one research project.
     *
     * @param p the project to join
     * @return {@code true} if successfully joined; {@code false} if already in a project or p is null
     */
    public boolean joinProject(Project p) {
        if (p == null || this.project != null) {
            return false;
        }
        this.project = p;
        p.addMember(this);
        return true;
    }

    /**
     * Leaves the currently joined research project.
     */
    public void leaveProject() {
        this.project = null;
    }

    /**
     * Returns the project currently joined by this full-time student.
     *
     * @return the project, or {@code null} if none
     */
    public Project getProject() {
        return project;
    }

    @Override
    public String toString() {
        return "FullTimeStudent [ID: " + getId() + ", Name: " + getName() + ", Major: " + getMajor() + "]";
    }
}

