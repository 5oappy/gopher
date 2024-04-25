#client.py
import socket
import os
import time
from parser import Parser
import statistics as s
stats_instance = s.Stats()
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
        self.parser = None
        self.visited = set()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Timestamp:", timestamp)
    
    def close(self):
        if self.socket:
            self.socket.close()
            print("Socket closed")
    
    def send_request(self, request):
        if self.socket:
            self.socket.sendall((request + "\r\n").encode())
            
    
    def receive_response(self):
        if self.socket:
            try:
                # Initialize an empty string to store the response
                response = ""
                # Receive data in chunks until all data is received
                while True:
                    chunk = self.socket.recv(4096).decode()  # Receive a chunk of data
                    if not chunk:  # Check if no more data is received
                        break
                    response += chunk  # Append the chunk to the response
                return response
            except socket.timeout:
                print("Response: (timeout)")
                return "empty"
            except Exception as e:
                print("Error receiving response:", e)
                return "error"


    def download_file(self, selector):
        print("Reached downloader")
        try:
            self.connect()
            print("Sent request:", selector)
            self.send_request(selector)
            response = self.receive_response()
            print("Received response")
            
            # Check if the file is text or binary
            save_path = os.path.join('downloads', os.path.basename(selector))
            if selector.endswith('.txt'):
                print("Downloading text file...")
                with open(save_path, 'w') as file:  # Open in text mode for text files
                    file.write(response)
                print("Text file downloaded successfully")
            else:
                print("Downloading binary file...")
                with open(save_path, 'wb') as file:  # Open in binary mode for binary files
                    file.write(response.encode())  # Encode the string response to bytes
                print("Binary file downloaded successfully")
            
            print(f"File saved to: {save_path}")
            
        except Exception as e:
            print("Error:", e)
            # Handle exceptions gracefully

        finally:
            self.close()
            
            
    def crawl(self, selector="", visited=set(), stats=None):
        self.initialise(selector)
        options = self.parser.parse_response()

        for option in options:
            if option['type'] == '1':  # Directory
                # Check if external server
                if option['host'] != self.server_host:
                    continue
                # Check if id exist in visited
                check = self.checkVisted(option['selector'], option['host'], option['port'])

                if check == True: continue

                self.visited.add(check)
                
                print("Crawling into directory:", option['name']) 
                self.crawl(option['selector'], self.visited, stats)
            elif option['type'] == '0':  # File or resource
                print("Downloading file:", option['name'])
                download_client = GopherClient(option['host'], int(option['port']))
                download_client.download_file(option['selector'])
                
        self.close()
        
       
    def run(self):
        self.initialise("")
        options = self.parser.extract_paths()
        print("Select from the following options:")
        for option in options:
            print(option)

        user_input = input("Enter your choice: ")
        
        if user_input:
            self.connect()
            self.send_request(user_input)
            response = self.receive_response()
            self.parser = Parser(response)
            print("Response:",response)
            if user_input.endswith('.txt'):
                self.download_file(user_input)
    
    
    def checkVisted(self, selector, host, port):
        id = host + str(port) + selector
        if id in self.visited:
            return True
        return id

        
    def initialise(self, selector):
        self.connect()
        print("Request: ", selector)
        self.send_request(selector)
        response = self.receive_response()
        self.parser = Parser(response)
        print(response)
        
        
    def check_external(self, host):
        if self.server_host != host:
            return True
        return False
    
