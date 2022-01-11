from os import stat
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Counter

class User:
    def __init__(self):
        self.role = 0
        self.uername = ""
        self.password = ""

    def validateLogin(self):
        
        q = "SELECT * FROM USER WHERE USERNAME = '" + self.username + "' AND PASSWORD = '" + self.password + "' AND ROLE = '" + str(self.role) + "';"
        cur.execute(q)

        rows = cur.fetchall()
        if len(rows) == 0:
            print("Login Successful!")
        else:
            print("Login Failed!")
        return len(rows) == 0


global users 
conn = sqlite3.connect('uwe.sqlite')
cur = conn.cursor()

def btn_clicked():
    users = User()
    def delete():
        selected = my_tree.focus()
        values = ('', ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), '', '', "Unoccupied", co.get(), ln8_entry.get(), '')
        my_tree.item(selected, text="", values=values)

        q = "UPDATE HALL SET LEASE_NUMBER = '', STUDENT_ID = '', STUDENT_NAME = '', DURATION = '', OCCUPANCY_STATUS = 'Unoccupied' WHERE HALL_NAME = '" + ln2_entry.get() + "' AND HALL_NUMBER = '" + ln3_entry.get() + "' AND ROOM_NUMBER = '" + ln4_entry.get() + "';"

        cur.execute(q)
        conn.commit()

        ln2_entry.config(state="normal")
        ln3_entry.config(state="normal")
        ln4_entry.config(state="normal")
        ln6_entry.config(state="normal")
        ln7_entry.config(state="normal")
        ln8_entry.config(state="normal")

        ln1_entry.delete(0, END)
        ln2_entry.delete(0, END)
        ln3_entry.delete(0, END)
        ln4_entry.delete(0, END)
        ln5_entry.delete(0, END)
        ln6_entry.delete(0, END)
        co.set("                            ")
        ln8_entry.delete(0, END)
        ln9_entry.delete(0, END)
        ln10_entry.delete(0, END)

        selected= my_tree.focus()

        values = my_tree.item(selected, 'values')

        ln1_entry.insert(0, values[0])
        ln2_entry.insert(0, values[1])
        ln3_entry.insert(0, values[2])
        ln4_entry.insert(0, values[3])
        ln10_entry.insert(0, values[4])
        ln5_entry.insert(0, values[5])
        ln6_entry.insert(0, values[6])
        co.set(values[7])
        ln8_entry.insert(0, values[8])
        ln9_entry.insert(0, values[9])

        ln2_entry.config(state="disable")
        ln3_entry.config(state="disable")
        ln4_entry.config(state="disable")
        ln6_entry.config(state="disable")
        ln8_entry.config(state="disable")

        if user == "Warden":
            ln1_entry.config(state="disable")
            ln5_entry.config(state="disable")
            ln9_entry.config(state="disable")
            ln10_entry.config(state="disable")

        if user == "Manager":
            ln7_entry.config(state="disable")

    def update():
        if user != "Warden":
            q = "SELECT * FROM HALL WHERE LEASE_NUMBER = '" + ln1_entry.get() + "' AND HALL_NUMBER = '" + ln3_entry.get() + "' AND ROOM_NUMBER = '" + ln4_entry.get() + "';"
            cur.execute(q)

            rows = cur.fetchall()
            if (co.get() == "Offline" or ln6_entry.get() == "Occupied") and len(rows) == 0:
                if co.get() == "Offline" and ln6_entry.get() == "Occupied":
                    messagebox.showerror("Room is Occupied and Offline!", "To add Lease the Room shouldn't be Occupied or Offline!")
                if co.get() == "Offline":
                    messagebox.showerror("Room is Offline!", "To add Lease the Room shouldn't be Offline!")
                else:
                    messagebox.showerror("Room is Occupied!", "To add Lease the Room shouldn't be Occupied!")

                return 0

            if ln1_entry.get() and ln10_entry.get() and ln5_entry.get() and ln9_entry.get():

                q = "SELECT * FROM HALL WHERE STUDENT_ID = '" + ln10_entry.get() + "' AND HALL_NUMBER != '" + ln3_entry.get() + "' AND ROOM_NUMBER != '" + ln4_entry.get() + "';"
                cur.execute(q)

                rows = cur.fetchall()

                if len(rows) != 0:
                    messagebox.showerror("Student Already Exists!", "Student has been allocated a Room already with this ID!")
                    return 0

                q = "SELECT * FROM HALL WHERE LEASE_NUMBER = '" + ln1_entry.get() + "' AND HALL_NUMBER != '" + ln3_entry.get() + "' AND ROOM_NUMBER != '" + ln4_entry.get() + "';"
                cur.execute(q)

                rows = cur.fetchall()

                if len(rows) != 0:
                    messagebox.showerror("Lease Already Exists!", "Existing list found with this number!")
                    return 0
            

            
                selected = my_tree.focus()
                values = (ln1_entry.get(), ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), ln10_entry.get(), ln5_entry.get(), "Occupied", co.get(), ln8_entry.get(), ln9_entry.get())
                my_tree.item(selected, text="", values=values)

                q = "UPDATE HALL SET LEASE_NUMBER = '" + ln1_entry.get() + "', STUDENT_ID = '" + ln10_entry.get() + "', STUDENT_NAME = '" + ln5_entry.get() + "', DURATION = '" + ln9_entry.get() + "', OCCUPANCY_STATUS = 'Occupied' WHERE HALL_NAME = '" + ln2_entry.get() + "' AND HALL_NUMBER = '" + ln3_entry.get() + "' AND ROOM_NUMBER = '" + ln4_entry.get() + "';"

                cur.execute(q)
                conn.commit()
            else:
                messagebox.showerror("Missing Data!", "Fill up all the required field to update!")
                return 0

            

        else:
            selected = my_tree.focus()
            values = (ln1_entry.get(), ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), ln10_entry.get(), ln5_entry.get(), ln6_entry.get(), co.get(), ln8_entry.get(), ln9_entry.get())
            my_tree.item(selected, text="", values=values)

            print(co.get())

            q = "UPDATE HALL SET CLEANING_STATUS = '" + co.get() + "' WHERE HALL_NAME = '" + ln2_entry.get() + "' AND HALL_NUMBER = '" + ln3_entry.get() + "' AND ROOM_NUMBER = '" + ln4_entry.get() + "';"

            cur.execute(q)
            conn.commit()


            
        ln2_entry.config(state="normal")
        ln3_entry.config(state="normal")
        ln4_entry.config(state="normal")
        ln6_entry.config(state="normal")
        ln7_entry.config(state="normal")
        ln8_entry.config(state="normal")

        ln1_entry.delete(0, END)
        ln2_entry.delete(0, END)
        ln3_entry.delete(0, END)
        ln4_entry.delete(0, END)
        ln5_entry.delete(0, END)
        ln6_entry.delete(0, END)
        co.set("                            ")
        ln8_entry.delete(0, END)
        ln9_entry.delete(0, END)
        ln10_entry.delete(0, END)

        selected= my_tree.focus()

        values = my_tree.item(selected, 'values')

        ln1_entry.insert(0, values[0])
        ln2_entry.insert(0, values[1])
        ln3_entry.insert(0, values[2])
        ln4_entry.insert(0, values[3])
        ln10_entry.insert(0, values[4])
        ln5_entry.insert(0, values[5])
        ln6_entry.insert(0, values[6])
        co.set(values[7])
        ln8_entry.insert(0, values[8])
        ln9_entry.insert(0, values[9])
        

        ln2_entry.config(state="disable")
        ln3_entry.config(state="disable")
        ln4_entry.config(state="disable")
        ln6_entry.config(state="disable")
        ln8_entry.config(state="disable")

        if user == "Warden":
            ln1_entry.config(state="disable")
            ln5_entry.config(state="disable")
            ln9_entry.config(state="disable")
            ln10_entry.config(state="disable")

        if user == "Manager":
            ln7_entry.config(state="disable")

    def select(e):
        ln2_entry.config(state="normal")
        ln3_entry.config(state="normal")
        ln4_entry.config(state="normal")
        ln6_entry.config(state="normal")
        ln7_entry.config(state="normal")
        ln8_entry.config(state="normal")

        ln1_entry.delete(0, END)
        ln2_entry.delete(0, END)
        ln3_entry.delete(0, END)
        ln4_entry.delete(0, END)
        ln5_entry.delete(0, END)
        ln6_entry.delete(0, END)
        co.set("                            ")
        ln8_entry.delete(0, END)
        ln9_entry.delete(0, END)
        ln10_entry.delete(0, END)

        selected= my_tree.focus()

        values = my_tree.item(selected, 'values')

        ln1_entry.insert(0, values[0])
        ln2_entry.insert(0, values[1])
        ln3_entry.insert(0, values[2])
        ln4_entry.insert(0, values[3])
        ln10_entry.insert(0, values[4])
        ln5_entry.insert(0, values[5])
        ln6_entry.insert(0, values[6])
        co.set(values[7])
        ln8_entry.insert(0, values[8])
        ln9_entry.insert(0, values[9])

        ln2_entry.config(state="disable")
        ln3_entry.config(state="disable")
        ln4_entry.config(state="disable")
        ln6_entry.config(state="disable")
        ln8_entry.config(state="disable")

        if user == "Warden":
            ln1_entry.config(state="disable")
            ln5_entry.config(state="disable")
            ln9_entry.config(state="disable")
            ln10_entry.config(state="disable")

        if user == "Manager":
            ln7_entry.config(state="disable")



    role = n.get()
    user = n.get()
    users.username = entry1.get()
    users.password = entry0.get()

    if role == "Admin":
        users.role = 1
    elif role == "Manager":
        users.role = 2
    elif role == "Warden":
        users.role = 3
    else:
        users.role = -1
        messagebox.showwarning("Invalid User Role!", "Please choose a Role to Login!")
        return 0

    isLoginValid = users.validateLogin()


    # q = "SELECT * FROM USER WHERE USERNAME = '" + user.username + "' AND PASSWORD = '" + user.password + "' AND ROLE = '" + str(usdrrole) + "';"
    # cur.execute(q)

    # rows = cur.fetchall()

    if isLoginValid:
        messagebox.showerror("Invalid Credential!", "Invalid Username or Password!")
    else:
        messagebox.showinfo("Success", "Login Success!")
        newWindow = Toplevel(window)
 
        # sets the title of the
        # Toplevel widget
        newWindow.title("UWE " + user + " Dashboard")
    
        # sets the geometry of toplevel
        newWindow.geometry("1600x600")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",  background="#093545", foreground="white", rowheight=25, fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', '#093545')])

        tree_frame = Frame(newWindow)
        tree_frame.pack(padx=20)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll2 = Scrollbar(tree_frame, orient='horizontal')
        tree_scroll.pack(side=RIGHT, fill=Y)
        tree_scroll2.pack(side=BOTTOM, fill=X)
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, xscrollcommand=tree_scroll2.set, selectmode="extended")
        my_tree.pack()

        tree_scroll.configure(command=my_tree.yview)
        tree_scroll2.configure(command=my_tree.xview)

        my_tree['columns'] = ('Lease Number', 'Hall Name', 'Hall Number', 'Room Number', 'Student ID', 'Student Name', 'Occupancy Status', 'Cleaning Status', 'Rent Per Month', 'Duration (Month)')

        my_tree.column('#0', width=0, stretch=NO)
        my_tree.column("Lease Number", anchor=CENTER, width=140)
        my_tree.column("Hall Name", anchor=CENTER, width=140)
        my_tree.column("Hall Number", anchor=CENTER, width=140)
        my_tree.column("Room Number", anchor=CENTER, width=140)
        my_tree.column("Student ID", anchor=CENTER, width=140)
        my_tree.column("Student Name", anchor=W, width=200)
        my_tree.column("Occupancy Status", anchor=CENTER, width=140)
        my_tree.column("Cleaning Status", anchor=CENTER, width=140)
        my_tree.column("Rent Per Month", anchor=CENTER, width=140)
        my_tree.column("Duration (Month)", anchor=CENTER, width=140)

        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Lease Number", text="Lease Number", anchor=CENTER)
        my_tree.heading("Hall Name", text="Hall Name", anchor=CENTER)
        my_tree.heading("Hall Number", text="Hall Number", anchor=CENTER)
        my_tree.heading("Room Number", text="Room Number", anchor=CENTER)
        my_tree.heading("Student ID", text="Student ID", anchor=CENTER)
        my_tree.heading("Student Name", text="Student Name", anchor=CENTER)
        my_tree.heading("Occupancy Status", text="Occupancy Status", anchor=CENTER)
        my_tree.heading("Cleaning Status", text="Cleaning Status", anchor=CENTER)
        my_tree.heading("Rent Per Month", text="Rent Per Month", anchor=CENTER)
        my_tree.heading("Duration (Month)", text="Duration (Month)", anchor=CENTER)

        q = "SELECT LEASE_NUMBER, HALL_NAME, HALL_NUMBER, ROOM_NUMBER, STUDENT_ID, STUDENT_NAME, OCCUPANCY_STATUS, CLEANING_STATUS, RENT, DURATION FROM HALL ORDER BY HALL_NUMBER, ROOM_NUMBER;"
        cur.execute(q)

        rows = cur.fetchall()


        data = rows

        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="#99FEFF")

        global Counter
        count = 0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values=record, tags=('evenrow',))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values=record, tags=('oddrow',))

            count += 1
        # A Label widget to show in toplevel

        data_frame = LabelFrame(newWindow, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        

        ln2_label = Label(data_frame, text="Hall Name")
        ln2_label.grid(row=0, column=0, padx=10, pady=10)
        ln2_entry = Entry(data_frame, state="disable")
        ln2_entry.grid(row=0, column=1, padx=10, pady=10)

        ln3_label = Label(data_frame, text="Hall Number")
        ln3_label.grid(row=0, column=2, padx=10, pady=10)
        ln3_entry = Entry(data_frame, state="disable")
        ln3_entry.grid(row=0, column=3, padx=10, pady=10)

        ln4_label = Label(data_frame, text="Room Number")
        ln4_label.grid(row=0, column=4, padx=10, pady=10)
        ln4_entry = Entry(data_frame, state="disable")
        ln4_entry.grid(row=0, column=5, padx=10, pady=10)

        

        ln6_label = Label(data_frame, text="Occupancy Status")
        ln6_label.grid(row=0, column=8, padx=10, pady=10)
        ln6_entry = Entry(data_frame, state="disable")
        ln6_entry.grid(row=0, column=9, padx=10, pady=10)

        co = tk.StringVar(window)
        co.set("                            ")
        co_list = ["Clean", "Dirty", "Offline"]

        if user == "Warden" or user == "Admin":
            ln7_label = Label(data_frame, text="Cleaning Status")
            ln7_label.grid(row=0, column=10, padx=10, pady=10)
            ln7_entry = tk.OptionMenu(data_frame, co, *co_list)
            ln7_entry.configure(bg="white", bd=0, fg="black", highlightthickness = 0)
            ln7_entry.place(width=200, height=50)
            ln7_entry.grid(row=0, column=11, padx=10, pady=10)
        elif user == "Manager":
            ln7_label = Label(data_frame, text="Cleaning Status")
            ln7_label.grid(row=0, column=10, padx=10, pady=10)
            ln7_entry = tk.OptionMenu(data_frame, co, *co_list)
            ln7_entry.configure(bg="white", bd=0, fg="black", highlightthickness = 0, state="disable")
            ln7_entry.place(width=200, height=50)
            ln7_entry.grid(row=0, column=11, padx=10, pady=10)
       
        if user == "Admin" or user == "Manager":
            ln1_label = Label(data_frame, text="Lease Number")
            ln1_label.grid(row=1, column=0, padx=10, pady=10)
            ln1_entry = Entry(data_frame)
            ln1_entry.grid(row=1, column=1, padx=10, pady=10)

            ln5_label = Label(data_frame, text="Student Name")
            ln5_label.grid(row=1, column=6, padx=10, pady=10)
            ln5_entry = Entry(data_frame)
            ln5_entry.grid(row=1, column=7, padx=10, pady=10)

            ln9_label = Label(data_frame, text="Duration (Month)")
            ln9_label.grid(row=1, column=2, padx=10, pady=10)
            ln9_entry = Entry(data_frame)
            ln9_entry.grid(row=1, column=3, padx=10, pady=10)

            ln10_label = Label(data_frame, text="Student ID")
            ln10_label.grid(row=1, column=4, padx=10, pady=10)
            ln10_entry = Entry(data_frame)
            ln10_entry.grid(row=1, column=5, padx=10, pady=10)
        elif user == "Warden":
            ln1_label = Label(data_frame, text="Lease Number")
            ln1_label.grid(row=1, column=0, padx=10, pady=10)
            ln1_entry = Entry(data_frame, state="disable")
            ln1_entry.grid(row=1, column=1, padx=10, pady=10)

            ln5_label = Label(data_frame, text="Student Name")
            ln5_label.grid(row=1, column=6, padx=10, pady=10)
            ln5_entry = Entry(data_frame, state="disable")
            ln5_entry.grid(row=1, column=7, padx=10, pady=10)

            ln9_label = Label(data_frame, text="Duration (Month)")
            ln9_label.grid(row=1, column=2, padx=10, pady=10)
            ln9_entry = Entry(data_frame, state="disable")
            ln9_entry.grid(row=1, column=3, padx=10, pady=10)

            ln10_label = Label(data_frame, text="Student ID")
            ln10_label.grid(row=1, column=4, padx=10, pady=10)
            ln10_entry = Entry(data_frame, state="disable")
            ln10_entry.grid(row=1, column=5, padx=10, pady=10)

        ln8_label = Label(data_frame, text="Rent Per Month")
        ln8_label.grid(row=0, column=6, padx=10, pady=10)
        ln8_entry = Entry(data_frame, state="disable")
        ln8_entry.grid(row=0, column=7, padx=10, pady=10)

        

        

        button_frame = LabelFrame(newWindow, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        button1 = Button(button_frame, text="Update", command=update)
        button1.grid(row=0, column=0, padx=10, pady=10)

        button2 = Button(button_frame, text="Delete", command=delete)
        button2.grid(row=0, column=1, padx=10, pady=10)

        my_tree.bind("<ButtonRelease-1>", select)





window = Tk()

window.geometry("1280x720")
window.configure(bg = "#093545")
canvas = Canvas(
    window,
    bg = "#093545",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 490, y = 485,
    width = 300,
    height = 45)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    640.0, 426.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#224957",
    fg = "white",
    highlightthickness = 0)

entry0.place(
    x = 500.0, y = 404,
    width = 280.0,
    height = 43)

canvas.create_text(
    543.5, 427.0,
    text = "Password",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(14.0)))

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    640.0, 347.5,
    image = entry1_img)

entry2_bg = canvas.create_image(
    640.0, 268.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#224957",
    fg = "white",
    highlightthickness = 0)

entry1.place(
    x = 500.0, y = 325,
    width = 280.0,
    height = 43)

entry1.insert(0, "Username")
entry0.insert(0, "Password")

n = tk.StringVar(window)
n.set("Select Role")
options_list = ["Manager", "Warden", "Admin"]
entry2 = tk.OptionMenu(window, n, *options_list)
entry2.pack()
  
entry2.configure(bg="#224957", bd=0, fg="white", highlightthickness = 0)
  
entry2.place(
    x = 500.0, y = 246,
    width = 280.0,
    height = 43)

canvas.create_text(
    548.0, 348.0,
    text = "Username",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(14.0)))

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    640.0, 360.0,
    image=background_img)

canvas.create_text(
    639.5, 179.0,
    text = "Sign in to UWE Bristol Accommodation System!",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(16.0)))

canvas.create_text(
    640.0, 88.5,
    text = "Sign in",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(64.0)))

window.resizable(False, False)
window.mainloop()
