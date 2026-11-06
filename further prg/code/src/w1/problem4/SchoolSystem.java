package w1.problem4;

/**
 * Test program for the implementation of Lecturer and Project
 * @author COSC2440 Teaching Team
 * @version 1.0
 */

public class SchoolSystem {
    public static void main(String[] args) {
        Lecturer lecturer1 = new Lecturer("L001", "Alice", "Lecturer");
        Lecturer lecturer2 = new Lecturer("L002", "Bob", "Senior Lecturer");
        Lecturer lecturer3 = new Lecturer("L003", "Carol", "Assoc Lecturer");

        Project p1 = new Project("AI", 999.9);
        Project p2 = new Project("ML", 1234.5);

        // Must display true
        boolean b = lecturer1.leadProject(p1);
        System.out.println(b);

        // Must display false (p1 has a leader already)
        b = lecturer2.leadProject(p1);
        System.out.println(b);

        // Must display false (lecturer1 is leading a project)
        b = lecturer1.leadProject(p2);
        System.out.println(b);

        // Must display lecturer1 as a leader and lecturer2 and lecturer3 as members
        lecturer2.joinProject(p1);
        lecturer3.joinProject(p1);
        p1.displayMembers();
    }
}
