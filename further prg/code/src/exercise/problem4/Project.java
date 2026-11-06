package exercise.problem4;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Represents a Research Project at the university.
 * Each research project has a name, a budget, exactly one leader (who must be a lecturer),
 * and one or more members (each of whom can be a full-time student or a lecturer).
 */
public final class Project {
    private String name;
    private double budget;
    private Lecturer leader;
    private final List<Object> members;

    /**
     * Constructs a Project with the specified name and budget.
     *
     * @param name   the name of the project
     * @param budget the budget allocated to the project
     */
    public Project(String name, double budget) {
        this.name = name;
        this.budget = budget;
        this.members = new ArrayList<>();
    }

    /**
     * Constructs a Project with the specified name, budget, and leader.
     *
     * @param name   the name of the project
     * @param budget the budget allocated to the project
     * @param leader the lecturer who leads the project
     */
    public Project(String name, double budget, Lecturer leader) {
        this(name, budget);
        setLeader(leader);
    }

    /**
     * Returns the name of the project.
     *
     * @return the project name
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the name of the project.
     *
     * @param name the project name to set
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Returns the budget of the project.
     *
     * @return the budget
     */
    public double getBudget() {
        return budget;
    }

    /**
     * Sets the budget of the project.
     *
     * @param budget the budget to set
     */
    public void setBudget(double budget) {
        this.budget = budget;
    }

    /**
     * Returns the leader of the project.
     *
     * @return the project leader
     */
    public Lecturer getLeader() {
        return leader;
    }

    /**
     * Sets the leader of the project. The leader must be a {@link Lecturer}.
     * If the lecturer can lead this project, the leader reference is updated.
     *
     * @param leader the lecturer to lead the project
     * @return {@code true} if the leader was successfully assigned; {@code false} otherwise
     */
    public final boolean setLeader(Lecturer leader) {
        if (leader == null) {
            this.leader = null;
            return true;
        }

        if (this.leader == leader) {
            return true;
        }

        if (leader.getLeadingProject() != null && leader.getLeadingProject() != this) {
            return false;
        }

        this.leader = leader;
        leader.leadProject(this);
        return true;
    }

    /**
     * Adds a member to the project.
     * A member can be a {@link Lecturer} or a student (specifically full-time student).
     *
     * @param member the member to add
     * @return {@code true} if the member was added; {@code false} if member is null or already added
     */
    public boolean addMember(Object member) {
        if (member == null) {
            return false;
        }

        if (!members.contains(member)) {
            members.add(member);
            if (member instanceof Lecturer) {
                ((Lecturer) member).joinProject(this);
            }
            return true;
        }

        return false;
    }

    /**
     * Returns an unmodifiable list of all regular members in the project.
     *
     * @return list of project members
     */
    public List<Object> getMembers() {
        return Collections.unmodifiableList(members);
    }

    /**
     * Prints out all members of the current project, including its leader
     * and regular members.
     */
    public void displayMembers() {
        System.out.println("==================================================");
        System.out.println("Project Name : " + name);
        System.out.println("Budget       : $" + String.format("%,.2f", budget));
        System.out.println("Leader       : " + (leader != null ? leader : "[No Leader Assigned]"));
        System.out.println("Regular Members (" + members.size() + "):");
        if (members.isEmpty()) {
            System.out.println("  (None)");
        } else {
            for (int i = 0; i < members.size(); i++) {
                System.out.println("  " + (i + 1) + ". " + members.get(i));
            }
        }
        System.out.println("==================================================");
    }

    @Override
    public String toString() {
        return "Project [Name: " + name + ", Budget: $" + budget + "]";
    }
}

