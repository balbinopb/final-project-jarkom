import sys       # For accessing command-line arguments
import socket    # For creating TCP socket connections

def client():
    
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 4:
        print("Usage: client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    # Extract arguments: server IP/hostname, port, and requested filename
    server_host = sys.argv[1]          # e.g., "127.0.0.1"
    server_port = int(sys.argv[2])     # e.g., 1234
    filename = sys.argv[3]             # e.g., "index.html"

    # Create a TCP socket (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the client socket to the server's IP and port
        client_socket.connect((server_host, server_port))

        # Create a valid HTTP GET request
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"

        # Send the HTTP request to the server
        client_socket.sendall(request.encode())

        # Receive the full response from the server in chunks
        response = b""  # Store raw bytes
        while True:
            chunk = client_socket.recv(1024)  # Read 1024-byte chunks
            if not chunk:  # No more data
                break
            response += chunk  # Append received data

        # Decode the full byte response to text (UTF-8 by default)
        response_text = response.decode()

        # Extract the first line of the HTTP response (status line)
        status_line = response_text.splitlines()[0]  # e.g., "HTTP/1.1 200 OK"

        # Check the status line and print result accordingly
        if "200 OK" in status_line:
            # If successful, print the full URL as output
            print(f"http://{server_host}:{server_port}/{filename}")
        else:
            # If failed (e.g., 404), show the status line as error
            print("Error from server:")
            print(status_line)

    except Exception as e:
        # Handle connection or socket errors
        print(f"[!] Connection error: {e}")

    finally:
        # Always close the socket after use
        client_socket.close()

# Standard Python entry point
if __name__ == "__main__":
    client()
