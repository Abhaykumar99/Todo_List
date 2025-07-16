from tkinter import *
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "tasks.json")

# ── Colors ─────────────────────────────────────────────────────────────────
BG       = "#1e1e2e"
CARD     = "#2a2a3e"
ACCENT   = "#89b4fa"
GREEN    = "#a6e3a1"
RED      = "#f38ba8"
YELLOW   = "#f9e2af"
GRAY     = "#585b70"
TEXT     = "#cdd6f4"
FONT     = ("Segoe UI", 11)
FONT_B   = ("Segoe UI", 11, "bold")

# priority ke liye color map — High=red, Medium=yellow, Low=green
PRIORITY_COLOR = {"High": RED, "Medium": YELLOW, "Low": GREEN}


def load_tasks():
    # JSON file se tasks load karo — file nahi hai toh empty list
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    # current tasks list ko JSON mein save karo
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def refresh_list():
    # listbox clear karo aur dobara sab tasks dikhao
    task_list.delete(0, END)
    tasks = load_tasks()

    for i, t in enumerate(tasks):
        status = "✅" if t["done"] else "⬜"
        label  = f"{status}  [{t['priority']}]  {t['task']}  —  {t['date']}"
        task_list.insert(END, label)

        # done tasks gray, baaki priority color se
        if t["done"]:
            task_list.itemconfig(i, fg=GRAY)
        else:
            task_list.itemconfig(i, fg=PRIORITY_COLOR.get(t["priority"], TEXT))

    # total aur done count update karo
    done  = sum(1 for t in tasks if t["done"])
    total = len(tasks)
    count_label.config(text=f"Total: {total}   Done: {done}   Pending: {total - done}")


def add_task():
    task_text = task_entry.get().strip()
    if not task_text:
        messagebox.showwarning("Error", "Task likhna toh padega!", parent=window)
        return

    tasks = load_tasks()
    tasks.append({
        "task":     task_text,
        "priority": priority_var.get(),
        "done":     False,
        "date":     datetime.now().strftime("%d-%m %H:%M"),
    })
    save_tasks(tasks)
    task_entry.delete(0, END)
    refresh_list()


def mark_done():
    # selected task ko done/undone toggle karo
    selected = task_list.curselection()
    if not selected:
        return
    tasks = load_tasks()
    idx = selected[0]
    tasks[idx]["done"] = not tasks[idx]["done"]  # toggle karo
    save_tasks(tasks)
    refresh_list()


def delete_task():
    # selected task permanently delete karo
    selected = task_list.curselection()
    if not selected:
        return
    tasks = load_tasks()
    idx = selected[0]
    confirm = messagebox.askyesno("Delete", f"Delete: '{tasks[idx]['task']}'?", parent=window)
    if confirm:
        tasks.pop(idx)
        save_tasks(tasks)
        refresh_list()


def clear_done():
    # jo tasks done hain unhe sab ek saath hata do
    tasks = [t for t in load_tasks() if not t["done"]]
    save_tasks(tasks)
    refresh_list()


# ── Window ─────────────────────────────────────────────────────────────────
window = Tk()
window.title("Day 33 – To-Do List")
window.config(bg=BG, padx=20, pady=20)
window.resizable(False, False)

# ── Header ─────────────────────────────────────────────────────────────────
Label(window, text="📝  My To-Do List", bg=BG, fg=ACCENT,
      font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 15))

# ── Input Row ──────────────────────────────────────────────────────────────
task_entry = Entry(window, width=35, bg=CARD, fg=TEXT,
                   insertbackground=TEXT, font=FONT, relief="flat")
task_entry.grid(row=1, column=0, padx=(0, 8), ipady=6)
task_entry.bind("<Return>", lambda e: add_task())  # Enter dabane par bhi add ho

# priority dropdown
priority_var = StringVar(value="Medium")
priority_menu = OptionMenu(window, priority_var, "High", "Medium", "Low")
priority_menu.config(bg=CARD, fg=TEXT, font=FONT, relief="flat",
                     activebackground=ACCENT, width=7)
priority_menu.grid(row=1, column=1, padx=(0, 8))

Button(window, text="Add ➕", bg=ACCENT, fg=BG, font=FONT_B,
       relief="flat", padx=10, command=add_task).grid(row=1, column=2)

# ── Task Listbox ────────────────────────────────────────────────────────────
list_frame = Frame(window, bg=CARD)
list_frame.grid(row=2, column=0, columnspan=3, pady=12, sticky="ew")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=RIGHT, fill=Y)

# yahan tasks dikhenge — ek ek row mein
task_list = Listbox(list_frame, width=65, height=14, bg=CARD, fg=TEXT,
                    font=FONT, selectbackground=ACCENT, selectforeground=BG,
                    relief="flat", yscrollcommand=scrollbar.set,
                    activestyle="none")
task_list.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=task_list.yview)

# ── Action Buttons ─────────────────────────────────────────────────────────
btn_frame = Frame(window, bg=BG)
btn_frame.grid(row=3, column=0, columnspan=3, sticky="ew")

Button(btn_frame, text="✅ Mark Done", bg=GREEN, fg=BG, font=FONT_B,
       relief="flat", padx=10, pady=5, command=mark_done).pack(side=LEFT, padx=(0, 8))

Button(btn_frame, text="🗑️ Delete", bg=RED, fg=BG, font=FONT_B,
       relief="flat", padx=10, pady=5, command=delete_task).pack(side=LEFT, padx=(0, 8))

Button(btn_frame, text="🧹 Clear Done", bg=GRAY, fg=TEXT, font=FONT_B,
       relief="flat", padx=10, pady=5, command=clear_done).pack(side=LEFT)

# ── Count Label ────────────────────────────────────────────────────────────
count_label = Label(window, text="", bg=BG, fg=GRAY, font=("Segoe UI", 10))
count_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))

# app open hote hi existing tasks load karo
refresh_list()
window.mainloop()
