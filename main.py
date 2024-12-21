import tkinter as tk
from tkinter import ttk, messagebox
import os

# File to store habits persistently
HABITS_FILE = "habits.txt"


# Function to load habits from file
def load_habits():
    if os.path.exists(HABITS_FILE):
        with open(HABITS_FILE, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
    return []


# Function to save habits to file
def save_habits(habits):
    with open(HABITS_FILE, "w") as file:
        for habit in habits:
            file.write(",".join(habit) + "\n")


# Function to add a new habit
def add_habit():
    habit_name = habit_name_entry.get().strip()
    if habit_name:
        if any(habit[0] == habit_name for habit in habits):
            messagebox.showerror("Error", "Habit already exists.")
        else:
            habits.append([habit_name, "0"])
            save_habits(habits)
            update_habit_list()
            habit_name_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Habit name cannot be empty.")


# Function to mark a habit as done
def mark_done(index):
    habits[index][1] = str(int(habits[index][1]) + 1)
    save_habits(habits)
    update_habit_list()


# Function to reset a habit's streak
def reset_streak(index):
    habits[index][1] = "0"
    save_habits(habits)
    update_habit_list()


# Function to delete a habit
def delete_habit(index):
    if messagebox.askyesno("Delete Habit", f"Are you sure you want to delete the habit '{habits[index][0]}'?"):
        del habits[index]
        save_habits(habits)
        update_habit_list()


# Function to update the habit list display
def update_habit_list():
    for widget in habit_frame.winfo_children():
        widget.destroy()

    if not habits:
        ttk.Label(habit_frame, text="No habits to display. Add a new habit!", font=("Arial", 14)).pack(pady=10)
    else:
        for i, (name, count) in enumerate(habits):
            row_frame = ttk.Frame(habit_frame)
            row_frame.pack(fill="x", pady=5)

            ttk.Label(row_frame, text=name, font=("Arial", 14)).pack(side="left", padx=10)
            ttk.Label(row_frame, text=f"Streak: {count}", font=("Arial", 14)).pack(side="left", padx=10)

            ttk.Button(row_frame, text="✔️ Done", command=lambda i=i: mark_done(i)).pack(side="right", padx=5)
            ttk.Button(row_frame, text="🔄 Reset", command=lambda i=i: reset_streak(i)).pack(side="right", padx=5)
            ttk.Button(row_frame, text="❌ Delete", command=lambda i=i: delete_habit(i)).pack(side="right", padx=5)


# Load initial habits
habits = load_habits()

# Create the GUI
root = tk.Tk()
root.title("Habit Tracker")
root.geometry("600x500")
root.resizable(False, False)

# Style
style = ttk.Style()
style.configure("TLabel", font=("Arial", 14))
style.configure("TButton", font=("Arial", 12))
style.configure("Header.TLabel", font=("Arial", 20, "bold"), foreground="#3b5998")

# Header
header = ttk.Label(root, text="Habit Tracker", style="Header.TLabel")
header.pack(pady=10)

# Habit Input
habit_input_frame = ttk.Frame(root)
habit_input_frame.pack(pady=20)

ttk.Label(habit_input_frame, text="Add New Habit:").grid(row=0, column=0, padx=10, pady=10)
habit_name_entry = ttk.Entry(habit_input_frame, width=30, font=("Arial", 14))
habit_name_entry.grid(row=0, column=1, padx=10, pady=10)

add_habit_button = ttk.Button(habit_input_frame, text="Add Habit", command=add_habit)
add_habit_button.grid(row=0, column=2, padx=10, pady=10)

# Habit List
habit_frame = ttk.Frame(root)
habit_frame.pack(fill="both", expand=True, padx=10, pady=10)

update_habit_list()

# Footer
footer = ttk.Label(root, text="Made with ❤️ using Python", font=("Arial", 10), foreground="#555")
footer.pack(pady=10)

# Start the app
root.mainloop()