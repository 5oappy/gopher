#controller.py
from client import GopherClient

server_host = 'comp3310.ddns.net'
server_port = 70

def run():
    client = GopherClient(server_host, server_port)
    
    try:
        while True:
            # Perform Gopher client operations here
            user_input = input("Enter 'c' to crawl, Enter 'r' to run client, 'b' to exit program, 's' to scan: ")
            if user_input.lower() == 'c':
                print("Crawling..")
                client.crawl()
                  
            if user_input.lower() == 'r':
                client.run()
                print("running")
            # Break out of the loop if 'b' is entered
            if user_input.lower() == 'b':
                break
    finally:
        client.close()
    
