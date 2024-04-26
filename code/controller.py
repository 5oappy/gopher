#controller.py
import os
from client import GopherClient

"""
Controller Module
=================

This module serves as the controller for interacting with the Gopher client and managing file downloads.

Attributes:
    server_host (str): The hostname of the Gopher server.
    server_port (int): The port number of the Gopher server.
    downloads_path (str): The path to the downloads directory.

Functions:
    run(): Starts the Gopher client and handles user inputs.
    purge_downloads(): Purges all files in the downloads directory.
    check_download_path(): Checks if the downloads directory exists and creates it if not.

"""

server_host = 'comp3310.ddns.net'
server_port = 70
downloads_path = os.path.join(os.path.dirname(__file__), '..', 'downloads')

def run():
    client = GopherClient(server_host, server_port)
    check_download_path()
    try:
        while True:

            user_input = input("Enter 'c' to crawl, Enter 'r' to manually traverse, 'b' to exit program, 'x' to purge downloads: ")
            if user_input.lower() == 'c':
                print("Crawling..")
                client.crawl()
                client.stats.analyse_references()
                  
            if user_input.lower() == 'r':
                client.run()
                print("running")

            if user_input.lower() == 'x':
                purge_downloads()

            if user_input.lower() == 'b':
                break
    finally:
        client.close()
    
def purge_downloads():
    """
    Remove all files in the 'downloads' directory.
    """
    try:
        # Iterate over files in the downloads directory and remove them
        for file_name in os.listdir(downloads_path):
            file_path = os.path.join(downloads_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Downloads purged successfully.")
    except Exception as e:
        print("Error purging downloads:", e)

def check_download_path():    
    # Check if the downloads directory exists
    if not os.path.exists(downloads_path):
        # If not, create the downloads directory
        os.makedirs(downloads_path)