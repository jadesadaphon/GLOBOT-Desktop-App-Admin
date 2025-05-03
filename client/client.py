import requests
import logging
import base64
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] %(levelname)s - %(message)s')

class Client:
    def __init__(self):

        load_dotenv()

        self.__logger = logging.getLogger("Client")
        self.__api_key:str = os.getenv("SERVER_API_KEY")
        self.id_token:str = ""
        self.message = ""

        self.host = f'http://{os.getenv("SERVER_HOST")}:{os.getenv("SERVER_PORT")}'

    def login(self, email: str, password: str) -> dict:
        payload = {"email": email, "password": password, "returnSecureToken": True}
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.__api_key}"
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.message  = "Login successful"
                self.__logger.info(self.message)
                return self.__verify_token(data['idToken'])
            else:
                error:dict = response.json()
                self.message  = f"Login failed: {error}"
                self.__logger.error(self.message)
                return
        except requests.exceptions.RequestException as e:
            self.message  = f"login Request failed: {e}"
            self.__logger.error(self.message)
            return
    
    def loadslipsbase64(self, path):
        try:
            url = f"{self.host}/slips"
            payload = {"path": path}
            response = requests.post(url, json=payload)
            if response:
                result = response.json()
                if result['success']:
                    img_base64 = result['img_base64']
                    file_path = result['file_path']

                    # ตรวจสอบและสร้างไดเรกทอรีหากไม่มีอยู่
                    directory = os.path.dirname(file_path)
                    os.makedirs(directory, exist_ok=True)

                    # Decode and save image
                    img_data = base64.b64decode(self.__clean_base64_data(img_base64))
                    with open(file_path, 'wb') as f:
                        f.write(img_data)

                    return file_path
                else:
                    self.message = result['message']
                    return
            else:
                self.message = response.json()
                return
        except requests.exceptions.RequestException as e:
            self.message = f"Load Slips Base64 Request failed: {e}"
            self.__logger.error(self.message)
            return
        except Exception as e:
            self.message = f"Unexpected error: {e}"
            self.__logger.error(self.message)
            return
    
    def loadUsers(self, search, searchby=None):
        try:
            url = f"{self.host}/users"
            params = {"search": search}
            if searchby is not None:
                params["searchby"] = searchby
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            self.message = f"Request failed: {e}"
            self.__logger.error(self.message)
            return
        except Exception as e:
            self.message = f"Unexpected error: {e}"
            self.__logger.error(self.message)
            return
        
    def updateUser(self, id, updateby, data):
        try:
            url = f"{self.host}/users"
            payload = data.copy()
            payload['id'] = id
            payload['updateby'] = updateby

            response = requests.patch(url, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
                error_msg = error_response.get('error', 'Unknown error')
                error_details = error_response.get('details', '')
                self.message = (
                    f"Server error / ข้อผิดพลาดจากเซิร์ฟเวอร์: {error_msg} - {error_details}"
                )
            except Exception:
                self.message = (
                    f"HTTP error occurred / เกิดข้อผิดพลาด HTTP: {e} (ไม่มีรายละเอียด JSON)"
                )
            self.__logger.error(self.message)
            return

        except requests.exceptions.RequestException as e:
            self.message = f"Connection error / ข้อผิดพลาดการเชื่อมต่อ: {e}"
            self.__logger.error(self.message)
            return

        except Exception as e:
            self.message = f"Unexpected error / ข้อผิดพลาดที่ไม่คาดคิด: {e}"
            self.__logger.error(self.message)
            return

    def updateCredit(self, userid, updateby, value):
        try:
            url = f"{self.host}/credit"
            payload = {'userid': userid, 'updateby': updateby, 'credit': value}

            response = requests.put(url, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
                error_msg = error_response.get('error', 'Unknown error')
                error_details = error_response.get('details', '')
                self.message = (
                    f"Server error / ข้อผิดพลาดจากเซิร์ฟเวอร์: {error_msg} - {error_details}"
                )
            except Exception:
                self.message = (
                    f"HTTP error occurred / เกิดข้อผิดพลาด HTTP: {str(e)}"
                )
            self.__logger.error(self.message)
            return

        except requests.exceptions.RequestException as e:
            self.message = f"Request failed / การร้องขอล้มเหลว: {e}"
            self.__logger.error(self.message)
            return

        except Exception as e:
            self.message = f"Unexpected error / ข้อผิดพลาดที่ไม่คาดคิด: {e}"
            self.__logger.error(self.message)
            return

    def __verify_token(self,token:str) -> dict:
        try:
            url = f"{self.host}/verify"
            payload = {"idToken": token}
            response = requests.post(url, json=payload)
            if response:
                result:dict = response.json()
                if result['verify']:
                    if int(result['level']) == 0:
                        self.id_token = token
                        self.message  = result['message']
                        self.__logger.info(self.message)
                        return result
                    else:
                        self.message  = 'Your account does not have administrator privileges'
                        return   
                else:
                    self.message = result['message']
                    return
            else:
                self.message = response.json()
                return
        except requests.exceptions.RequestException as e:
            self.message =  f"Verify Token Request failed: {e}"
            self.__logger.error(self.message)
            return

    def __clean_base64_data(self,img_base64):
        if ',' in img_base64:
            return img_base64.split(',')[1]
        return img_base64