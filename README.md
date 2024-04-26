# gopher
welcome to the last Gopher client you'll ever cry about 

## About
Based on rfc1436, the GopherClient is designed to interact with Gopher servers, facilitating seamless communication and file retrieval. By establishing a connection to the specified server, it enables users to send requests and receive responses, handling both text and binary files efficiently. Utilizing methods such as download_text_file() and download_binary_file(), it offers a straightforward approach to retrieve files from the server. Additionally, with features like directory crawling and error handling, the GopherClient ensures a smooth and reliable experience, making it an essential tool for navigating Gopher networks effortlessly.

currently the gopher is only setup for the specified anu server site: https://gopher.floodgap.com/gopher/gw?gopher://comp3310.ddns.net:70/1 however, the logic can be easily modified to have conections specific to all gopher servers.
## Setup

### requirements 
Python 2.7.18 +
zsh for mac 
powershell core for windows


After extracting from .zip or cloning from git repo https://github.com/5oappy/gopher
simply run the main.py file from your chosen terminal or preffered python ide.

command:
python3 ~/`<path to extracted zip file or cloned repo>`/gopher/code/main.py

Follow the terminal instructions to utilise the tool more info at [interactions](#Intercations) section.

If there is a break ensure the client is properly instantiated as there may be a chance that the specified server is no longer availible at which you will have to modify the code and provide your own server host and port.

## Classes
Documentation of classes within the code

### GopherClient
within client.py there is also a class level instance of FileStats

#### Attributes
- `server_host`: Hostname of the Gopher server.
- `server_port`: Port number of the Gopher server.
- `socket`: Socket object for communication.
- `parser`: Parser object for parsing responses.
- `visited`: Set to track visited directories.
- `stats`: FileStats instance for tracking file statistics.

#### Methods
- `connect()`: Establishes a connection to the Gopher server.
- `close()`: Closes the connection with the server.
- `send_request(request)`: Sends a request to the server.
- `receive_response(timeout)`: Receives and returns the server's response.
- `save_path(selector)`: Generates a save path for downloaded files.
- `download_text_file(selector)`: Downloads a text file from the server.
- `download_binary_file(selector)`: Downloads a binary file from the server.
- `crawl(selector)`: Crawls through Gopher directories recursively.
- `run()`: Runs the client manually, allowing user interaction.

### Parser
The parser is the backbone of the client's response processing mechanism. Upon receiving data from the Gopher server, it meticulously dissects each line, identifying different types of content such as directories, text files, or binary files based on predefined indicators. more availible at 'downloads/rfc1436.txt' (you will have to run the gopher client first for easy viewing).

#### Methods

- `__init__(input_text, client_instance)`: Initializes the Parser object with input text and a client instance.
- `parse_response()`: Parses the input text and extracts options.
    - Currently only resources `'type' == '0'`, binary `'type' == '9'`, and directories `'type' == '1'` are processed, others mentioned within the rfc1436 are inlcuded with templates.
- `parse_option(parts)`: Parses an individual option and returns a dictionary.
- `extract_paths()`: Extracts paths from the input text.


### FileStats
Acts as a singleton class where all interation files directly refernce an instance of it with the client class to ensure the acuracy of stats at the end of each crawl.

#### Attributes

- `gopher_dirs`: Number of Gopher directories on the server.
- `simple_text_files`: List of full paths of simple text files.
- `binary_files`: List of full paths of simple binary files.
- `smallest_text_file_content`: Contents of the smallest text file.
- `largest_text_file_size`: Size of the largest text file.
- `smallest_binary_file_size`: Size of the smallest binary file.
- `largest_binary_file_size`: Size of the largest binary file.
- `unique_invalid_references`: List of unique invalid references.
- `external_servers`: Dictionary of external servers with their status.

#### Methods

- `add_binary_file(path)`: Adds a binary file to the list.
- `add_simple_text_file(path)`: Adds a simple text file to the list.
- `increment_dirs()`: Increments the count of Gopher directories.
- `add_external(host, port, status)`: Adds an external server with its status.
- `update_text_file_stats(content)`: Updates statistics for text files.
- `update_binary_file_stats(file_size)`: Updates statistics for binary files.
- `add_invalid_references(path)`: Adds an invalid reference to the list.
- `analyse_references()`: Analyzes and prints statistics for file references.

## Intercations
when running the code you are provided with a number of actions:
Enter 'c' to crawl, Enter 'r' to manually traverse, 'b' to exit program, 'x' to purge downloads: 
- crawling the server will make the client traverse the directories and download all the files it can printing a stat sheet at the end of execution.
- exiting the program kills the main process.
- purging downloads gets rid of everything inside the downloads folder, or creates one if it does not exist.
- manually traversing the directories will present the user with a list of options of directories or resoruces to pick from. Of which choosing a direcotry will step you into it one step, and choosing a resourse will download it only if it ends in .txt to ensure safety.

#### example:

```
/opt/homebrew/bin/python3 ~/gopher/code/main.py
Enter 'c' to crawl, Enter 'r' to manually traverse, 'b' to exit program, 'x' to purge downloads: r
Timestamp: 2024-04-26 22:53:55
`<inital response printed here>`
Select from the following options:
/rfc1436.txt

/acme
/maze/17
/misc

Enter your choice (or press 'q' to quit): /acme
Timestamp: 2024-04-26 22:54:07
Response: iWelcome to Acme Rocket-Powered Products Pty. Ltd.'s Gopher site!             invalid 0
i               invalid 0
0About Us       /acme/about     comp3310.ddns.net       70
1Products       /acme/products  comp3310.ddns.net       70
0Contact Us     /acme/contact   comp3310.ddns.net       70
.

Enter your choice (or press 'q' to quit): 
```

### controller.py

#### Variables

- `server_host`: Hostname of the Gopher server.
- `server_port`: Port number of the Gopher server.
- `downloads_path`: Path to the downloads directory.

#### Methods

- `run()`: Main function to run the Gopher client.
- `purge_downloads()`: Removes all files in the downloads directory.
- `check_download_path()`: Checks if the downloads directory exists and creates it if not.


## Parser design
The parser was designed for simplicity as it is understood that gopher servers vary drastically within what functions are accessible (server side) depending on use cases. Thus the decision was made to implement the essentials, just enough to traverse the full server and download what resources it may contain, essentially a get request. 

many of these decisons are reflected within the file sats:
- All directories will be accessed once when crawling the file structure.
- All resources will be downloaded if reachable.
- All downloads will opperate on a separate client instance to avoid memory conflicts with proccesses that are currently accessing the main client
- Malformed resources within the response will not be downloaded if its format is too deviated.
- Client sockets will time out when server is too slow, which may indicate too much traffic, regardless of reason the data trasnmistted is now less reliable as such it is in the best interest to kill the client socket and try again when there is a better connection.
- Servers may send infinitely long data to hog the client whether it be simply bad code server side or bad actors keeping the connection open to pass through malicious pakages, in all cases it is best to simply time the receiving connection if it has taken longer than usual. This may not be as accurate as a checksum, however, will function well enough for obvious sittuations.

## wire Shark

[wireshark setup and ready to listen to gopher](photos/wireshark1.png)

[wireshark stats within initial crawl](photos/wireshark2.png)

[wire shark stats after executing crawl and downloading all files](photos/wireshark3.png)
