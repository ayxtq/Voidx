from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def generate_keys():
    key = RSA.generate(4096)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_file(input_file, output_file, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)

    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while chunk := infile.read(470):  # RSA can encrypt up to 470 bytes with 4096-bit key
            encrypted_chunk = cipher.encrypt(chunk)
            outfile.write(encrypted_chunk)

def decrypt_file(input_file, output_file, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)

    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while chunk := infile.read(512):  # Encrypted chunks are 512 bytes with 4096-bit key
            decrypted_chunk = cipher.decrypt(chunk)
            outfile.write(decrypted_chunk)

def select_file():
    file_path = filedialog.askopenfilename(title="Select File")
    return file_path

def save_file():
    file_path = filedialog.asksaveasfilename(title="Save As")
    return file_path

def generate_keys_gui():
    private_key, public_key = generate_keys()
    with open("private_key.pem", "wb") as priv_file:
        priv_file.write(private_key)
    with open("public_key.pem", "wb") as pub_file:
        pub_file.write(public_key)
    messagebox.showinfo("Keys Generated", "Private and public keys have been generated and saved.")

def encrypt_gui():
    try:
        with open("public_key.pem", "rb") as pub_file:
            public_key = pub_file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "Public key file not found.")
        return

    input_file = select_file()
    if not input_file:
        return

    output_file = save_file()
    if not output_file:
        return

    try:
        encrypt_file(input_file, output_file, public_key)
        messagebox.showinfo("Success", "File encrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")

def decrypt_gui():
    try:
        with open("private_key.pem", "rb") as priv_file:
            private_key = priv_file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "Private key file not found.")
        return

    input_file = select_file()
    if not input_file:
        return

    output_file = save_file()
    if not output_file:
        return

    try:
        decrypt_file(input_file, output_file, private_key)
        messagebox.showinfo("Success", "File decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")

# Create GUI window
root = tk.Tk()
root.title("RSA File Encryption/Decryption")

# Set window size
root.geometry("400x200")

# Generate keys button
generate_keys_button = tk.Button(root, text="Generate Keys", command=generate_keys_gui, height=2, width=20)
generate_keys_button.pack(pady=10)

# Encrypt button
encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_gui, height=2, width=20)
encrypt_button.pack(pady=10)

# Decrypt button
decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_gui, height=2, width=20)
decrypt_button.pack(pady=10)

# Run the GUI
root.mainloop()
