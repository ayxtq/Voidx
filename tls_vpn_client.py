import ssl
import socket

def start_tls_client():
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    with socket.create_connection(("localhost", 8443)) as sock:
        with context.wrap_socket(sock, server_hostname="localhost") as ssock:
            ssock.sendall(b"Hello, secure world!")
            data = ssock.recv(1024)
            print(f"Received: {data.decode()}")

if __name__ == "__main__":
    start_tls_client()