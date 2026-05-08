students = []

with open("students.csv", "r") as file:
    lines = file.readlines()

headers = lines[0].strip().split(",")

for line in lines[1:]:
    data = line.strip().split(",")

    student = {
        headers[0]: data[0],
        headers[1]: int(data[1]),
        headers[2]: int(data[2])
    }

    students.append(student)

print(students)

total = 0

for student in students:
    total += student["MARKS"]

average = total / len(students)

print("Average Marks:", average)