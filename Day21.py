def is_prime(number):
    if number < 2:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True


# Test Prime Function
num = int(input("Enter a number: "))

if is_prime(num):
    print(num, "is a prime number")
else:
    print(num, "is not a prime number")


# 2. Function using *args to find the largest number
def find_largest(*args):
    if not args:
        return None

    return max(args)


print("\nLargest Number:", find_largest(10, 25, 7, 45, 18))


# 3. Function using **kwargs to print student information
def student_info(**kwargs):
    print("\nStudent Information:")

    for key, value in kwargs.items():
        print(f"{key}: {value}")


student_info(
    name="Sahil",
    age=19,
    course="B.Tech AIML",
    year=2,
    university="Kurukshetra University"
)


# 4. Challenge - List Statistics
def calculate_statistics(numbers):
    total = sum(numbers)
    maximum = max(numbers)
    minimum = min(numbers)
    average = total / len(numbers)

    return maximum, minimum, average, total


numbers = [10, 20, 30, 40, 50]

maximum, minimum, average, total = calculate_statistics(numbers)

print("\nList Statistics:")
print("Maximum:", maximum)
print("Minimum:", minimum)
print("Average:", average)
print("Sum:", total)