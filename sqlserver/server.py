from dotenv import load_dotenv
import os
import logging

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
        # try:
        #     self.__connection = pyodbc.connect(
        #         f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.__server};DATABASE={self.__database};UID={self.__username};PWD={self.__password}"
        #     )
        #     self.__cursor = self.__connection.cursor()
        #     self.__logger.info("Connected successfully.")
        #     return True
        # except pyodbc.Error as e:
        #     messagebox.showerror("Error", f"{e}")
        #     return False
        pass

    def select_all_history(self,search,date=None,searchby=None):
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
        
    


        


        
