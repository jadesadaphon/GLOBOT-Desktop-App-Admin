import customtkinter
from PIL import Image
import os
import threading
import time
import logging
from tkcalendar import Calendar

import sys
import re
from tkinter import messagebox

customtkinter.set_appearance_mode("dark")
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] %(levelname)s - %(message)s')

class App(customtkinter.CTk):
    width = 1180
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__logger:logging = logging.getLogger(f"AppUI")

        self.title("GLOBOT Admin V1")
        
        if hasattr(sys, "_MEIPASS"):
            temp_icon_path = os.path.join(sys._MEIPASS, "ui/icons/icon.ico")
        else:
            temp_icon_path = "ui/icons/icon.ico"

        # ตรวจสอบว่าไฟล์ .ico มีอยู่จริง
        if not os.path.exists(temp_icon_path):
            raise FileNotFoundError(f"Icon file not found: {temp_icon_path}")

        # ใช้ไอคอน
        self.iconbitmap(temp_icon_path)
        
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))

        if hasattr(sys, "_MEIPASS"):
            # กรณีที่สร้าง .exe โดยใช้ PyInstaller
            images_path = os.path.join(sys._MEIPASS, 'images', 'untitled.png')
        else:
            # กรณีรันจากโค้ด Python ปกติ
            images_path = os.path.join(current_path, 'images', 'untitled.png')

        # โหลดภาพพื้นหลัง
        self.bg_image = customtkinter.CTkImage(Image.open(images_path), size=(self.width, self.height))

        # สร้าง Label สำหรับแสดงภาพพื้นหลัง
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        
        self.messagebox = messagebox
        
        self.create_login_frame()
        self.create_home_frame()
        self.create_menu_admin()
        self.create_display_form_register()
        self.create_display_manage()
        self.create_display_from_manage()
        self.create_display_history()
        
    def create_login_frame(self):
        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="GLOBOT",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 2))
        
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="AdminTools",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.login_label.grid(row=1, column=0, padx=30, pady=(2, 15))
        
        self.username_login_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Email")
        self.username_login_entry.grid(row=2, column=0, padx=30, pady=(15, 15))
        self.password_login_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Password")
        self.password_login_entry.grid(row=3, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", width=200)
        self.login_button.grid(row=4, column=0, padx=30, pady=(15, 15))  
        
    def create_home_frame(self):
        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=0)  # Fixed size for column 0
        self.home_frame.grid_columnconfigure(1, weight=1)  # Expandable size for column 1
         # create info frame
        self.menu_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=10)
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 
        self.menu_frame.grid_rowconfigure(2, weight=1)
        self.program_name_label = customtkinter.CTkLabel(self.menu_frame, text="AdminTools", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.program_name_label.grid(row=0, column=0, pady=(15, 5))
        # create menu frame
        self.list_menu_frame = customtkinter.CTkFrame(self.menu_frame, corner_radius=10, width=200, height=300)
        self.list_menu_frame.grid(row=2, column=0, padx=15, pady=(15, 15), sticky="nsew") 
        self.list_menu_frame.grid_columnconfigure(0, weight=1)
        self.list_menu_frame.grid_propagate(False)
        self.button_log_out = customtkinter.CTkButton(self.menu_frame, text="LogOut", command=self.logout, width=150)
        self.button_log_out.grid(row=3, column=0, pady=(15, 15), sticky="s")
        # create display frame
        self.display_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=10)
        self.display_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.display_frame.grid_rowconfigure(0, weight=1)  # ตั้งค่าโครงร่างที่นี่
        self.display_frame.grid_columnconfigure(0, weight=1)
          
    def create_display_form_register(self):
        self.register_frame = customtkinter.CTkFrame(self.display_frame, corner_radius=10)
        self.register_frame.grid_columnconfigure(0, weight=1)  # คอลัมน์ 0 ขยายเต็มความกว้าง
        
        # Label: Register
        self.fmu_manage_info_label = customtkinter.CTkLabel(self.register_frame, text="Register", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.fmu_manage_info_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="ew")  # ขยายเต็มความกว้าง
        
         # Label: Name
        self.name_label = customtkinter.CTkLabel(self.register_frame, text="Name", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.name_label.grid(row=1, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย
        
        # Entry: name Address
        self.name_entry = customtkinter.CTkEntry(
            self.register_frame,  
            placeholder_text="name address",
            textvariable=customtkinter.StringVar())
        self.name_entry.grid(row=2, column=0, padx=30, pady=1, sticky="ew")  # ขยายเต็มความกว้าง
        
        
        # Label: Email Address
        self.email_label = customtkinter.CTkLabel(self.register_frame, text="Email Address", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.email_label.grid(row=3, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย

        # Entry: Email Address
        self.email_entry = customtkinter.CTkEntry(
            self.register_frame,  
            placeholder_text="email address",
            textvariable=customtkinter.StringVar())
        self.email_entry.grid(row=4, column=0, padx=30, pady=1, sticky="ew")  # ขยายเต็มความกว้าง
        
        # Label: Password
        self.password_label = customtkinter.CTkLabel(self.register_frame, text="Password", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.password_label.grid(row=5, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย

        # Entry: Password
        self.password_entry = customtkinter.CTkEntry(
            self.register_frame,
            placeholder_text="password",
            textvariable=customtkinter.StringVar())
        self.password_entry.grid(row=6, column=0, padx=30, pady=1, sticky="ew")  # ขยายเต็มความกว้าง
        
        # Label: Confirm Password
        self.confirm_password_label = customtkinter.CTkLabel(self.register_frame, text="Confirm Password", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.confirm_password_label.grid(row=7, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย

        # Entry: Confirm Password
        self.confirm_password_entry = customtkinter.CTkEntry(
            self.register_frame,
            placeholder_text="confirm password",
            textvariable=customtkinter.StringVar())
        self.confirm_password_entry.grid(row=8, column=0, padx=30, pady=1, sticky="ew")  # ขยายเต็มความกว้าง
        
        # Frame: Button
        self.button_frame = customtkinter.CTkFrame(self.register_frame)
        self.button_frame.grid(row=9, column=0, pady=(10, 30), padx=30, sticky="ew")  # ขยายเต็มความกว้าง
    
        self.button_clear_from = customtkinter.CTkButton(self.button_frame, text="Clear", command=self.clear_form_register)
        self.button_clear_from.grid(row=0, column=0, padx=(0, 2.5)) 
        
        self.button_register = customtkinter.CTkButton(self.button_frame, text="Register")
        self.button_register.grid(row=0, column=1, padx=(2.5, 0))  

    def create_display_manage(self):
        self.manage_users_frame = customtkinter.CTkFrame(self.display_frame, corner_radius=10)
        self.manage_users_frame.grid_rowconfigure(1, weight=1)
        self.manage_users_frame.grid_columnconfigure(0, weight=1)
        self.manage_users_frame.configure(fg_color="gray20")

        search_frame = customtkinter.CTkFrame(self.manage_users_frame, corner_radius=10)
        search_frame.grid(row=0, column=0, padx=5, pady=(10, 2), sticky="nsew")
        search_frame.configure(fg_color="gray20")
        search_frame.grid_columnconfigure(2, weight=1)  # เพิ่มน้ำหนักให้คอลัมน์ของ manage_users_search_entry

        self.search_users_radio_var = customtkinter.StringVar(value="name")
        radio_uid = customtkinter.CTkRadioButton(search_frame, text="Search By UID", variable=self.search_users_radio_var, value="uid")
        radio_uid.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        radio_name = customtkinter.CTkRadioButton(search_frame, text="Search By Name", variable=self.search_users_radio_var, value="name")
        radio_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.manage_users_search_entry = customtkinter.CTkEntry(search_frame, corner_radius=10)
        self.manage_users_search_entry.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")  # ใช้ sticky="nsew" เพื่อขยายเต็มพื้นที่

        self.button_search_users = customtkinter.CTkButton(search_frame, text="Search")
        self.button_search_users.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        

    def create_display_from_manage(self):
        self.from_manage_user_frame = customtkinter.CTkFrame(self.display_frame, corner_radius=10)
        self.from_manage_user_frame.grid_columnconfigure(0, weight=1)  # คอลัมน์ 0 ขยายเต็มความกว้าง
        
        # Label: manage info
        self.fmu_manage_info_label = customtkinter.CTkLabel(self.from_manage_user_frame, text="Manage", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.fmu_manage_info_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="ew")  # ขยายเต็มความกว้าง
        
         # Label: UID
        self.fmu_uid_label = customtkinter.CTkLabel(self.from_manage_user_frame, text="UID : ", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.fmu_uid_label.grid(row=1, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย

        # Label: Name
        self.fmu_name_label = customtkinter.CTkLabel(self.from_manage_user_frame, text="Name", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.fmu_name_label.grid(row=2, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย

        # Entry: Name
        self.fmu_name_entry = customtkinter.CTkEntry(
            self.from_manage_user_frame,  
            placeholder_text="Name",
            textvariable=customtkinter.StringVar())
        self.fmu_name_entry.grid(row=3, column=0, padx=30, pady=1, sticky="ew")  # ขยายเต็มความกว้าง
        
        # Label: Credit
        self.fmu_credit_label = customtkinter.CTkLabel(self.from_manage_user_frame, text="Credit", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.fmu_credit_label.grid(row=4, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย

        # Entry: Credit
        self.fmu_credit_entry = customtkinter.CTkEntry(
            self.from_manage_user_frame,
            placeholder_text="Credit",
            textvariable=customtkinter.StringVar())
        self.fmu_credit_entry.grid(row=5, column=0, padx=30, pady=1, sticky="ew")  # ขยายเต็มความกว้าง
        
        # Label: Account status
        self.fmu_account_status_label = customtkinter.CTkLabel(self.from_manage_user_frame, text="Account Status", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.fmu_account_status_label.grid(row=6, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย
        # Frame: Account status
        self.search_radio_frame = customtkinter.CTkFrame(self.from_manage_user_frame)
        self.search_radio_frame.grid(row=7, column=0, pady=(10, 30), padx=30, sticky="ew")  # ขยายเต็มความกว้าง
        self.search_radio_frame.configure(fg_color="gray17")

        # ตั้งค่า StringVar สำหรับเก็บสถานะ
        self.account_status_var = customtkinter.StringVar(value="")
        # Radio button: Enable
        self.fmu_account_status_enable = customtkinter.CTkRadioButton(
            self.search_radio_frame,
            text="Enable",
            variable=self.account_status_var,
            value="enable"
        )
        self.fmu_account_status_enable.grid(row=0, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย
        # Radio button: Disable
        self.fmu_account_status_disable = customtkinter.CTkRadioButton(
            self.search_radio_frame,
            text="Disable",
            variable=self.account_status_var,
            value="disable"
        )
        self.fmu_account_status_disable.grid(row=0, column=1, padx=30, pady=1, sticky="w")  # ชิดซ้าย

        # Label: Account blacklist
        self.fmu_account_blacklist_label = customtkinter.CTkLabel(self.from_manage_user_frame, text="Account Blacklist", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.fmu_account_blacklist_label.grid(row=8, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย
        # Frame: Account blacklist
        self.fmu_account_blacklist_radio_frame = customtkinter.CTkFrame(self.from_manage_user_frame)
        self.fmu_account_blacklist_radio_frame.grid(row=9, column=0, pady=(10, 30), padx=30, sticky="ew")  # ขยายเต็มความกว้าง
        self.fmu_account_blacklist_radio_frame.configure(fg_color="gray17")

        # ตั้งค่า StringVar สำหรับเก็บสถานะ
        self.account_blacklist_var = customtkinter.StringVar(value="")
        # Radio button: Enable
        self.fmu_account_blacklist_enable = customtkinter.CTkRadioButton(
            self.fmu_account_blacklist_radio_frame,
            text="Blacklist",
            variable=self.account_blacklist_var,
            value="enable"
        )
        self.fmu_account_blacklist_enable.grid(row=0, column=0, padx=30, pady=1, sticky="w")  # ชิดซ้าย
        # Radio button: Disable
        self.fmu_account_blacklist_disable = customtkinter.CTkRadioButton(
            self.fmu_account_blacklist_radio_frame,
            text="Normal",
            variable=self.account_blacklist_var,
            value="disable"
        )
        self.fmu_account_blacklist_disable.grid(row=0, column=1, padx=30, pady=1, sticky="w")  # ชิดซ้าย
        
        # Frame: Button
        self.fmu_button_frame = customtkinter.CTkFrame(self.from_manage_user_frame)
        self.fmu_button_frame.grid(row=10, column=0, pady=(10, 30), padx=30, sticky="n")  # ขยายเต็มความกว้าง
        self.fmu_button_frame.configure(fg_color="gray17")
    
        self.fmu_button_cancel = customtkinter.CTkButton(self.fmu_button_frame, text="Cancel", command=self.clear_form_register)
        self.fmu_button_cancel.grid(row=0, column=0, padx=(0, 2.5)) 
        
        self.fmu_button_save = customtkinter.CTkButton(self.fmu_button_frame, text="Save")
        self.fmu_button_save.grid(row=0, column=1, padx=(2.5, 0))  
    
    def create_display_history(self):
        self.history_frame = customtkinter.CTkFrame(self.display_frame, corner_radius=10)
        self.history_frame.grid_rowconfigure(2, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.configure(fg_color="gray20")

        search_options_frame = customtkinter.CTkFrame(self.history_frame, corner_radius=10)
        search_options_frame.grid(row=0, column=0, padx=5, pady=(10, 2), sticky="ew")
        search_options_frame.configure(fg_color="gray20")
        search_options_frame.grid_rowconfigure(0, weight=1)
        search_options_frame.grid_columnconfigure(1, weight=1)

        self.search_options_calendar = Calendar(search_options_frame, selectmode="day", background='gray')
        self.search_options_calendar.grid(row=0, column=0, padx=(5, 5), pady=5, sticky="w")

        search_options_setup_frame = customtkinter.CTkFrame(search_options_frame, corner_radius=10)
        search_options_setup_frame.grid(row=0, column=1, padx=(5, 5), pady=5, sticky="nsew")
        search_options_setup_frame.grid_rowconfigure(0, weight=1)  
        search_options_setup_frame.grid_rowconfigure(1, weight=0)  
        search_options_setup_frame.grid_rowconfigure(2, weight=0)  
        search_options_setup_frame.grid_columnconfigure(0, weight=1)
        
        checkbox_frame = customtkinter.CTkFrame(search_options_setup_frame, corner_radius=10)
        checkbox_frame.grid(row=1, column=0, padx=30, pady=(0, 5), sticky="ew")
        self.search_checkbox_var = customtkinter.StringVar(value="off")
        checkbox_all_history = customtkinter.CTkCheckBox(checkbox_frame, text="All History", command=self.toggle_search_options, variable=self.search_checkbox_var, onvalue="on", offvalue="off")
        checkbox_all_history.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        radio_frame = customtkinter.CTkFrame(search_options_setup_frame, corner_radius=10)
        radio_frame.grid(row=2, column=0, padx=30, pady=(0, 5), sticky="ew")

        self.search_history_radio_var = customtkinter.StringVar(value="name")
        # กำหนดให้ radio buttons เป็น properties
        radio_uid = customtkinter.CTkRadioButton(radio_frame, text="Search By UID", variable=self.search_history_radio_var, value="uid")
        radio_uid.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        radio_name = customtkinter.CTkRadioButton(radio_frame, text="Search By Name", variable=self.search_history_radio_var, value="name")
        radio_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.toggle_search_options()
        
        search_entry_frame = customtkinter.CTkFrame(search_options_setup_frame, corner_radius=10)
        search_entry_frame.grid(row=3, column=0, padx=30, pady=(0, 5), sticky="ew")
        search_entry_frame.grid_columnconfigure(0, weight=1) 
        search_entry_frame.grid_columnconfigure(1, weight=0) 

        self.search_history_entry = customtkinter.CTkEntry(search_entry_frame, corner_radius=10)
        self.search_history_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  
        self.search_history_entry.configure(fg_color="gray17")

        self.button_search_history = customtkinter.CTkButton(search_entry_frame, text="Search")
        self.button_search_history.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 

    def toggle_search_options(self):
        is_checked = self.search_checkbox_var.get() == "on"
        self.search_options_calendar.configure(state="disabled" if is_checked else "normal")

    def clear_form_register(self):
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
        self.register_frame.focus_set()

    def create_menu_admin(self):
        # สร้าง label และ button พร้อมจัดให้อยู่ชิดขอบบน
        self.list_menu_frame.grid_rowconfigure(0, weight=0)
        self.user_name_label = customtkinter.CTkLabel(self.list_menu_frame, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.user_name_label.grid(row=0, column=0, pady=(10, 5), sticky="n")

        self.list_menu_frame.grid_rowconfigure(1, weight=0)
        self.button_open_from_register_new_user = customtkinter.CTkButton(self.list_menu_frame, text="Register", command=self.show_register, width=150)
        self.button_open_from_register_new_user.grid(row=1, column=0, pady=(5, 5), sticky="n")

        self.list_menu_frame.grid_rowconfigure(2, weight=0)
        self.button_manage_user = customtkinter.CTkButton(self.list_menu_frame, text="Manage", width=150)
        self.button_manage_user.grid(row=2, column=0, pady=(5, 5), sticky="n")

        self.list_menu_frame.grid_rowconfigure(2, weight=0)
        self.button_history = customtkinter.CTkButton(self.list_menu_frame, text="History", width=150)
        self.button_history.grid(row=3, column=0, pady=(5, 10), sticky="n")

    def show_register(self):
        self.manage_users_frame.grid_forget()
        self.history_frame.grid_forget()

        self.from_manage_user_frame.grid_forget()

        self.register_frame.grid(row=0, column=0, padx=5, pady=(10, 10))
        self.register_frame.focus_set()

    def show_manage(self):
        self.register_frame.grid_forget()
        self.history_frame.grid_forget()

        self.from_manage_user_frame.grid_forget()

        self.manage_users_frame.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="nsew")
            
    def show_from_manage(self):
        self.register_frame.grid_forget()
        self.history_frame.grid_forget()

        self.manage_users_frame.grid_forget()

        self.from_manage_user_frame.grid(row=0, column=0, padx=5, pady=(10, 10))

    def show_history(self):
        self.register_frame.grid_forget()
        self.manage_users_frame.grid_forget()

        self.from_manage_user_frame.grid_forget()

        self.history_frame.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="nsew")
        
    def show_home_page(self):
        self.login_frame.grid_forget()
        self.home_frame.grid(row=0, column=0, sticky="nsew", padx=100)
    
    def show_login_page(self):
        self.home_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, sticky="ns", pady=(20,20))
        
    def logout(self):
        self.home_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, sticky="ns", pady=(20,20))  # show login frame
    

