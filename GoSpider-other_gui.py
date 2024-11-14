import requests
import os
import random
import re
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class GoSpider(object):
    def __init__(self):
        self.get_data = {}
        self.USER_AGENT_LIST = [
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
        ]
        self.TimeSleepTime = 1 + random.random()

    def init_window(self):
        self.root = tk.Tk()
        self.root.title('GoSpider')
        self.root.geometry('600x400')

        self.title_label = tk.Label(self.root, text="Eriddds/ES原创", font=("Arial", 25), bg='white', fg='black')
        self.title_label.pack(pady=10)

        self.text1_label = tk.Label(self.root, text="爬虫请求方式，只能选一个", font=("黑体", 15), bg='white', fg='black')
        self.text1_label.pack(pady=5)

        self.get_var = tk.BooleanVar()
        self.get_checkbutton = tk.Checkbutton(self.root, text='Get请求', variable=self.get_var)
        self.get_checkbutton.pack(pady=5)

        self.post_var = tk.BooleanVar()
        self.post_checkbutton = tk.Checkbutton(self.root, text='Post请求', variable=self.post_var)
        self.post_checkbutton.pack(pady=5)

        self.chose_var = tk.StringVar()
        self.chose_var.set('请选择获取什么信息')
        self.chose_combobox = ttk.Combobox(self.root, values=['二进制文件（媒体等等）', '网页源码(前端)'], textvariable=self.chose_var)
        self.chose_combobox.pack(pady=5)

        self.text2_label = tk.Label(self.root, text='网址:', font=('黑体', 15), bg='white', fg='black')
        self.text2_label.pack(pady=5)

        self.text3_entry = tk.Entry(self.root, font=('黑体', 15), bg='white', fg='black')
        self.text3_entry.pack(pady=5)

        self.text4_label = tk.Label(self.root, text='', font=('黑体', 20), bg='white', fg='black')
        self.text4_label.pack(pady=5)

        self.confirm_button = tk.Button(self.root, text='确认', command=self.start_spider)
        self.confirm_button.pack(pady=5)

        self.cancel_button = tk.Button(self.root, text='取消', command=self.root.quit)
        self.cancel_button.pack(pady=5)

        self.root.mainloop()

    def start_spider(self):
        self.get_data = {
            'Get': self.get_var.get(),
            'Post': self.post_var.get(),
            'chose': self.chose_var.get(),
            '网址': self.text3_entry.get(),
        }

        if not (self.get_data['Get'] or self.get_data['Post']) or self.get_data['chose'] == '请选择获取什么信息':
            messagebox.showerror('错误', '请填写完整信息')
            return

        if self.get_data['chose'] == '二进制文件（媒体等等）':
            messagebox.showinfo('注意', '注意目前仅支持下载图片,不允许视频,敬请谅解')
            self.get_c()
        else:
            if self.get_data['Get']:
                self.get()
            elif self.get_data['Post']:
                self.Post()

    def get(self):
        try:
            self.html_data = requests.get(self.get_data['网址'], headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
        except:
            messagebox.showerror('错误', '未知/错误 网址')
            return

        self.get_window = tk.Toplevel(self.root)
        self.get_window.title('获取信息')

        self.get_title_label = tk.Label(self.get_window, text="Eriddds/ES原创", font=("Arial", 25), bg='white', fg='black')
        self.get_title_label.pack(pady=10)

        self.get_status_label = tk.Label(self.get_window, text=f'响应状态码: {self.html_data}')
        self.get_status_label.pack(pady=5)

        self.get_data_label = tk.Label(self.get_window, text='源码：')
        self.get_data_label.pack(pady=5)

        self.get_data_text = tk.Text(self.get_window, font=('黑体', 15), bg='white', fg='black', height=10, width=50)
        self.get_data_text.insert(tk.END, self.html_data.text)
        self.get_data_text.pack(pady=5)

        self.get_cmd_label = tk.Label(self.get_window, text='正则表达查找指令: 如：(.*?).*  等等', font=('黑体', 15), bg='white', fg='red')
        self.get_cmd_label.pack(pady=5)

        self.get_cmd_entry = tk.Entry(self.get_window, font=('黑体', 18))
        self.get_cmd_entry.pack(pady=5)

        self.get_run_button = tk.Button(self.get_window, text='运行正则代码', command=self.run_regex)
        self.get_run_button.pack(pady=5)

        self.get_save_button = tk.Button(self.get_window, text='保存html源码', command=self.save_html)
        self.get_save_button.pack(pady=5)

        self.get_code_button = tk.Button(self.get_window, text='获取爬虫代码和正则代码', command=self.get_code)
        self.get_code_button.pack(pady=5)

        self.get_exit_button = tk.Button(self.get_window, text='退出', command=self.get_window.quit)
        self.get_exit_button.pack(pady=5)

        self.get_window.mainloop()

    def run_regex(self):
        cmd = self.get_cmd_entry.get()
        try:
            re_data = re.findall(cmd, self.html_data.text, re.S)
            messagebox.showinfo('正则运行结果', '\n'.join(re_data))
        except:
            messagebox.showerror('错误', '正则报错')

    def save_html(self):
        try:
            with open('html_data.txt', 'w', encoding='utf-8') as f:
                f.write(self.html_data.text)
            messagebox.showinfo('保存成功', '已保存为‘html_data.txt’文件中')
        except:
            messagebox.showerror('错误', '保存失败')

    def get_code(self):
        try:
            with open('source_code.py', 'w', encoding='utf-8') as f:
                code_py = f"""\
# 代码经过删减,作者:eriddds/ES
import requests
import re
import random

ua = {self.USER_AGENT_LIST}
"""
                code = f"""

r = requests.get('{self.get_data['网址']}', headers={'User-Agent': random.choice(ua)})
print(r)
print('='*15)
print(r.text)
"""
                f.write(code_py)
                f.write(code)
            messagebox.showinfo('保存成功', '文件已保存至"source_code.py"')
        except:
            messagebox.showerror('错误', '保存失败')

    def Post(self):
        try:
            self.html_data = requests.post(self.get_data['网址'], headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
        except:
            messagebox.showerror('错误', '未知/错误 网址')
            return

        self.post_window = tk.Toplevel(self.root)
        self.post_window.title('获取信息')

        self.post_title_label = tk.Label(self.post_window, text="Eriddds/ES原创", font=("Arial", 25), bg='white', fg='black')
        self.post_title_label.pack(pady=10)

        self.post_status_label = tk.Label(self.post_window, text=f'响应状态码: {self.html_data}')
        self.post_status_label.pack(pady=5)

        self.post_data_label = tk.Label(self.post_window, text='源码：')
        self.post_data_label.pack(pady=5)

        self.post_data_text = tk.Text(self.post_window, font=('黑体', 15), bg='white', fg='black', height=10, width=50)
        self.post_data_text.insert(tk.END, self.html_data.text)
        self.post_data_text.pack(pady=5)

        self.post_cmd_label = tk.Label(self.post_window, text='正则表达查找指令: 如：(.*?).*  等等', font=('黑体', 15), bg='white', fg='red')
        self.post_cmd_label.pack(pady=5)

        self.post_cmd_entry = tk.Entry(self.post_window, font=('黑体', 18))
        self.post_cmd_entry.pack(pady=5)

        self.post_run_button = tk.Button(self.post_window, text='运行正则代码', command=self.run_regex)
        self.post_run_button.pack(pady=5)

        self.post_save_button = tk.Button(self.post_window, text='保存html源码', command=self.save_html)
        self.post_save_button.pack(pady=5)

        self.post_code_button = tk.Button(self.post_window, text='获取爬虫代码和正则代码', command=self.get_code)
        self.post_code_button.pack(pady=5)

        self.post_exit_button = tk.Button(self.post_window, text='退出', command=self.post_window.quit)
        self.post_exit_button.pack(pady=5)

        self.post_window.mainloop()

    def get_c(self):
        http = self.get_data['网址']
        base = os.path.basename(http)
        _, ext = os.path.splitext(base)
        last_data = ext[1:] if ext else None

        try:
            self.html_data = requests.get(self.get_data['网址'], headers={'User-Agent': random.choice(self.USER_AGENT_LIST)})
            im_data = self.html_data.content
            with open(f'image.{last_data}', 'wb') as f:
                f.write(im_data)
            messagebox.showinfo('保存成功', f'图片已经自动保存至"image.{last_data}"')
        except:
            messagebox.showerror('错误', '未知/错误 网址')

        self.get_image_window = tk.Toplevel(self.root)
        self.get_image_window.title('图片信息')

        self.get_image_label = tk.Label(self.get_image_window, text="Eriddds/ES原创", font=("Arial", 25), bg='white', fg='black')
        self.get_image_label.pack(pady=10)

        self.get_image_status_label = tk.Label(self.get_image_window, text=f'响应状态码: {self.html_data}')
        self.get_image_status_label.pack(pady=5)

        self.get_image_render_label = tk.Label(self.get_image_window, text='图片渲染', font=('黑体', 15), bg='white', fg='red')
        self.get_image_render_label.pack(pady=5)

        self.get_image_canvas = tk.Canvas(self.get_image_window, width=400, height=300)
        self.get_image_canvas.pack(pady=5)

        self.get_image_exit_button = tk.Button(self.get_image_window, text='退出', command=self.get_image_window.quit)
        self.get_image_exit_button.pack(pady=5)

        self.get_image_window.mainloop()

if __name__ == '__main__':
    try:
        a = GoSpider()
        a.init_window()
    except:
        pass
