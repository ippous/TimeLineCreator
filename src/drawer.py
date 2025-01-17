import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import matplotlib.dates as mdates


def plot_timeline(data):
    # Parse the input data
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    tasks = data['tasks']
    milestones = data['milestones']

    # Set spacing between tasks
    task_spacing = 0.4  # Adjust vertical spacing dynamically

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Format the x-axis to show months
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.tick_params(axis='x', labelsize=10)

    # Draw the timeline line in the middle
    ax.axhline(0, color='black', linewidth=1.2)  # Timeline line

    # Plot milestones on the timeline
    for milestone in milestones:
        milestone_date = datetime.strptime(milestone['date'], '%Y-%m-%d')
        color = milestone.get('color', 'blue')
        percentage = milestone.get('percentage', None)

        # Draw the milestone
        ax.plot(milestone_date, 0, marker='v', color=color, markersize=10)

        # Display the title of the milestone
        ax.text(milestone_date, 0.3, milestone['title'], horizontalalignment='center', fontsize=10)

        # Display the percentage under the milestone title
        if percentage is not None:
            ax.text(milestone_date, 0.15, f"{percentage}%", horizontalalignment='center', fontsize=9, color='gray')

    # Track task levels to avoid overlaps
    task_levels = []  # Each level contains the end times of tasks at that level

    def assign_task_level(task_start, task_end):
        """Assign the task to the first available level without overlap."""
        for level, level_end_times in enumerate(task_levels):
            if all(task_start > prev_end or task_end < prev_start for prev_start, prev_end in level_end_times):
                level_end_times.append((task_start, task_end))
                return level
        # If no existing level is free, create a new one
        task_levels.append([(task_start, task_end)])
        return len(task_levels) - 1

    # Plot tasks below the timeline
    for task in tasks:
        task_start = datetime.strptime(task['start_date'], '%Y-%m-%d')
        task_end = datetime.strptime(task['end_date'], '%Y-%m-%d')

        # Determine the appropriate level for the task
        level = assign_task_level(task_start, task_end)
        y_pos = -level * task_spacing - 0.2  # Tasks go below the timeline with dynamic spacing

        # Draw the task rectangle
        rect_height = 0.3  # Height of the task rectangle
        ax.add_patch(patches.Rectangle((task_start, y_pos - rect_height / 2),
                                        task_end - task_start, rect_height,
                                        color='skyblue'))

        # Add the task title inside the rectangle
        text_x = task_start + (task_end - task_start) / 2
        ax.text(text_x, y_pos, task['title'], verticalalignment='center',
                horizontalalignment='center', fontsize=9, color='black')

    # Adjust vertical limits dynamically
    min_y = -len(task_levels) * task_spacing - 0.5  # Calculate the minimum y-coordinate for the lowest task
    ax.set_ylim(min_y, 2)

    # Set labels and title
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_title('Project Timeline')

    # Tight layout for better spacing
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Load data from JSON file
    with open('timeline_data.json', 'r') as file:
        data = json.load(file)
    plot_timeline(data)
