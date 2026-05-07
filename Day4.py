logs = [
    "ERROR DISK FULL",
    "INFO STARTED",
    "ERROR FILE MISSING",
    "WARNING MEMORY LOW"
]


count_logs = {
    "ERROR": 0,
    "INFO": 0,
    "WARNING": 0
}


for log in logs:
    log = log.upper()   

    if "ERROR" in log:
        count_logs["ERROR"] += 1

    elif "INFO" in log:
        count_logs["INFO"] += 1

    elif "WARNING" in log:
        count_logs["WARNING"] += 1

print("Log Counts:")
for key, value in count_logs.items():
    print(key, ":", value)

most_frequent = max(count_logs, key=count_logs.get)

print("\nMost Frequent Log Type:", most_frequent)