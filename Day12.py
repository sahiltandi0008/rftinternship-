import matplotlib.pyplot as plt
import numpy as np

students = ["AMIT", "RIYA", "JOHN"]


maths = [85, 92, 78]
science = [88, 90, 80]


plt.figure(figsize=(6, 4))

plt.bar(students, maths)

plt.title("Student Performance Dashboard")
plt.xlabel("Students")
plt.ylabel("Maths Marks")

plt.show()

x = np.arange(len(students))
width = 0.35

plt.figure(figsize=(7, 5))

plt.bar(x - width/2, maths, width, label='Maths')
plt.bar(x + width/2, science, width, label='Science')

plt.title("Student Performance Comparison")
plt.xlabel("Students")
plt.ylabel("Marks")

plt.xticks(x, students)

plt.legend()

plt.show()