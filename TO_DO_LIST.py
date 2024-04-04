import tkinter as tk
from tkinter import *
import sqlite3 as sql
from tkinter import messagebox

def add_task():  
    task_string = entry_task.get()  
    if len(task_string) == 0:  
        messagebox.showinfo('Error', 'Field is Empty.')  
    else:    
        tasks.append(task_string)   
        the_cursor.execute('insert into tasks values (?)', (task_string ,))    
        list_update()    
        entry_task.delete(0, 'end') 

def delete_task():  
    try:  
        the_value = listbox_tasks.get(listbox_tasks.curselection())    
        if the_value in tasks:  
            tasks.remove(the_value)    
            list_update()   
            the_cursor.execute('delete from tasks where title = ?', (the_value,))  
    except:   
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')
def delete_all_tasks():  
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')  
    if message_box == True:    
        while(len(tasks) != 0):    
            tasks.pop()    
        the_cursor.execute('delete from tasks')   
        list_update()         

def list_update():    
    clear_list()    
    for task in tasks:    
        listbox_tasks.insert('end', task)

def clear_list():   
    listbox_tasks.delete(0, 'end')  
  
def close():    
    print(tasks)   
    root.destroy()  
    
def retrieve_database():    
    while(len(tasks) != 0):    
        tasks.pop()    
    for row in the_cursor.execute('select title from tasks'):    
        tasks.append(row[0])              


root=Tk()
root.title("To Do List")
root.configure()
root.geometry("400x650+400+100")
root.resizable(False,False)

the_connection = sql.connect('listOfTasks.db')   
the_cursor = the_connection.cursor()   
the_cursor.execute('create table if not exists tasks (title text)')  
    
tasks = []  

fsc=Frame(root,bg="#32405b",height=70,width=400)
heading= Label(fsc, text="TO DO LIST", font="arial 20 bold", fg="white", bg="#32405b") 
heading.place(x=130,y=20)
fsc.pack()

fsc=Frame(root,height=50,width=400)
fsc.pack()

fsc=Frame(root, bg="WHITE")
entry_task = tk.Entry(fsc, width=18,font="arial 20",border=0)
entry_task.pack(side=LEFT,padx=20,pady=7)
button_add_task=Button(fsc, text="ADD" ,font ="ARIAL 15",borderwidth = 0,width=6,fg="white", bg="#5a95ff",command=add_task)
button_add_task.pack(side=LEFT)
button_add_task
fsc.pack()

frame_tasks = tk.Frame(root, bg="#c1f4c2")
frame_tasks.pack(pady=10)

listbox_tasks = tk.Listbox(frame_tasks,font="arial 20",fg="white", height=10, width=25, bg="#32405b", border=0)
listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.BOTH)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

fsc=Frame(root)
button_delete_task = tk.Button(fsc, text="Delete Task" ,font ="ARIAL 15 bold",borderwidth = 0, fg="white",bg="red",command=delete_task)
button_delete_task.pack(side=LEFT,padx=10)
button_all_delete_task = tk.Button(fsc, text="Delete All" ,font ="ARIAL 15 bold",borderwidth = 0, fg="white",bg="red",command=delete_all_tasks)
button_all_delete_task.pack(side=LEFT,padx=10)
fsc.pack()

retrieve_database()  
list_update()    
root.mainloop()    
the_connection.commit()  
the_cursor.close()