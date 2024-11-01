import re
from collections import namedtuple, defaultdict
import datetime

Log = namedtuple('Log', ['remote_addr', 'remote_user', 'time_local',
                         'request', 'status', 'body_bytes_sent', 'referal',
                         'user_agent'])
error_codes = list(range(400, 600))
max_requests_per_second = 10
suspicious_paths = ["/login", "/admin", "/api"]

def analize_logs(filename):
    requests_per_second = defaultdict(lambda: {"count": 0, "last_time": None})
    error_counts = defaultdict(int)
    hack = []
    try:
        with open(filename, 'r') as infile:
            for line in infile:
                match = re.match(
                    '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (.*?) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"', line)
                if match:
                    remote_addr, remote_user, time_local, request, status, body_bytes_sent, referal, user_agent = match.groups()

                    time = datetime.datetime.strptime(time_local, "%d/%b/%Y:%H:%M:%S %z")
                    http_method = request.split()[0] if len(request.split()) > 0 else "-"
                    try:
                        path = request.split()[1] if len(request.split()) > 0 else "-"
                    except:
                        hack.append(line)
                    ip = remote_addr
                    http_code = status

                    if http_code in error_codes:
                        error_counts[ip] += 1

                    if http_method == '-': hack.append(line) #Отсутствует http метод(get, post...)
                    if path == '-': hack.append(line) #Отсутствует параметры http методов
                    if (path in suspicious_paths) and (http_code in error_codes): #Попытка доступа в запрещенный каталог
                        hack.append(line)

                    if error_counts[ip] > 5: hack.append(line) #Лимит количества ошибок 4хх или 5хх

                    #Вычисление частоты запросов в секунду
                    if (requests_per_second[ip]["last_time"] is not None) and ((time.second - requests_per_second[ip]["last_time"]) <= 1) and (len(requests_per_second[ip]) >= 4):
                        requests_per_second[ip]["count"] += 1
                        requests_per_second[ip]["last_time"] = time.second
                    else:
                        requests_per_second[ip]["count"] = 1
                        requests_per_second[ip]["last_time"] = time.second

                    if requests_per_second[ip]["count"] > max_requests_per_second:
                        hack.append(line)

        print("IP адреса атакующих!")
        for line in sorted(hack):
            print("".join(line))

    except Exception as e:
        print(f"Ошибка при обработке строки лог файла!: {e}")



log_file = "log.txt"
log_list = analize_logs(log_file)