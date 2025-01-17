import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import json


class TimelineEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Timeline Editor")
        self.data = None
        self.file_path = None

        # UI components
        self.create_widgets()

    def create_widgets(self):
        # File menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Start and End dates
        date_frame = tk.Frame(self.root, pady=10)
        date_frame.pack(fill="x")
        tk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5)
        self.start_date_entry = DateEntry(date_frame, width=15, date_pattern="yyyy-mm-dd")
        self.start_date_entry.grid(row=0, column=1, padx=5)

        tk.Label(date_frame, text="End Date:").grid(row=0, column=2, padx=5)
        self.end_date_entry = DateEntry(date_frame, width=15, date_pattern="yyyy-mm-dd")
        self.end_date_entry.grid(row=0, column=3, padx=5)

        # Tasks and milestones tabs
        self.tabs = ttk.Notebook(self.root)
        self.tasks_tab = ttk.Frame(self.tabs)
        self.milestones_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.tasks_tab, text="Tasks")
        self.tabs.add(self.milestones_tab, text="Milestones")
        self.tabs.pack(fill="both", expand=True)

        # Tasks section
        self.task_list = ttk.Treeview(self.tasks_tab, columns=("Title", "Start Date", "End Date"), show="headings")
        self.task_list.heading("Title", text="Title")
        self.task_list.heading("Start Date", text="Start Date")
        self.task_list.heading("End Date", text="End Date")
        self.task_list.pack(fill="both", expand=True, padx=5, pady=5)

        task_button_frame = tk.Frame(self.tasks_tab)
        task_button_frame.pack(fill="x", pady=5)
        tk.Button(task_button_frame, text="Add Task", command=self.add_task).pack(side="left", padx=5)
        tk.Button(task_button_frame, text="Edit Task", command=self.edit_task).pack(side="left", padx=5)
        tk.Button(task_button_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5)

        # Milestones section
        self.milestone_list = ttk.Treeview(self.milestones_tab, columns=("Title", "Date", "Percentage", "Color"), show="headings")
        self.milestone_list.heading("Title", text="Title")
        self.milestone_list.heading("Date", text="Date")
        self.milestone_list.heading("Percentage", text="Percentage")
        self.milestone_list.heading("Color", text="Color")
        self.milestone_list.pack(fill="both", expand=True, padx=5, pady=5)

        milestone_button_frame = tk.Frame(self.milestones_tab)
        milestone_button_frame.pack(fill="x", pady=5)
        tk.Button(milestone_button_frame, text="Add Milestone", command=self.add_milestone).pack(side="left", padx=5)
        tk.Button(milestone_button_frame, text="Edit Milestone", command=self.edit_milestone).pack(side="left", padx=5)
        tk.Button(milestone_button_frame, text="Delete Milestone", command=self.delete_milestone).pack(side="left", padx=5)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not self.file_path:
            return
        with open(self.file_path, "r") as file:
            self.data = json.load(file)
        self.populate_fields()

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if not self.file_path:
                return
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)
        messagebox.showinfo("Success", "File saved successfully!")

    def populate_fields(self):
        self.start_date_entry.set_date(self.data["start_date"])
        self.end_date_entry.set_date(self.data["end_date"])

        # Populate tasks
        for row in self.task_list.get_children():
            self.task_list.delete(row)
        for task in self.data["tasks"]:
            self.task_list.insert("", "end", values=(task["title"], task["start_date"], task["end_date"]))

        # Populate milestones
        for row in self.milestone_list.get_children():
            self.milestone_list.delete(row)
        for milestone in self.data["milestones"]:
            self.milestone_list.insert("", "end", values=(milestone["title"], milestone["date"], milestone.get("percentage", ""), milestone.get("color", "")))

    def add_task(self):
        self.edit_task(new=True)

    def edit_task(self, new=False):
        selected = self.task_list.selection()
        task_data = None
        if not new and selected:
            task_data = self.task_list.item(selected[0], "values")
        task_window = TaskWindow(self.root, task_data)
        self.root.wait_window(task_window.top)
        if task_window.result:
            if new:
                self.data["tasks"].append(task_window.result)
            else:
                index = self.task_list.index(selected[0])
                self.data["tasks"][index] = task_window.result
            self.populate_fields()

    def delete_task(self):
        selected = self.task_list.selection()
        if not selected:
            return
        index = self.task_list.index(selected[0])
        del self.data["tasks"][index]
        self.populate_fields()

    def add_milestone(self):
        self.edit_milestone(new=True)

    def edit_milestone(self, new=False):
        selected = self.milestone_list.selection()
        milestone_data = None
        if not new and selected:
            milestone_data = self.milestone_list.item(selected[0], "values")
        milestone_window = MilestoneWindow(self.root, milestone_data)
        self.root.wait_window(milestone_window.top)
        if milestone_window.result:
            if new:
                self.data["milestones"].append(milestone_window.result)
            else:
                index = self.milestone_list.index(selected[0])
                self.data["milestones"][index] = milestone_window.result
            self.populate_fields()

    def delete_milestone(self):
        selected = self.milestone_list.selection()
        if not selected:
            return
        index = self.milestone_list.index(selected[0])
        del self.data["milestones"][index]
        self.populate_fields()


class TaskWindow:
    def __init__(self, parent, task_data=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Task")
        self.result = None

        tk.Label(self.top, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.top)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Start Date:").grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(self.top, width=15, date_pattern="yyyy-mm-dd")
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.top, text="End Date:").grid(row=2, column=0, padx=5, pady=5)
        self.end_date_entry = DateEntry(self.top, width=15, date_pattern="yyyy-mm-dd")
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        if task_data:
            self.title_entry.insert(0, task_data[0])
            self.start_date_entry.set_date(task_data[1])
            self.end_date_entry.set_date(task_data[2])

        tk.Button(self.top, text="Save", command=self.save).grid(row=3, column=0, columnspan=2, pady=5)

    def save(self):
        self.result = {
            "title": self.title_entry.get(),
            "start_date": self.start_date_entry.get(),
            "end_date": self.end_date_entry.get()
        }
        self.top.destroy()


class MilestoneWindow:
    def __init__(self, parent, milestone_data=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Milestone")
        self.result = None

        tk.Label(self.top, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.top)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.top, width=15, date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Percentage:").grid(row=2, column=0, padx=5, pady=5)
        self.percentage_entry = tk.Entry(self.top)
        self.percentage_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Color:").grid(row=3, column=0, padx=5, pady=5)
        self.color_entry = tk.Entry(self.top)
        self.color_entry.grid(row=3, column=1, padx=5, pady=5)

        if milestone_data:
            self.title_entry.insert(0, milestone_data[0])
            self.date_entry.set_date(milestone_data[1])
            self.percentage_entry.insert(0, milestone_data[2])
            self.color_entry.insert(0, milestone_data[3])

        tk.Button(self.top, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=5)

    def save(self):
        self.result = {
            "title": self.title_entry.get(),
            "date": self.date_entry.get(),
            "percentage": self.percentage_entry.get(),
            "color": self.color_entry.get()
        }
        self.top.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimelineEditor(root)
    root.mainloop()
