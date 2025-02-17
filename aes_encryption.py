import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(input_file, output_file):
    key = os.urandom(32)  # Generate a random 32-byte key
    iv = os.urandom(16)  # AES requires a 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        outfile.write(key)  # Write the key to the output file
        outfile.write(iv)  # Write the IV to the output file

        while chunk := infile.read(1024):
            padding_length = 16 - (len(chunk) % 16)
            chunk += bytes([padding_length] * padding_length)
            outfile.write(encryptor.update(chunk))

        outfile.write(encryptor.finalize())

def decrypt_file(input_file, output_file):
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        key = infile.read(32)  # Read the key from the input file
        iv = infile.read(16)  # Read the IV from the input file
        ciphertext = infile.read()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

        while decrypted_data:
            chunk_size = len(decrypted_data) if len(decrypted_data) % 16 == 0 else len(decrypted_data) - (decrypted_data[-1] or 0)
            outfile.write(decrypted_data[:chunk_size])
            decrypted_data = decrypted_data[chunk_size:]

def select_file():
    file_path = filedialog.askopenfilename(title="Select File")
    return file_path

def save_file():
    file_path = filedialog.asksaveasfilename(title="Save As")
    return file_path

def encrypt_gui():
    input_file = select_file()
    if not input_file:
        return

    output_file = save_file()
    if not output_file:
        return

    try:
        encrypt_file(input_file, output_file)
        messagebox.showinfo("Success", "File encrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")

def decrypt_gui():
    input_file = select_file()
    if not input_file:
        return

    output_file = save_file()
    if not output_file:
        return

    try:
        decrypt_file(input_file, output_file)
        messagebox.showinfo("Success", "File decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")

# Create GUI window
root = tk.Tk()
root.title("AES File Encryption/Decryption")

# Set window size
root.geometry("400x200")

# Encrypt button
encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_gui, height=2, width=20)
encrypt_button.pack(pady=10)

# Decrypt button
decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_gui, height=2, width=20)
decrypt_button.pack(pady=10)

# Run the GUI
root.mainloop()
