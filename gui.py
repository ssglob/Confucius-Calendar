import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, font
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from tkcalendar import Calendar
from PIL import Image, ImageTk
from handle_task import get_task_duration
import Task_Scheduler

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Confucius Calendar")
        self.geometry("1000x800")

        self.quotes = [
            "It does not matter how slowly you go so long as you do not stop.",
            "The man who moves a mountain begins by carrying away small stones.",
            "Success depends upon previous preparation, and without such preparation there is sure to be failure.",
            "Learn as if you were not reaching your goal and as though you were scared of missing it.",
            "To see what is right and not do it is a lack of courage.",
            "A great man is hard on himself; a small man is hard on others.",
            "I hear and I forget. I see and I remember. I do and I understand.",
            "Wheresoever you go, go with all your heart.",
            "Our greatest glory is not in never falling, but in getting up every time we do.",
            "He that would perfect his work must first sharpen his tools."
        ]

        self.task_file = Path('.') / "data" / "tasklist.json"
        self.schedule_file = Path('.') / "data" / "schedule.json"
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MainPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        try:
            self.bg_image = Image.open("background.jpg")
            self.bg_image = self.bg_image.resize((1000, 800), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            
            canvas = tk.Canvas(self, width=1000, height=800)
            canvas.pack(fill="both", expand=True)
            canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

            title_font = font.Font(family="Helvetica", size=48, weight="bold")
            canvas.create_text(500, 300, text="Confucius Calendar", font=title_font, fill="white")

            style = ttk.Style()
            style.configure("Modern.TButton", font=("Helvetica", 18), background="#4CAF50", foreground="black", padding=10, borderwidth=0)
            style.map("Modern.TButton", background=[("active", "#45a049")])

            begin_button = ttk.Button(self, text="Begin", style="Modern.TButton", command=lambda: controller.show_frame("MainPage"))
            canvas.create_window(500, 450, window=begin_button)

        except FileNotFoundError:
            label = ttk.Label(self, text="Welcome to Confucius Calendar", font=("Helvetica", 24))
            label.pack(pady=100)
            begin_button = ttk.Button(self, text="Begin", command=lambda: controller.show_frame("MainPage"))
            begin_button.pack()
            messagebox.showinfo("Info", "background.jpg not found. Please add it to the root directory for a better experience.")


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.load_tasks()
        self.create_widgets()
        self.load_schedule()
        self.update_calendar_events()

    def load_tasks(self):
        if not self.controller.task_file.exists():
            self.controller.task_file.write_text("[]", encoding="utf-8")
        
        try:
            with self.controller.task_file.open("r") as f:
                self.tasklist = json.load(f)
        except json.JSONDecodeError:
            self.tasklist = []

        for task in self.tasklist:
            if isinstance(task["date"], str):
                task["date"] = Task_Scheduler._d(task["date"])

    def save_tasks(self):
        tasklist_to_save = [task.copy() for task in self.tasklist]
        for task in tasklist_to_save:
            if isinstance(task["date"], datetime):
                task["date"] = task["date"].strftime("%d-%m-%Y")
        
        with self.controller.task_file.open("w") as f:
            json.dump(tasklist_to_save, f, indent=4)

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        actions_frame = ttk.LabelFrame(left_frame, text="Actions")
        actions_frame.pack(pady=10, fill=tk.X)

        add_button = ttk.Button(actions_frame, text="Add Task", command=self.add_task_window)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = ttk.Button(actions_frame, text="Update Selected", command=self.update_task_window)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        remove_button = ttk.Button(actions_frame, text="Remove Selected", command=self.remove_task_window)
        remove_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        refresh_button = ttk.Button(actions_frame, text="Refresh Tasks", command=self.print_tasks)
        refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        schedule_button = ttk.Button(actions_frame, text="Generate Schedule", command=self.generate_schedule_window)
        schedule_button.pack(side=tk.LEFT, padx=5, pady=5)

        tasks_frame = ttk.LabelFrame(left_frame, text="Tasks")
        tasks_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tasks_frame, columns=("ID", "Task", "Due Date", "Duration"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Duration", text="Duration (h)")
        self.tree.column("Duration", width=80)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.print_tasks()

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.cal = Calendar(right_frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(fill="both", expand=True)
        
        self.cal.tag_config('task', background='lightblue')
        self.cal.tag_config('deadline_soon', background='yellow')
        self.cal.tag_config('deadline_today', background='red')

        self.cal.bind("<<CalendarSelected>>", self.display_schedule_for_date)

        self.schedule_display = tk.Text(right_frame, height=10)
        self.schedule_display.pack(fill=tk.X, pady=10)

    def add_task_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Task")

        ttk.Label(add_window, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        task_name_entry = ttk.Entry(add_window, width=40)
        task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Due Date (dd-mm-yyyy):").grid(row=1, column=0, padx=5, pady=5)
        due_date_entry = ttk.Entry(add_window, width=40)
        due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Duration (hours):").grid(row=2, column=0, padx=5, pady=5)
        duration_entry = ttk.Entry(add_window, width=40)
        duration_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Unsure about duration? Let Confucius use his wisdom (Leave Blank)").grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        def save_new_task():
            task_name = task_name_entry.get()
            due_date_str = due_date_entry.get()
            duration_str = duration_entry.get()

            if not task_name or not due_date_str:
                messagebox.showerror("Error", "Task name and due date are required.")
                return

            try:
                due_date = Task_Scheduler._d(due_date_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use dd-mm-yyyy.")
                return

            if duration_str.isdigit():
                duration = int(duration_str)
            else:
                duration = get_task_duration(task_name, due_date)

            new_task = {"task": task_name, "date": due_date, "duration": duration}
            Task_Scheduler.insert_task(self.tasklist, new_task)
            self.save_tasks()
            self.print_tasks()
            add_window.destroy()
            messagebox.showinfo("Success", "Task added successfully!")

        save_button = ttk.Button(add_window, text="Save Task", command=save_new_task)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_task_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to update.")
            return

        task_id = int(self.tree.item(selected_item[0])["values"][0]) - 1
        task = self.tasklist[task_id]

        update_window = tk.Toplevel(self)
        update_window.title("Update Task")

        ttk.Label(update_window, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        task_name_entry = ttk.Entry(update_window, width=40)
        task_name_entry.grid(row=0, column=1, padx=5, pady=5)
        task_name_entry.insert(0, task["task"])

        ttk.Label(update_window, text="Due Date (dd-mm-yyyy):").grid(row=1, column=0, padx=5, pady=5)
        due_date_entry = ttk.Entry(update_window, width=40)
        due_date_entry.grid(row=1, column=1, padx=5, pady=5)
        due_date_entry.insert(0, task["date"].strftime("%d-%m-%Y") if isinstance(task["date"], datetime) else task["date"])

        ttk.Label(update_window, text="Duration (hours):").grid(row=2, column=0, padx=5, pady=5)
        duration_entry = ttk.Entry(update_window, width=40)
        duration_entry.grid(row=2, column=1, padx=5, pady=5)
        duration_entry.insert(0, task["duration"])

        def save_updated_task():
            task_name = task_name_entry.get()
            due_date_str = due_date_entry.get()
            duration_str = duration_entry.get()

            if not task_name or not due_date_str:
                messagebox.showerror("Error", "Task name and due date are required.")
                return

            try:
                due_date = Task_Scheduler._d(due_date_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use dd-mm-yyyy.")
                return

            if duration_str.isdigit():
                duration = int(duration_str)
            else:
                duration = get_task_duration(task_name, due_date)

            self.tasklist[task_id] = {"task": task_name, "date": due_date, "duration": duration}
            Task_Scheduler.refresh_list(self.tasklist, self.tasklist[task_id])
            self.save_tasks()
            self.print_tasks()
            update_window.destroy()
            messagebox.showinfo("Success", "Task updated successfully!")

        save_button = ttk.Button(update_window, text="Save Changes", command=save_updated_task)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def print_tasks(self):
        self.load_tasks()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i, task in enumerate(self.tasklist):
            date_str = task['date'].strftime('%d-%m-%Y') if isinstance(task['date'], datetime) else task['date']
            self.tree.insert("", "end", values=(i + 1, task["task"], date_str, task["duration"]))

    def remove_task_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to remove.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to remove the selected task?"):
            selected_indices = [self.tree.index(item) for item in selected_item]
            selected_indices.sort(reverse=True)

            for index in selected_indices:
                del self.tasklist[index]

            self.save_tasks()
            self.print_tasks()
            messagebox.showinfo("Success", "Task(s) removed successfully!")

    def generate_schedule_window(self):
        Task_Scheduler.schedule_tasks(self.tasklist)
        self.load_schedule()
        self.update_calendar_events()
        messagebox.showinfo("Success", "Schedule generated and updated in the calendar.")

    def load_schedule(self):
        if not self.controller.schedule_file.exists():
            self.schedule = {}
            return
        try:
            with self.controller.schedule_file.open("r") as f:
                self.schedule = json.load(f)
        except json.JSONDecodeError:
            self.schedule = {}
            
    def update_calendar_events(self):
        self.cal.calevent_remove("all")
        
        if not self.schedule:
            return

        first_date_str = min(self.schedule.keys())
        first_date = datetime.strptime(first_date_str, "%Y-%m-%d")
        self.cal.selection_set(first_date)

        for date_str, events in self.schedule.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if events:
                    self.cal.calevent_create(date, "", tags=['task'])
            except ValueError:
                print(f"Warning: Could not parse date {date_str} from schedule.json")

        today = datetime.now().date()
        for task in self.tasklist:
            due_date = task['date'].date() if isinstance(task['date'], datetime) else datetime.strptime(task['date'], '%d-%m-%Y').date()
            if due_date == today:
                self.cal.calevent_create(due_date, "", tags=['deadline_today'])
            elif today < due_date <= today + timedelta(days=3):
                self.cal.calevent_create(due_date, "", tags=['deadline_soon'])

    def display_schedule_for_date(self, event):
            date = self.cal.get_date()
            self.schedule_display.delete("1.0", tk.END)
            
            date_obj = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")

            if self.schedule and date_obj in self.schedule and self.schedule[date_obj]:
                self.show_image_popup()
                events_for_day = self.schedule[date_obj]
                display_text = f"Schedule for {date}:\n\n"
                for event in events_for_day:
                    display_text += f"{event['name']}: {event['start_time']} - {event['end_time']}\n"
                self.schedule_display.insert("1.0", display_text)
            else:
                self.schedule_display.insert("1.0", f"No events scheduled for {date}.")

    def show_image_popup(self):
        popup = Toplevel(self)
        popup.title("Confucius")
        
        try:
            image = Image.open("confucius1.jpg")
            photo = ImageTk.PhotoImage(image)
            
            label = ttk.Label(popup, image=photo)
            label.image = photo 
            label.pack()

            quote = random.choice(self.controller.quotes)
            quote_label = ttk.Label(popup, text=quote, wraplength=400, justify="center")
            quote_label.pack(pady=10, padx=10)
            
        except FileNotFoundError:
            popup.destroy()
            messagebox.showerror("Error", "Image file not found: confucius1.jpg")


if __name__ == "__main__":
    app = App()
    app.mainloop()