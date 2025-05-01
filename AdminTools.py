import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime
from Lib.ui import App
from Lib.sqlserver import Server
import re
import pyodbc
import json
from tkinter import messagebox
import logging
import customtkinter
import threading
from Lib.client import Client
from pathlib import Path
from PIL import Image
import sys
import os

# pyinstaller --onefile --add-data "serviceAccountKey.json;." --add-data "server.json;." --noconsole --add-data "Lib/ui/images/untitled.png;images" --add-data "Lib/ui/icons/icon.ico;Lib/ui/icons" --icon="Lib\ui\icons\icon.ico" AdminTools.py



logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(name)s] %(levelname)s - %(message)s")
logger: logging = logging.getLogger(f"Main")

if hasattr(sys, "_MEIPASS"):
    serviceaccountkey_path = os.path.join(sys._MEIPASS, "serviceAccountKey.json")
else:
    serviceaccountkey_path = "serviceAccountKey.json"

cred = credentials.Certificate(serviceaccountkey_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def handle_login():
    global app, server, client
    app.login_button.configure(state="disabled")
    email = app.username_login_entry.get()
    password = app.password_login_entry.get()
    
    print(email)
    print(password)

    def login_task():
        try:
            result = client.login(email, password)
            message = client.message
        except Exception as e:
            messagebox.showerror("Login Error", f"An error occurred: {e}")
            app.after(0, lambda: app.login_button.configure(state="normal"))
            return

        def update_ui():
            if result != None:
                server.id = result['id']
                print(server.id)
                app.user_name_label.configure(text=result['name'])
                app.show_home_page()
            else:
                messagebox.showerror("Login Failed", message)
            app.login_button.configure(state="normal")

        app.after(0, update_ui)

    threading.Thread(target=login_task, daemon=True).start()

def handle_register():
    global app, server
    app.button_register.configure(state="disabled")
    name = app.name_entry.get()
    email = app.email_entry.get()
    password = app.password_entry.get()
    confirm_password = app.confirm_password_entry.get()

    if not email or not password or not confirm_password:
        app.messagebox.showerror("Error", "All fields are required. Please fill out all fields.")
        app.button_register.configure(state="normal")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        app.messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
        app.button_register.configure(state="normal")
        return

    if password != confirm_password:
        app.messagebox.showerror("Error", "Passwords do not match. Please re-enter your password.")
        app.button_register.configure(state="normal")
        return

    try:
        user = auth.create_user(email=email, password=password)
        logging.info("Firebase User successfully added.")
        server.insert_new_user(user.uid,name)
        
        app.messagebox.showinfo("Success", f"Registration successful!\nFirebase UID: {user.uid}")
        app.button_register.configure(state="normal")
        
        app.clear_form_register()
    except Exception as e:
        app.messagebox.showerror("Error", f"Error creating user: {e}")
        app.button_register.configure(state="normal")

def handle_manage_user():
    global app
    app.show_manage()
    insert_item_manage_user()

def insert_item_manage_user():
    global app, server, manage_scrollable_frame

    if manage_scrollable_frame != None:
        manage_scrollable_frame.destroy()

    manage_scrollable_frame = customtkinter.CTkScrollableFrame(app.manage_users_frame, corner_radius=10, fg_color="gray20")
    manage_scrollable_frame.grid(row=1, column=0, padx=5, pady=(2, 5), sticky="nsew")
    manage_scrollable_frame.configure(fg_color="gray17")
    
    search = app.manage_users_search_entry.get()
    searchradio = app.search_users_radio_var.get()
    users = server.select_all_users(search,searchradio)
    
    for i, user in enumerate(users):
        row_frame = customtkinter.CTkFrame(manage_scrollable_frame, height=40, corner_radius=10, fg_color="#2f2f2f")
        row_frame.pack(fill="x", expand=True, pady=(10 if i == 0 else 2, 2), padx=5)
        row_frame.grid_columnconfigure(0, weight=1)

        uid_label = customtkinter.CTkLabel(row_frame, text=user['uid'], font=customtkinter.CTkFont(size=12))
        uid_label.grid(row=0, column=0, padx=(10, 5), sticky="w")
        name_label = customtkinter.CTkLabel(row_frame, text=user['name'], font=customtkinter.CTkFont(size=12))
        name_label.grid(row=0, column=1, padx=(10, 5), sticky="w")
        credit_label = customtkinter.CTkLabel(row_frame, text=f"Credit {user['credit']}", font=customtkinter.CTkFont(size=12))
        credit_label.grid(row=0, column=2, padx=(5, 5))
        
        enable_label = customtkinter.CTkLabel(
            row_frame,
            text=f"Enabled" if user["enable"] else "Disabled",
            text_color="Green" if user["enable"] else "Orange",
            font=customtkinter.CTkFont(size=12))
        enable_label.grid(row=0, column=3, padx=(5, 5))

        blacklist_label = customtkinter.CTkLabel(
            row_frame,
            text=f"Blacklist" if user["blacklist"] else "Normal",
            text_color="Red" if user["blacklist"] else "Green",
            font=customtkinter.CTkFont(size=12))
        blacklist_label.grid(row=0, column=4, padx=(5, 5))

        button_manage = customtkinter.CTkButton(row_frame, text="Manage", width=50,  font=customtkinter.CTkFont(weight="bold"))
        button_manage.configure(command=lambda DATA=user : button_manage_event(DATA))
        button_manage.grid(row=0, column=5, padx=(5, 5), pady=5)

def handle_history():
    global app  
    app.show_history()
    insert_item_history()

def insert_item_history():
    global app, server, history_scrollable_frame

    if history_scrollable_frame != None:
        history_scrollable_frame.destroy()
    
    history_scrollable_frame = customtkinter.CTkScrollableFrame(app.history_frame, corner_radius=10, fg_color="gray20")
    history_scrollable_frame.grid(row=2, column=0, padx=5, pady=(2, 5), sticky="nsew")
    history_scrollable_frame.configure(fg_color="gray17")
    
    selected_date = app.search_options_calendar.get_date()
    date_object = datetime.strptime(selected_date, "%m/%d/%y")
    searchdate = date_object.strftime("%Y-%m-%d")
    
    search = app.search_history_entry.get()
    searchby = app.search_history_radio_var.get()
    
    if app.search_checkbox_var.get() == 'on':
        historys = server.select_all_history(search,searchby=searchby)
    else:
        historys = server.select_all_history(search,date=searchdate,searchby=searchby)


    for i, history in enumerate(historys):
        row_frame = customtkinter.CTkFrame(history_scrollable_frame, height=40, corner_radius=10, fg_color="#2f2f2f")
        row_frame.pack(fill="x", expand=True, pady=(10 if i == 0 else 2, 2), padx=5)
        row_frame.grid_columnconfigure(0, weight=1)

        uid_label = customtkinter.CTkLabel(row_frame, text=history['uid'], font=customtkinter.CTkFont(size=12))
        uid_label.grid(row=0, column=0, padx=(10, 5), sticky="w")
        name_label = customtkinter.CTkLabel(row_frame, text=history['name'], font=customtkinter.CTkFont(size=12))
        name_label.grid(row=0, column=1, padx=(10, 5), sticky="w")
        credit_label = customtkinter.CTkLabel(row_frame, text=history['syscreate'], font=customtkinter.CTkFont(size=12))
        credit_label.grid(row=0, column=2, padx=(5, 5))
    
        button_manage = customtkinter.CTkButton(row_frame, text="Image", width=50,  font=customtkinter.CTkFont(weight="bold"))
        button_manage.configure(command=lambda DATA=history : button_image_event(DATA))
        button_manage.grid(row=0, column=3, padx=(5, 5), pady=5)
        
def button_image_event(data):
    global client
    file_path = Path(data['image'])
    if file_path.is_file():
        img = Image.open(file_path)
        img.show()
    else:
        file_path_str = str(file_path).replace('\\', '/')
        file_path = client.loadslipsbase64(file_path_str)
        if file_path != None:
            img = Image.open(file_path)
            img.show()
    
def button_manage_event(data):
    global app
    # print(data)
    app.fmu_button_cancel.configure(command=app.show_manage)
    app.fmu_button_save.configure(command=lambda ID=data['id'], CREDIT=data['credit'] :update_user(ID,CREDIT))
    app.fmu_uid_label.configure(text=f"UID : {data['uid']}")
    app.fmu_name_entry.delete(0, customtkinter.END)
    app.fmu_name_entry.insert(customtkinter.END, data['name'])
    app.fmu_credit_entry.delete(0, customtkinter.END)
    app.fmu_credit_entry.insert(customtkinter.END, data['credit'])
    
    if data['enable']:
        app.account_status_var.set("enable")
    else:
        app.account_status_var.set("disable")
        
    app.fmu_account_status_enable.configure(variable=app.account_status_var)
        
    if data['blacklist']:
        app.account_blacklist_var.set("enable")
    else:
        app.account_blacklist_var.set("disable")
        
    app.fmu_account_blacklist_enable.configure(variable=app.account_blacklist_var)
        
    app.show_from_manage()

def update_user(id,default_credit):
    global server, app
    name = app.fmu_name_entry.get()
    enable = True if app.account_status_var.get() == 'enable' else False
    blacklist = True if app.account_blacklist_var.get() == 'enable' else False

    server.update_user(name,enable,blacklist,id)

    credit = float(app.fmu_credit_entry.get())
    default_credit = float(default_credit)
    if default_credit != credit:
        server.update_credit(id,credit)
    
    app.show_manage()
    insert_item_manage_user()

def load_server_json_file():
    global config
    try:
        if hasattr(sys, "_MEIPASS"):
            serverjson_path = os.path.join(sys._MEIPASS, "server.json")
        else:
            serverjson_path = "server.json"
        with open(serverjson_path, 'r') as file:
            config = json.load(file)
        return config
    except Exception as e:
        messagebox.showerror("Error", f"{e}")
        return

if __name__ == "__main__":
    manage_scrollable_frame = None
    history_scrollable_frame = None
    config = load_server_json_file()
    if config:
        server = Server(config)
        connect = server.connect()
        if connect:
            app = App()
            client = Client()
            app.login_button.configure(command=lambda: handle_login())
            app.button_register.configure(command=lambda: handle_register())
            app.button_manage_user.configure(command=lambda: handle_manage_user())
            app.button_search_users.configure(command=lambda: handle_manage_user())
            app.button_history.configure(command=lambda: handle_history())
            app.button_search_history.configure(command=lambda: handle_history())

            app.username_login_entry.insert(0, "jadesadaphon.chaykaew@gmail.com")
            app.password_login_entry.insert(0, "admin@1234")
           

            app.show_login_page()
            app.mainloop()
    
    
    


