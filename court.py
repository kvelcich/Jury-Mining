import requests
import datetime
import BeautifulSoup

date = '-1/-1/-1'
GROUP_RANGE = 10000
url = 'http://sanmateocourt.org/court_divisions/juror_services/jurorstatus.php'

file_data = open('data.csv', 'a+')
file_log = open('info.log', 'a+')
file_error = open('error.log', 'a+')

group_count = 0
excused = 0
callback = 0
summoned = 0

for group_number in range(GROUP_RANGE):
    r = requests.post(url, data={'groupNumber': group_number})
    content = BeautifulSoup.BeautifulSoup(r.content)

    date = str(content.find('div', {'id': 'dateStamp'}).text.replace('Last updated: ','')) 
    msg = str(content.find('div', {'id': 'msg'}))

    if 'Invalid group number' in msg:
        continue
    elif 'No Reporting Instructions available' in msg:
        group_count += 1
        continue    
    if 'you are now excused' in msg:
        group_count += 1
        excused += 1
        status = 0
    elif 'call back status' in str(msg):
        group_count += 1
        callback += 1
        status = 2
    #elif 'summoned':
    #    group_count += 1
    #    summoned += 1
    #    status = 1
    else:
        file_error.write('\nUNKNOWN MESSAGE: ' + "'" + date + "'" + ', ' + str(group_number) + ', ' + msg + '\n\n')
        continue

    file_data.write("'" + date + "'" + ', ' + str(group_number) + ', ' + str(status) + '\n')

log = date + '\n'
log += 'Checked ' + str(GROUP_RANGE) + ' total groups.\n'
log += 'Identified ' + str(group_count) + ' valid groups.\n'
log += str(summoned) + ' groups summoned.\n'
log += str(callback) + ' groups have a callback.\n'
log += str(excused) + ' groups have been excused.\n'
log += str(group_count - summoned - callback - excused) + ' groups have no reporting instructions.\n\n'
file_log.write(log)

file_data.close()
file_log.close()
file_error.close()
