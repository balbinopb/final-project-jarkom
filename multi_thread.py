import socket
import threading

# Define the host and port for the server to bind to
HOST = '127.0.0.1'
PORT = 1234

# Function to handle individual client connections
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        # Receive the HTTP request from the client
        request = conn.recv(1024).decode()
        print(f"Request:\n{request}")

        # Extract the requested filename from the HTTP request
        filename = request.split()[1][1:]
        if filename == "":
            filename = "index.html"  # Default file if no specific file is requested

        # Open and read the content of the requested file
        with open(filename, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Prepare a successful HTTP response with the file content
        response = f"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n{content}"
    except FileNotFoundError:
        # Handle the case where the requested file does not exist
        response = "HTTP/1.0 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile Not Found"
    except Exception as e:
        # Handle any other unexpected errors
        response = f"HTTP/1.0 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError: {str(e)}"

    # Send the HTTP response to the client and close the connection
    conn.sendall(response.encode())
    conn.close()

# Function to start the multi-threaded server
def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the specified host and port
    server_socket.bind((HOST, PORT))
    # Start listening for incoming connections (max 5 in queue)
    server_socket.listen(5)
    print(f"Multi-threaded server started at http://{HOST}:{PORT}")

    # Continuously accept and handle incoming connections
    while True:
        conn, addr = server_socket.accept()
        # Handle each client connection in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

# Start the server when this script is executed directly
if __name__ == "__main__":
    start_server()
