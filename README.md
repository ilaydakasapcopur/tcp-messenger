# TCP Dynamic Messenger CLI

A modular, thread-based Command Line Interface (CLI) application built with Python. This project utilizes the **TCP/IP protocol** to enable real-time, dynamic message exchange between a Server and a Client, featuring a modern UI powered by the `Rich` library.



---

## 🚀 Features
* **Modular Architecture:** Clean separation between Networking, UI, and Logging logic.
* **Mode Selection:** Choose between Server or Client mode at startup.
* **Dynamic Messaging:** Supports multiple message types with specific parameters:
    * **Message Type 1 (Personal):** Name, Surname, Age, Residence.
    * **Message Type 2 (Education):** Degree, Institution, Graduation Year.
* **Real-time Interaction:** Uses Python `threading` to receive messages in the background while navigating the menu.
* **Message Logs:** Detailed logging system with timestamps and unique IDs.
* **Modern UI:** Enhanced terminal experience using tables, panels, and colors.

---

## 📂 Project Structure
```text
messenger_project/
├── main.py            # Entry point of the application
├── core/              # Networking logic
│   ├── __init__.py
│   ├── server.py      # Server socket initialization
│   ├── client.py      # Client socket initialization
│   └── network.py     # Main Node class handling send/receive
├── ui/                # User Interface components
│   ├── __init__.py
│   └── menu.py        # Menu navigation and input handling
├── utils/             # Helper utilities
│   ├── __init__.py
│   └── logger.py      # Message history and log formatting
