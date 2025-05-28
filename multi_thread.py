import socket
import threading

HOST = '127.0.0.1'
PORT = 1234

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        request = conn.recv(1024).decode()
        print(f"Request:\n{request}")

        # Extract requested file name
        filename = request.split()[1][1:]
        if filename == "":
            filename = "index.html"

        with open(filename, "r", encoding='utf-8') as f:
            content = f.read()
        response = f"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n{content}"
    except FileNotFoundError:
        response = "HTTP/1.0 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile Not Found"
    except Exception as e:
        response = f"HTTP/1.0 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError: {str(e)}"

    conn.sendall(response.encode())
    conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Multi-threaded server started at http://{HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
