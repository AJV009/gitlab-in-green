import requests
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

def main():
    page = 1
    url = urlGen(page)
    response = requests.get(url)
    data = response.json()
    # check if data has message key
    if 'message' in data and data['message'] == '401 Unauthorized':
        # throw error
        raise Exception('401 Unauthorized')
    created_time = []
    validUrl = True
    while validUrl:
        url = urlGen(page)
        tempDt = fetch(url)
        if tempDt == []:
            validUrl = False
        else:
            created_time = created_time + tempDt
            page += 1
    if created_time != []:
        print("NOTICE: Fetched all data.")
        if os.path.exists('data.txt'):
            os.remove('data.txt')
        os.system('git checkout --orphan latest_branch')
        os.system('git add .')
        os.system('git commit -am "Reset all commits"')
        os.system('git branch -D main')
        os.system('git branch -m main')
        os.system('git push origin main -f')
        created_time = [x for x in created_time if x != []]
        created_time = [dateToTs(x) for x in created_time]
        created_time.sort()
        for dt in created_time:
            print(dt)
            sdt = "\n" + str(dt)
            if fileChange(sdt):
                os.system('git add .')
                command = 'git commit --date "' + str(dt) + '" -am "Add an activity commit"'
                os.system(command)
        os.system('git push origin main -f')
    else:
        return 'No Data'

def urlGen(page):
    return "http://" + os.getenv('GITLAB_BASE_URL') + "/api/v4/events?private_token=" + os.getenv('GITLAB_PRIVATE_TOKEN') + "&page=" + str(page)

def fetch(url):
    created_time = []
    try:
        response = requests.get(url)
        data = response.json()
        if data == []:
            return created_time
        for i in data:
            created_time.append(i['created_at'])
        return created_time
    except:
        return created_time

def fileChange(data):
    try:
        if not os.path.exists('data.txt'):
            with open('data.txt', 'w') as f:
                f.write('')
        with open('data.txt', 'a') as f:
            f.write(data)
            return True
    except:
        return False

def dateToTs(data):
    dateTime = data.split('T')
    date = dateTime[0].split('-')
    time = dateTime[1].split(':')
    time[2] = time[2].split('.')[0]
    ts = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])).timestamp()
    return int(ts)

if __name__ == '__main__':
    main()