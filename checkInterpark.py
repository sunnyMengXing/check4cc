import urllib.request
from bs4 import BeautifulSoup
from playsound import playsound
import os, re, argparse

ALERTAUDIOFILEPATH = 'MengHuiTangKa.wav'
TABLEURL = "https://gpoticket.globalinterpark.com/Global/Play/Book/Lib/BookInfoXml.asp?Flag=SeatGradeBlock&PlaceCode=19001504&LanguageType=G2001&MemBizCode=10965&Tiki=N&BizCode=10965&PlaySeq=001&TmgsOrNot=D2003"
BLOCKURL = "https://gpoticket.globalinterpark.com/Global/Play/Book/BookSeatDetail.asp?PlaceCode=19001504&LanguageType=G2001&MemBizCode=10965&PlaySeq=001&SeatGrade=&TmgsOrNot=D2003&LocOfImage=&Tiki=N&UILock=Y&SessionId=8647CB8EEFF042B2ACF86C8B1586FBC0&BizCode=10965&GoodsBizCode=12930"

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

def getTabelPathInfo(goodsCode, ticketType):   
    url = TABLEURL + "&GoodsCode=" + goodsCode + "&SeatGrade=" + str(ticketType) + "&SeatGradeIdx=" + str(ticketType)
    pageInfo = urlRequest(url)
    soup = BeautifulSoup(pageInfo, "html.parser")

    blockNameList = soup.find_all('selfdefineblock')
    blockRemainCntList = soup.find_all('totalremaincnt')

    assert(len(blockNameList) == len(blockRemainCntList))
    
    return  blockNameList, blockRemainCntList
        
def getRemainTabelList(blockNameList, remainCntList):
    res = []
    for i in range(len(blockNameList)):
        if str(remainCntList[i]) != "<totalremaincnt>0</totalremaincnt>":
            res.append(str(re.findall(r"<selfdefineblock>(.+?)</selfdefineblock>",str(blockNameList[i]))[0]))
    return res

def getRemainBlockList(remainList, isPlayed, ticketType, goodsCode):
    url = BLOCKURL + "&GoodsCode=" + goodsCode + "&Block="
    for block in remainList:
        detailInfo = urllib.request.urlopen(url + block).read()
        detailInfo = str(detailInfo.decode('utf-8'))
        if detailInfo.find("<span class='SeatN' id=\"Seats\"") > 0:
            if not isPlayed:
                playsound(ALERTAUDIOFILEPATH, False)
                isPlayed = True
            print(ticketType + "\t" + block)
    
    return isPlayed

def main(ticketType, goodsCode):
    isPlayed = False
    count = 0
    while(not isPlayed):
        print(ticketType + "\tsearch iterate " + str(count))
        count += 1

        ### ticketType: 1-gold, 2-silver
        goldBlockNameList, goldRemainCntList = getTabelPathInfo(goodsCode, 1)
        silverBlockNameList, silverRemainCntList = getTabelPathInfo(goodsCode, 2)

        goldRemainList = getRemainTabelList(goldBlockNameList, goldRemainCntList)
        silverRemainList = getRemainTabelList(silverBlockNameList, silverRemainCntList)
        
        isPlayed = getRemainBlockList(goldRemainList, isPlayed, ticketType, goodsCode)
        isPlayed = getRemainBlockList(silverRemainList, isPlayed, ticketType, goodsCode)

if __name__ == "__main__":
    # Main
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', required=True, type=str, help="0206|0207|0208|0209|gala|package")
    parser.add_argument('--audioPath', required=False, type=str, help="")
    args = parser.parse_args()

    if args.audioPath != None and os.path.exists(args.audioPath):
        ALERTAUDIOFILEPATH = args.audioPath
    else:
        if not os.path.exists(ALERTAUDIOFILEPATH):
            print('Audio path not exist!')
            exit()

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