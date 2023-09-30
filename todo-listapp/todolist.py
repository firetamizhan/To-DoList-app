import tkinter as tk
import mysql.connector


class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.task_listbox = tk.Listbox(root, width=5100, height=10)

        # Configure your MySQL connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jothiram@2119",
            database="todolist"

        )
        self.cursor = self.conn.cursor()

        # Create the tasks table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                task TEXT NOT NULL,
                                status INT DEFAULT 0
                            )''')
        self.conn.commit()

        self.tasks = []
        self.load_tasks()

        # Initialize the task_listbox attribute
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        # ... other initialization code ...

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(root, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        clear_button = tk.Button(root, text="Clear Completed", command=self.clear_completed)
        clear_button.grid(row=0, column=2, padx=10, pady=10)

        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.update_task_listbox()

        self.task_listbox.bind("<<ListboxSelect>>", self.toggle_status)

    # Add, load, and update methods would remain similar, but use MySQL queries.
    # You'll need to replace the SQLite queries with MySQL queries.

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            # Modify this method to insert tasks into MySQL.
            query = "INSERT INTO tasks (task, status) VALUES (%s, %s)"
            values = (task_text, 0)  # 0 for incomplete
            self.cursor.execute(query, values)
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()



    def load_tasks(self):
        self.tasks = []
        # Modify this method to load tasks from MySQL.
        query = "SELECT id, task, status FROM tasks"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            task = {"id": row[0], "text": row[1], "status": row[2]}
            self.tasks.append(task)
        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status_icon = "✓" if task["status"] else " "
            self.task_listbox.insert(tk.END, f"{status_icon} {task['text']}")

    def new_method(self):
        self.task_listbox.delete(0, tk.END)

    def toggle_status(self, event):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_index = int(selected_task_index[0])
            selected_task = self.tasks[selected_task_index]
            new_status = 1 - selected_task["status"]
            task_id = selected_task["id"]
            # Modify this method to toggle task status in MySQL.
            query = "UPDATE tasks SET status = %s WHERE id = %s"
            values = (new_status, task_id)
            self.cursor.execute(query, values)
            self.conn.commit()
            self.load_tasks()

    def clear_completed(self):
        completed_task_ids = [task["id"] for task in self.tasks if task["status"]]
        for task_id in completed_task_ids:
            # Modify this method to clear completed tasks from MySQL.
            query = "DELETE FROM tasks WHERE id = %s"
            values = (task_id,)
            self.cursor.execute(query, values)
        self.conn.commit()
        self.load_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
