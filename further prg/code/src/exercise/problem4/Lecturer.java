package exercise.problem4;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Represents a Lecturer at the university.
 * Lecturers are responsible for teaching and research.
 * A lecturer can lead at most one research project at a time,
 * but can join multiple research projects simultaneously as a member.
 */
public class Lecturer {
    private String employeeId;
    private String fullName;
    private String rank;

    /**
     * The research project currently led by this lecturer (at most one).
     */
    private Project leadingProject;

    /**
     * The list of research projects this lecturer has joined as a member.
     */
    private final List<Project> joinedProjects;

    /**
     * Default constructor.
     */
    public Lecturer() {
        this.joinedProjects = new ArrayList<>();
    }

    /**
     * Constructs a Lecturer with the specified employee ID, full name, and academic rank.
     *
     * @param employeeId the unique identifier of the lecturer
     * @param fullName   the full name of the lecturer
     * @param rank       the academic rank (e.g., Professor, Senior Lecturer, Lecturer)
     */
    public Lecturer(String employeeId, String fullName, String rank) {
        this.employeeId = employeeId;
        this.fullName = fullName;
        this.rank = rank;
        this.joinedProjects = new ArrayList<>();
    }

    /**
     * Attempts to lead the specified project.
     * <p>
     * A lecturer can lead at most one project at a time. Therefore, this method
     * will return {@code false} if the lecturer is already leading another project
     * or if the specified project already has a different leader.
     * </p>
     *
     * @param p the project to lead
     * @return {@code true} if this lecturer successfully leads the project; {@code false} otherwise
     */
    public boolean leadProject(Project p) {
        if (p == null) {
            return false;
        }

        // A lecturer can lead at most one project at a time
        if (this.leadingProject != null && this.leadingProject != p) {
            return false;
        }

        // The project cannot already have another leader
        if (p.getLeader() != null && p.getLeader() != this) {
            return false;
        }

        this.leadingProject = p;
        if (p.getLeader() != this) {
            p.setLeader(this);
        }
        return true;
    }

    /**
     * Joins the specified project as a regular member.
     * <p>
     * A lecturer can join many projects at the same time.
     * </p>
     *
     * @param p the project to join
     * @return {@code true} if the lecturer joined successfully; {@code false} if project is null
     */
    public boolean joinProject(Project p) {
        if (p == null) {
            return false;
        }

        if (!joinedProjects.contains(p)) {
            joinedProjects.add(p);
        }

        if (!p.getMembers().contains(this)) {
            p.addMember(this);
        }

        return true;
    }

    /**
     * Returns the employee ID.
     *
     * @return the employee ID
     */
    public String getEmployeeId() {
        return employeeId;
    }

    /**
     * Sets the employee ID.
     *
     * @param employeeId the employee ID to set
     */
    public void setEmployeeId(String employeeId) {
        this.employeeId = employeeId;
    }

    /**
     * Returns the full name of the lecturer.
     *
     * @return the full name
     */
    public String getFullName() {
        return fullName;
    }

    /**
     * Sets the full name of the lecturer.
     *
     * @param fullName the full name to set
     */
    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    /**
     * Returns the academic rank of the lecturer.
     *
     * @return the academic rank
     */
    public String getRank() {
        return rank;
    }

    /**
     * Sets the academic rank of the lecturer.
     *
     * @param rank the rank to set
     */
    public void setRank(String rank) {
        this.rank = rank;
    }

    /**
     * Returns the project currently led by this lecturer, or {@code null} if none.
     *
     * @return the led project
     */
    public Project getLeadingProject() {
        return leadingProject;
    }

    /**
     * Returns an unmodifiable list of projects this lecturer has joined as a member.
     *
     * @return list of joined projects
     */
    public List<Project> getJoinedProjects() {
        return Collections.unmodifiableList(joinedProjects);
    }

    @Override
    public String toString() {
        return "Lecturer [ID: " + employeeId + ", Name: " + fullName + ", Rank: " + rank + "]";
    }
}

