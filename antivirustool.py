from cryptography.fernet import Fernet
import os

# Load the key for decryption
def load_key():
    try:
        return open("key.key", "rb").read()
    except FileNotFoundError:
        print("Decryption key not found. Ensure 'key.key' is in the directory.")
        exit()

# Function to scan and detect encrypted files
def detect_encrypted_files():
    encrypted_files = []
    for file in os.listdir():
        if file.endswith(".txt") and file != "antivirus_tool.py":
            try:
                with open(file, "rb") as f:
                    data = f.read()
                # Attempt to decrypt to check if it's encrypted
                Fernet(load_key()).decrypt(data)
                encrypted_files.append(file)
            except Exception:
                pass  # File is not encrypted
    return encrypted_files

# Function to restore files
def restore_files(encrypted_files):
    key = load_key()
    fernet = Fernet(key)
    for file in encrypted_files:
        with open(file, "rb") as f:
            encrypted_data = f.read()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            with open(file, "wb") as f:
                f.write(decrypted_data)
            print(f"Restored {file}")
        except Exception as e:
            print(f"Failed to restore {file}: {e}")

# Main function
if __name__ == "__main__":
    print("Scanning for encrypted files...")
    encrypted_files = detect_encrypted_files()
    if encrypted_files:
        print(f"Detected encrypted files: {encrypted_files}")
        restore_choice = input("Do you want to restore them? (yes/no): ").lower()
        if restore_choice == "yes":
            restore_files(encrypted_files)
        else:
            print("Restoration aborted.")
    else:
        print("No encrypted files detected.")


