#controller.py
import os
from client import GopherClient

server_host = 'comp3310.ddns.net'
server_port = 70

def run():
    client = GopherClient(server_host, server_port)
    
    try:
        while True:
            # Perform Gopher client operations here
            user_input = input("Enter 'c' to crawl, Enter 'r' to manually traverse, 'b' to exit program, 'x' to purge downloads (debug): ")
            if user_input.lower() == 'c':
                print("Crawling..")
                client.crawl()
                  
            if user_input.lower() == 'r':
                client.run()
                print("running")
            
            if user_input.lower() == 'x':
                purge_downloads()
                
            # Break out of the loop if 'b' is entered    
            if user_input.lower() == 'b':
                break
    finally:
        client.close()
    
def purge_downloads():
    """
    Remove all files in the 'downloads' directory.
    """
    try:
        # Get the absolute path of the downloads directory
        downloads_path = os.path.join(os.path.dirname(__file__), '..', 'downloads')

        # Iterate over files in the downloads directory and remove them
        for file_name in os.listdir(downloads_path):
            file_path = os.path.join(downloads_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Downloads purged successfully.")
    except Exception as e:
        print("Error purging downloads:", e)
