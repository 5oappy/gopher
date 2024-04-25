#client.py
import socket
import time
from parser import Parser
import stats as file_stats
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
                response = self.socket.recv(4096).decode()
                return response
            except socket.timeout:
                print("Response: (timeout)")
                return "empty"

            

    def scan_directory(self, directory):
        # Implement directory scanning logic here
        
        pass

    def download_file(self, selector):
        print("Reached downloader")
        try:
            self.connect()
            print("connected")
            print("Sent request:", selector)
            self.send_request(selector)
            response = self.receive_response()
            print("Received response")
            
            # Check if the file is text or binary
            if selector.endswith('.txt'):
                print("Downloading text file...")
                print(response)  # Print or process the text file content
            else:
                print("Downloading binary file...")
                # Implement logic to save or process binary file content
                
        except Exception as e:
            print("Error:", e)
            # Handle exceptions gracefully

        finally:
            self.close()
        
       
    def run(self):
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



    def check_external(self, host, port):
        if self.server_host != host:
            return True
        elif self.server_port != port:
            return True
        return False


        # do stuff
     
    
    # def intialise(self):
    #     self.send_request("")
    #     initial_response = self.receive_response()
    #     self.parser = Parser(initial_response)
    #     print(initial_response)
        
    
                
"""
empty = "\r\n"
self.send_request(empty)
initial_response = self.receive_response()
print("Initial Response:", initial_response)
"""