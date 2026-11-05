start_hour = 0
end_hour = 23

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
    print("7. Set time window")
    print("8. Save report")
    print("9. Exit")
    choice = input("Pick a number from 1-9: ")
    

    if choice == "1":
        skipped = 0
        dates.clear()
        times.clear()
        ips.clear()
        endpoints.clear()
        statuses.clear()
        response_times.clear()  

        try:
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

                hour = int(parts[1][0:2])          
                if hour < start_hour or hour > end_hour: 
                    continue 

                dates.append(parts[0])
                times.append(parts[1])
                ips.append(parts[2])
                endpoints.append(parts[3])
                statuses.append(int(parts[4]))
                response_times.append(int(parts[5]))
            
            file.close()
            print("Loaded: ", len(ips), "lines, skipped", skipped)
        except FileNotFoundError:
            print("File not found: server.log")

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
        if len(ips) == 0:
            print("Please load the file first (option 1)")
        else:
            fails = {}
            for i in range(len(ips)):
                if statuses[i] == 401:
                    ip = ips[i]
                    if ip in fails:
                        fails[ip] = fails[ip] + 1
                    else:
                        fails[ip] = 1
            
            found = False
            print("Suspicious IPs (5 or more failed logins)")
            for ip in fails:
                if fails[ip] >= 5:
                    print("WARNING:", ip, "has", fails[ip], "failed logins - possible brute force attack")
                    found = True

            if found == False:
                print("No suspicious IPs found")
        
    elif choice == "7":
        s = input("Start hour (0-23)")
        e = input("End hour (0-23)")
        if not s.isdigit() or not e.isdigit():
            print("Please enter numbers only")
        elif int(s) > 23 or int(e) > 23:
            print("Hours must be between 0 - 23 only")
        elif int(s) > int(e):
            print("Start hour must be before an hour")
        else:
            start_hour = int(s)
            end_hour = int(e)
            print("Time window set. Now load the file again (option 1)")

    elif choice == "8":
        if len(ips) == 0:
            print("Please load the file first (option 1)")
        else:
            report = open("report.txt", "w")
            report.write("LogLens Report\n")
            report.write("Lines loaded: " + str(len(ips)) + "\n\n")

            report.write("Requests by status code\n")
            count = {}
            for key in statuses:
                if key in count:
                    count[key] = count[key] + 1
                else:
                    count[key] = 1
            for key in count:
                report.write(str(key) + " : " + str(count[key]) + "\n")

            report.write("\nSuspicious IPs\n")
            fails = {}
            for i in range(len(ips)):
                if statuses[i] == 401:
                    ip = ips[i]
                    if ip in fails:
                        fails[ip] = fails[ip] + 1
                    else:
                        fails[ip] = 1
            for ip in fails:
                if fails[ip] >= 5:
                    report.write(ip + " : " + str(fails[ip]) + " failed logins\n")

            report.close()
            print("Report saved to report.txt")

    elif choice == "9":
        print("Goodbye")
        break
    else:
        print("Invalid, select from between 1-7")