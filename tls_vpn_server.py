import ssl
import socket

def start_tls_vpn_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', 443))  # VPN server listens on port 443 (HTTPS)
        server_socket.listen(5)
        print("TLS VPN Server is running on port 443...")

        with context.wrap_socket(server_socket, server_side=True) as secure_socket:
            while True:
                conn, addr = secure_socket.accept()
                print(f"🔒 Secure connection established with {addr}")
                data = conn.recv(1024)
                print("📩 Received:", data.decode())
                conn.sendall("🔒 Secure Data Transmitted Over TLS VPN")

start_tls_vpn_server()
