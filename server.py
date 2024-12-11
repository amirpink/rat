import socket

# تنظیمات سرور
SERVER_IP = '127.0.0.1'  # آدرس IP سرور (localhost)
SERVER_PORT = 8080  # پورت برای ارتباط با کلاینت

# ایجاد اتصال به سرور
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)  # برای پذیرش تنها یک اتصال همزمان

    print(f"Server started, listening on {SERVER_IP}:{SERVER_PORT}")
    
    client_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
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

# شروع سرور
if __name__ == "__main__":
    start_server()
