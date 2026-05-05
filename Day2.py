MARKS =[78,85,90,67,82,92,78]


def analyse_stats(MARKS):
    total = sum(MARKS)
    average = total/len(MARKS)


    count = 0
    for item in MARKS:
        if item > average:
            count = count + 1

    highest = max(MARKS)
    lowest = min(MARKS)

    return average,highest,lowest,count


def identify_grades(MARKS):

    grades = {
        "A":[],
        "B":[],
        "C":[],
        "FAIL":[]
    }

    for num in MARKS:
        if num >= 90:
            grades["A"].append(num)
        elif num >= 80:
            grades["B"].append(num)
        elif num >= 70:
            grades["C"].append(num)
        else:
            grades["FAIL"].append(num)

    return grades

average,highest,lowest,count = analyse_stats(MARKS)
grades = identify_grades(MARKS)        

print("Average:",average)
print("Highest:",highest)
print("Lowest:",lowest)
print("Students above average:",count)
print("Grades:",grades)          