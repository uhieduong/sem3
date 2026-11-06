package w2;

/**
 * Represents a Part-Time Student.
 * Includes a static counter to track how many PartTimeStudent objects have been created (Question 2).
 */
public class PartTimeStudent extends Student {
    // Static counter shared across all PartTimeStudent instances
    private static int counter = 0;

    private int minHour;
    private int maxHour;

    public PartTimeStudent() {
        super();
        counter++;
    }

    public PartTimeStudent(String id, String name, String major) {
        super(id, name, major);
        counter++;
    }

    /**
     * Returns the number of PartTimeStudent instances created.
     *
     * @return the total count
     */
    public static int count() {
        return counter;
    }

    /**
     * Registers the minimum and maximum hours spent on instructor-led learning.
     *
     * @param minHour minimum hours
     * @param maxHour maximum hours
     */
    public void registerHour(int minHour, int maxHour) {
        if (minHour >= 0 && maxHour >= minHour) {
            this.minHour = minHour;
            this.maxHour = maxHour;
        }
    }

    public int getMinHour() {
        return minHour;
    }

    public int getMaxHour() {
        return maxHour;
    }

    @Override
    public String toString() {
        return String.format("PartTimeStudent [ID: %s, Name: %s, Major: %s, Hours: %d-%d]",
                getId(), getName(), getMajor(), minHour, maxHour);
    }
}

