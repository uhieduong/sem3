package w2;

/**
 * Represents a Full-Time Student who can optionally join one project.
 */
public class FullTimeStudent extends Student {
    private Project joinedProject;

    public FullTimeStudent() {
        super();
    }

    public FullTimeStudent(String id, String name, String major) {
        super(id, name, major);
    }

    /**
     * Joins a project if the student is not currently in any project.
     *
     * @param project the project to join
     * @return true if successfully joined, false otherwise
     */
    public boolean joinProject(Project project) {
        if (project != null && this.joinedProject == null) {
            if (project.addMember(this)) {
                this.joinedProject = project;
                return true;
            }
        }
        return false;
    }

    public Project getJoinedProject() {
        return joinedProject;
    }

    @Override
    public String toString() {
        return String.format("FullTimeStudent [ID: %s, Name: %s, Major: %s]", getId(), getName(), getMajor());
    }
}

