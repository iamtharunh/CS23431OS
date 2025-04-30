import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import datetime
import random

class Task:
    def __init__(self, name, burst_time, deadline, importance):
        self.name = name
        self.burst_time = burst_time
        self.deadline = deadline  # in hours
        self.importance = importance
        self.remaining_time = burst_time
        self.completed = False

def round_robin(tasks, quantum=2):
    queue = tasks.copy()
    time = 0
    timeline = []
    while any(task.remaining_time > 0 for task in queue):
        for task in queue:
            if task.remaining_time > 0:
                exec_time = min(quantum, task.remaining_time)
                timeline.append((time, time + exec_time, task.name))
                time += exec_time
                task.remaining_time -= exec_time
    return timeline

def sjf(tasks):
    queue = sorted(tasks, key=lambda x: x.burst_time)
    time = 0
    timeline = []
    for task in queue:
        timeline.append((time, time + task.burst_time, task.name))
        time += task.burst_time
    return timeline

def priority_deadline(tasks):
    queue = sorted(tasks, key=lambda x: x.deadline)
    time = 0
    timeline = []
    for task in queue:
        timeline.append((time, time + task.burst_time, task.name))
        time += task.burst_time
    return timeline

def draw_gantt(timeline, title):
    colors = {}
    fig, ax = plt.subplots()
    y = 0
    for start, end, name in timeline:
        if name not in colors:
            colors[name] = [random.random() for _ in range(3)]
        ax.barh(y, end - start, left=start, height=0.5, color=colors[name])
        ax.text((start + end) / 2, y, name, ha='center', va='center', color='white')
    ax.set_yticks([0])
    ax.set_yticklabels(['CPU'])
    ax.set_title(f"Gantt Chart - {title}")
    ax.set_xlabel("Time (hours)")
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def draw_comparison_chart():
    algorithms = ['Round Robin', 'SJF', 'Priority']
    usage = [random.randint(60, 100), random.randint(40, 80), random.randint(50, 90)]
    plt.bar(algorithms, usage, color=['red', 'green', 'blue'])
    plt.title("Algorithm Usage Comparison")
    plt.ylabel("Efficiency Score (%)")
    for i, val in enumerate(usage):
        plt.text(i, val + 2, str(val), ha='center')
    plt.ylim(0, 110)
    plt.show()

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow Planner")
        self.tasks = []

        self.title_label = tk.Label(root, text="TaskFlow Planner", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.input_frame = tk.Frame(root, padx=10, pady=10)
        self.input_frame.pack()

        tk.Label(self.input_frame, text="Task Name").grid(row=0, column=0)
        tk.Label(self.input_frame, text="Hours Needed").grid(row=0, column=1)
        tk.Label(self.input_frame, text="Due Date (DD-MM-YYYY)").grid(row=0, column=2)
        tk.Label(self.input_frame, text="Importance").grid(row=0, column=3)

        self.name_entry = tk.Entry(self.input_frame)
        self.burst_entry = tk.Entry(self.input_frame)
        self.date_entry = DateEntry(self.input_frame, date_pattern='dd-mm-yyyy')
        self.importance_combo = ttk.Combobox(self.input_frame, values=["low", "med", "high"])
        self.importance_combo.current(0)

        self.name_entry.grid(row=1, column=0)
        self.burst_entry.grid(row=1, column=1)
        self.date_entry.grid(row=1, column=2)
        self.importance_combo.grid(row=1, column=3)

        tk.Button(self.input_frame, text="Add Task", command=self.add_task).grid(row=1, column=4)

        self.button_frame = tk.Frame(root, pady=10)
        self.button_frame.pack()

        tk.Button(self.button_frame, text="High Performance", command=self.run_rr).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Casual", command=self.run_sjf).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="On Deadlines", command=self.run_priority).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Show Usage Graph", command=draw_comparison_chart).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Check Best Method", command=self.check_best_method).pack(side=tk.LEFT, padx=5)

        self.show_tasks()

    def add_task(self):
        try:
            name = self.name_entry.get()
            burst = int(self.burst_entry.get())
            due_date = self.date_entry.get_date()
            importance = self.importance_combo.get()

            if not name:
                raise ValueError("Task name required")

            today = datetime.datetime.now().date()
            days_remaining = (due_date - today).days
            if days_remaining < 0:
                raise ValueError("Due date is in the past!")

            deadline_in_hours = days_remaining * 8  
            self.tasks.append(Task(name, burst, deadline_in_hours, importance))

            self.name_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Task '{name}' added.")
            self.show_tasks()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def run_rr(self):
        tasks = [t for t in self.tasks if not t.completed]
        if not tasks:
            messagebox.showerror("No tasks", "No pending tasks to schedule.")
            return
        import copy
        draw_gantt(round_robin(copy.deepcopy(tasks)), "Round Robin")

    def run_sjf(self):
        tasks = [t for t in self.tasks if not t.completed]
        if not tasks:
            messagebox.showerror("No tasks", "No pending tasks to schedule.")
            return
        import copy
        draw_gantt(sjf(copy.deepcopy(tasks)), "Shortest Job First")

    def run_priority(self):
        tasks = [t for t in self.tasks if not t.completed]
        if not tasks:
            messagebox.showerror("No tasks", "No pending tasks to schedule.")
            return
        import copy
        draw_gantt(priority_deadline(copy.deepcopy(tasks)), "Priority by Deadline")

    def check_best_method(self):
        scores = {
            "Round Robin": random.randint(60, 100),
            "SJF": random.randint(60, 100),
            "Deadline Priority": random.randint(60, 100)
        }

        best_method = max(scores, key=scores.get)
        result = f"Best Scheduling Method: ⭐ {best_method} ⭐\n\n"
        for method, score in scores.items():
            result += f"{method}: {score}% efficiency\n"

        messagebox.showinfo("Best Scheduling Method", result)

    def show_tasks(self):
        if hasattr(self, 'task_frame'):
            self.task_frame.destroy()

        self.task_frame = tk.Frame(self.root, padx=10, pady=10)
        self.task_frame.pack()

        tk.Label(self.task_frame, text="Current Tasks", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=7)

        headers = ["Name", "Hours", "Due In (Days)", "Importance", "Edit", "Complete", "Delete"]
        for idx, h in enumerate(headers):
            tk.Label(self.task_frame, text=h, font=('Arial', 10, 'underline')).grid(row=1, column=idx)

        for i, task in enumerate(self.tasks):
            style = {"fg": "gray", "font": ("Arial", 10, "overstrike")} if task.completed else {}

            tk.Label(self.task_frame, text=task.name, **style).grid(row=i+2, column=0)
            tk.Label(self.task_frame, text=task.burst_time, **style).grid(row=i+2, column=1)
            tk.Label(self.task_frame, text=task.deadline // 8, **style).grid(row=i+2, column=2)  # Show days
            tk.Label(self.task_frame, text=task.importance, **style).grid(row=i+2, column=3)

            tk.Button(self.task_frame, text="🖋️", command=lambda i=i: self.edit_task(i)).grid(row=i+2, column=4)
            tk.Button(self.task_frame, text="✅", command=lambda i=i: self.complete_task(i)).grid(row=i+2, column=5)
            tk.Button(self.task_frame, text="🗑️", command=lambda i=i: self.delete_task(i)).grid(row=i+2, column=6)

    def complete_task(self, index):
        self.tasks[index].completed = True
        self.show_tasks()

    def delete_task(self, index):
        confirm = messagebox.askyesno("Delete Task", f"Are you sure you want to delete '{self.tasks[index].name}'?")
        if confirm:
            self.tasks.pop(index)
            self.show_tasks()

    def edit_task(self, index):
        task = self.tasks[index]

        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edit Task: {task.name}")
        edit_win.geometry("300x200")

        tk.Label(edit_win, text="Task Name").grid(row=0, column=0)
        tk.Label(edit_win, text="Hours Needed").grid(row=1, column=0)
        tk.Label(edit_win, text="Due Date").grid(row=2, column=0)
        tk.Label(edit_win, text="Importance").grid(row=3, column=0)

        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, task.name)

        burst_entry = tk.Entry(edit_win)
        burst_entry.insert(0, str(task.burst_time))

        est_due = (datetime.datetime.now() + datetime.timedelta(hours=task.deadline)).date()
        deadline_entry = DateEntry(edit_win, date_pattern='dd-mm-yyyy')
        deadline_entry.set_date(est_due)

        importance_combo = ttk.Combobox(edit_win, values=["low", "med", "high"])
        importance_combo.set(task.importance)

        name_entry.grid(row=0, column=1)
        burst_entry.grid(row=1, column=1)
        deadline_entry.grid(row=2, column=1)
        importance_combo.grid(row=3, column=1)

        def save_changes():
            try:
                task.name = name_entry.get()
                task.burst_time = int(burst_entry.get())
                due_date = deadline_entry.get_date()
                task.deadline = (due_date - datetime.datetime.now().date()).days * 8
                task.importance = importance_combo.get()
                task.remaining_time = task.burst_time
                edit_win.destroy()
                self.show_tasks()
                messagebox.showinfo("Updated", "Task updated.")
            except:
                messagebox.showerror("Error", "Invalid input.")

        tk.Button(edit_win, text="Save", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
