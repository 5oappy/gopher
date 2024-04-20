#client.py
import socket
import time
"""
site: https://gopher.floodgap.com/gopher/gw?gopher://comp3310.ddns.net:70/1

Host is: comp3310.ddns.net
Port is 70
"""

class GopherClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))
        print("Connected to server.")
    
    def close(self):
        if self.socket:
            self.socket.close()
    
    def send_request(self, request):
        if self.socket:
            self.socket.sendall(request.encode())

    def receive_response(self):
        if self.socket:
            return self.socket.recv(4096).decode()

    def scan_directory(self, directory):
        # Implement directory scanning logic here
        
        pass

    def download_file(self, file_path):
        # Implement file download logic here
        pass

    def run(self):
        # Implement main logic to connect, scan directories, download files, and print statistics
        self.connect()
        empty = "\r\n"
        self.send_request(empty)
        initial_response = self.receive_response()
        print("Initial Response:", initial_response)
        self.close()
        print("Connection Closed")

