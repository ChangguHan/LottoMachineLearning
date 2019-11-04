from items import GlobalMethod, Lotto
import datetime, json, threading
from scripts import helpers


numsList = [5,10,30,50,100,300,500,1000]

def predictCheckThread() :
    print(datetime.datetime.now(), ": Check Predicted Numbers")

    thisTime = GlobalMethod.getthisTime()
    # 이번 예상 번호가 없으면,없을경우 false
    if not (helpers.check_predictedData(thisTime)) :
    #     로또 origin 데이터 먼저 받았는지 확인
        GlobalMethod.db_checkOriginData(thisTime-1)

        # 예상번호 생성
        result = {}
        for i in numsList :
            result[i] = Lotto.getPredict(i)
        result = json.dumps(result)

        helpers.add_predictedData(thisTime, datetime.datetime.now(), Lotto.learning_rate, Lotto.steps, result)

    # 한번 더 검사
    if not (helpers.check_predictedData(thisTime)):
        print("scripts-init Error")
        quit()

    #     1시간마다 가동
    threading.Timer(3600, predictCheckThread).start()

predictCheckThread()