import socket
import webbrowser
import tempfile
import os

def http_client():
    host = "127.0.0.1"  # input("Enter server host (ex, 127.0.0.1): ")
    port = "8080"       # input("Enter server port (ex, 8080): ")
    filename = "index2.html"  # input("Enter filename (ex, index.html): ")

    try:
        port = int(port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))

            # Send HTTP GET request
            request = f"GET /{filename} HTTP/1.0\r\nHost: {host}\r\n\r\n"
            client_socket.sendall(request.encode())

            # Receive response
            response = b""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data

        # Decode response with error handling
        response_str = response.decode(errors='replace')

        # Find header-body separator
        separator = "\r\n\r\n"
        header_end = response_str.find(separator)
        if header_end == -1:
            print("Invalid HTTP response")
            return

        # Extract HTML content after headers
        html_content = response_str[header_end + len(separator):]

        # Save HTML content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as tmp_file:
            tmp_file.write(html_content)
            temp_file_path = tmp_file.name

        print(f"\n--- Server Response Succes ---")

        # Open the temp file in default browser
        webbrowser.open(f"file://{os.path.abspath(temp_file_path)}")

    except ValueError:
        print("Port must be a number.")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    http_client()
