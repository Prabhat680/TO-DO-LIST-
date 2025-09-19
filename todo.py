import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def refresh_tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔" if task["done"] else "✘"
        task_listbox.insert(tk.END, f"[{status}] {task['task']}")

def add_task():
    task_name = simpledialog.askstring("Add Task", "Enter task:")
    if task_name:
        tasks.append({"task": task_name, "done": False})
        save_tasks(tasks)
        refresh_tasks()

def mark_done():
    try:
        selected_index = task_listbox.curselection()[0]
        tasks[selected_index]["done"] = True
        save_tasks(tasks)
        refresh_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as done.")

def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        deleted_task = tasks.pop(selected_index)
        save_tasks(tasks)
        refresh_tasks()
        messagebox.showinfo("Deleted", f"Task '{deleted_task['task']}' deleted!")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")


tasks = load_tasks()

root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x400")
root.configure(bg="#f0f0f0")


title_label = tk.Label(root, text="📝 To-Do List", font=("Arial", 18, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)


task_listbox = tk.Listbox(root, font=("Arial", 12), width=40, height=15, selectbackground="#a6a6a6")
task_listbox.pack(pady=5)
refresh_tasks()


button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Task", command=add_task, width=10, bg="#4CAF50", fg="white")
add_button.grid(row=0, column=0, padx=5)

done_button = tk.Button(button_frame, text="Mark Done", command=mark_done, width=10, bg="#2196F3", fg="white")
done_button.grid(row=0, column=1, padx=5)

delete_button = tk.Button(button_frame, text="Delete", command=delete_task, width=10, bg="#f44336", fg="white")
delete_button.grid(row=0, column=2, padx=5)

root.mainloop()
