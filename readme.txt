you can start a server by simply typing: 
    python3 .\server.py

or using the Makefile:
    make server

you can join a server by typing:
    python3 .\client.py

or using the Makefile:
    make client

if you want to host a server on a specific IPv6, and/or port, you can add it as parameters while running:
    python3 .\server.py ::1 60606
    python3 .\client.py ::1 60606