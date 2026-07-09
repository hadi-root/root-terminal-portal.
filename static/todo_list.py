tasks = []

print("📝 TO-DO LIST")

while True:

    task = input("Add task (or done): ")

    if task.lower() == "done":
        break

    tasks.append(task)

print("\nYOUR TASKS")

for i, task in enumerate(tasks, start=1):

    print(i, ".", task)
