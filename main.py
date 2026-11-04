dates = []
times = []
ips = []
endpoints = []
statuses = []
response_times = []

while True:
    print("====LogLens====")
    print("1. Load log file")
    print("2. Requests by status code")
    print("3. Top 5 IPs and endpoints")
    print("4. Errors per hour")
    print("5. Slowest endpoints")
    print("6. Suspicious IPs")
    print("7. Exit")
    choice = input("Pick a number from 1-7: ")

    if choice == "1":
        skipped = 0
        file = open("server.log", "r")
        for line in file:
            line = line.strip()
            parts = line.split()

            if len(parts) != 6:
                skipped = skipped + 1
                continue

            if not parts[4].isdigit() or not parts[5].isdigit():
                skipped = skipped + 1
                continue

            dates.append(parts[0])
            times.append(parts[1])
            ips.append(parts[2])
            endpoints.append(parts[3])
            statuses.append(int(parts[4]))
            response_times.append(int(parts[5]))
        
        file.close()
        print("Loaded: ", len(ips), "lines, skipped", skipped)

    elif choice == "2":
        print("Coming soon")
    elif choice == "3":
        print("Coming soon")
    elif choice == "4":
        print("Coming soon")
    elif choice == "5":
        print("Coming soon")
    elif choice == "6":
        print("Coming soon")
    elif choice == "7":
        print("Goodbye")
        break
    else:
        print("Invalid, select from between 1-7")