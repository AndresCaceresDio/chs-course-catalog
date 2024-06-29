import os
import numpy as np

class Archive:
    def __init__(self):
        self.fileList = []

    def create_file(self, file_name):
        try:
            open(file_name, "x")
            self.fileList.append(file_name)
        except FileExistsError:
            print(f"Error: File '{file_name}' already exists")

    def write_to_file(self, file_name, content):
        if file_name in self.fileList:
            if os.path.isfile(file_name):
                f = open(file_name, "a")
                f.write(content)
            else:
                print(f"Error: File '{file_name}' does not exist")
        else:
            print(f"Error: File '{file_name}' is not in the list")

    def read_file(self, file_name):
        if file_name in self.fileList:
            try:
                f = open(file_name, "r")
                print(f.read())
            except FileNotFoundError:
                print(f"Error: File '{file_name}' does not exist")
        else:
            print(f"Error: File '{file_name}' is not in the list")

class Computer:
    def __init__(self, list):
        self.fileLists = []
        for i in list:
            self.fileLists.append(np.array(i))
        self.allFiles = np.sort(np.hstack(self.fileLists))
        self.allArchives = np.vstack(self.fileLists)


# Create an Archive object
archive1 = Archive()

# Create some files
archive1.create_file("file1.txt")
archive1.create_file("file2.txt")

# Try to create an existing file
archive1.create_file("file1.txt")

# Write to the files
archive1.write_to_file("file1.txt", "Hello, World!\n")
archive1.write_to_file("file2.txt", "This is a test.\n")

# Try to write to a non-existent file
archive1.write_to_file("file3.txt", "This should fail.\n")

# Read the files
archive1.read_file("file1.txt")
archive1.read_file("file2.txt")

# Try to read a non-existent file
archive1.read_file("file3.txt")

# Create another Archive object
archive2 = Archive()

# Create a file in the second archive
archive2.create_file("file3.txt")
archive2.create_file("file4.txt")

# Create a Computer object with the two archives
computer = Computer([archive1.fileList, archive2.fileList])

# Print the sorted list of all files in the Computer object
print("All files in the computer:", computer.allFiles)

# Print the 2D array of all archives in the Computer object
print("All archives in the computer:\n", computer.allArchives)

# Access "file3.txt" from allFiles
print(computer.allFiles[2])

# Access "file3.txt" from allArchives
print(computer.allArchives[1, 0])
