# check4cc

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
    可选，设定自己的提示音频，应该是wav和mp3都可以

### Test:
```
python checkInterpark.py --type 0206
```
因为目前只有6号的票还有，可以用来做测试