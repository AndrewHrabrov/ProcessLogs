from collections import namedtuple
import re
from itertools import count

Log = namedtuple('Log', ['remote_addr', 'remote_user', 'time_local',
                         'request', 'status', 'body_bytes_sent', 'referal',
                         'user_agent'])

def logs(filename):
    ip_count = {}
    max_count = 0
    max_ip = None
    with open(filename, 'r') as infile:
        for line in infile:
                match = re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (.*?) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"', line)
                if match:
                    ip = match.group(1)
                    if ip not in ip_count:
                        ip_count[ip] = 1
                    else: ip_count[ip] += 1

                    if ip_count[ip] > max_count:
                        max_count = ip_count[ip]
                        max_ip = ip


    return ip_count, max_ip, max_count

log_file = "log.txt"
log_list = logs(log_file)
for i in log_list:
    print(i)