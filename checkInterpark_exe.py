import urllib.request
from playsound import playsound
import os, re, argparse

ALERTAUDIOFILEPATH = 'MengHuiTangKa.wav'
GLOBALURL = "https://gpoticket.globalinterpark.com/Global/Play/Book/Lib/BookInfoXml.asp?Flag=SeatGrade&PlaceCode=19001504&LanguageType=G2001&MemBizCode=10965&BizCode=10965&PlaySeq=001"
ALLBLOCKURL = "https://gpoticket.globalinterpark.com/Global/Play/Book/Lib/BookInfoXml.asp?Flag=AllBlock&PlaceCode=19001504&LanguageType=G2001&MemBizCode=10965&PlaySeq=001&Tiki=N&TmgsOrNot=D2003"
TABLELENGTH = 2

### User defined
ticketThreshold = 5
### 0-all 1-gold 2-silver
gradeType = 0

### Count of each table
goldCount = 18
silverCount = 24

### Goods code on interpark
goodsCode0206 = "19016425"
goodsCode0207 = "19016426"
goodsCode0208 = "19016427"
goodsCode0209 = "19016428"
goodsCodeGALA = "19016424"
goodsCodePACK = "19016423"

def urlRequest(url):
    tmp = urllib.request.urlopen(url).read()
    return tmp.decode('utf-8')

def getGlobalInfo(goodsCode):
    url = GLOBALURL + "&GoodsCode=" + goodsCode
    info = str(urlRequest(url))

    return re.findall(r"<RemainCnt>(.+?)</RemainCnt>", info)

def getAllBlockInfo(goodsCode):
    url = ALLBLOCKURL + "&GoodsCode=" + goodsCode
    info = str(urlRequest(url))

    blockNameList = re.findall(r"<SelfDefineBlock>(.+?)</SelfDefineBlock>", info)
    blockRemainCntList = re.findall(r"<RemainCnt>(.+?)</RemainCnt>", info)
    assert(len(blockNameList) == len(blockRemainCntList))

    return blockNameList, blockRemainCntList

def main(ticketType, goodsCode):
    isPlayed = False
    count = 0
    while(not isPlayed):
        print(ticketType + "\tsearch iterate " + str(count))
        count += 1

        remainTableList = getGlobalInfo(goodsCode)
        assert(len(remainTableList) == TABLELENGTH)
        blockInfo = None

        ### gold
        if (gradeType == 1 or gradeType == 0) and int(remainTableList[0]) > ticketThreshold:
            blockInfo = getAllBlockInfo(goodsCode)
            for i in range(goldCount):
                if int(blockInfo[1][i]) > 0:
                    if not isPlayed:
                        playsound(ALERTAUDIOFILEPATH, False)
                        isPlayed = True
                    print("gold\t" + blockInfo[0][i] + '\t' + blockInfo[1][i])

        ### silver
        if gradeType == 2 or gradeType == 0 and int(remainTableList[1]) > ticketThreshold:
            if blockInfo == None:
                blockInfo = getAllBlockInfo(goodsCode)
            
            for i in range(goldCount, silverCount):
                if int(blockInfo[1][i]) > 0:
                    if not isPlayed:
                        playsound(ALERTAUDIOFILEPATH, False)
                        isPlayed = True
                    print("silver\t" + blockInfo[0][i] + '\t' + blockInfo[1][i])

if __name__ == "__main__":
    # Main
    while True:
        ticketType = input("Enter ticket type(0206|0207|0208|0209|gala|package):")
        audioPath = input("Enter alert audio file path:")
        gradeTypeTmp = input("Enter the grade type(0-all, 1-gold, 2-silver):")
        ticketThresholdTmp = input("Enter the minimun of ticket count(such as 10):")
    
        if os.path.exists(audioPath):
            ALERTAUDIOFILEPATH = audioPath
            if ticketType == "0206":
                main(ticketType, goodsCode0206)
            elif ticketType == "0207":
                main(ticketType, goodsCode0207)
            elif ticketType == "0208":
                main(ticketType, goodsCode0208)
            elif ticketType == "0209":
                main(ticketType, goodsCode0209)
            elif ticketType.lower() == "gala":
                main(ticketType, goodsCodeGALA)
            elif ticketType.lower() == "package":
                main(ticketType, goodsCodePACK)
            else:
                print('Input type error！')

            if len(gradeTypeTmp) > 0:
                gradeType = int(gradeTypeTmp)
            if len(ticketThresholdTmp) > 0:
                ticketThreshold = int(ticketThresholdTmp)

        else:
            print('Audio path not exist!')

        