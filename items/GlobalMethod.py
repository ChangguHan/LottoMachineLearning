import datetime
import ssl, json
from urllib.request import urlopen
from scripts import helpers

def getToday():
    today = datetime.date.today()
    return today

def getDDay():
    today = getToday();

    # 만약 일요일일경우
    if (today.weekday() == 6):
        dDay = today + datetime.timedelta(days=6)
    else:
        dDay = today + datetime.timedelta(days=5 - today.weekday())

    return dDay


def getthisTime():

    # 이번 회차 구하기
    lottoOriginDay = datetime.date(2002, 12, 7)
    dDay = getDDay()
    thisTime = int((dDay - lottoOriginDay).days / 7 + 1)

    return thisTime



def db_checkPredictedData(predictedNum) :

    if helpers.check_predictedData(predictedNum) : return True
    else : return False


def db_checkOriginData(predictedNum) :
    # 주어진 숫자만큼 전에 originData 있는지 확인
    # originData는 처음부터 끝까지 있어야 되니까 모두 확인해야함.


    for i in range(predictedNum) :
        i += 1
        if not helpers.check_originData(i) :
            helpers.add_originData(i,getOriginDataURL(i))

    for j in range(predictedNum):
        j += 1
        if not helpers.check_originData(j):
            print("Error in originDataCheck")
            quit()

    return True

def getOriginDataURL(num) :
    # url에서 데이터 array로 추출
    result = []

    context = ssl._create_unverified_context()
    url = "https://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo=" + str(num)
    url_data = urlopen(url, context=context)
    url_read = url_data.read()

    data = json.loads(url_read)

    for i in range(7):
        if i == 6:
            result.append(data["bnusNo"])
        else:
            result.append(data["drwtNo" + str(i + 1)])

    return json.dumps(result)

