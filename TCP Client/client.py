# STUDENT NAME: Abhishek Dan 816024372, Tamika Brittney Ramkissoon 816010368
# COMP2602: Computer Networks (Semester I- 2021/2022)
# 27th September 2021
# Connetion type use: TCP
# Members contribution: Both members utilized the discord platform for collaboration while learning to python languages and as well the basics of socket programming through lecture notes and additional research. Real time coding collaboration was done on replit.com. Both members contributed to the development and pseudocode algorithm of each command on the server.py and client.py files.
#Abhishek Dan 816024372 contribution to the server.py file: LIST, SHOW, DELETE, WORDCOUNT
#Abhishek Dan 816024372 contribution to the python.py file:
#PUT, CREATE, SEARCH, EXIT and commands validation(errors statements)
#Tamika Ramkissoon 816010368 contributions to the server.py file: PUT, CREATE, SEARCH, EXIT and commands validation(errors statements)
#Tamika Ramkissoon 816010368 contributions to the python.py
#LIST, SHOW, DELETE, WORDCOUNT
# Both Abhishek Dan and Tamika Ramkission made contributions to the documentation

import socket 
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)# creates tuple
FORMAT = "utf-8"
SIZE = 1024

def main():
    running = True
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#uses TCP socket
    client.connect(ADDR)#client connects to socket
    
    while running:
        
    # Sends commands from the Client to the Server
        print()
        print("Command List: PUT, CREATE, LIST, SHOW, DELETE, WORDCOUNT, SEARCH, EXIT")
        print()
        line = input("Enter a command: ")
        command = line.split()
        client.send(str(command[0]).encode(FORMAT))
        if(command[0] != "LIST"):
            if(command[0] != "EXIT"):
                client.send(str(command[1]).encode(FORMAT))
    ############################################
    #PUT
    
    # If file is found, read and send the file contents to the server
        if(command[0] == "PUT"):
            filename = command[1]
            found = False
            dir = os.getcwd()
            for files in os.listdir(dir):
                if (files == filename):
                    found = True
                
            client.send(str(found).encode(FORMAT))
            
            if (found == True):
                file = open(filename, "r")
                data = file.read()
                client.send(data.encode(FORMAT))
                msg = client.recv(SIZE).decode(FORMAT)
                print(f"[SERVER]: {msg}")

                client.send(data.encode(FORMAT))
                msg = client.recv(SIZE).decode(FORMAT)
                print(f"[SERVER]: {msg}")

                file.close()#closes file for PUT

            else:
                print("[ERROR] Invalid file name!!! ")

    ###########################################
    #CREATE
    
    # Sends to data(file content) to the Server
        if(command[0] == "CREATE"):
            createFilename = command[1]
            createText = input("[CLIENT INPUT] Enter your file data: ")
            createMsg = client.recv(SIZE).decode(FORMAT)
            print(createMsg)
            client.send(createText.encode(FORMAT))
            createMsg = client.recv(SIZE).decode(FORMAT)
            print("[SENT] File information sent to server")
            print(createMsg)
            
    ###############################################
    #LIST
    
    # Recieves the list of server files and prints it to the terminal
        if(command[0] == "LIST"):
            msg = client.recv(SIZE).decode(FORMAT)
            print("Files: ")
            print(msg)
    
    ###########################################
    #SHOW

    #Receives the file contents and prints the message
        if(command[0] == "SHOW"):
            fileToShow = command[1]
            fileContent = client.recv(SIZE).decode(FORMAT)
            print("Content of ", fileToShow, ": ",  "\n", fileContent)
    
    ###########################################
    #DELETE
    
    # Deletes the file from the server side and or returns the appropriate message
        if(command[0] == "DELETE"):
            fileToDelete = command[1]
            msg = client.recv(SIZE).decode(FORMAT)
            print(msg)

    ##########################################################
    #WORDCOUNT

    # Receives and Prints the wordcount of the file specified
        if(command[0] == "WORDCOUNT"):
            countFile = command[1]
            numWords = client.recv(SIZE).decode(FORMAT)
            print("The number of words in ",countFile, " is: ", "\n", numWords)

    ################################################################
    #SEARCH
    
    # Sends the word to search for to the server
    # Prints the returned message
        if(command[0] == "SEARCH"):
            fileSearch = command[1]
            wordSearch = input("[CLIENT INPUT] Enter word to search for: ")
            client.send(wordSearch.encode(FORMAT))
            found = client.recv(SIZE).decode(FORMAT)
            print(found)

    ######################################################
    #EXIT
    
    # Closes the connection and ends the loop
        if(command[0] == "EXIT"):
            print("[DISCONNECTED] Client disconnected from server")
            client.close()#ends connection
            running = False
        
        command = None
        line = None
        
if __name__ == "__main__":
    main()
    
####################################################################################
    










