# check4cc

## Package:
### Make package
```
PyInstaller -F c:\Personal\Git\check4cc\checkInterpark_exe.py
```
### Usage:
+ 点击绿色写着“clone or download”按钮，download zip，下载到本地
+ 解压缩
+ 双击checkInterpark_exe.exe
+ Input:
  + ticketType -- 必须输入，类型0206|0207|0208|0209|gala|package
  + audioPath -- 必须输入，提示音频的路径，可以直接把音频拖到窗口里，建议全英文，不要使用中文
  + threshold -- 可选，默认5，因为只有两三张的时候可能是幽灵票，和一个刷到票的妹纸聊了一下，当突然出现一个比较大的数值的时候，才应该是放票了，并且才有可能抢到，所以这里可以设置一个最小提示的阈值，也可以设置为0
  + gradeType -- 可选，默认0,0代表所有票都刷，1代表只刷金票，2代表只刷银票
+ 主函数和python中是一致的，这个版本为了打包方便
+ TODO: merge two version

## Python

### Base environment: python3

### Dependency:
+ pip install beautifulsoup4
+ pip install playsound

### Usage:
```
python checkInterpark.py --type ticket_type [--audioPath audio_file_path]
```
+ type
  + 0206
  + 0207
  + 0208
  + 0209
  + gala
  + package(套票)
  
+ audioPath
    可选，默认的是“梦回唐卡”，可以设定自己的提示音频，应该是wav和mp3都可以
  
+ threshold
    可选，默认5，因为只有两三张的时候可能是幽灵票，和一个刷到票的妹纸聊了一下，当突然出现一个比较大的数值的时候，才应该是放票了，并且才有可能抢到，所以这里可以设置一个最小提示的阈值，也可以设置为0，注意gold和silver都是使用这个阈值，每个单独的票数大于这个阈值的时候进行提示
    
+ gradeType
    可选，默认0,0代表所有票都刷，1代表只刷金票，2代表只刷银票

### Test:
```
python checkInterpark.py --type 0206
```
+ 因为目前只有6号的票还有，可以用来做测试
+ 如果要刷多个，相当于开多个命令行窗口一起刷，输入不同的type即可

### Update log:
+ 20200107

  + 修改算法

    由于之前的判断条件比较严格，需要出现绿色可以点的票才认为有票，但经测试发现，放票的时候，绿色可点击的框出现的并不稳定，时有时没有，并且由于需要多次http请求，延迟比较大，很可能get不到。
  + 增加threshold

    和一个抢到票的妹纸聊了一下，决定用总票数来作为是否放票的依据，因为长期滞留在那的两三张票可以认为是幽灵票，当出现比较大的余票数值的时候可能是真正的放票，所以可以设定一个threshold，这个是gold和silver共同使用，但任何一个的余票数大于这个阈值的时候会进行提示。
  + 增加gradeType

    可以只刷银票或者只刷金票

  + 速度
    
    测了一下速度，基本每个http请求耗时0.5秒，数据处理的时间0.02秒,由于播放时间和检查每个block的情况中间还有个http请求，所以播放提示音乐的时间还会晚个0.5秒
