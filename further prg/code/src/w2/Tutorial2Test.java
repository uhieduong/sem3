package w2;

/**
 * Comprehensive test suite for Tutorial 2 (Questions 1, 2, and 3).
 */
public class Tutorial2Test {

    public static void main(String[] args) {
        printHeader("TUTORIAL 2 TEST SUITE");

        testQuestion1_FullTimeStudent();
        testQuestion1_PartTimeStudent();
        testQuestion1_LecturerAndProject();
        testQuestion2_StaticCounter();
        testQuestion3_SchoolSystem();

        printHeader("ALL TESTS COMPLETED SUCCESSFULLY");
    }

    /**
     * Tests FullTimeStudent requirements (inheritance, project joining rules).
     */
    private static void testQuestion1_FullTimeStudent() {
        printSection("Testing Question 1: FullTimeStudent");

        FullTimeStudent ft1 = new FullTimeStudent("s101", "Alice Smith", "Software Engineering");
        Project p1 = new Project("AI Diagnostics", 100_000.0);
        Project p2 = new Project("Cloud Security", 50_000.0);

        // Test 1: Full-time student joins a project (should succeed)
        boolean joinedP1 = ft1.joinProject(p1);
        assertCondition(joinedP1, "FT student joins Project 1 (Expected: true)");
        assertCondition(ft1.getJoinedProject() == p1, "FT student's joinedProject is Project 1");

        // Test 2: Full-time student attempts to join a 2nd project (should fail - only 1 allowed)
        boolean joinedP2 = ft1.joinProject(p2);
        assertCondition(!joinedP2, "FT student attempts to join Project 2 while already in Project 1 (Expected: false)");

        // Test 3: Null project check
        FullTimeStudent ft2 = new FullTimeStudent("s102", "Bob Vance", "Computer Science");
        boolean joinedNull = ft2.joinProject(null);
        assertCondition(!joinedNull, "FT student joining null project (Expected: false)");
    }

    /**
     * Tests PartTimeStudent requirements (hours registration).
     */
    private static void testQuestion1_PartTimeStudent() {
        printSection("Testing Question 1: PartTimeStudent");

        PartTimeStudent pt = new PartTimeStudent("s201", "Charlie Brown", "Data Science");
        pt.registerHour(10, 25);

        assertCondition(pt.getMinHour() == 10, "Min hours registered correctly (10)");
        assertCondition(pt.getMaxHour() == 25, "Max hours registered correctly (25)");

        // Invalid registration: min > max (should be rejected/ignored)
        pt.registerHour(30, 20);
        assertCondition(pt.getMinHour() == 10 && pt.getMaxHour() == 25, "Invalid hours (30 > 20) rejected");
    }

    /**
     * Tests Lecturer and Project leadership and membership rules.
     */
    private static void testQuestion1_LecturerAndProject() {
        printSection("Testing Question 1: Lecturer & Project Logic");

        Lecturer profSmith = new Lecturer("L001", "Dr. John Smith", "Associate Professor");
        Lecturer drTaylor = new Lecturer("L002", "Dr. Sarah Taylor", "Senior Lecturer");
        Lecturer mrDavis = new Lecturer("L003", "Mr. Robert Davis", "Lecturer");

        Project projectA = new Project("Quantum Computing", 200_000.0);
        Project projectB = new Project("Autonomous Vehicles", 150_000.0);

        // 1. Dr. Smith leads Project A
        boolean smithLeadsA = profSmith.leadProject(projectA);
        assertCondition(smithLeadsA, "Dr. Smith leads Project A (Expected: true)");
        assertCondition(profSmith.isLeading(), "Dr. Smith isLeading() (Expected: true)");
        assertCondition(projectA.getLeader() == profSmith, "Project A leader is Dr. Smith");

        // 2. Dr. Smith tries to lead Project B as well (should fail: at most 1 led project)
        boolean smithLeadsB = profSmith.leadProject(projectB);
        assertCondition(!smithLeadsB, "Dr. Smith tries to lead Project B while leading A (Expected: false)");

        // 3. Dr. Taylor leads Project B (should succeed)
        boolean taylorLeadsB = drTaylor.leadProject(projectB);
        assertCondition(taylorLeadsB, "Dr. Taylor leads Project B (Expected: true)");

        // 4. Mr. Davis tries to lead Project A (should fail: Project A already has Dr. Smith as leader)
        boolean davisLeadsA = mrDavis.leadProject(projectA);
        assertCondition(!davisLeadsA, "Mr. Davis tries to lead Project A which already has a leader (Expected: false)");

        // 5. Lecturers joining projects as members (can join multiple)
        boolean smithJoinsB = profSmith.joinProject(projectB);
        boolean davisJoinsA = mrDavis.joinProject(projectA);
        boolean davisJoinsB = mrDavis.joinProject(projectB);

        assertCondition(smithJoinsB, "Dr. Smith joins Project B as member (Expected: true)");
        assertCondition(davisJoinsA, "Mr. Davis joins Project A as member (Expected: true)");
        assertCondition(davisJoinsB, "Mr. Davis joins Project B as member (Expected: true)");

        // 6. Test displayMember()
        System.out.println("\nCalling projectA.displayMember():");
        projectA.displayMember();
    }

    /**
     * Tests Question 2: Static counter tracking PartTimeStudent instances.
     */
    private static void testQuestion2_StaticCounter() {
        printSection("Testing Question 2: PartTimeStudent Static Counter");

        int initialCount = PartTimeStudent.count();
        System.out.println("Part-time students count before new instances: " + initialCount);

        // Creating FullTimeStudent should NOT affect PartTimeStudent counter
        new FullTimeStudent("ft_test1", "FT Student", "IT");
        new FullTimeStudent("ft_test2", "FT Student 2", "SE");
        assertCondition(PartTimeStudent.count() == initialCount, "Creating FullTimeStudents does not change PartTimeStudent count");

        // Creating PartTimeStudents should increment count
        new PartTimeStudent("pt_test1", "PT Student 1", "IT");
        new PartTimeStudent("pt_test2", "PT Student 2", "Business");
        new PartTimeStudent(); // default constructor

        int updatedCount = PartTimeStudent.count();
        System.out.println("Part-time students count after creating 3 instances: " + updatedCount);
        assertCondition(updatedCount == initialCount + 3, "Static counter correctly incremented by 3 (Expected: " + (initialCount + 3) + ")");
    }

    /**
     * Tests Question 3: SchoolSystem management class.
     */
    private static void testQuestion3_SchoolSystem() {
        printSection("Testing Question 3: SchoolSystem Class");

        SchoolSystem system = new SchoolSystem();

        // 1. Add students (both polymorphic types: FullTimeStudent and PartTimeStudent)
        Student s1 = new FullTimeStudent("s301", "Emma Watson", "Drama");
        Student s2 = new PartTimeStudent("s302", "Daniel Radcliffe", "Film");
        system.addStudent(s1);
        system.addStudent(s2);
        assertCondition(system.getStudents().size() == 2, "SchoolSystem contains 2 students");

        // 2. Duplicate student should not be added twice
        system.addStudent(s1);
        assertCondition(system.getStudents().size() == 2, "Duplicate student rejected");

        // 3. Null student should be ignored
        system.addStudent(null);
        assertCondition(system.getStudents().size() == 2, "Null student ignored");

        // 4. Add lecturers
        Lecturer l1 = new Lecturer("L101", "Prof. McGonagall", "Professor");
        Lecturer l2 = new Lecturer("L102", "Prof. Flitwick", "Senior Lecturer");
        system.addLecturer(l1);
        system.addLecturer(l2);
        assertCondition(system.getLecturers().size() == 2, "SchoolSystem contains 2 lecturers");

        // 5. Add projects
        Project p1 = new Project("Transfiguration AI", 85_000.0);
        system.addProject(p1);
        assertCondition(system.getProjects().size() == 1, "SchoolSystem contains 1 project");

        System.out.println("SchoolSystem state verified: "
                + system.getStudents().size() + " students, "
                + system.getLecturers().size() + " lecturers, "
                + system.getProjects().size() + " projects.");
    }

    // --- Helper Utilities for Pretty Output ---

    private static void assertCondition(boolean condition, String description) {
        if (condition) {
            System.out.println("  [PASS] " + description);
        } else {
            System.err.println("  [FAIL] " + description);
            throw new AssertionError("Test failed: " + description);
        }
    }

    private static void printHeader(String title) {
        System.out.println("\n==================================================");
        System.out.println("   " + title);
        System.out.println("==================================================");
    }

    private static void printSection(String sectionName) {
        System.out.println("\n--- " + sectionName + " ---");
    }
}

