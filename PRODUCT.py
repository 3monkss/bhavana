#!/usr/bin/env python
# coding: utf-8

# In[6]:


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import sys
import os


HEADING_FONT = ("Verdana", 25)
LARGE_FONT = ("Helvetica", 18)
NAME = None

conn = sqlite3.connect('store.db')
c = conn.cursor()

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def create_model_table():
    c.execute('CREATE TABLE IF NOT EXISTS Model(Id INTEGER PRIMARY KEY, Code VARCHAR NOT NULL, Model VARCHAR NOT NULL, Company VARCHAR NOT NULL) ')

def create_customer_table():
    c.execute('CREATE TABLE IF NOT EXISTS Customer(Id INTEGER PRIMARY KEY, Name VARCHAR NOT NULL, Age INTEGER NOT NULL, Contact VARCHAR NOT NULL, Code VARCHAR NOT NULL) ')

def create_status_table():
    c.execute('CREATE TABLE IF NOT EXISTS Status(Id INTEGER PRIMARY KEY, Name VARCHAR NOT NULL, Code VARCHAR NOT NULL, Message VARCHAR NOT NULL) ')


def insert_customer( name, age, contact, code):
    c.execute('INSERT INTO Customer(Name, Age, Contact, Code) VALUES(?,?,?,?)',(name, age, contact, code,))
    conn.commit()
    messagebox.showinfo(title = "Success", message = "Rental Request Successfuly Sent")


def insert_model(code, model, company):
    c.execute('INSERT INTO Model(Code, Model, Company) VALUES(?,?,?)',(code, model, company,))
    conn.commit()
    messagebox.showinfo(title = "Success", message = "New Model Was Successfully Added")
    restart_program()

def insert_status(name, code, message):
    c.execute('INSERT INTO Status(Name, Code, Message) VALUES(?,?,?)',(name, code, message,))
    conn.commit()
    restart_program()

def update_status(name, code, message):
    c.execute("""UPDATE Status SET Message = ? WHERE Name = ? AND Code = ? """,(message, name, code,))
    conn.commit()
    messagebox.showinfo(title = "Success", message = "Message Sent To Customer")
    restart_program()


class store(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "store")

        container = tk.Frame(self)
        container.pack(side="top", fill ="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for page in (MainPage, CustomerPage, CompanyPage, ViewAllCarPage, ViewStatusPage, ApplyPage, PostProductPage, ViewCustomerPage, ContactCustomerPage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)
        
    def dynamic_page(self, page, parent, var):
        if var is not None:
            self.frames[page] = page(parent, self, var)
        
    def show_frame(self, cont):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cont]
        frame.grid()
        frame.tkraise()



class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self, text="MAIN MENU", font = HEADING_FONT)
        option1 = tk.Label(self, text="- CUSTOMER PORTAL", font = HEADING_FONT)
        option2 = tk.Label(self, text="- PRODUCT PORTAL", font = HEADING_FONT)
        

        label.grid(row=0, columnspan= 2,padx = 40, pady=40)
        option1.grid(row=1,column=1,padx = 40, pady=40)
        option2.grid(row=2,column=1,padx = 40, pady=40)
        
        button1 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(CustomerPage))
        button1.grid(row=1, column=2, sticky = "es",padx = 40, pady=40 )
        button2 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(CompanyPage))
        button2.grid(row=2, column=2, sticky = "es",padx = 40, pady=40 )

        
class CustomerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="CUSTOMER PORTAL", font = HEADING_FONT)
        option1 = tk.Label(self, text="- BUY A PRODUCT", font = LARGE_FONT)
        option2 = tk.Label(self, text="- VIEW ALL PRODUCTS", font = LARGE_FONT)
        option4 = tk.Label(self, text="- VIEW SHIPPING STATUS", font = LARGE_FONT)

        label.grid(row=1, column=1,columnspan=2, padx = 20, pady=20)
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option4.grid(row=4,column=1,padx = 20, pady=20)
        
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(MainPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button2 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ApplyPage))
        button2.grid(row=2, column = 2, sticky = "es",padx = 20, pady=20 )
        button3 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ViewAllCarPage))
        button3.grid(row=3, column = 2, sticky = "es",padx = 20, pady=20 )
        button5 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ViewStatusPage))
        button5.grid(row=4, column = 2, sticky = "es",padx = 20, pady=20 )



class ApplyPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(name, age, contact, code):
            c.execute('SELECT * FROM Model WHERE Code = ?',(code.get(),))
            info = c.fetchall()
            if len(info) == 0:
                messagebox.showinfo(title = "Caution", message = "No Such Car exists")
                controller.show_frame(ApplyPage)
            else:
                insert_customer( name.get(), age.get(), contact.get(), code.get())
                message =  "Not Yet Viewed"
                insert_status(name.get(), code.get(), message)
                
        option1 = tk.Label(self, text="- YOUR NAME ", font = LARGE_FONT)
        option2 = tk.Label(self, text="- YOUR AGE", font = LARGE_FONT)
        option3 = tk.Label(self, text="- YOUR CONTACT INFO", font = LARGE_FONT)
        option4 = tk.Label(self, text="- PRODUCT CODE ", font = LARGE_FONT)
        
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)
        option4.grid(row=5,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=2,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=3,column=2,padx = 20, pady=20)
        entry3 = tk.Entry(self)
        entry3.grid(row=4,column=2,padx = 20, pady=20)
        entry4 = tk.Entry(self)
        entry4.grid(row=5,column=2,padx = 20, pady=20)
    
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(CustomerPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Store",
                            command= lambda: wrapper(entry1, entry2, entry3, entry4))
        button1.grid(row=6, columnspan = 3, padx = 20, pady=20 )




class ViewStatusPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(entry1, entry2):
            c.execute('SELECT * FROM Status WHERE Name = ? AND Code = ?',(entry1.get(),entry2.get(),))
            info = c.fetchall()
            if len(info) == 0:
                messagebox.showinfo(title = "Caution", message = "No Such order is placed")
            else:
                ROW = info[0]
                controller.dynamic_page(DisplayStatus, parent, ROW)
                controller.show_frame(DisplayStatus)


        query1 = tk.Label(self, text="- ENTER YOUR NAME: ", font = LARGE_FONT)
        query2 = tk.Label(self, text="- ENTER PRODUCT CODE: ", font = LARGE_FONT)

        query1.grid(row=1,column=1,padx = 20, pady=20)
        query2.grid(row=2,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=1,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=2,column=2,padx = 20, pady=20)
  
  
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(CustomerPage))
        button1.grid(row=0, columnspan = 2, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Fetch",
                            command= lambda: wrapper(entry1,entry2))
        button1.grid(row=3, columnspan = 2, padx = 20, pady=20 )



class DisplayStatus(tk.Frame):

    row = None
    
    def __init__(self, parent, controller, ROW):
        tk.Frame.__init__(self,parent)
        row = ROW
       
        option2 = tk.Label(self, text="NAME :", font = LARGE_FONT)
        option3 = tk.Label(self, text="PRODUCT CODE :", font = LARGE_FONT)
        option4 = tk.Label(self, text="STATUS :", font = LARGE_FONT)
        
        option2.grid(row=1,column=1,padx = 20, pady=20)
        option3.grid(row=2,column=1,padx = 20, pady=20)
        option4.grid(row=3,column=1,padx = 20, pady=20)

        tk.Label(self, text=row[1], font = LARGE_FONT).grid(row=1, column=2,padx = 20, pady=20)
        tk.Label(self, text=row[2], font = LARGE_FONT).grid(row=2, column=2,padx = 20, pady=20)
        tk.Label(self, text=row[3], font = LARGE_FONT).grid(row=3, column=2,padx = 20, pady=20)
               
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(CustomerPage))
        button1.grid(row=0, columnspan = 2, padx = 20, pady=20 )
        



        
class ViewAllCarPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        option1 = tk.Label(self, text="ID", font = LARGE_FONT)
        option2 = tk.Label(self, text="CODE", font = LARGE_FONT)
        option3 = tk.Label(self, text="MODEL", font = LARGE_FONT)
        option4 = tk.Label(self, text="COMPANY", font = LARGE_FONT)

        option1.grid(row=1,column=0,padx = 20, pady=20)
        option2.grid(row=1,column=1,padx = 20, pady=20)
        option3.grid(row=1,column=2,padx = 20, pady=20)
        option4.grid(row=1,column=3,padx = 20, pady=20)


        with conn:
            c = conn.cursor()
            c.execute('SELECT * FROM Model')
            index=2
            for row in c.fetchall():
                tk.Label(self, text=row[0], font = LARGE_FONT).grid(row=index, column=0,padx = 20, pady=20)
                tk.Label(self, text=row[1], font = LARGE_FONT).grid(row=index, column=1,padx = 20, pady=20)
                tk.Label(self, text=row[2], font = LARGE_FONT).grid(row=index, column=2,padx = 20, pady=20)
                tk.Label(self, text=row[3], font = LARGE_FONT).grid(row=index, column=3,padx = 20, pady=20)
                index+=1
        
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(CustomerPage))
        button1.grid(row=0,column = 1,columnspan = 2, padx = 20, pady=20 )




class CompanyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="PRODUCT PORTAL", font = HEADING_FONT)
        option2 = tk.Label(self, text="- POST A NEW PRODUCT MODEL", font = LARGE_FONT)
        option3 = tk.Label(self, text="- VIEW CUSTOMERS", font = LARGE_FONT)
        option4 = tk.Label(self, text="- CONTACT A CUSTOMER", font = LARGE_FONT)
        
        label.grid(row=1, column=1,columnspan=2, padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)
        option4.grid(row=5,column=1,padx = 20, pady=20)
                
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(MainPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button3 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(PostCarPage))
        button3.grid(row=3, column = 2, sticky = "es",padx = 20, pady=20 )
        button4 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ViewCustomerPage))
        button4.grid(row=4, column = 2, sticky = "es",padx = 20, pady=20 )
        button5 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ContactCustomerPage))
        button5.grid(row=5, column = 2, sticky = "es",padx = 20, pady=20 )


class ViewCustomerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        option1 = tk.Label(self, text="ID", font = LARGE_FONT)
        option2 = tk.Label(self, text="NAME", font = LARGE_FONT)
        option3 = tk.Label(self, text="AGE ", font = LARGE_FONT)
        option4 = tk.Label(self, text="CONTACT ", font = LARGE_FONT)
        option5 = tk.Label(self, text="PRODUCT CODE ", font = LARGE_FONT)
        option6 = tk.Label(self, text="PRODUCT MODEL ", font = LARGE_FONT)
        option7 = tk.Label(self, text="PRODUCT COMPANY ", font = LARGE_FONT)

        option1.grid(row=1,column=0,padx = 20, pady=20)
        option2.grid(row=1,column=1,padx = 20, pady=20)
        option3.grid(row=1,column=2,padx = 20, pady=20)
        option4.grid(row=1,column=3,padx = 20, pady=20)
        option5.grid(row=1,column=4,padx = 20, pady=20)
        option6.grid(row=1,column=5,padx = 20, pady=20)
        option7.grid(row=1,column=6,padx = 20, pady=20)


        c.execute('SELECT customer.Id, customer.Name, customer.Age, customer.Contact, customer.Code, model.Model, model.Company FROM customer INNER JOIN model ON customer.Code = model.Code')
        index=2
        for row in c.fetchall():
            tk.Label(self, text=row[0], font = LARGE_FONT).grid(row=index, column=0,padx = 20, pady=20)
            tk.Label(self, text=row[1], font = LARGE_FONT).grid(row=index, column=1,padx = 20, pady=20)
            tk.Label(self, text=row[2], font = LARGE_FONT).grid(row=index, column=2,padx = 20, pady=20)
            tk.Label(self, text=row[3], font = LARGE_FONT).grid(row=index, column=3,padx = 20, pady=20)
            tk.Label(self, text=row[4], font = LARGE_FONT).grid(row=index, column=4,padx = 20, pady=20)
            tk.Label(self, text=row[5], font = LARGE_FONT).grid(row=index, column=5,padx = 20, pady=20)
            tk.Label(self, text=row[6], font = LARGE_FONT).grid(row=index, column=6,padx = 20, pady=20)
            index+=1
        
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(CompanyPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )



class PostcarPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper( code, model, company):
                insert_model(code.get(), model.get(), company.get(),)
                controller.show_frame(CompanyPage)

        
        option1 = tk.Label(self, text="- PRODUCT UNIQUE CODE ", font = LARGE_FONT)
        option2 = tk.Label(self, text="- PRODUCT MODEL", font = LARGE_FONT)
        option3 = tk.Label(self, text="- PRODUCT COMPANY", font = LARGE_FONT)
        
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=2,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=3,column=2,padx = 20, pady=20)
        entry3 = tk.Entry(self)
        entry3.grid(row=4,column=2,padx = 20, pady=20)
    
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(CompanyPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Store",
                            command= lambda:  wrapper(entry1, entry2, entry3))
        button1.grid(row=6, columnspan = 3, padx = 20, pady=20 )        

class ContactCustomerPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(name, code, message):
            c.execute('SELECT * FROM Status WHERE Name = ? AND Code = ?',(name.get(), code.get(),))
            info = c.fetchall()
            if len(info) == 0:
                messagebox.showinfo(title = "Caution", message = "No Such Order Placed")
            else:
                update_status( name.get(), code.get(), message.get())
                messagebox.showinfo(title = "Success", message = "Message Sent Successfully")
                controller.show_frame(CompanyPage)

                
        option1 = tk.Label(self, text="- NAME OF CUSTOMER", font = LARGE_FONT)
        option2 = tk.Label(self, text="- PRODUCT CODE CUSTOMER WANTS", font = LARGE_FONT)
        option3 = tk.Label(self, text="- MESSAGE YOU WANT TO CONVEY", font = LARGE_FONT)
        
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=2,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=3,column=2,padx = 20, pady=20)
        entry3 = tk.Entry(self)
        entry3.grid(row=4,column=2,padx = 20, pady=20)
    
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(CompanyPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Store",
                            command= lambda: wrapper(entry1, entry2, entry3))
        button1.grid(row=6, columnspan = 3, padx = 20, pady=20 )


        
create_status_table()
create_model_table()
create_customer_table()
app = store()
app.mainloop()


# In[ ]:





# In[ ]:




