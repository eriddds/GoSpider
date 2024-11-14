import requests
import os
import random
import time
import re
from bs4 import BeautifulSoup
from jsonpath import jsonpath
import PySimpleGUI as sg

class GoSpider(object):
    def __init__(self):
        self.get_data = {}
        self.USER_AGENT_LIST = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
                  'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
                  'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
                  'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
                  'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
                  'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
                  'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                  'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.7 Firefox/68.0 PaleMoon/28.16.0',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
                  'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
                  'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                  ]
        self.TimeSleepTime = 1 + random.random()
        self.layout = [
            [sg.T(text="Eriddds/ES原创                  ", font=("Arial",25),background_color='white', key='-title-',text_color='black')],
            [sg.T(text="爬虫请求方式，只能选一个", font=("黑体",15),background_color='white', key='-text1-',text_color='black')],
            [sg.Checkbox('Get请求', key='-Get-'),
             sg.Checkbox('Post请求', key='-Post-')],
            [sg.Combo(['二进制文件（媒体等等）','网页源码(前端)'], '请选择获取什么信息', key='-chose-', font=('黑体',15),background_color='white',
                      size=(45, 50),tooltip='请选择方式来爬虫',enable_events=True)],
            [sg.T(text='网址:',font=('黑体',15),background_color='white', key='-text2-',text_color='black'),
             sg.I(tooltip='输入要获取信息的网址',font=('黑体',15),background_color='white', key='-text3-',text_color='black')],
            [sg.T('',font=('黑体',20),background_color='white', key='-text4-',text_color='black')],
            # [sg.I('正则表达使用',key='-none-',background_color='white', text_color='black',disabled=True,font=('黑体'),size=(50,50))],
            [sg.B('确认'),sg.B('取消',key='Exit')]
        ]
        self.html_data = ''
    def init_window(self):
        sg.theme('GrayGrayGray')
        window = sg.Window('GoSpider', self.layout)
        while True:
            event, values = window.read()
            if event == None or event == 'Exit':
                window.close()
                quit(0)
            # match values['-chose-']:
            #     case '二进制文件（媒体等等）':
            #         window['-none-'].update('', disabled=True)
            #         window['-text4-'].update('')
            #     case '网页源码(前端)':
            #         window['-none-'].update('', disabled=True)
            #         window['-text4-'].update('')
            #     case 're正则表达找信息':
            #         window['-none-'].update('',disabled=False)
            #         window['-text4-'].update('请输入正则表达式的代码：')
            if event == '确认':
                return_data = 'next'
                self.data = values
                break
            # print(values,';',event)
        if return_data == 'next':
            window.close()
            self.start_spider()

    def start_spider(self):
        # print(self.data)
        if self.data['-Get-']  | self.data['-Post-'] == False or self.data['-chose-'] == '请选择获取什么信息':
                sg.popup_error('错误：请填写完整信息')
                quit(1)
        if self.data['-chose-'] == 're正则表达找信息' and self.data['-none-'] == '':
            sg.popup_error('请输入正确的正则表达代码')
            quit(1)
        else:
            self.get_data = {
                'Get':self.data['-Get-'],
                'Post':self.data['-Post-'],
                'chose':self.data['-chose-'],
                '网址':self.data['-text3-'],
                # '正则代码':self.data['-none-']
            }
            if self.get_data['Get'] == True:
                if self.get_data['Post'] == True:
                    sg.popup_error('错误，只能选一个Get，或者Post')
                else:
                    if self.get_data['chose'] == '二进制文件（媒体等等）':
                        sg.Popup('注意目前仅支持下载图片,不允许视频,敬请谅解')
                        self.get_c()
                    else:
                        self.get()
            elif self.get_data['Post'] == True:
                self.Post()
            else:
                sg.popup_error('错误，只能选一个Get，或者Post')

    def get(self):
        try:
            self.html_data = requests.get(self.get_data['网址'], headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
        except:
            sg.popup_error('未知/错误 网址')
            quit(1)
        layout = [
            [sg.T(text="Eriddds/ES原创         ", font=("Arial", 25), background_color='white', key='-title-',
                  text_color='black')],
            [sg.T(text=f'响应状态码:{self.html_data}')],
            [sg.T(text='源码：')],
            [sg.Multiline('如无法显示源码请刷新，谢谢',font=('黑体', 15), background_color='white', key='-data-', text_color='black',size=(80,20))],
            [sg.T(text='正则表达查找指令: 如：(.*?).*  等等',font=('黑体',15), background_color='white',text_color='red')],
            [sg.I(key='-cmd-',tooltip='输入python正则的代码',background_color='white',text_color='black',font=('黑体',18))],
            [sg.B('运行正则代码',font=('黑体',15)),sg.B('保存html源码',font=('黑体',15)),sg.B('获取爬虫代码和正则代码',font=('黑体',15))],
            [sg.B('退出',key='Exit',font=10),sg.B('刷新',font=10)]
        ]
        get_win = sg.Window('获取信息',layout)
        self.re_data = ''
        while True:
            event, values = get_win.read()
            get_win['-data-'].update(self.html_data.text)
            if event == None or event == 'Exit':
                quit(0)
            if event == '运行正则代码':
                z = values['-cmd-']
                try:
                    self.re_data = re.findall(z,self.html_data.text,re.S)
                except:
                    sg.popup_error(f'正则报错')
                else:
                    sg.Popup('re运行获得的信息为\n',self.re_data,font=('黑体',15))
            if event == '保存html源码':
                self.html_data = requests.get(self.get_data['网址'],headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
                with open('html_data.txt','w',encoding='utf-8') as f:
                    f.write(self.html_data.text)
                sg.Popup('已保存为‘html_data.txt’文件中')
            if event == '获取爬虫代码和正则代码':
                with open('source_code.py','w',encoding='utf-8') as f:
                    code_py = \
                    """
# 代码经过删减,作者:eriddds/ES
import requests
import re
import random

ua = %s
""" % self.USER_AGENT_LIST
                    code = """ \

r = requests.get('%s',headers={'User-Agent': random.choice(ua)})
print(r)
print('='*15)
print(r.text)
""" % self.get_data['网址']
                    f.write(code_py)
                    f.write(code)
                    if self.re_data == '':
                        pass
                    else:
                        code_py2 = \
                        """ 
z = %s
re_data = re.findall(z,r.text,re.S)
print(re_data)
""" % self.re_data
                        f.write(code_py2)
                sg.Popup('文件已保存至"source_code.py"')


    def Post(self):
        try:
            self.html_data = requests.post(self.get_data['网址'],headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
        except:
            sg.popup_error('未知/错误 网址')
            quit(1)
        layout = [
            [sg.T(text="Eriddds/ES原创   d      ", font=("Arial", 25), background_color='white', key='-title-',
                  text_color='black')],
            [sg.T(text=f'响应状态码:{self.html_data}')],
            [sg.T(text='源码：')],
            [sg.Multiline('如无法显示源码请刷新，谢谢', font=('黑体', 15), background_color='white', key='-data-',
                          text_color='black', size=(80, 20))],
            [sg.T(text='正则表达查找指令: 如：(.*?).*  等等', font=('黑体', 15), background_color='white',
                  text_color='red')],
            [sg.I(key='-cmd-', tooltip='输入python正则的代码', background_color='white', text_color='black',
                  font=('黑体', 18))],
            [sg.B('运行正则代码', font=('黑体', 15)), sg.B('保存html源码', font=('黑体', 15)),
             sg.B('获取爬虫代码和正则代码', font=('黑体', 15))],
            [sg.B('退出', key='Exit', font=10), sg.B('刷新', font=10)]
        ]
        get_win = sg.Window('获取信息', layout)
        self.re_data = ''
        while True:
            event, values = get_win.read()
            get_win['-data-'].update(self.html_data.text)
            if event == None or event == 'Exit':
                quit(0)
            if event == '运行正则代码':
                z = values['-cmd-']
                try:
                    self.re_data = re.findall(z, self.html_data.text, re.S)
                except:
                    sg.popup_error(f'正则报错')
                else:
                    sg.Popup('re运行获得的信息为\n', self.re_data, font=('黑体', 15))
            if event == '保存html源码':
                self.html_data = requests.post(self.get_data['网址'],headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
                with open('html_data.txt', 'w', encoding='utf-8') as f:
                    f.write(self.html_data.text)
                sg.Popup('已保存为‘html_data.txt’文件中')
            if event == '获取爬虫代码和正则代码':
                with open('source_code.py', 'w', encoding='utf-8') as f:
                    code_py = """ \
# 代码经过删减,作者:eriddds/ES
import requests
import re
import random

ua = %s
""" % self.USER_AGENT_LIST
                    code = """ \

r = requests.post('%s',headers={'User-Agent': random.choice(ua)})
print(r)
print('='*15)
print(r.text)
""" % self.get_data['网址']
                    f.write(code_py)
                    f.write(code)
                    if self.re_data == '':
                        pass
                    else:
                        code_py2 = """ \
z = %s
re_data = re.findall(z,r.text,re.S)
print(re_data)
""" % self.re_data
                        f.write(code_py2)
                sg.Popup('文件已保存至"source_code.py"')


    def get_c(self):
        http = self.get_data['网址']
        base = os.path.basename(http)
        # 使用os.path.splitext分离文件名和扩展名
        _, ext = os.path.splitext(base)
        # 返回扩展名，不包括点（.）
        last_data = ext[1:] if ext else None
        try:
            self.html_data = requests.get(self.get_data['网址'], headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
            im_data = self.html_data.content
            with open(f'image.{last_data}', 'wb') as f:
                f.write(im_data)
        except:
            sg.popup_error('未知/错误 网址')
            quit(1)
        try:
            layout = [
                [sg.T(text="Eriddds/ES原创         ", font=("Arial", 25), background_color='white', key='-title-',
                      text_color='black')],
                [sg.T(text=f'响应状态码:{self.html_data}')],
                [sg.T(text='图片渲染',font=('黑体',15), background_color='white', text_color='red')],
                [sg.Image(filename=f'image.{last_data}')],
                [sg.B('退出',font=('黑体',15))]
            ]
            sg.Popup(f'图片已经自动保存至"image.{last_data}"')
            window = sg.Window('图片信息',layout)
            while True:
                event, values = window.read()
                if event == None:
                    window.close()
                    quit(0)
                if event == '退出':
                    window.close()
                    quit(0)
        except:
            sg.popup_error('已退出\n原因:退出或无法渲染该文件的图片,但已保存')

    def post_c(self):
        http = self.get_data['网址']
        base = os.path.basename(http)
        # 使用os.path.splitext分离文件名和扩展名
        _, ext = os.path.splitext(base)
        # 返回扩展名，不包括点（.）
        last_data = ext[1:] if ext else None
        try:
            self.html_data = requests.post(self.get_data['网址'], headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
            im_data = self.html_data.content
            with open(f'image.{last_data}', 'wb') as f:
                f.write(im_data)
        except:
            sg.popup_error('未知/错误 网址')
            quit(1)
        try:
            layout = [
                [sg.T(text="Eriddds/ES原创         ", font=("Arial", 25), background_color='white', key='-title-',
                      text_color='black')],
                [sg.T(text=f'响应状态码:{self.html_data}')],
                [sg.T(text='图片渲染',font=('黑体',15), background_color='white', text_color='red')],
                [sg.Image(filename=f'image.{last_data}')],
                [sg.B('退出',font=('黑体',15))]
            ]
            sg.Popup(f'图片已经自动保存至"image.{last_data}"')
            window = sg.Window('图片信息',layout)
            while True:
                event, values = window.read()
                if event == None:
                    window.close()
                    quit(0)
                if event == '退出':
                    window.close()
                    quit(0)
        except:
            sg.popup_error('已退出\n原因:退出或无法渲染该文件的图片,但已保存')

if __name__ == '__main__':
    a = GoSpider()
    a.init_window()