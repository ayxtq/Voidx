import paramiko
import socket
import threading

SSH_HOST = "0.0.0.0"  # Listen on all interfaces
SSH_PORT = 2222  # Custom SSH Port

def handle_client(client_sock, ssh_tunnel):
    """Handles client traffic through SSH"""
    try:
        while True:
            data = client_sock.recv(4096)
            if not data:
                break
            print(f"Received: {data.decode()}")
            ssh_tunnel.sendall(data)  # Forward through SSH tunnel
            response = ssh_tunnel.recv(4096)
            client_sock.sendall(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_sock.close()

def start_vpn_server():
    """Starts an SSH-based VPN server"""
    server = paramiko.ServerInterface()
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SSH_HOST, SSH_PORT))
    server_sock.listen(5)
    print(f"SSH VPN Server running on port {SSH_PORT}")

    while True:
        client_sock, addr = server_sock.accept()
        print(f"Client connected: {addr}")

        # Establish SSH tunnel
        ssh_tunnel = paramiko.Transport(client_sock)
        ssh_tunnel.start_server(server=server)

        vpn_thread = threading.Thread(target=handle_client, args=(client_sock, ssh_tunnel))
        vpn_thread.start()

start_vpn_server()
