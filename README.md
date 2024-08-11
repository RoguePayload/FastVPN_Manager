# FastVPN Manager

![License](https://img.shields.io/badge/License-MIT-blue) ![Python](https://img.shields.io/badge/Python-3.6%2B-brightgreen) ![OpenVPN](https://img.shields.io/badge/OpenVPN-Compatible-yellowgreen) ![Downloads](https://img.shields.io/github/downloads/yourusername/FastVPN-Manager/total)

FastVPN Manager is a command-line tool designed to simplify the management of FastVPN connections provided by NameCheap. It allows users to easily set up VPN credentials, connect to VPN servers using TCP or UDP protocols, check connection status, and disconnect from the VPN with ease.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features
- **VPN Credential Management**: Save and update your VPN username and password securely.
- **Seamless Connection**: Choose from a list of available TCP and UDP servers to connect effortlessly.
- **Connection Status Check**: Display detailed information about your internal, external, and VPN IP addresses.
- **Safe Disconnection**: Terminate VPN connections cleanly and restore your original IP settings.
- **Developer Information**: Quick access to the developer's website for more resources.

## Installation

1. **Clone the Repository**
```
$ git clone https://github.com/yourusername/FastVPN-Manager.git
$ cd FastVPN-Manager
```
2. **Install Dependencies**
_Ensure you have Python 3.6+ and PIP Installed, then run:_
```
$ pip install -r requirements.txt
```
3. **Setup OpenVPN**
```
$ sudo apt-get install -y openvpn
```

## Usage
Run the script using Python:
```
$ python3 FastVPN_Manager.py
```
### Main Menu

    1. Set VPN Username and Password: Store your VPN credentials for easy access.
    2. Connect via TCP: Select from a list of TCP server configurations to establish a connection.
    3. Connect via UDP: Select from a list of UDP server configurations to establish a connection.
    4. Check VPN Connection: View detailed IP information to verify your VPN status.
    5. Disconnect VPN: Safely terminate the VPN connection and check your IP settings.
    6. About Developer: Open the developer's website for further information.
    7. Exit: Close the application.

## Contributing

We welcome contributions from the community. Please read our [Contribution Guidelines](Contribution_Guidelines.txt) for more details on how to get involved. Fork the repository and submit a pull request with your changes. Make sure to follow our contribution guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.

### Developed by RoguePayload
_Visit our website at [darkmcs.com](https://darkmcs.com) for more projects & updates!_

