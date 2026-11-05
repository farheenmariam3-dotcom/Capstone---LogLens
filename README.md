# CP-093 LogLens: Server Log Analytics and Anomaly Detection Tool

LogLens is a menu-driven console tool that reads a web server log file and finds problems in it: error spikes, slow pages and possible brute-force login attacks.

## Team
Mariam Farheen Saif (1AT24IS115) and Monali Sethi (1AT24IS127), Python track

## How to run
```
python main.py
```
`server.log` must be in the same folder as `main.py`.

## Log format
Each line in `server.log` is one request, separated by spaces:

```
date        time      IP            endpoint  status  response_time_ms
2026-10-14  09:15:32  192.168.1.10  /login    401     120
```

Lines that do not have exactly 6 fields, or whose status or response time is not a number, are skipped and counted.

## Features that work

### Core features
1. **Load and parse the log file**: reads every line, skips broken lines and reports how many were loaded and skipped
2. **Requests by status code**: counts how many requests got each status (200, 401, 404, 500, ...)
3. **Top 5 IPs and endpoints**: the IP addresses and pages with the most requests
4. **Errors per hour and slowest endpoints**: number of errors (status 400 and above) in each hour, and endpoints ranked by average response time
5. **Suspicious IPs**: flags any IP with 5 or more failed logins (status 401) as a possible brute-force attack

### Stretch features
- **Time window filter** (option 7): analyse only the log lines between a start hour and an end hour
- **Save report** (option 8): writes a summary report to `report.txt`

### Wrong input handled
- Invalid menu choices (letters, empty input, numbers outside 1-9)
- Missing log file
- Using options 2-6 or 8 before loading the file
- Invalid hours in the time window (not a number, above 23, or start after end)
- Loading the file twice does not double the counts

## Design decisions
- **Error** = any status code 400 or above (client errors like 401/404 and server errors like 500)
- **Suspicious** = 5 or more 401s from the same IP, because one or two wrong passwords are normal but many in a row look like an automated password-guessing attack
- Data is stored in six parallel lists (dates, times, IPs, endpoints, statuses, response times), and dictionaries are used for counting

## Sample run
```
====LogLens====
1. Load log file
2. Requests by status code
3. Top 5 IPs and endpoints
4. Errors per hour
5. Slowest endpoints
6. Suspicious IPs
7. Set time window
8. Save report
9. Exit
Pick a number from 1-9: 1
Loaded:  18 lines, skipped 2

Pick a number from 1-9: 2
401 : 6
200 : 7
500 : 4
404 : 1

Pick a number from 1-9: 3
Top IPs
192.168.1.10 : 6
10.0.0.5 : 5
10.0.0.8 : 4
10.0.0.12 : 3
Top Endpoints
/login : 7
/products : 5
/checkout : 4
/about : 2

Pick a number from 1-9: 4
Errors per hour
9 :00 - 6 errors
10 :00 - 1 errors
14 :00 - 4 errors

Pick a number from 1-9: 5
Slowest endpoints (average response time)
/checkout : 2825 ms
/products : 434 ms
/login : 113 ms
/about : 55 ms

Pick a number from 1-9: 6
Suspicious IPs (5 or more failed logins)
WARNING: 192.168.1.10 has 6 failed logins - possible brute force attack

Pick a number from 1-9: 7
Start hour (0-23): 9
End hour (0-23): 10
Time window set. Now load the file again (option 1)

Pick a number from 1-9: 1
Loaded:  11 lines, skipped 2

Pick a number from 1-9: 8
Report saved to report.txt

Pick a number from 1-9: 9
Goodbye
```
(The menu is shown before every choice; it is printed only once above to keep this short.)

## What we would add next
- Detect a sudden spike in errors automatically instead of reading the hourly table
- Support log files in other formats