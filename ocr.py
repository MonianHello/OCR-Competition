# coding=utf-8

import hashlib
import ssl
import sys
import json
import base64
import os
import time
import getpass
import requests
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus


print(time.strftime("%m-%d %H:%M", time.localtime(time.time())).rjust(30))

#一言函数
hitokotourl = 'https://v1.hitokoto.cn/?c=i&encode=text'
def hitokoto(num):
    try:
        for i in range(num):
            hitokoto = requests.get(hitokotourl)
            hitokoto = hitokoto.text
            print(hitokoto)

    except:
        print('无法与 '+hitokotourl+' 服务器通讯')
        print('请检查您的网络连接')
        hitokoto = 'Hello,World!'


#认证系统
os.system('cls')
os.system('color 3f')
print('''==============================

    永吉实验高中 参赛作品
     2019级 10班 赵春旭
        
         光学字符识别    
Optical Character Recognition
       
==============================
''')
hitokoto(1)

#管理员认证
times = 0
while True:
    password = getpass.getpass('''
    现在开始进行管理员认证
    请键入管理员密码：''')
    #md5散列
    #此处通过添加salt防止使用彩虹表破解
    #本程序
    #       salt为 'abcdefg1234567'
    #       密码为 'OCRpassword'
    #实际程序中的salt应使用random并存储在数据库中，本程序尚未完成对多用户账户管理，故salt为固定值
    salt = 'abcdefg1234567'
    passwordmd5 = hashlib.md5(password.encode(encoding='UTF-8')+salt.encode(encoding='UTF-8')).hexdigest()
    #失败次数
    times += 1
    #if passwordmd5 == "5f4dcc3b5aa765d61d8327deb882cf99":
    #if passwordmd5 == "8223fe8dc0533c6ebbb717e7fda2833c":
    if passwordmd5 == 'd37446b56a526e8c43e2cf039af4ae0e':
        break
    #认证失败
    if times >= 3:
        os.system('color 0c')
        os.system('cls')
        print('''
        
    密码输入失败3次以上
    已拒绝管理员认证操作
    即将强制退出
    
        ''')
        time.sleep(2.5)
        quit()
    print(' ')
    print('密码错误，剩余尝试次数'+str((3 - int(times)))+'次')

#认证通过
os.system('color 0b')
os.system('mkdir C:\MonianHello\\')
os.system('cls')
print('''
已通过认证，欢迎您登入 光学字符识别 系统 
请将图片复制到C:\MonianHello文件夹内
进行OCR文字识别
''')
choice = input('是否打开图片文件夹(Y/N)')
if choice == 'Y':
    os.system('explorer C:\MonianHello')
else:
    pass
linemode = input('输出内容是否换行(Y/N):')
if linemode != 'Y':
    linemode = 'N'
os.system('pause')

textlist = []
IS_PY3 = sys.version_info.major == 3
# 防止https证书校验不正确
ssl._create_default_https_context = ssl._create_unverified_context
# 此处填写ak/sk
API_KEY = '[ak]'
SECRET_KEY = '[sk]'
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
outputtext = "C:\\MonianHello\\list.txt"

def fetch_token():
    #获取token
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('请确认ak/sk是否正确')
            exit()
        return result['access_token']
    else:
        print ('ak/sk失效或未连接到互联网')
        exit()

def read_file(image_path):
    #读取文件
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('读取图片失败，请确认文件是否被其他程序占用')
        return None
    finally:
        if f:
            f.close()

def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)
        

def get_file_path(root_path,file_list,dir_list):
    #获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            #递归获取所有文件和目录的路径
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)        

def ocr(path):

    # 获取access token
    token = fetch_token()
    # 拼接图像审核url
    image_url = OCR_URL + "?access_token=" + token
    text = ""
    file_content = read_file(path)
    result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))
    result_json = json.loads(result)
    textlist.append('文件目录:'+path)
    textlist.append('----------')
    print('文件目录:'+path)
    print('----------')
    for words_result in result_json["words_result"]:
        if linemode == 'Y':        
            text = text + words_result["words"] + '\n'
        else:
            text = text + words_result["words"]
    textlist.append(text)
    textlist.append('==========')
    print(text)
    print('----------')

os.system('color 3f')
os.system('cls')
textlist = []
root_path = r"C:\MonianHello"
#用来存放所有的文件路径
file_list = []
#用来存放所有的目录路径
dir_list = []
get_file_path(root_path,file_list,dir_list)
fl=open(outputtext,'w')
os.system('color 3f')
count = int(len(file_list) - 1)
allcount = count
print('==========')
print('启动时间:'+time.asctime( time.localtime(time.time()) ))
print('共找到文件数:'+str(count))
print('当前换行模式设置:'+str(linemode))
print('==========')
textlist.append('==========')
textlist.append('光学字符识别')
textlist.append('启动时间:'+time.asctime( time.localtime(time.time()) ))
textlist.append('共找到文件数:'+str(count))
textlist.append('当前换行模式设置:'+str(linemode))
textlist.append('==========')
#文字识别
for path in file_list:
    if path == "C:\\MonianHello\\list.txt":
        continue
    try:
        ocr(path)
        count -= 1
        if count == 0 :
            continue
        print('剩余项' + str(count) + ' / ' + str(allcount) )
        print('==========')
        time.sleep(1)
    except:
        print('出现内部错误')
#写入文件
print('识别完成，现在将结果写入文件...')
print('==========')
try:
    for i in textlist:
        fl.write(i)
        fl.write("\n")
    fl.write('结束时间:'+time.asctime( time.localtime(time.time()) ))
    fl.close()
    print('写入成功，已将文件写入'+str(outputtext))
    print('结束时间:'+time.asctime( time.localtime(time.time()) ))
    os.system('pause')
except:
    os.system('color cf')
    print('写入失败，请确认'+str(fl)+'目录以及文件存在')
    os.system('pause')

os.system('notepad C:\\MonianHello\\list.txt')
os.system('color')
quit()
