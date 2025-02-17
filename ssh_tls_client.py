import paramiko
import ssl
import socket

# SSH Client Setup
def create_ssh_tunnel(ssh_host, ssh_port, username, password, remote_port):
    # Create SSH Client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        ssh_client.connect(ssh_host, port=ssh_port, username=username, password=password)
        print(f"SSH connection established to {ssh_host}:{ssh_port}")

        # Open an SSH tunnel
        tunnel = ssh_client.get_transport().open_channel(
            'direct-tcpip', ('localhost', remote_port), ('localhost', 0)
        )
        print(f"SSH tunnel created to remote port {remote_port}")
        return tunnel
    except Exception as e:
        print(f"Error creating SSH tunnel: {e}")
        return None

# TLS Client Setup (Connect to the TLS Server)
def create_tls_connection(tunnel):
    try:
        # Wrap the SSH tunnel with TLS encryption
        context = ssl.create_default_context()
        tls_connection = context.wrap_socket(tunnel, server_hostname="localhost")
        print("TLS connection established")

        return tls_connection
    except Exception as e:
        print(f"Error setting up TLS: {e}")
        return None

# Send and receive data over TLS connection
def send_data(tls_connection, data):
    try:
        # Send data to the TLS server
        tls_connection.sendall(data.encode('utf-8'))

        # Receive response from the server
        response = tls_connection.recv(4096)
        print(f"Received response from server: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error during communication: {e}")

# Main function to start the client VPN
def start_client_vpn():
    # SSH server details
    ssh_host = "your.ssh.server.com"  # SSH server address
    ssh_port = 22  # SSH port
    username = "your_ssh_username"  # SSH username
    password = "your_ssh_password"  # SSH password
    
    # Remote TLS server port (on which the server is listening)
    remote_port = 443  # Remote TLS port

    # Create SSH tunnel
    tunnel = create_ssh_tunnel(ssh_host, ssh_port, username, password, remote_port)
    if not tunnel:
        print("Failed to create SSH tunnel")
        return

    # Establish a TLS connection over the SSH tunnel
    tls_connection = create_tls_connection(tunnel)
    if not tls_connection:
        print("Failed to establish TLS connection")
        return

    # Send some data (e.g., a simple HTTP request)
    send_data(tls_connection, "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

    # Close the TLS connection
    tls_connection.close()

if __name__ == "__main__":
    start_client_vpn()
