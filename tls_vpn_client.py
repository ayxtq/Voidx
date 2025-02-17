import ssl
import socket

def connect_to_tls_vpn():
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    with socket.create_connection(("your_server_ip", 443)) as sock:
        with context.wrap_socket(sock, server_hostname="vpn-server") as secure_sock:
            secure_sock.sendall(b"Hello, Secure VPN Server!")
            response = secure_sock.recv(1024)
            print(f"🔐 Secure Response: {response.decode()}")

connect_to_tls_vpn()

