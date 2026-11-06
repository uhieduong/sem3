package w2;

import java.util.ArrayList;

/**
 * Represents a Lecturer who can lead at most one project and join multiple projects.
 */
public class Lecturer {
    private String id;
    private String name;
    private String rank;
    private Project projectLed;
    private ArrayList<Project> joinedProject;

    public Lecturer() {
        this("Default", "Default", "Default");
    }

    public Lecturer(String id, String name, String rank) {
        this.id = id;
        this.name = name;
        this.rank = rank;
        this.joinedProject = new ArrayList<>();
    }

    /**
     * Leads the specified project if the lecturer is not already leading a project
     * and the project has no current leader.
     *
     * @param p the project to lead
     * @return true if successfully assigned, false otherwise
     */
    public boolean leadProject(Project p) {
        if (p != null && !isLeading() && p.getLeader() == null) {
            this.projectLed = p;
            p.assignLeader(this);
            return true;
        }
        return false;
    }

    /**
     * Joins the specified project as a member.
     *
     * @param p the project to join
     * @return true if successfully joined, false otherwise
     */
    public boolean joinProject(Project p) {
        if (p != null && !joinedProject.contains(p) && p.addMember(this)) {
            this.joinedProject.add(p);
            return true;
        }
        return false;
    }

    /**
     * Checks if this lecturer is currently leading any project.
     *
     * @return true if leading a project, false otherwise
     */
    public boolean isLeading() {
        return projectLed != null;
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

    public String getRank() {
        return rank;
    }

    public void setRank(String rank) {
        this.rank = rank;
    }

    public Project getProjectLed() {
        return projectLed;
    }

    public ArrayList<Project> getJoinedProject() {
        return joinedProject;
    }

    @Override
    public String toString() {
        return String.format("Lecturer [ID: %s, Name: %s, Rank: %s]", id, name, rank);
    }
}

