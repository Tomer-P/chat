Python Chat Application
A Python-based chat project that uses Sockets and Select for real-time communication between a server and multiple clients.

🚀 Features
Multi-Client Communication: Supports multiple clients connecting to the server simultaneously.

Chat Management: Send public messages to all users or private messages to specific individuals.

Manager System:

Appoint users as managers.

Kick users off the server.

Mute/Unmute users.

Real-Time Processing: Uses select for efficient handling of requests without blocking.

🛠 Technologies
Python (Socket programming, Select, Datetime).

💻 How to Run
Start the Server:
Open a terminal in the project folder and run:
python chat_server.py

Start the Client:
Open a new terminal and run:
python chat_client.py

Connection:
After the client launches, enter 1 to log in with a username, then choose an action from the menu.

Available Commands
1: Log in.

2: Send a message to all users.

3: Send a private message.

4: Get the managers list.

5: Log out.

Commands 6-9 are available for managers only (appoint, kick, mute, unmute).
