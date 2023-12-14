from TrashHubBackend import create_app
import socket
socket.setdefaulttimeout(120)
app = create_app()