import csv

data = [
    ["id", "title", "completed"],
    [1, "Learn FastAPI", False],
    [2, "Build Task Manager", True]
]

with open("tasks.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file created successfully")
