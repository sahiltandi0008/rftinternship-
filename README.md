## Day 1 - List Cleaner
- Description:-
This Python program removes duplicate values and invalid entries like None and empty strings from a list and returns a clean list.
- Features:-
Removes duplicates
Removes invalid values
Counts removed elements
- Example:-
Input: [10, None, 20, 10, "", 30, None, 40]
Output: [10, 20, 30, 40]
Removed values: 4
- Run:-
python Day1.py

## Day 2 - Student Score Analyzer
- Description:-
This python program calculate average,highest,lowest, count how many studnet score above average and create grade distribution for them.
- Features:-
Calculate Average
Calculate Highest & Lowest
Count students scored above average
Create grade distribution
- Example:-
Input: [78,85,90,67,85,92,78]
Output:
Average: 81.71428571428571
Highest: 92
Lowest: 67
Students above average: 4
Grades: {'A': [90, 92], 'B': [85, 82], 'C': [78, 78], 'FAIL': [67]}
- Run:-
python Day2.py

## Day 3 - Dictionary - Based Phonebook
- Description:-
This Python program manages a phonebook using a dictionary. It allows users to store, search, update, and delete contact details efficiently.
- Features:-
Add new contact (name & phone number)
Search contact by name
Update existing contact
Delete contact
Display all contacts
- Example:-
  Input:
  Add → Name: Rahul, Number: 9876543210
  Add → Name: Aman, Number: 9123456780

  Output:
  Phonebook: {'Rahul': '9876543210', 'Aman': '9123456780'}

  Search: Rahul → 9876543210
  Update: Rahul → 9999999999
  Delete: Aman

  Final Output:
  {'Rahul': '9999999999'}

- Run:-
python Day3.py

## Day 4 - Simple Log Analyzer
- Description:-
This Python program analyzes log messages and counts how many times each log type appears.
It also finds the most frequent log type using a dictionary.

- Features
Count ERROR logs
Count INFO logs
Count WARNING logs
Ignore case sensitivity
Find most frequent log type

- Example:-
Input:
logs = [
    "ERROR DISK FULL",
    "INFO STARTED",
    "ERROR FILE MISSING",
    "WARNING MEMORY LOW"

]

Output:
Log Counts:
ERROR : 2
INFO : 1
WARNING : 1

Most Frequent Log Type: ERROR

- Run:-
python Day4.py
