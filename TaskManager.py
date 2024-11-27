#!/usr/bin/env python
# coding: utf-8

# In[25]:


task_deadlines = {}
#####################################################################################
import time
import datetime
import threading
from win10toast import ToastNotifier
toaster = ToastNotifier()
def check_and_notify_deadlines():
    while True:
        current_time = datetime.datetime.now()
        for task_index, deadline in task_deadlines.items():
            deadline_time = datetime.datetime.strptime(deadline, "%Y-%m-%d, %H:%M")
            time_remaining = deadline_time - current_time        
            if time_remaining <= datetime.timedelta(hours=24):
                task_text = tasks[task_index][0]
                message = f"Deadline for task: {task_text}, is near.\nLess than 24 hours left."
                title = "Deadline Reminder"
                
                toaster.show_toast(title, message, duration=10)      
        time.sleep(7200)

deadline_thread = threading.Thread(target=check_and_notify_deadlines)
deadline_thread.daemon = True
deadline_thread.start()

#####################################################################################
import pyperclip
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import datetime 
import csv
import os
import tkinter.messagebox
from tkinter.simpledialog import askstring
import json
import time
import tkinter

color_variables = []
json_path = 'C:/Users/Sezar/settings.txt'    
def read_json_from_file(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)
    
def set_color_variables(colors):
    for i in range(5):
        color_variables[i].set(colors[i])
        
def delete_all_tasks():
    global tasks, task_status, task_priority, task_deadlines
    confirmed = tkinter.messagebox.askokcancel("Delete All Tasks", "Are you sure you want to delete all tasks?")
    if confirmed:
        tasks = []
        task_status = []
        task_priority = []
        task_deadlines = {}
        update_listbox()
        update_report()
        save_data_to_file()  

        
task_name = ""  
task_status_local = ""
task_priority_local = ""
task_entry_time = ""
task_deadline = ""        
task_details_window = None
def show_task_details():
    global task_details_window, task_name, task_status_local, task_priority_local, task_entry_time, task_deadline

    if task_details_window is not None:
        task_details_window.destroy()

    task_details_window = tk.Toplevel(root)
    #task_details_window.geometry("200x200")

    selected_task_indices = list(listbox.curselection())
    if selected_task_indices:
        task_index = selected_task_indices[0]

        task_name = tasks[task_index][0]
        task_status_local = "Completed" if task_status[task_index] else "Not Completed"

        if task_index < len(task_priority):
            task_priority_local = task_priority[task_index]
        else:
            task_priority_local = "N/A"

        task_entry_time = tasks[task_index][2]

        if task_index in task_deadlines:
            task_deadline = task_deadlines[task_index]
        else:
            task_deadline = "No Deadline"

        #task_details = = f"Task Name: {task_name}\nStatus: {task_status_local}\nPriority: {task_priority_local}\nEntry Date: {task_entry_time}\nDeadline: {task_deadline}"
        task_details1 = f"Task Name: {task_name}"
        task_details2 = f"Status: {task_status_local}"
        task_details3 = f"Priority: {task_priority_local}"
        task_details4 = f"Entry Date: {task_entry_time}"
        task_details5 = f"Deadline: {task_deadline}"

        spacer_label1 = tk.Label(task_details_window, text="")
        spacer_label1.pack()
        info_label1 = tk.Label(task_details_window, text=task_details1)
        info_label1.pack()
        info_label2 = tk.Label(task_details_window, text=task_details2)
        info_label2.pack()
        info_label3 = tk.Label(task_details_window, text=task_details3)
        info_label3.pack()
        info_label4 = tk.Label(task_details_window, text=task_details4)
        info_label4.pack()
        info_label5 = tk.Label(task_details_window, text=task_details5)
        info_label5.pack()

        spacer_label2 = tk.Label(task_details_window, text="")
        spacer_label2.pack()

        copy_to_clipboard_button = tk.Button(task_details_window, text="Copy to Clipboard", command=copy_task_details_to_clipboard)
        copy_to_clipboard_button.pack()
        
def copy_task_details_to_clipboard():
    task_details = f"Task Name: {task_name}\nStatus: {task_status_local}\nPriority: {task_priority_local}\nEntry Date: {task_entry_time}\nDeadline: {task_deadline}"
    pyperclip.copy(task_details)
    tkinter.messagebox.showinfo("Copy to Clipboard", "Task Details Copied to Clipboard!")
    task_details_window.destroy()

def set_deadline():
    selected_task_indices = list(listbox.curselection())
    if selected_task_indices:
        task_index = selected_task_indices[0]
        task_text = tasks[task_index][0]

        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        date_prompt = "Set a deadline date for task (YYYY-MM-DD, or press Enter for default 'Tomorrow'):"
        while True:
            date = askstring("Set Deadline Date", date_prompt, initialvalue=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            if date is not None:
                if validate_date_format(date):
                    deadline_date = datetime.datetime.strptime(date, "%Y-%m-%d")
                    current_date = datetime.datetime.now()
                    if deadline_date >= current_date:
                        break
                    else:
                        tkinter.messagebox.showerror("Invalid Deadline Date", "The deadline cannot be earlier than the current date.")
                else:
                    tkinter.messagebox.showerror("Invalid Deadline Date", "Please enter a valid date format (YYYY-MM-DD)")
            else:
                break 
                return 

        time_prompt = f"Set a deadline time for task (HH:MM, or press Enter for default 12:00):"
        time = askstring("Set Deadline Time", time_prompt, initialvalue='12:00')

        if time is not None:
            if validate_time_format(time):
                task_deadlines[task_index] = f"{date}, {time}"
            else:
                tkinter.messagebox.showerror("Invalid Deadline Time", "Please enter a valid time format (HH:MM)")
        else:
            #task_deadlines[task_index] = f"{date}, 12:00"
            return
        
        update_listbox()
        save_data_to_file()

def validate_deadline_format(deadline):
    date, time = deadline.split(', ')
    if not validate_date_format(date):
        return False
    if time:
        if not validate_time_format(time):
            return False
    return True                
                
def validate_date_format(date):
    try:
        year, month, day = map(int, date.split('-'))
        if not (1 <= month <= 12) or not (1 <= day <= 31):
            return False
    except ValueError:
        return False
    return True

def validate_time_format(time):
    try:
        hours, minutes = map(int, time.split(':'))
        if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
            return False
    except ValueError:
        return False
    return True
    
root = tk.Tk()
color_variables = [tk.StringVar() for _ in range(5)]
if os.path.exists(json_path):
    with open(json_path, 'r') as file:
        your_json = json.load(file)
        user_colors = your_json.get("user_colors", [])
        for i in range(5):
            if i < len(user_colors):
                color_variables[i].set(user_colors[i])
            else:
                color_variables[i].set("red")
else:
    default_colors = ["blue", "purple", "green", "darkorange", "red"]
    for i in range(5):
        color_variables[i].set(default_colors[i])

def load_settings():
    try:
        with open('settings.txt', 'r') as settings_file:
            settings = json.load(settings_file)
            user_colors = settings.get("user_colors", [])

            for i, color in enumerate(user_colors):
                if i < len(color_variables):
                    color_variables[i].set(color)
    except FileNotFoundError:
        pass

load_settings()

tasks = []

selected_task_indices = []

settings_window = None
def open_settings_window():
    global settings_window
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    color_label = tk.Label(settings_window, text="Choose your desired colors:")
    color_label.pack()

    reset_button = tk.Button(settings_window, text="Reset to Default", command=reset_to_default_colors)
    reset_button.pack()

    for i in range(1, 6):
        color_label = tk.Label(settings_window, text=f"Priority {i}:")
        color_label.pack()
        color_variable = tk.StringVar()
        color_entry = ttk.Combobox(settings_window, textvariable=color_variable, values=["black", "gray", "silver", "darkred", "red","brown", "chocolate", "darkkhaki", "darkorange", "orange", "gold", "yellow","green", "olive", "lime", "blue", "aqua", "darkcyan", "cyan", "purple", "magenta", "hotpink","white"])
        color_entry.pack()
        color_variables[i - 1] = color_variable

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack()

def reset_to_default_colors():
    for i in range(5):
        color_variables[i].set(["blue", "purple", "green", "darkorange", "red"][i])     
            
def save_settings():
    user_colors = [color_variable.get() for color_variable in color_variables[:5]]
    valid_colors = ["black", "gray", "silver", "darkred", "red", "brown", "chocolate", "darkkhaki", "darkorange", "orange", "gold", "yellow", "green", "olive", "lime", "blue", "aqua", "darkcyan", "cyan", "purple", "magenta", "hotpink", "white"]
    for color in user_colors:
        if color not in valid_colors:
            tkinter.messagebox.showerror("Invalid Color", f"Color '{color}' is not a valid color. \nPlease fill all the blanks with the valid colors.")
            return  

    settings = {
        "user_colors": user_colors
    }

    with open('settings.txt', 'w') as settings_file:
        json.dump(settings, settings_file)

    update_listbox()

def show_context_menu(event):
    selected_task_indices = list(listbox.curselection())
    if selected_task_indices:
        task_index = selected_task_indices[0]
        task_text = tasks[task_index][0]

        toggle_command = lambda index=task_index: toggle_task(index)  
        local_context_menu = tk.Menu(root, tearoff=0)
        local_context_menu.add_command(label="Set a Deadline", command=lambda: set_deadline())
        local_context_menu.add_command(label="Edit Task", command=lambda: edit_task())
        local_context_menu.add_command(label="Toggle Task", command=toggle_command)
        local_context_menu.add_command(label="Remove Task", command=lambda: remove_task())
        local_context_menu.add_command(label="Show Task Details", command=lambda: show_task_details())
        local_context_menu.add_command(label="Copy Selected Task to Clipboard", command=lambda: copy_selected_task_to_clipboard())
        local_context_menu.add_command(label="Copy All Tasks to Clipboard", command=lambda: copy_all_tasks_to_clipboard())
        local_context_menu.add_command(label="Show Remaining Tasks", command=lambda: show_remaining_tasks())
        local_context_menu.add_command(label="Show Completed Tasks", command=lambda: show_completed_tasks())
        local_context_menu.add_command(label="Show All Tasks", command=lambda: show_all_tasks())
        local_context_menu.add_command(label="Remove All Tasks", command=lambda: delete_all_tasks())
        local_context_menu.add_command(label="Settings", command=lambda: open_settings_window())
        local_context_menu.add_command(label="Quit", command=lambda: on_closing())

        local_context_menu.post(event.x_root, event.y_root)    
    
def show_remaining_tasks():
    remaining_task_indices = [i for i, status in enumerate(task_status) if not status]
    update_listbox(remaining_task_indices)                  

def show_completed_tasks():
    completed_task_indices = [i for i, status in enumerate(task_status) if status]
    update_listbox(completed_task_indices)
    
def show_all_tasks():
    all_task_indices = list(range(len(tasks)))
    update_listbox(all_task_indices)
                       
def on_closing():
    root.destroy()

task_names = []
    
def copy_selected_task_to_clipboard():
    selected_task_indices = list(listbox.curselection())
    if selected_task_indices:
        task_index = selected_task_indices[0]
        task_text = tasks[task_index][0]
        pyperclip.copy(task_text)
        tkinter.messagebox.showinfo("Copy to Clipboard", "Task Copied to Clipboard!")

def copy_all_tasks_to_clipboard():
    result_string = '\n'.join(task[0] for task in tasks)
    pyperclip.copy(result_string)
    tkinter.messagebox.showinfo("Copy All Tasks to Clipboard", "All Tasks Copied to Clipboard")

def option_selected(option):
    print(f"Selected option: {option}")

for i in range(len(tasks)):
    listbox.bind("<Button-3>", show_context_menu)
    
editing_task_index = None

if not os.path.exists('tasks.csv'):
    with open('tasks.csv', 'w', newline='') as file:
        pass   

def toggle_task(task_index):
    task_status[task_index] = not task_status[task_index]
    update_listbox()
    update_report()
    save_data_to_file()

def toggle_task_with_double_click(event):
    selected_task_indices = list(listbox.curselection())
    if selected_task_indices:
        task_index = selected_task_indices[0]
        toggle_task(task_index) 
        
task_priority = [] 
task_status = []
def add_task():
    global editing_task_index
    new_task = entry.get()
    priority = priority_combobox.get()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if new_task:
        if editing_task_index is not None:
            tasks[editing_task_index][0] = new_task
            tasks[editing_task_index][1] = priority
            tasks[editing_task_index][2] = current_time
            entry.delete(0, tk.END)
            update_listbox()
            editing_task_index = None
        else:
            new_task_data = [new_task, priority, current_time]
            tasks.append(new_task_data)
            task_status.append(False)
            task_priority.append(priority)
            entry.delete(0, tk.END)
            update_listbox()

    update_report()
    save_data_to_file()
    
def add_task_on_enter(event):
    add_task()

def remove_task():
    global tasks, task_status, task_priority, task_deadlines
    selected_task_indices = list(listbox.curselection())
    selected_task_indices.reverse()
    for index in selected_task_indices:
        if index in task_deadlines:
            del task_deadlines[index] 
        del tasks[index]
        del task_status[index]
        del task_priority[index]
    update_listbox()
    update_report()
    save_data_to_file()    
    
def edit_task():
    global editing_task_index
    selected_task_indices = list(listbox.curselection())
    if selected_task_indices:
        editing_task_index = selected_task_indices[0]
        entry.delete(0, tk.END)
        entry.insert(0, tasks[editing_task_index][0])
        priority_combobox.set(task_priority[editing_task_index])

def save_edited_task():
    global editing_task_index
    if editing_task_index is not None:
        new_task = entry.get()
        priority = priority_combobox.get()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if new_task:
            tasks[editing_task_index][0] = new_task
            task_priority[editing_task_index] = priority
            tasks[editing_task_index][2] = current_time
            entry.delete(0, tk.END)
            update_listbox()
            editing_task_index = None
    save_data_to_file()

def perform_search():
    query = search_entry.get()
    matching_tasks = []
    for i, task in enumerate(tasks):
        if query.lower() in task[0].lower():
            matching_tasks.append(i)
    update_listbox(matching_tasks)

def update_listbox(task_indices=None):
    listbox.delete(0, tk.END)
    if task_indices is None:
        task_indices = range(len(tasks))
    for i, task_index in enumerate(task_indices):
        task_index = int(task_index)  # تبدیل به عدد صحیح
        if task_index < len(tasks):
            listbox.bind("<Button-3>", lambda event, i=i: show_context_menu(event))
            status = "✓" if task_status[task_index] else " "
            priority = int(task_priority[task_index])
            task_number = task_index + 1
            
            if task_index in task_deadlines:
                deadline = task_deadlines[task_index]
            else:
                deadline = "No Deadline"  
            text_color = color_variables[priority - 1].get()  
            listbox.insert(tk.END, f"  [{status}] [P: {priority}] No. {task_number}: {tasks[task_index][0]}     {tasks[task_index][2]}     Deadline: {deadline}")
            listbox.itemconfig(i, {'fg': text_color})

    listbox_frame.update_idletasks()
    list_canvas.config(scrollregion=list_canvas.bbox("all"))
    
def update_report():
    done_tasks = sum(task_status)
    total_tasks = len(tasks)
    if total_tasks == 0:
        report_label1.config(text="")
        report_label2.config(text="No tasks added.")
    else:
        done_percentage = (done_tasks / total_tasks) * 100
        report_label1.config(text=f"{total_tasks} tasks in total")
        report_label2.config(text=f"Done: {done_tasks}, Remaining: {total_tasks - done_tasks}, Progress: {done_percentage:.2f}%")       
        
def save_data_to_file():
    with open('tasks.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for task_index in range(len(tasks)):
            task = tasks[task_index][0]
            status = task_status[task_index]
            priority = task_priority[task_index]
            deadline = task_deadlines.get(task_index, "No Deadline")
            entered_time = tasks[task_index][2] 
            writer.writerow([task, status, priority, entered_time, deadline])            
            
def load_data_from_file():
    try:
        with open('tasks.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 5:  
                    task, status, priority, entered_time, deadline = row  # دسترسی به entered_time
                    tasks.append([task, priority, entered_time])  # اضافه کردن entered_time به tasks
                    task_status.append(status == 'True')
                    task_priority.append(priority)
                    if deadline != "No Deadline":
                        task_deadlines[len(tasks) - 1] = deadline
    except FileNotFoundError:
        pass

#finish
               

root.title("TaskManager")

empty_label0 = tk.Label(root, text="", height=1)
empty_label0.pack()

main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

title_label1 = tk.Label(left_frame, text="New Task:", font=("Arial", 11), height=1)
title_label1.pack()

entry = tk.Entry(left_frame, width=50)
entry.pack()
entry.bind("<Return>", add_task_on_enter)

priority_label = tk.Label(left_frame, text="Priority:", font=("Arial", 11))
priority_label.pack()

priority_combobox = ttk.Combobox(left_frame, values=["1", "2", "3", "4", "5"], width=6)
priority_combobox.set("1")
priority_combobox.pack()

add_icon = PhotoImage(file="images/add.png")
add_button = tk.Button(left_frame, image=add_icon, command=add_task)
add_button.pack()

title_label2 = tk.Label(right_frame, text="Look among your tasks:", font=("Arial", 11), height=1)
title_label2.pack()

search_entry = tk.Entry(right_frame, width=21)
search_entry.pack()

search_icon = PhotoImage(file="images/search.png")
search_button = tk.Button(right_frame, image=search_icon, command=perform_search)
search_button.pack()

empty_label1 = tk.Label(root, text="", height=1)
empty_label1.pack()

list_canvas = tk.Canvas(root, height=300, width=560)
list_canvas.pack()

scrollbar = tk.Scrollbar(root, command=list_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
list_canvas.config(yscrollcommand=scrollbar.set)
scrollbar.config(width=20)

listbox_frame = tk.Frame(list_canvas)
list_canvas.create_window((0, 0), window=listbox_frame, anchor='nw')

listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, width=70, height=20, font=("Calibri", 12))
listbox.pack()

listbox.bind("<Double-Button-1>", toggle_task_with_double_click)

empty_label2 = tk.Label(root, text="", height=1)
empty_label2.pack()

listbox_frame.update_idletasks()
list_canvas.config(scrollregion=list_canvas.bbox("all"))                     
                     
edit_icon = PhotoImage(file="images/edit.png")
edit_button = tk.Button(root, image=edit_icon, command=edit_task)
toggle_icon = PhotoImage(file="images/tick.png")
toggle_button = tk.Button(root, image=toggle_icon, command=lambda: [toggle_task(i) for i in listbox.curselection()])
delete_icon = PhotoImage(file="images/delete.png")
remove_button = tk.Button(root, image=delete_icon, command=remove_task)

button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)
edit_button.pack(side=tk.LEFT)
toggle_button.pack(side=tk.LEFT)
remove_button.pack(side=tk.LEFT)

report_label1 = tk.Label(root, text="", height=1)
report_label1.pack()

report_label2 = tk.Label(root, text="", height=1)
report_label2.pack()

load_data_from_file()
update_listbox()

x_scrollbar = tk.Scrollbar(root, orient="horizontal")
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
listbox.config(xscrollcommand=x_scrollbar.set)
x_scrollbar.config(command=listbox.xview)
x_scrollbar.config(width=20)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


# In[ ]:




