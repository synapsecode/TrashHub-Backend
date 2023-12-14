from TrashHubBackend import create_app
from TrashHubBackend.config import Config
import socket

socket.setdefaulttimeout(120)
app = create_app()
config = Config()
if __name__ == '__main__':
	app.run(debug=True, host=config.HOST_NAME, port=config.PORT_NUMBER)