package w2;

import java.util.ArrayList;

/**
 * Manages students, lecturers, and projects within the school system (Question 3).
 */
public class SchoolSystem {
    private ArrayList<Student> students;
    private ArrayList<Lecturer> lecturers;
    private ArrayList<Project> projects;

    public SchoolSystem() {
        this.students = new ArrayList<>();
        this.lecturers = new ArrayList<>();
        this.projects = new ArrayList<>();
    }

    /**
     * Adds a student to the system.
     *
     * @param s the student to add
     */
    public void addStudent(Student s) {
        if (s != null && !students.contains(s)) {
            students.add(s);
        }
    }

    /**
     * Adds a lecturer to the system.
     *
     * @param l the lecturer to add
     */
    public void addLecturer(Lecturer l) {
        if (l != null && !lecturers.contains(l)) {
            lecturers.add(l);
        }
    }

    /**
     * Adds a project to the system.
     *
     * @param p the project to add
     */
    public void addProject(Project p) {
        if (p != null && !projects.contains(p)) {
            projects.add(p);
        }
    }

    public ArrayList<Student> getStudents() {
        return students;
    }

    public ArrayList<Lecturer> getLecturers() {
        return lecturers;
    }

    public ArrayList<Project> getProjects() {
        return projects;
    }

    /**
     * Simple demonstration runner for Questions 1, 2, and 3.
     */
    public static void main(String[] args) {
        SchoolSystem system = new SchoolSystem();

        // Question 1 & 2: Students and static count test
        FullTimeStudent ft1 = new FullTimeStudent("s001", "Alice Smith", "Software Engineering");
        PartTimeStudent pt1 = new PartTimeStudent("s002", "Bob Jones", "Information Technology");
        PartTimeStudent pt2 = new PartTimeStudent("s003", "Charlie Green", "Cybersecurity");
        pt1.registerHour(10, 20);

        System.out.println("Part-time students count (Question 2): " + PartTimeStudent.count());

        // Question 1: Lecturers and Project
        Lecturer profDr = new Lecturer("L001", "Dr. David Evans", "Associate Professor");
        Lecturer drTaylor = new Lecturer("L002", "Dr. Sarah Taylor", "Senior Lecturer");

        Project aiProject = new Project("AI Diagnostics", 120_000.0);

        profDr.leadProject(aiProject);
        drTaylor.joinProject(aiProject);
        ft1.joinProject(aiProject);

        // Question 3: Adding objects to SchoolSystem
        system.addStudent(ft1);
        system.addStudent(pt1);
        system.addStudent(pt2);
        system.addLecturer(profDr);
        system.addLecturer(drTaylor);
        system.addProject(aiProject);

        System.out.println("\nSchoolSystem Summary:");
        System.out.println("Total Students : " + system.getStudents().size());
        System.out.println("Total Lecturers: " + system.getLecturers().size());
        System.out.println("Total Projects : " + system.getProjects().size());

        System.out.println();
        aiProject.displayMember();
    }
}

