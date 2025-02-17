import paramiko
import socket

SSH_SERVER = "your_ssh_server_ip"
SSH_PORT = 2222
SSH_USERNAME = "your_ssh_user"
SSH_PASSWORD = "your_ssh_password"

def connect_to_vpn():
    """Connects to the SSH VPN"""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh_client.connect(SSH_SERVER, port=SSH_PORT, username=SSH_USERNAME, password=SSH_PASSWORD)
    print("Connected to SSH VPN Server!")

    # Create a socket to send data through the VPN
    vpn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vpn_sock.connect((SSH_SERVER, SSH_PORT))

    vpn_sock.sendall(b"Hello!")
    response = vpn_sock.recv(4096)
    print(f"VPN Server Response: {response.decode()}")

connect_to_vpn()
