# This code is used to protect and encrypt importtant files with password made by user and have some other features and its work for windows only

# importing modules
from tabulate import tabulate
import os
from termcolor import colored
import time
import glob
from getpass import getpass
from cryptography.fernet import Fernet # we use AES (Advanced Encryption Standard) encryption

# Initializing important variables
if "Locker" not in os.listdir("C:\\"):
    os.mkdir("C:\Locker")
filesPath = r"C:\Locker"  # Windows files path
usersPath = r"C:\Users\{}\Desktop".format(os.getlogin())  # Windows users path
search = r"C:\Users\{}".format(os.getlogin())

data = os.listdir(filesPath)
users = []
for file in data:
    if file.endswith(".txt"):
        users.append(file[:-4])

help = colored("Type \"help\" to see all available commands", "yellow")

# Function to make the output look like its being typed
def Print(theMessage, delay):
    for letter in theMessage:
        print(letter, end='', flush=True)
        time.sleep(delay)
    print('')


# Function to check and match user and password
def login(check):
    boxName = input(colored("Enter username >> ", "magenta")).lower()
    if boxName + ".txt" not in data:
        message = colored(f"User \"{boxName}\" Not Found", "red")
        Print(message, 0.06)
        return -1
    else:
        if check == 1:
            if boxName not in os.listdir(usersPath):
                message = colored("Files is locked please unlock it first", "red")
                Print(message, 0.06)
                return 2
        try:
            os.chdir(filesPath)
        except Exception as Error:
            message = colored(f"Can't access \"{filesPath}\", Error : {Error}", "red")
            Print(message, 0.06)
        try:
            mainKeyFile = open(f"main-{boxName}.key", "rb")
        except Exception as Error:
            message = colored(f"An error occurred when opening \"{mainKeyFile}\", Error : {Error}", "red")
            Print(message, 0.06)
        else:
            mainKey = mainKeyFile.read()
            mainKeyFile.close()
            fernet = Fernet(mainKey)
            try:
                passFile = open(f"{boxName}.txt", "rb")
            except Exception as Error:
                message = colored(f"An error occurred when opening \"{boxName}\", Error : {Error}", "red")
                Print(message, 0.06)
            else:
                passwordBytes = passFile.read()
                passFile.close()
                password = str(fernet.decrypt(passwordBytes))[2:-1]
                passw = getpass(colored(f"Type the password for user \"{boxName}\" >> ", "magenta"))
                if passw != password:
                    message = colored("Wrong password :(", "red")
                    Print(message, 0.06)
                    print('')
                    return 0
                else:
                    return boxName


Print(help, 0.03)

while 1:

    data = os.listdir(filesPath)

    command = input(colored(">> ", "magenta")).capitalize()
    # Create new user
    if command == "Create":
        boxName = input(colored("Create username for the new user >> ", "magenta")).lower()
        if boxName == "" or boxName.startswith("."):
            message = colored("Please, choose a valid username", "red")
            Print(message, 0.06)
        elif boxName + ".txt" in data:
            message = colored("Choose another username, this username is used", "red")
            Print(message, 0.06)
        else:
            box_pass = input(colored(f"Create password for user \"{boxName}\" >> ", "magenta"))
            if len(box_pass) < 6:
                message = colored("Please, create a valid password, password should at least contain 6 characters", "red")
                Print(message, 0.06)
            else:
                try:
                    os.chdir(filesPath)
                except Exception as Error:
                    message = colored(f"Can't access \"{filesPath}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                mainKey = Fernet.generate_key()
                try:
                    mainFile = open(f"{filesPath}\\main-{boxName}.key", "wb")
                except Exception as Error:
                    message = colored(f"An error occurred when opening \"main-{boxName}.key\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                else:
                    mainFile.write(mainKey)
                    mainFile.close()
                    os.system(f"attrib +h main-{boxName}.key")
                    fernet = Fernet(mainKey)
                    passwordBytes = bytes(box_pass, 'utf-8')
                    secret = boxName + ".txt"
                    with open(secret, "wb") as secret_file:
                        secret_file.write(fernet.encrypt(passwordBytes))
                    os.system(f"attrib +h {secret}")
                    os.chdir(usersPath)
                    os.system(f"mkdir \"{boxName}\"")
                    message = colored("User created successfully", "green")
                    Print(message, 0.06)
    # Delete user
    elif command == "Delete":
        flag = login(0)
        boxName = flag
        if type(flag) is str:
            if boxName in os.listdir(usersPath):
                try:
                    os.chdir(filesPath)
                except Exception as Error:
                    message = colored(f"An error occurred when opening \"{filesPath}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                try:
                    os.remove(f"{boxName}.txt")
                except Exception as Error:
                    message = colored(f"An error occurred when deleting \"{boxName}.txt\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                try:
                    os.remove(f"main-{boxName}.key")
                except FileNotFoundError as Error:
                    message = colored(f"An error occurred when deleting \"main-{boxName}.key\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                try:
                    os.chdir(f"{usersPath}\\{boxName}")
                except Exception as Error:
                    message = colored(f"Can't access \"{usersPath}\\{boxName}\", Error : {Error}")
                    Print(message, 0.06)
                    continue
                else:
                    allFiles = os.listdir()
                    for file in allFiles:
                        try:
                            os.remove(file)
                        except FileNotFoundError as Error:
                            message = colored(f"File {file} not found", "red")
                            Print(message, 0.06)
                            continue
                    os.chdir(usersPath)
                    try:
                        os.system(f"rmdir \"{boxName}\"")
                    except FileNotFoundError as Error:
                        message = colored(f"Couldn't find \"{boxName}\"", "red")
                        Print(message, 0.06)
                        continue
                    message = colored(f"User \"{boxName}\" Deleted successfully", "green")
                    Print(message, 0.06)
    # Clear terminal
    elif command == "Clear" or command == "Cls":
        os.system("cls")

    # Change the user password (need the old password)
    elif command == "Update":
        flag = login(0)
        boxName = flag
        if type(flag) is str:
            newPassword = input(colored("Type your new password >> ", "magenta"))
            passwordBytes = bytes(newPassword, 'utf-8')
            try:
                os.chdir(filesPath)
            except Exception as Error:
                message = colored(f"Can't access \"{filesPath}\", Error : {Error}", "red")
                Print(message, 0.06)
                continue
            try:
                mainKeyFile = open(f"main-{boxName}.key", "rb")
            except Exception as Error:
                message = colored(f"An error occurred when opening \"main-{boxName}.key\", Error : {Error}", "red")
                Print(message, 0.06)
                continue
            else:
                mainKey = mainKeyFile.read()
                mainKeyFile.close()
                fernet = Fernet(mainKey)
                os.remove(f"{boxName}.txt")
                secret_file = open(f"{boxName}.txt", "wb")
                secret_file.write(fernet.encrypt(passwordBytes))
                secret_file.close()
                os.system(f"attrib +h {boxName}.txt")
                message = colored("Password changed successfully", "green")
                Print(message, 0.06)
    # Lock the files inside the user folder
    elif command == "Lock":
        flag = login(1)
        boxName = flag
        if type(flag) is str:
            os.chdir(filesPath)
            files = os.listdir()
            file = boxName + ".key"
            if file not in files:
                try:
                    os.chdir(f"{usersPath}\\{boxName}")
                except Exception as Error:
                    message = colored(f"Can't access \"{usersPath}\\{boxName}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                allFiles = glob.glob(f"{usersPath}\\{boxName}\\**\\*.*", recursive=True)
                filesWithPath = []
                files = []
                for file in allFiles:
                    if os.path.isfile(file):
                        filesWithPath.append(file)
                    else:
                        continue
                for file in filesWithPath:
                    new = file.split(f"\\")
                    newFile = new[-1]
                    files.append(newFile)
                key = Fernet.generate_key()
                try:
                    os.chdir(filesPath)
                except Exception as Error:
                    message = colored(f"Can't access \"{filesPath}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                try:
                    keyFile = open(boxName + ".key", "wb")
                except Exception as Error:
                    message = colored(f"An error occurred when opening \"{boxName}.key\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                keyFile.write(key)
                try:
                    os.system(f"attrib +h {boxName}.key")
                except Exception as error:
                    message = colored("An error occurrred while hiding" + f".{boxName}.key", "red")
                    Print(message, 0.06)
                    continue
                try:
                    os.chdir(f"{usersPath}\\{boxName}")
                except Exception as Error:
                    message = colored(f"Can't access \"{usersPath}\\{boxName}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                else:
                    fernet = Fernet(key)
                    for file in files:
                        with open(file, "rb") as tf:
                            tfBytes = tf.read()
                        tfBytesEnc = fernet.encrypt(tfBytes)
                        with open(file, "wb") as tf:
                            tf.write(tfBytesEnc)
                    os.chdir(usersPath)
                    os.system(f"attrib +h {boxName}")
                    message = colored("Files locked successfully", "green")
                    Print(message, 0.06)
            else:
                message = colored("files already locked", "red")
                Print(message, 0.06)
    # Unlock the files in the user folder
    elif command == "Unlock":
        flag = login(0)
        boxName = flag
        if type(flag) is str:
            os.chdir(filesPath)
            theFiles = os.listdir()
            theFile = boxName + ".key"
            if theFile in theFiles:
                try:
                    os.chdir(f"{usersPath}\\{boxName}")
                except Exception as Error:
                    message = colored(f"Can't access \"{usersPath}\\{boxName}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                allFiles = glob.glob(f"{usersPath}\\{boxName}\\**\\*.*", recursive=True)
                filesWithPath = []
                files = []
                for file in allFiles:
                    if os.path.isfile(file):
                        filesWithPath.append(file)
                    else:
                        continue
                for file in filesWithPath:
                    new = file.split(f"\\")
                    newFile = new[-1]
                    files.append(newFile)
                fileName = boxName + ".key"
                try:
                    os.chdir(filesPath)
                except Exception as Error:
                    message = colored(f"Can't access \"{filesPath}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                try:
                    keyFile = open(fileName, "rb")
                except Exception as Error:
                    message = colored(f"An error occurred when opening \"{fileName}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                else:
                    key = keyFile.read()
                    keyFile.close()
                    fernet = Fernet(key)
                    try:
                        os.chdir(f"{usersPath}\\{boxName}")
                    except Exception as Error:
                        message = colored(f"Can't access \"{usersPath}\\{boxName}\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    for file in files:
                        try:
                            tf = open(file, "rb")
                        except Exception as Error:
                            message = colored(f"An error occurred when opening \"{file}\", Error : {Error}", "red")
                            Print(message, 0.06)
                            continue
                        else:
                            tfEnc = tf.read()
                            tfBytes = fernet.decrypt(tfEnc)
                            try:
                                tf = open(file, "wb")
                            except Exception as Error:
                                message = colored(f"An error occurred when opening \"{file}\"\", Error : {Error}", "red")
                                Print(message, 0.06)
                                continue
                            tf.write(tfBytes)
                    try:
                        os.chdir(usersPath)
                    except Exception as Error:
                        message = colored(f"Can't access \"{usersPath}\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    os.chdir(usersPath)
                    try:
                        os.system(f"attrib -h {boxName}")
                    except Exception as Error:
                        message = colored(f"An error occurred when hiding \"{boxName}\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    else:
                        message = colored("Files unlocked successfully", "green")
                        Print(message, 0.06)
                        try:
                            os.chdir(filesPath)
                        except Exception as Error:
                            message = colored(f"Can't access \"{filesPath}\", Error : {Error}", "red")
                            Print(message, 0.06)
                            continue
                        try:
                            os.remove(boxName + ".key")
                        except Exception as Error:
                            message = colored(f"An error occurred when deleting \"{boxName}.key\", Error : {Error}", "red")
                            Print(message, 0.06)
                            continue
            else:
                message = colored("Files already unlocked", "red")
                Print(message, 0.06)
    # Show current users and there state and the number of files inside
    elif command == "Users":
        os.chdir(filesPath)
        allFiles = os.listdir()
        files = []
        data = []
        state = "Not Checked"
        length = 0
        for file in allFiles:
            if file.endswith(".txt"):
                files.append(file)
        for file in files:
            if f"{file[:-4]}.key" in os.listdir(filesPath):
                state = "locked"
                color = "red"
                length = len(os.listdir(f"{usersPath}\\{file[:-4]}"))
            else:
                state = "unlocked"
                color = "green"
                length = len(os.listdir(f"{usersPath}\\{file[:-4]}"))
            data.append([colored(f"{file[:-4]}", color), colored(state, color), colored(length, color)])
        col = [colored("User name", "yellow"), colored("User status", "yellow"), colored("Current number of files", "yellow")]
        if not files:
            message = colored("There is no users found :(", "yellow")
            Print(message, 0.03)
        else:
            print(tabulate(data, headers=col, tablefmt="fancy_grid"))

    # Show help menu
    elif command == "Help":
        data = [[colored("Help", "cyan"), colored("Show this table", "green")],
            [colored("Modules", "cyan"), colored("Check used modules in the program and install any missing module", "green")],
            [colored("Create", "cyan"), colored("Create new user", "green")],
            [colored("Update", "cyan"), colored("Update the password for spacified user", "green")],
            [colored("Delete", "cyan"), colored("Delete spacific user (also the files in the user folder)", "green")],
            [colored("Flush", "cyan"), colored("Delete all the files inside the user folder (not delete the user only the files inside the folder)", "green")],
            [colored("Users", "cyan"), colored("Display all users and the user state and number of files in each user", "green")],
            [colored("Lock", "cyan"), colored("Encrypt the files inside the the user folder and make the folder hidden", "green")],
            [colored("Unlock", "cyan"), colored("Decrypt the files inside the user folder and make the folder visible", "green")],
            [colored("Add", "cyan"), colored("Add file to user folder", "green")],
            [colored("Rename", "cyan"), colored("Change user name", "green")],
            [colored("Files", "cyan"), colored("Show all files inside the user folder", "green")],
            [colored("Arrange", "cyan"), colored("Rename all files inside the user folder to number starting by 1", "green")],
            [colored("Clear", "cyan"), colored("Clear the terminal", "green")],
            [colored("Exit","cyan"), colored("Close the program", "green")]]
        col_name = [colored("Command", "yellow"), colored("Description", "yellow")]
        print(tabulate(data, headers=col_name, tablefmt="fancy_grid"))
    # Add file into the user folder (the files must be unlocked)
    elif command == "Add":
        flag = login(1)
        boxName = flag
        if type(flag) is str:
            fileName = input(colored("Type the file name you want to add >> ", "magenta"))
            allFiles = glob.glob(f"{search}\\**\\*.*", recursive=True)
            files = []
            for file in allFiles:
                c = 0
                if os.path.isfile(file) and file not in files:
                    if fileName in file:
                        for user in users:
                            if user in file:
                                c = 1
                                break
                            else:
                                continue
                        if c == 1:
                            continue
                        else:
                            files.append(file)
                else:
                    continue
            search = []
            for file in files:
                if f"{usersPath}\\{boxName}" in file:
                    continue
                elif fileName.lower() in file.lower():
                    search.append(file)
                else:
                    continue
            c = 0
            for file in search:
                c += 1
                print(colored(str(c).zfill(len(str(len(search)))) + ": " + file, "yellow"))
            if not search:
                message = colored('No files found', "red")
                Print(message, 0.06)
            else:
                select = input(colored("Select files to move to the user locker >> ", "magenta"))
                selected = select.split(",")
                for num in selected:
                    file = search[int(num) - 1]
                    fileName = file.split("\\")[-1]
                    thePath = f"\\".join(file.split(f"\\")[:-1])
                    try:
                        os.chdir(thePath)
                    except Exception as Error:
                        message = colored(f"Can't access \"{thePath}\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    try:
                        os.rename(file, f"{usersPath}\\{boxName}\\{fileName}")
                    except Exception as Error:
                        message = colored(f"An error occurred when moving \"{file}\" to \"{usersPath}\\{boxName}\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                try:
                    os.chdir(f"{usersPath}\\{boxName}")
                except Exception as Error:
                    message = colored(f"Can't access \"{usersPath}\\{boxName}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                else:
                    if fileName in os.listdir():
                        message = colored('File added successfully', "green")
                        Print(message, 0.06)

    # Show the files inside the user folder
    elif command == "Files":
        flag = login(0)
        boxName = flag
        if type(flag) is str:
            try:
                os.chdir(f"{usersPath}\\{boxName}")
            except Exception as Error:
                message = colored(f"Can't access \"{usersPath}\\{boxName}\", Error : {Error}", "red")
                Print(message, 0.06)
                continue
            message = colored(f"You have {len(os.listdir())} files in {boxName}'s folder", "yellow")
            Print(message, 0.06)
            c = 1
            for file in os.listdir():
                print(colored(f"{c} : " + file, "yellow"))
                c += 1
    # Rename the user (change folder name and all files that control the user)
    elif command == "Rename":
        flag = login(1)
        boxName = flag
        if type(flag) is str:
            name = input(colored("Enter the new name >> ", "magenta")).lower()
            if name == boxName:
                message = colored("User name not changed", "red")
                Print(message, 0.06)
            else:
                try:
                    os.chdir(usersPath)
                except Exception as Error:
                    message = colored(f"Cant access \"{usersPath}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
                if boxName in os.listdir(usersPath):
                    try:
                        os.rename(boxName, name)
                    except Exception as Error:
                        message = colored(f"An error occurred when rename \"{boxName}\" to \"{name}\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    try:
                        os.chdir(filesPath)
                    except Exception as Error:
                        message = colored(f"Can't access \"{filesPath}\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    try:
                        os.rename(f"{boxName}.txt", f"{name}.txt")
                    except Exception as Error:
                        message = colored(f"An error occurred when rename \"{boxName}.txt\" to \"{name}.txt\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    try:
                        os.rename(f"main-{boxName}.key", f"main-{name}.key")
                    except Exception as Error:
                        message = colored(f"An error occurred when rename \"main-{boxName}.key\" to \"main-{name}.key\", Error : {Error}", "red")
                        Print(message, 0.06)
                        continue
                    else:
                        message = colored(f"User \"{boxName}\" Renamed To \"{name}\"", "green")
                        Print(message, 0.06)
    # Arrange files in the user folder
    elif command == "Arrange":
        flag = login(0)
        boxName = flag
        if type(flag) is str:
            if boxName in os.listdir(usersPath):
                os.chdir(f"{usersPath}\\{boxName}")
                i = 1
                files = os.listdir()
                if not files:
                    message = colored("No files found", "red")
                    Print(message, 0.06)
                else:
                    for file in files:
                        try:
                            os.rename(file, f"{i}.{file.split('.')[-1]}")
                        except Exception as Error:
                            message = colored(f"An error occurred when rename \"{file}\" to \"{i}.{file.split('.')[-1]}\", Error : {Error}", "red")
                            Print(message, 0.06)
                            continue
                        i += 1
                    message = colored("Files arranged successfully", "green")
                    Print(message, 0.06)
    # Delete all files in the user folder also if it was locked
    elif command == "Flush":
        flag = login(0)
        boxName = flag
        if type(flag) is str:
            try:
                os.chdir(f"{usersPath}\\{boxName}")
            except FileNotFoundError:
                message = colored(f"Cant access \"{usersPath}\\{boxName}\"")
                Print(message, 0.06)
                continue
            files = os.listdir()
            for file in files:
                try:
                    os.remove(file)
                except Exception as Error:
                    message = colored(f"An error occurred when deleting \"{file}\", Error : {Error}", "red")
                    Print(message, 0.06)
                    continue
            if not os.listdir(f"{usersPath}\\{boxName}"):
                message = colored(f"User {boxName} cleared successfully", "green")
            else:
                message = colored(f"Unknown error happened", "red")
            Print(message, 0.06)
    # Close the script
    elif command == "Exit":
        message = colored("Good bye", "green")
        Print(message, 0.06)
        break
    # Show the error message if the user choose unsupported command
    else:
        message = colored(f"Command \"{command}\" not found", "red")
        Print(message, 0.06)
