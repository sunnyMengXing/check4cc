import urllib.request
from playsound import playsound
import os, re, argparse

ALERTAUDIOFILEPATH = "MengHuiTangKa.wav"
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
    count = 0
    while(True):
        print(ticketType + "\tsearch iterate " + str(count))
        count += 1
        isAlert = False

        remainTableList = getGlobalInfo(goodsCode)       
        assert(len(remainTableList) == TABLELENGTH)
        blockInfo = None

        ### gold
        if (gradeType == 1 or gradeType == 0) and int(remainTableList[0]) > ticketThreshold:
            print("!!!!!!gold checked \t" + remainTableList[0])
            blockInfo = getAllBlockInfo(goodsCode)
            for i in range(goldCount):
                if int(blockInfo[1][i]) > 0:
                    print("gold\t" + blockInfo[0][i] + '\t' + blockInfo[1][i])
                    isAlert = True

        ### silver
        if gradeType == 2 or gradeType == 0 and int(remainTableList[1]) > ticketThreshold:
            print("!!!!!!silver checked \t" + remainTableList[1])
            if blockInfo == None:
                blockInfo = getAllBlockInfo(goodsCode)
            
            for i in range(goldCount, silverCount):
                if int(blockInfo[1][i]) > 0:
                    print("silver\t" + blockInfo[0][i] + '\t' + blockInfo[1][i])
                    isAlert = True

        if isAlert:
            playsound(ALERTAUDIOFILEPATH, True)
            break


if __name__ == "__main__":
    # Main
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', required=True, type=str, help="0206|0207|0208|0209|gala|package")
    parser.add_argument('--audioPath', required=False, type=str, help="The absolute file path(optional)")
    parser.add_argument('--threshold', required=False, type=int, help="The minimun of ticket count, default is 5")   
    parser.add_argument('--gradeType', required=False, type=int, help="The ticket type, 1-gold, 2-silver, 0-all") 
    args = parser.parse_args()

    if args.audioPath != None and os.path.exists(args.audioPath):
        ALERTAUDIOFILEPATH = args.audioPath
    else:
        if not os.path.exists(ALERTAUDIOFILEPATH):
            print('Audio path not exist!')
            exit()
    
    if args.gradeType != None:
        gradeType = args.gradeType

    if args.threshold != None:
        ticketThreshold = args.threshold

    if args.type == "0206":
        main(args.type, goodsCode0206)
    elif args.type == "0207":
        main(args.type, goodsCode0207)
    elif args.type == "0208":
        main(args.type, goodsCode0208)
    elif args.type == "0209":
        main(args.type, goodsCode0209)
    elif args.type.lower() == "gala":
        main(args.type, goodsCodeGALA)
    elif args.type.lower() == "package":
        main(args.type, goodsCodePACK)
    else:
        print('Input type error')
        exit()