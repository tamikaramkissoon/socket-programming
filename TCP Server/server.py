import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)  # creates tuple
FORMAT = "utf-8"
SIZE = 1024

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # uses TCP socket
    server.bind(ADDR)
    server.listen()  # listen for 1 connection
    print("[Listening] Server is listening for connection request from client...")
    conn, addr = server.accept()  # accepts connection from client
    print(f"[NEW CONNECTION] {addr} connected.")
    print()
    running = True
    # handles only one client at a time
    # while loop terminates only when the program is terminated
    while running:
        
    # Receives Commands from the Client
        print()
        print("[WAITING] Waiting for command from user ...")
        print()
        command = conn.recv(SIZE).decode(FORMAT)
        if(command != "LIST"):
            if(command != "EXIT"):
                command2 = conn.recv(SIZE).decode(FORMAT)
                
    #############################################################
    #PUT

    # If file is found, creates the file and prints the data received in to the file.
        if(command == "PUT"):
            
            found = str(conn.recv(SIZE).decode(FORMAT))
            print(found)
            
            if(found == "True"):
                data = conn.recv(SIZE).decode(FORMAT)
                filename = command2
                print("[RECEIVED] Filename received...")
                print(filename)
                print(data)
                file = open(filename, "w")
                conn.send("Filename received.".encode(FORMAT))
                data = conn.recv(SIZE).decode(FORMAT)
                print(f"[RECEIVED] File data received...")
                file.write(data)
                conn.send("File data received...".encode(FORMAT))
                file.close()  # closes file for PUT

    #############################################################
    # CREATE

    # Creates a file with the specified name.
    # Receives and prints the data from the Client in to the file.
        if(command == "CREATE"):
            createFilename = command2
            print("[RECEIVED] Filename received...")
            createFile = open(createFilename, "w")
            conn.send("Filename received.".encode(FORMAT))
            createText = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECEIVED] File data received...")
            createFile.write(createText)
            conn.send("File data received by server...".encode(FORMAT))
            createFile.close()  # closes file for CREATE


    ####################################################
    #LIST

    # Gets the list of files in the source folder and sends the string to the Client
        if(command == "LIST"):
            dir = os.getcwd()
            tempString = ""
            for file in os.listdir(dir):
                tempString += (os.path.join(file, "\n"))
            conn.send(tempString.encode(FORMAT))
            print("[SERVER] List of files sent")


    ###########################################
    #SHOW
    
    # Finds the file in the directory, reads and returns the file contents.
    # Return Error is the file is not found.
        if(command == "SHOW"):
            fileToShow = command2
            found = False
            dir = os.getcwd()
            for files in os.listdir(dir):
                if (files == fileToShow):
                    found = True

            if (found == True):
                openFile = open(fileToShow, "r")
                text = openFile.read()
                conn.send(text.encode(FORMAT))
                print("[SERVER] File Content sent!")
                print("[SENT] File contents sent: ", text)
                openFile.close()
            else:
                conn.send("[ERROR] File does not exist, no contents to show".encode(FORMAT))
                print("[ERROR] File does not exist, no contents to show")

    ###########################################
    #DELETE
    
    # Deletes the file specified by the Client and returns the appropriate message
        if(command == "DELETE"):
            fileToDelete = command2
            found = False
            dir = os.getcwd()
            for files in os.listdir(dir):
                if (files == fileToDelete):
                    found = True

            if (found == True):
                os.remove(fileToDelete)
                conn.send("File Deleted!".encode(FORMAT))
                print("[SERVER]", fileToDelete, " has been deleted.")
            else:
                conn.send("[ERROR] File does not exist, Unable to delete file".encode(FORMAT))
                print("[ERROR] File does not exist, Unable to delete file")

    ##########################################################
    #WORDCOUNT

    # Finds the file in the directory and counts the number of words. Returns the appropriate message to the Client.
        if(command == "WORDCOUNT"):
            countFile = command2
            found = False
            dir = os.getcwd()
            for files in os.listdir(dir):
                if (files == countFile):
                    found = True

            if (found == True):
                file = open(countFile, "r")
                numWords = 0
                for line in file:
                    line = line.split()
                    numWords += len(line)
                file.close()
                
                conn.send(str(numWords).encode(FORMAT))
                print("[SENT] Number of words sent: ", numWords)
                
            else:
                conn.send("[ERROR] File does not exist, Unable to count words in file".encode(FORMAT))
                print("[ERROR] File does not exist, Unable to count words in file")


    ##########################################################
    #SEARCH
    
    # Opens the file specified and search for the specified word.
    # Returns the appropriate message
        if(command == "SEARCH"):
            fileSearch = command2
            wordSearch = conn.recv(SIZE).decode(FORMAT)
            found = False
            dir = os.getcwd()
            for files in os.listdir(dir):
                if (files == fileSearch):
                    found = True

            if (found == True):
                openFile = open(fileSearch, "r")
                wordFound = 0
                count = 0

                for i in openFile:
                    if wordSearch in i:
                        wordFound = 1
                        count = count+1

                if wordFound == 0:
                    print("[SERVER]", wordSearch, " not found in ", fileSearch)
                    conn.send(" Word not found!".encode(FORMAT))
                else:
                    print("[SERVER]", wordSearch, " found in ", fileSearch)
                    conn.send(" Word found!".encode(FORMAT))

                openFile.close()
            else:
                conn.send("[ERROR] File does not exist, Unable to search for word in file".encode(FORMAT))
                print("[ERROR] File does not exist, Unable to search for word in file") 

    ######################################################
    # EXIT
    
    # Closes the connection and ends the loop
        if(command == "EXIT"):
            print(f"[DISCONNECTED] {addr} disconnected...")
            print("[DISCONNECTED] Socket closed")
            conn.close()  # end connection
            running = False
        
        command = None
        command2 = None

if __name__ == "__main__":
    main()

####################################################################################
