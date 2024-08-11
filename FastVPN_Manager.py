import os
import time
import subprocess
import requests
import json
import webbrowser
import getpass
from cryptography.fernet import Fernet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Application details
app_name = "FastVPN Manager"
app_description = "Manage your VPN connections with ease."
app_developer = "Developed by RoguePayload"

# File to store VPN credentials
credentials_file = 'vpn_credentials.txt'

# Key for encryption (In a real application, this should be securely stored and not hard-coded)
encryption_key_file = 'encryption_key.key'

def generate_encryption_key():
    # Generate and save the encryption key
    if not os.path.exists(encryption_key_file):
        key = Fernet.generate_key()
        with open(encryption_key_file, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(encryption_key_file, 'rb') as key_file:
            key = key_file.read()
    return key

encryption_key = generate_encryption_key()
cipher = Fernet(encryption_key)

# Function to encrypt data
def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

# Function to decrypt data
def decrypt_data(data):
    return cipher.decrypt(data.encode()).decode()

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display loading animation
def loading_animation(message):
    print(Fore.RED + message, end='', flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print('.', end='', flush=True)
    print()

# Function to get internal IP
def get_internal_ip():
    return subprocess.check_output(["hostname", "-I"]).decode().strip()

# Function to get external IP
def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json().get('ip', 'Unavailable')
    except requests.RequestException:
        return 'Unavailable'

# Function to set VPN credentials
def set_vpn_credentials():
    username = input("Enter VPN Username: ")
    password = getpass.getpass("Enter VPN Password: ")
    encrypted_username = encrypt_data(username)
    encrypted_password = encrypt_data(password)
    with open(credentials_file, 'w') as f:
        f.write(f"{encrypted_username}\n{encrypted_password}\n")
    print(Fore.GREEN + "VPN credentials updated successfully.")

# Function to retrieve VPN credentials
def get_vpn_credentials():
    try:
        with open(credentials_file, 'r') as f:
            encrypted_username = f.readline().strip()
            encrypted_password = f.readline().strip()
        username = decrypt_data(encrypted_username)
        password = decrypt_data(encrypted_password)
        return username, password
    except FileNotFoundError:
        print(Fore.RED + "Credentials file not found. Please set your credentials first.")
        return None, None

# Function to display server list and select server
def select_server(protocol):
    server_list = os.listdir(f'serverList{protocol}')
    clear_screen()
    print(Fore.GREEN + app_name)
    print(Fore.BLUE + app_description)
    print(Fore.YELLOW + app_developer)
    print(Fore.RED + f"{protocol} Connections")
    
    # Check VPN status
    vpn_ip = check_vpn_connection(quiet=True)
    if vpn_ip:
        print(Fore.GREEN + f"Your VPN Connection is: {vpn_ip}")
    else:
        public_ip = get_external_ip()
        print(Fore.RED + f"Your IP Address is: {public_ip}")
    
    print("\nSelect a server:")
    for idx, server in enumerate(server_list, start=1):
        print(f"{idx}) {server}")

    choice = int(input("Enter server number: ")) - 1
    server_path = os.path.join(f'serverList{protocol}', server_list[choice])

    # Disconnect current VPN if connected
    if vpn_ip:
        disconnect_vpn()

    # Retrieve credentials
    username, password = get_vpn_credentials()
    if username is None or password is None:
        input("Press any key to return to the main menu...")
        return

    # Run the OpenVPN command with credentials
    with open('auth.txt', 'w') as auth_file:
        auth_file.write(f"{username}\n{password}\n")

    try:
        subprocess.run(["sudo", "openvpn", "--config", server_path, "--daemon", "--auth-user-pass", 'auth.txt'])
        print(Fore.GREEN + f"Connected via {protocol}.")
    finally:
        os.remove('auth.txt')  # Clean up the credentials file after use

    input("Press any key to return to the main menu...")

# Function to check VPN connection
def check_vpn_connection(quiet=False):
    vpn_ip = None
    result = subprocess.run(["curl", "-s", "https://ipinfo.io"], capture_output=True, text=True)
    data = json.loads(result.stdout)
    if 'org' in data and 'VPN' in data['org']:
        vpn_ip = data.get('ip')
    
    if not quiet:
        internal_ip = get_internal_ip()
        external_ip = get_external_ip()
        print(Fore.BLUE + f"Internal IP Address: {internal_ip}")
        print(Fore.RED + f"External IP Address: {external_ip}")
        if vpn_ip:
            print(Fore.GREEN + f"VPN IP Address: {vpn_ip}")
        else:
            print(Fore.RED + "Not connected to VPN.")
        input("Press any key to return to the main menu...")
    
    return vpn_ip

# Function to disconnect VPN
def disconnect_vpn():
    subprocess.run(["sudo", "killall", "openvpn"])
    print(Fore.GREEN + "VPN disconnected.")
    internal_ip = get_internal_ip()
    external_ip = get_external_ip()
    print(Fore.BLUE + f"Internal IP Address: {internal_ip}")
    print(Fore.RED + f"External IP Address: {external_ip}")
    input("Press any key to return to the main menu...")

# Function to perform IP Leak Test
def ip_leak_test():
    print(Fore.YELLOW + "Opening IP Leak Test in your default browser...")
    webbrowser.open_new_tab("https://ipleak.net/")
    input("Press any key to return to the main menu...")

# Function to perform DNS Leak Test
def dns_leak_test():
    print(Fore.YELLOW + "Opening DNS Leak Test in your default browser...")
    webbrowser.open_new_tab("https://www.dnsleaktest.com/")
    input("Press any key to return to the main menu...")

# Function to open developer website
def open_developer_website():
    webbrowser.open_new_tab("https://darkmcs.com")
    print(Fore.GREEN + "Opening developer website...")
    input("Press any key to return to the main menu...")

# Main menu function
def main_menu():
    while True:
        clear_screen()
        print(Fore.GREEN + app_name)
        print(Fore.BLUE + app_description)
        print(Fore.YELLOW + app_developer)
        print(Fore.RED + "Menu Options:")
        print(Fore.RED + "1) Set VPN Username and Password")
        print(Fore.RED + "2) Connect VIA TCP")
        print(Fore.RED + "3) Connect VIA UDP")
        print(Fore.RED + "4) Check VPN Connection")
        print(Fore.RED + "5) IP Address Leak Test")
        print(Fore.RED + "6) DNS Leak Test")
        print(Fore.RED + "7) Disconnect VPN")
        print(Fore.RED + "8) About Developer")
        print(Fore.RED + "9) Exit")

        choice = input(Fore.YELLOW + "Select an option: ")

        if choice == '1':
            set_vpn_credentials()
        elif choice == '2':
            select_server('TCP')
        elif choice == '3':
            select_server('UDP')
        elif choice == '4':
            check_vpn_connection()
        elif choice == '5':
            ip_leak_test()
        elif choice == '6':
            dns_leak_test()
        elif choice == '7':
            disconnect_vpn()
        elif choice == '8':
            open_developer_website()
        elif choice == '9':
            print("Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# Entry point
if __name__ == "__main__":
    clear_screen()
    print(Fore.GREEN + app_name)
    print(Fore.BLUE + app_description)
    print(Fore.YELLOW + app_developer)
    time.sleep(1)
    loading_animation("Loading resources")
    time.sleep(1)
    main_menu()
