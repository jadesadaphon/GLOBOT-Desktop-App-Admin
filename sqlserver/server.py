from dotenv import load_dotenv
import pyodbc
import os
import logging
from tkinter import messagebox

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(name)s] %(levelname)s - %(message)s"
)

class Server:

    def __init__(self):

        load_dotenv()

        self.id = None
        self.__server = os.getenv("DB_HOST")
        self.__database = os.getenv("DN_NAME")
        self.__username = os.getenv("DB_USERNAME")
        self.__password = os.getenv("DB_PASSWORD")
        self.__logger: logging = logging.getLogger(f"SQL-Server")

    def connect(self):
        try:
            self.__connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.__server};DATABASE={self.__database};UID={self.__username};PWD={self.__password}"
            )
            self.__cursor = self.__connection.cursor()
            self.__logger.info("Connected successfully.")
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"{e}")
            return False

    def insert_new_user(self, uid, name):
        try:
            sql = """INSERT INTO users (uid, name, createdby, updateby) VALUES (?, ?, ?, ?)"""
            self.__cursor.execute(sql, uid, name,  self.id, self.id)
            self.__connection.commit()
            self.__logger.info("User inserted successfully.")
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"{e}")
            return False

    def select_all_users(self,search,searchby=None):
        try:
            if searchby != None:
                if searchby == 'uid':
                    sql = """SELECT 
                                users.id,
                                users.uid,
                                users.name,
                                credits.credit,
                                user_created_credit.name as credit_created_by,
                                user_update_credit.name as credit_update_by,
                                users.enable,
                                users.blacklist,
                                user_created.name as user_created_by,
                                user_update.name as user_update_by,
                                users.syscreate,
                                users.sysupdate
                            FROM
                                users
                                LEFT JOIN credits ON credits.userid = users.id
                                LEFT JOIN users AS user_created_credit ON user_created_credit.id = credits.createdby
                                LEFT JOIN users AS user_update_credit ON user_update_credit.id = credits.updateby
                                LEFT JOIN users AS user_created ON user_created.id = users.createdby
                                LEFT JOIN users AS user_update ON user_update.id = users.updateby
                                WHERE users.uid like ?"""
                if searchby == 'name':
                    sql = """SELECT 
                                users.id,
                                users.uid,
                                users.name,
                                credits.credit,
                                user_created_credit.name as credit_created_by,
                                user_update_credit.name as credit_update_by,
                                users.enable,
                                users.blacklist,
                                user_created.name as user_created_by,
                                user_update.name as user_update_by,
                                users.syscreate,
                                users.sysupdate
                            FROM
                                users
                                LEFT JOIN credits ON credits.userid = users.id
                                LEFT JOIN users AS user_created_credit ON user_created_credit.id = credits.createdby
                                LEFT JOIN users AS user_update_credit ON user_update_credit.id = credits.updateby
                                LEFT JOIN users AS user_created ON user_created.id = users.createdby
                                LEFT JOIN users AS user_update ON user_update.id = users.updateby
                                WHERE users.name like ?"""
                
                self.__cursor.execute(sql,f'%{search}%')
                 
            columns = [column[0] for column in self.__cursor.description]  # ชื่อคอลัมน์
            result = [dict(zip(columns, row)) for row in self.__cursor.fetchall()]  # แปลงเป็น dict
            self.__logger.info("Select all users successfully.")
            return result
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"{e}")
            return None

    def select_all_history(self,search,date=None,searchby=None):
        try:
            if date != None:
                if searchby == "name":
                    sql = """SELECT glohistory.userid,
                                users.uid,
                                users.name,
                                glohistory.image,
                                glohistory.syscreate
                            FROM glohistory
                                LEFT JOIN users ON users.id = glohistory.userid
                            WHERE CAST(glohistory.syscreate AS DATE) = ?
                                AND users.name like ?"""
                elif searchby == "uid":
                    sql = """SELECT glohistory.userid,
                                users.uid,
                                users.name,
                                glohistory.image,
                                glohistory.syscreate
                            FROM glohistory
                                LEFT JOIN users ON users.id = glohistory.userid
                            WHERE CAST(glohistory.syscreate AS DATE) = ?
                                AND users.uid like ?"""
                self.__cursor.execute(sql, date, f'%{search}%')
            else:
                if searchby == "name":
                    sql = """SELECT glohistory.userid,
                                users.uid,
                                users.name,
                                glohistory.image,
                                glohistory.syscreate
                            FROM glohistory
                                LEFT JOIN users ON users.id = glohistory.userid
                            WHERE users.name like ?"""
                elif searchby == "uid":
                    sql = """SELECT glohistory.userid,
                                users.uid,
                                users.name,
                                glohistory.image,
                                glohistory.syscreate
                            FROM glohistory
                                LEFT JOIN users ON users.id = glohistory.userid
                            WHERE users.uid like ?"""
                self.__cursor.execute(sql, f'%{search}%')
                                

            columns = [column[0] for column in self.__cursor.description]  
            result = [dict(zip(columns, row)) for row in self.__cursor.fetchall()] 
            self.__logger.info("Select all history successfully.")
            return result
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"{e}")
            return None
    
    def update_user(self,name,enable,blacklist,id):
        try:
            sql = """UPDATE users SET name = ?, enable = ?, blacklist = ?, updateby = ?, sysupdate = (getdate()) WHERE id = ?"""
            self.__cursor.execute(sql, name, enable, blacklist,  self.id,id)
            self.__connection.commit()
            self.__logger.info("User update successfully.")
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"{e}")
            return None
        
    def update_credit(self,userid,credit):
        try:
            sql = """UPDATE credits SET credit = ?, updateby = ?, sysupdate = (getdate()) WHERE userid = ?"""
            self.__cursor.execute(sql, credit,  self.id, userid)
            self.__connection.commit()
            self.__logger.info("User update successfully.")
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"{e}")
            return None
        


        
