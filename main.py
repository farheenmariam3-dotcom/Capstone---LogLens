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
        dates.clear()
        times.clear()
        ips.clear()
        endpoints.clear()
        statuses.clear()
        response_times.clear()  

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
        if len(statuses) == 0:
            print("please load the file first(option 1)")
        else: 
            count = {} 
            for key in statuses:
                if key in count:
                    count[key] = count[key] + 1
                else:
                    count[key] = 1

            for key in count:
                print(key, ":", count[key])

    elif choice == "3":
        if len(ips) == 0:
            print("Please load the file first(option 1)")
        else:
            print("Top IPs")
            ips_counts = {}
            for key in ips:
                if key in ips_counts:
                    ips_counts[key] = ips_counts[key] + 1
                else:
                    ips_counts[key] = 1

            order = sorted(ips_counts, key=ips_counts.get, reverse=True)
            top = order[:5]
            for key in top:
                print(key, ":", ips_counts[key])

            print("Top Endpoints")
            ep_counts = {}
            for key in endpoints:
                if key in ep_counts:
                    ep_counts[key] = ep_counts[key] + 1
                else:
                    ep_counts[key] = 1
            
            order = sorted(ep_counts, key=ep_counts.get, reverse=True)
            top = order[:5]
            for key in top:
                print(key, ":", ep_counts[key])

    elif choice == "4":
        if len(statuses) == 0:
            print("Please load the file first(option 1)")
        else:
            errors = [0] * 24
            for i in range(len(statuses)):
                if statuses[i] >= 400:
                    hour = int(times[i][0:2])
                    errors[hour] = errors[hour] + 1

            print("Errors per hour")
            for h in range(24):
                if errors[h] > 0:
                    print(h, ":00 -", errors[h], "errors")        

    elif choice == "5":
        if len(endpoints) == 0:
            print("Please load the file first (option 1)")
        else:
            total = {}
            num = {}
            for i in range(len(endpoints)):
                ep = endpoints[i]
                rt = response_times[i]
                if ep in total:
                    total[ep] = total[ep] + rt
                    num[ep] = num[ep] + 1
                else:
                    total[ep] = rt
                    num[ep] = 1

            avg = {}
            for ep in total:
                avg[ep] = total[ep] / num[ep]

            order = sorted(avg, key=avg.get, reverse = True)
            print("Slowest endpoints (average response time)")
            for ep in order:
                print(ep, ":", round(avg[ep]), "ms")

    elif choice == "6":
        print("Coming soon")
    elif choice == "7":
        print("Goodbye")
        break
    else:
        print("Invalid, select from between 1-7")