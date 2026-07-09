import os
import shutil

print("📁 FILE ORGANIZER")

folder = input("Enter folder path: ")

for file in os.listdir(folder):

    path = os.path.join(folder, file)

    if os.path.isfile(path):

        extension = file.split(".")[-1]

        destination = os.path.join(folder, extension)

        os.makedirs(destination, exist_ok=True)

        shutil.move(path, os.path.join(destination, file))

print("✅ Files organized successfully")
