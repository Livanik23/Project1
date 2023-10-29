import tkinter as tk        
from tkinter import ttk     
import sqlite3              


class Main(tk.Frame):
    def __init__(self, root):                               
        super().__init__(root)                              
        self.init_main()                                    
        self.db = db                                        
        self.view_records()                                 
    def init_main(self):                                    

        
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)             
        toolbar.pack(side=tk.TOP, fill=tk.X)                


        self.add_img = tk.PhotoImage(file="./img/add.png")  
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)                  
        
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email","salary"), height=45, show="headings"
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)          
        self.tree.column("name", width=300, anchor=tk.CENTER)       
        self.tree.column("tel", width=150, anchor=tk.CENTER)        
        self.tree.column("email", width=150, anchor=tk.CENTER)      
        self.tree.column("salary", width=90, anchor=tk.CENTER)      

        self.tree.heading("ID", text="ID")                          
        self.tree.heading("name", text="Name")                       
        self.tree.heading("tel", text="Phone")                    
        self.tree.heading("email", text="E-mail")                   
        self.tree.heading("salary", text="Salary")                   

        self.tree.pack(side=tk.LEFT)                                


        self.update_img = tk.PhotoImage(file="./img/update.png")    
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)                          


        self.delete_img = tk.PhotoImage(file="./img/delete.png")    
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)                               


        self.search_img = tk.PhotoImage(file="./img/search.png")    
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)                                                  
    def open_dialog(self):                                                              
        Child()                                                                         
    def records(self, name, tel, email,salary ):
        self.db.insert_data(name, tel, email,salary )                                   
        self.view_records()                                                             

    def view_records(self):
        self.db.cursor.execute("SELECT * FROM Employees")                                      
        [self.tree.delete(i) for i in self.tree.get_children()]                         
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]  

    def open_update_dialog(self):
        Update()                                                                       
    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute(                                                        
            """UPDATE Employees SET name=?, tel=?, email=?, salary=? WHERE id=?""",

            (name, tel, email,salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()                                                           
        self.view_records()                                                             

    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(                                                     
                "DELETE FROM Employees WHERE id=?", (self.tree.set(selection_items, "#1"))     
            )
        self.db.conn.commit()                                                           
        self.view_records()                                                             

    def open_search_dialog(self):
        Search()                                                                        

    def search_records(self, name):
        name = "%" + name + "%"                                                         
        self.db.cursor.execute("SELECT * FROM Employees WHERE name LIKE ?", (name,))          

        [self.tree.delete(i) for i in self.tree.get_children()]                         
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]  


class Child(tk.Toplevel):                                   
    def __init__(self):                                     
        super().__init__(root)                              
        self.init_child()                                   
        self.view = app

    def init_child(self):
        self.title("Add employee")                   
        self.geometry("400x220")                            
        self.resizable(False, False)                       
        self.grab_set()                                     
        self.focus_set()                                    

        label_name = tk.Label(self, text="Name:")           
        label_name.place(x=50, y=50)                        
        label_select = tk.Label(self, text="Phone:")      
        label_select.place(x=50, y=80)                      
        label_sum = tk.Label(self, text="E-mail:")          
        label_sum.place(x=50, y=110)                        

        label_salary = tk.Label(self, text="Salary:")          
        label_salary.place(x=50, y=140)                        


        self.entry_name = ttk.Entry(self)                   
        self.entry_name.place(x=200, y=50)                  
        self.entry_email = ttk.Entry(self)                  
        self.entry_email.place(x=200, y=80)                 
        self.entry_tel = ttk.Entry(self)                   
        self.entry_tel.place(x=200, y=110)                  

        self.entry_salary = ttk.Entry(self)                    
        self.entry_salary.place(x=200, y=140)                  

        self.btn_cancel = ttk.Button(self, text="Close", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        self.btn_ok = ttk.Button(self, text="Add")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )


class Update(Child):
    def __init__(self):                                             
        super().__init__()                                         
        self.init_edit()                                            
        self.view = app                                            
        self.db = db                                                
        self.default_data()                                         

    def init_edit(self):
        self.title("Edit employee data")             
        btn_edit = ttk.Button(self, text="Edit")            
        btn_edit.place(x=205, y=170)                                 

        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )

        btn_edit.bind(
            "<Button-1>",
            lambda event: self.destroy(), add="+"
        )

        self.btn_ok.destroy()                                              

    def default_data(self):
        self.db.cursor.execute(                                             
            "SELECT * FROM Employees WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),        
        )
        row = self.db.cursor.fetchone()                        
        self.entry_name.insert(0, row[1])                       
        self.entry_email.insert(0, row[2])                      
        self.entry_tel.insert(0, row[3])                        
        self.entry_salary.insert(0,row[4])



class Search(tk.Toplevel):
    def __init__(self):                                         
        super().__init__()                                      
        self.init_search()                                      
        self.view = app                                         

    def init_search(self):
        self.title("Search employee")                          
        self.geometry("300x100")                                
        self.resizable(False, False)                            

        label_search = tk.Label(self, text="Name:")              
        label_search.place(x=50, y=20)                          
        self.entry_search = ttk.Entry(self)                     
        self.entry_search.place(x=100, y=20, width=150)         

        btn_cancel = ttk.Button(self, text="Close", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        search_btn = ttk.Button(self, text="Search")
        search_btn.place(x=105, y=50)

        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")



class DB:
    def __init__(self):                                                                
        self.conn = sqlite3.connect("db.db")                                            
        self.cursor = self.conn.cursor()                                                
        self.cursor.execute(                                                            
            '''
            CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT NOT NULL,
            salary INTEGER
            )
            '''
        )
        self.conn.commit()                                                                                 
        self.data()

    def data(self):
        insert_into = 'INSERT INTO Employees (name, tel, email, salary) VALUES (?, ?, ?, ?)'


        user_data=('John Smith', '+123456789', 'johnsmith@example.com','120')
        user_data1=('Jane Doe', '+198765432', 'janedoe@example.com','120')
        user_data2=('Michael Johnson', '+154321098', 'michaeljohnson@example.com','120')
        user_data3=('Emily Davis', '+199999999', 'emilydavis@example.com','120')
        user_data4=('Daniel Brown', '+144444444', 'danielbrown@example.com','120')
        self.cursor.execute(insert_into,user_data )
        self.cursor.execute(insert_into,user_data1 )
        self.cursor.execute(insert_into,user_data2 )
        self.cursor.execute(insert_into,user_data3 )
        self.cursor.execute(insert_into,user_data4 )

        self.conn.commit()                                                                                          


    def insert_data(self, name, tel, email, salary):                                                                
        self.cursor.execute(                                                                                        
            """INSERT INTO Employees(name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary)    
        )
        self.conn.commit()                                                                                          
if __name__ == "__main__":
    root = tk.Tk()                                 
    db = DB()                                       
    app = Main(root)                                
    app.pack()                                      
    root.title("List of company employees")       
    root.geometry("765x450")                        
    root.resizable(False, False)                   
    root.mainloop()                                
