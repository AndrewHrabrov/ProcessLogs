from collections import namedtuple


def logs(record_string):
    log =  namedtuple('log', ['remote_addr', 'remote_user', 'time_local',
                              'request', 'status', 'body_bytes_sent', 'referal',
                              'user_agent'])

    remote_addr = record_string.split('-')[0]
    remote_user = record_string.split()[1]
    time_local = (record_string.split('-')[2].split()[0] + ' ' + record_string.split('-')[2].split()[1]).replace('[', '').replace(']', '')
    request = ((record_string.split('-')[2].split()[2] + ' ' +
               record_string.split('-')[2].split()[3]) + ' ' +
               record_string.split('-')[2].split()[4]).replace('"', '')
    status = int(record_string.split('-')[2].split()[5])
    body_bytes_sent = int(record_string.split('-')[2].split()[6])
    referal = record_string.split('-')[2].split()[7].replace('"', '')
    user_agent = ((record_string.split('-')[2].split()[8] + ' ' +
                  record_string.split('-')[2].split()[9]) + ' ' +
                  record_string.split('-')[2].split()[10] + ' ' +
                  record_string.split('-')[2].split()[11] + ' ' +
                  record_string.split('-')[2].split()[12] + ' ' +
                  record_string.split('-')[2].split()[13] + ' ' +
                  record_string.split('-')[2].split()[14]).replace('"', '')

    ans = log(remote_addr, remote_user, time_local, request,
              status, body_bytes_sent, referal, user_agent)

    print(ans)

record_string = '85.237.48.26 - - [02/Oct/2022:22:14:50 +0300] "GET /masterclass/ HTTP/1.1" 200 527 "http://82.179.90.12/" "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"'
logs(record_string)