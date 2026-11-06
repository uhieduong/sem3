package w1.problem4;

/**
 * @author COSC2440 Teaching Team
 * @version 1.0
 */

public class Project {
    private String name;
    private double budget;
    private Lecturer leader;
    private Lecturer[] members;
    private final int MAX_MEMBERS = 10;
    private int memberCount = 0;

    public Project() {
        this("Default", 0);
    }

    public Project(String name, double budget) {
        this.name = name;
        this.budget = budget;
        this.members = new Lecturer[MAX_MEMBERS];
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

    /**
     * get the current leader of this project
     * @return the Lecturer who is the leader,
     * or null if there is no leader for this project
     */
    public Lecturer getLeader() {
        return leader;
    }

    /**
     * assign a new leader for this project
     * <p>
     * Assign the given Lecturer as the new leader for this project.
     * It's the job of the Lecturer class to ensure this assignment
     * is valid. This class just does the assignment
     * </p>
     * @param leader the new leader for this project
     */
    public void assignLeader(Lecturer leader) {
        this.leader = leader;
    }

    /**
     * add a new member to this project
     * <p>
     * Add a new member to this project. At this point, there
     * is no checking at all
     * </p>
     * @param newMember a Lecturer who want to join this project
     */
    public boolean addMember(Lecturer newMember) {
        if (memberCount == MAX_MEMBERS) {
            return false;
        }
        /*
           Assume duplication has been handled when adding a new member
           so we do not have to check it
         */
        members[memberCount++] = newMember;
        return true;
    }

    /**
     * display all members in this project (including leader and regular member)
     */
    public void displayMembers() {
        // display leader
        System.out.println("Leader: " + leader);

        // display regular members
        for (int i = 0; i < memberCount; i++) {
            System.out.printf("Member #%d: %s\n", i + 1, members[i]);
        }
    }
}
