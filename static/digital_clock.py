import time

print("🕒 DIGITAL CLOCK")

while True:

    current = time.strftime("%H:%M:%S")

    print(current, end="\r")

    time.sleep(1)
