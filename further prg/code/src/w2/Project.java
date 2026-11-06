package w2;

import java.util.ArrayList;

/**
 * Represents a Research Project with one leader (Lecturer) and members.
 */
public class Project {
    private String name;
    private double budget;
    private Lecturer leader;
    private ArrayList<Object> members;

    public Project() {
        this("Default", 0.0);
    }

    public Project(String name, double budget) {
        this.name = name;
        this.budget = budget;
        this.members = new ArrayList<>();
    }

    /**
     * Assigns a lecturer as the leader of this project.
     *
     * @param leader the lecturer to lead the project
     * @return true if successfully assigned, false otherwise
     */
    public boolean assignLeader(Lecturer leader) {
        if (leader != null && this.leader == null) {
            this.leader = leader;
            return true;
        }
        return false;
    }

    /**
     * Adds a member to this project.
     *
     * @param member the member to add
     * @return true if added, false if null or duplicate
     */
    public boolean addMember(Object member) {
        if (member != null && !members.contains(member)) {
            members.add(member);
            return true;
        }
        return false;
    }

    /**
     * Displays all members including the leader.
     */
    public void displayMember() {
        System.out.println("==================================================");
        System.out.println("Project Name: " + name);
        System.out.println("Budget      : $" + String.format("%,.2f", budget));
        System.out.println("Leader      : " + (leader != null ? leader : "None"));
        System.out.println("Members (" + members.size() + "):");
        for (int i = 0; i < members.size(); i++) {
            System.out.println("  " + (i + 1) + ". " + members.get(i));
        }
        System.out.println("==================================================");
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getBudget() {
        return budget;
    }

    public void setBudget(double budget) {
        this.budget = budget;
    }

    public Lecturer getLeader() {
        return leader;
    }

    public ArrayList<Object> getMembers() {
        return members;
    }

    @Override
    public String toString() {
        return String.format("Project [Name: %s, Budget: $%.2f]", name, budget);
    }
}

