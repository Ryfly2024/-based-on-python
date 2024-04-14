import matplotlib.pyplot as plt

import pandas as pd
from scipy.fft import fft, fftfreq
import numpy as np
import tkinter as tk
from tkinter import ttk,messagebox
import os

class app():
    def __init__(self):
        # 一个文件名输入框、按钮、范围输入框、

        #  UI界面    
            # 创建主窗口/
            self.root = tk.Tk()
            self.root.title('数据分析小工具__________author:RyFly')
            self.root.geometry("500x225")
            


            # 数据处理模式
            self.process_mode=0 # 0: peak,,,,,1:fft
            self.label_process_mode=tk.Label(self.root,text="数据处理模式",font=",15")
            self.label_process_mode.place(x=0,y=0,width=100, height=50)
            self.combo_box_chal = ttk.Combobox(self.root, state="readonly",font=("Arial,15"))  # 创建一个下拉菜单，设为只读模式
            self.combo_box_chal['values'] = ("计算波峰","计算波谷","傅里叶变换")  # 设置下拉菜单的选项，后期加入频率和
            self.combo_box_chal.current(0)  # 设置默认选择的选项为第一个
            self.combo_box_chal.bind("<<ComboboxSelected>>", self.ch_mode)   
            self.combo_box_chal.place(x=100,y=0,width=150, height=50)
            
            # 程序按钮
            self.bt=tk.Button(self.root,text="执行",command=self.show_data,font=",200")
            self.bt.place(x=250,y=100,width=125,height=120)

            # 输入波峰过滤
            self.label_en_fiter = tk.Label(self.root,text="过滤波峰",font=",6")
            self.label_en_fiter.place(x=250,y=50,width=60, height=50)
            self.en_fiter=tk.Entry()
            self.en_fiter.place(x=250+62,y=50,width=60, height=50)
            self.fiter=0.1

            #数据结果显示
            self.label_result=tk.Label(self.root,text="结果",font=",24")
            self.label_result.place(x=250,y=0,width=60,height=50)
            self.result_var=tk.StringVar()
            self.result_var.set("巴拉巴拉")
            self.label_frame_reult = tk.Frame(self.root, bd=2, relief=tk.SOLID)
            self.label_frame_reult.place(x=250+62,y=0,width=60,height=50)
            self.label_result_var=tk.Label(self.label_frame_reult,textvariable=self.result_var,font=",24")
            self.label_result_var.pack(expand=True)

            # 文件输入端口
            self.label_en_file_name = tk.Label(self.root,text="文件地址输入",font=",15")
            self.label_en_file_name.place(x=0,y=50,width=100, height=50)
            self.en_file_name=tk.Entry()
            self.en_file_name.place(x=100,y=50,width=150, height=50)

            # 读取文件表头
            self.label_en_file_head = tk.Label(self.root,text="表头读取",font=",15")
            self.label_en_file_head.place(x=0,y=100,width=100, height=50)
            self.en_file_head=tk.Entry()
            self.en_file_head.place(x=100,y=100,width=150, height=50)

            # 时间间隔
            self.label_en_time_itrvl = tk.Label(self.root,text="时间间隔(ms)",font=",15")
            self.label_en_time_itrvl.place(x=0,y=150,width=100, height=50)
            self.en_time_itrvl=tk.Entry()
            self.en_time_itrvl.place(x=100,y=150,width=150, height=50)


            # 读取范围
            
            self.label_range=tk.Label(self.root,text='读取范围',font=",15")
            self.label_range.place(x=0,y=200-10,width=100,height=50)
            
            self.en_index_start = tk.Entry()
            self.en_index_start.place(x=100,y=200,width=60,height=25)
            self.label_hengxian=tk.Label(self.root,text="——")
            self.label_hengxian.place(x=160,y=200,width=30,height=25)
            self.en_index_end = tk.Entry()
            self.en_index_end.place(x=190,y=200,width=60,height=25)
                         

            
            # 右边帮助
            heip_text='''
文件开头不能出\n
现数字;       \n
文件路径最好不\n
要出现中文;不过\n
我自己测试倒是 \n
没什么问题     \n

'''
            self.label_help = tk.Label(self.root,text=heip_text,font=",5")
            self.label_help.place(x=380,y=0,width=120,height=220)




        # 数据分析
            
            self.file_path =''
            self.data_head=''
            self.index_end  =0
            self.index_start=0
            self.time_itrvl=0.4

            self.file_data=[]
            self.data=[]
            self.x=[]

            self.root.mainloop()

    def show_data(self):
        ## 输入配置
        if self.en_file_name.get():
            self.file_path=self.en_file_name.get()       
        else:
            messagebox.showerror("错误","未输入文件地址")
            return 0
        if self.en_file_head.get():
            self.data_head=self.en_file_head.get()
        else: 
            messagebox.showerror("错误","未输入表头")
            return 0
        if self.en_index_start.get():
            self.index_start = int(self.en_index_start.get())
        else :
            messagebox.showerror("错误","未输入开头")
            return 0
        if self.en_index_end.get():
            self.index_end  = int(self.en_index_end.get())
        else :
            messagebox.showerror("错误","未输入结尾")
            return 0
        if self.en_time_itrvl.get():
            self.time_itrvl = float(self.en_time_itrvl.get())
        else :
            messagebox.showerror("错误","未输入时间间隔")
            return 0
        if self.en_fiter.get():
            self.fiter = float(self.en_fiter.get())
        else :
            self.fiter = 0.2
            return 0

        ## 读取数据
        try :
            # self.file_data = pd.read_excel(self.file_path)
            
            # 检查文件名是否以数字开头
            file_name = os.path.basename(self.file_path)
            print("success_file_name")
            if file_name[0].isdigit():
                # 如果是数字开头，则将文件重命名为一个合法的文件名
                new_file_name = "file_" + file_name  # 这里可以根据需要修改新文件名
                os.rename(self.file_path, os.path.join(os.path.dirname(self.file_path), new_file_name))
                self.file_path = os.path.join(os.path.dirname(self.file_path), new_file_name)
                print("change digital head")
            # 尝试读取 Excel 文件
            self.file_data = pd.read_excel(r"{}".format(self.file_path))
            print("suceess for read")


        except : 
            messagebox.showerror("erroe","读取文件失败")



        ## 数据处理
        self.data = self.file_data[self.data_head]
        self.data=self.data.tolist()
        self.data=self.data[self.index_start-1:self.index_end]
        print(self.data_head ,self.data[:10])
        
        if self.process_mode==0:
            self.result=self.count_peaks(self.data)
        elif self.process_mode==1:
            self.result=self.count_trough(self.data)
        else :
            self.result=self.get_main_frequency(self.data)
        self.result_var.set(str(self.result))
        self.ploting()
        print("result:",self.result)


     # FFT
    def get_main_frequency(self,input_array):
        # 计算傅里叶变换
        fft_result = np.fft.fft(input_array)
        
        # 获取频率轴
        freq_axis = np.fft.fftfreq(len(input_array), self.time_itrvl)
        
        # 找到主频频率的索引
        main_freq_index = np.argmax(np.abs(fft_result))
        
        # 获取主频频率
        main_frequency = freq_axis[main_freq_index]
        
        return main_frequency
    
    def count_peaks(self,arr):
        peaks = 0
        n = len(arr)
        num_max=max(arr)
        nim_min=min(arr)
        buchang= (num_max-nim_min)*self.fiter
        print("num_max:",num_max,"num_min:",nim_min)

        if n < 3:
            return peaks

        for i in range(1, n - 1):
            if arr[i] > arr[i - 1]+buchang and arr[i] > arr[i + 1]+buchang:
                   
                peaks += 1

        return peaks
    def count_trough(self,arr):
        peaks = 0
        n = len(arr)
        num_max=max(arr)
        nim_min=min(arr)
        buchang= (num_max-nim_min)*self.fiter
        print("num_max:",num_max,"num_min:",nim_min)

        if n < 3:
            return peaks

        for i in range(1, n - 1):
            if arr[i]+buchang < arr[i - 1] and arr[i]+buchang < arr[i + 1]:
                   
                peaks += 1

        return peaks

    def ch_mode(self,event):
        if self.combo_box_chal.get()=="计算波峰":
            self.process_mode= 0
            print("mode have been changed to count_peck")
        elif self.combo_box_chal.get()=="计算波谷":
            self.process_mode= 1
            print("mode have been changed to count_roug")
        else :
            self.process_mode= 2
            print("mode have been changeed to fft")

    def ploting(self):
        # 创建 x 轴数据，从 0 开始递增
        lengh=len(self.data)
        print("lengh:",lengh)
        x = [(i+self.index_start)*self.time_itrvl for i in range(lengh)]
        
        scale = self.time_itrvl
        # 绘制曲线
        plt.plot(x, self.data)
        scale=str(scale)
        # 添加标题和轴标签
        plt.title('Curve Plot')
        plt.xlabel('time/ms')
        plt.ylabel('Y')
        
        # 显示图形
        plt.show()


if __name__ == '__main__':
    my_app=app()
