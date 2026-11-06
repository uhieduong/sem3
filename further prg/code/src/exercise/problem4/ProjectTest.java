package exercise.problem4;

/**
 * Test and demonstration program for Problem 4.
 * Demonstrates the behavior of leadProject(), joinProject(), and displayMembers().
 */
public class ProjectTest {
    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println("             PROBLEM 4 DEMONSTRATION             ");
        System.out.println("==================================================");

        // 1. Create Lecturers
        Lecturer profSmith = new Lecturer("L001", "Dr. John Smith", "Associate Professor");
        Lecturer drTaylor = new Lecturer("L002", "Dr. Emily Taylor", "Senior Lecturer");
        Lecturer mrDavis = new Lecturer("L003", "Mr. Robert Davis", "Lecturer");

        // 2. Create Projects
        Project aiProject = new Project("AI Healthcare Diagnostics", 150_000.00);
        Project cloudProject = new Project("Cloud Security Framework", 80_000.00);

        // 3. Test leadProject()
        System.out.println("\n--- Testing Lecturer.leadProject() ---");
        // Dr. Smith leads AI Project
        boolean smithLeadsAI = profSmith.leadProject(aiProject);
        System.out.println("Dr. Smith leads AI Project: " + smithLeadsAI + " (Expected: true)");

        // Dr. Smith attempts to lead Cloud Project as well
        boolean smithLeadsCloud = profSmith.leadProject(cloudProject);
        System.out.println("Dr. Smith attempts to lead Cloud Project: " + smithLeadsCloud + " (Expected: false, can lead at most one project)");

        // Dr. Taylor leads Cloud Project
        boolean taylorLeadsCloud = drTaylor.leadProject(cloudProject);
        System.out.println("Dr. Taylor leads Cloud Project: " + taylorLeadsCloud + " (Expected: true)");

        // Mr. Davis attempts to lead AI Project (which already has Dr. Smith as leader)
        boolean davisLeadsAI = mrDavis.leadProject(aiProject);
        System.out.println("Mr. Davis attempts to lead AI Project: " + davisLeadsAI + " (Expected: false, already has a leader)");

        // 4. Test joinProject()
        System.out.println("\n--- Testing Lecturer.joinProject() ---");
        // Mr. Davis joins AI Project as regular member
        boolean davisJoinsAI = mrDavis.joinProject(aiProject);
        System.out.println("Mr. Davis joins AI Project: " + davisJoinsAI + " (Expected: true)");

        // Mr. Davis also joins Cloud Project (can join many projects)
        boolean davisJoinsCloud = mrDavis.joinProject(cloudProject);
        System.out.println("Mr. Davis joins Cloud Project: " + davisJoinsCloud + " (Expected: true)");

        // Dr. Smith joins Cloud Project as regular member (even though he leads AI Project)
        boolean smithJoinsCloud = profSmith.joinProject(cloudProject);
        System.out.println("Dr. Smith joins Cloud Project: " + smithJoinsCloud + " (Expected: true)");

        // 5. Test Full-Time Student joining Project
        System.out.println("\n--- Adding Student Members ---");
        FullTimeStudent studentAlice = new FullTimeStudent(101, "Alice Walker", "Software Engineering");
        FullTimeStudent studentBob = new FullTimeStudent(102, "Bob Martin", "Computer Science");

        studentAlice.joinProject(aiProject);
        studentBob.joinProject(cloudProject);
        System.out.println("Alice joined AI Project: " + (studentAlice.getProject() != null));
        System.out.println("Bob joined Cloud Project: " + (studentBob.getProject() != null));

        // Alice attempts to join a second project
        boolean aliceJoinsSecond = studentAlice.joinProject(cloudProject);
        System.out.println("Alice attempts to join Cloud Project too: " + aliceJoinsSecond + " (Expected: false, only 1 project allowed for FT students)");

        // 6. Test displayMembers()
        System.out.println("\n--- Calling displayMembers() ---");
        aiProject.displayMembers();
        System.out.println();
        cloudProject.displayMembers();
    }
}

