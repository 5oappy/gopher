# gopher
welcome to the last Gopher client you'll ever cry about 

## Classes

### GopherClient

### Parser

### FileStats

## Methods

## Intercations

## Parser design

## Setup



## Requirements
What your successful and highly-rated indexing client will need to do:
1. Connect to the class gopher server, and get the initial response.
a. Wireshark (just) this initial-response conversation in both directions, from the starting TCP
connection to its closing, and include that wireshark summary in your README.
b. The class gopher site is not yet fully operational, an announcement will be made when it’s ready.
2. Starting with the initial response, automatically scan through the directories on the server, following links
to any other directories on the same server, and download any text and binary (non-text) files you find.
The downloading allows you to measure the file characteristics. Keep scanning till you run out of
references to visit. Note that there will be items linked more than once, so beware of getting stuck in a
loop.
3. While running, prints to STDOUT:
a. The timestamp (time of day) of each request, with
b. The client-request you are sending. This is good for debugging and checking if something gets
stuck somewhere, especially when dealing with a remote server.
4. Count, possibly store, and (at the end of the run) print out:
a. The number of Gopher directories on the server.
b. The number, and a list of all simple text files (full path)
c. The number, and a list of all binary (i.e. non-text) files (full path)
d. The contents of the smallest text file.
e. The size of the largest text file.
f. The size of the smallest and the largest binary files.
g. The number of unique invalid references (those with an “error” type)
h. A list of external servers (those on a different host and/or port) that were referenced, and
whether or not they were "up" (i.e. whether they accepted a connection on the specified port).
i. You should only connect to each external server (host+port combination) once. Don't
crawl their contents! We only need to know if they're "up" or not.
i. Any references that have “issues/errors”, that your code needs to explicitly deal with.
