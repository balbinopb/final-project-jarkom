
import socket
import os

HOST = '127.0.0.1'  # localhost
PORT = 1234 #port


def handle_client_connection(connection_socket):
    try:
        # Terima HTTP request dari client
        request_data = connection_socket.recv(1024).decode()
        print("Request received:")
        print(request_data)

        # Ambil nama file dari request
        request_line = request_data.splitlines()[0]
        filename = request_line.split()[1][1:] 

        if os.path.isfile(filename):
            # Buka dan baca isi file
            with open(filename, 'rb') as f:
                file_data = f.read()

            # Buat HTTP response dengan status 200 OK
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += f"Content-Length: {len(file_data)}\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "\r\n"

            connection_socket.sendall(response_header.encode() + file_data)
        else:
            # Jika file tidak ditemukan
            error_msg = "<h1>404 Not Found</h1>".encode()
            response_header = "HTTP/1.1 404 Not Found\r\n"
            response_header += f"Content-Length: {len(error_msg)}\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "\r\n"

            connection_socket.sendall(response_header.encode() + error_msg)

    except Exception as e:
        print("Error handling request:", e)
    finally:
        connection_socket.close()
        
def main():
    server_port = PORT  #port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind(('', server_port)) #to bind
    server_socket.listen(1)#listen

    print(f"Web server running on port {server_port}...")

    while True:
        print("Waiting for client...")
        connection_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client_connection(connection_socket)

if __name__ == "__main__":
    main()
