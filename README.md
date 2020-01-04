# check4cc

## Package:
### Make package
```
PyInstaller -F c:\Personal\Git\check4cc\checkInterpark_exe.py
```
### Usage:
+ 双击checkInterpark_exe即可
+ Inout:
  + ticketType -- 必须输入，类型同上
  + audioPath -- 必须输入，提示音频的路径，可以直接把音频拖到窗口里，建议全英文，不要使用中文
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

### Test:
```
python checkInterpark.py --type 0206
```
+ 因为目前只有6号的票还有，可以用来做测试
+ 如果要刷多个，相当于开多个命令行窗口一起刷，输入不同的type即可
