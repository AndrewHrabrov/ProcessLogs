from collections import namedtuple
import re

Log = namedtuple('Log', ['remote_addr', 'remote_user', 'time_local',
                         'request', 'status', 'body_bytes_sent', 'referal',
                         'user_agent'])

def logs(filename):
    log_list = []
    with open(filename, 'r') as infile:
        for line in infile:
                match = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (.*?) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"', line)
                if match:
                    remote_addr, remote_user, time_local, request, status, body_bytes_sent, referal, user_agent = match.groups()
                    log_list.append(Log(remote_addr, remote_user, time_local,
                                           request, int(status), int(body_bytes_sent), referal, user_agent))

    return log_list

def unique_ip(log_list):
    list_ip = set()
    for log in log_list:
        list_ip.add(log.remote_addr)
    return sorted(list(list_ip))

log_file = "log.txt"
log_list = logs(log_file)
for ip in unique_ip(log_list):
    print(ip)