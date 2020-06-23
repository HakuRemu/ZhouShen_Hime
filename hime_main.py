
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication
import os
import re
from asstm import *

from hime_ui2_0 import Ui_MainWindow


biaodian = {'。。。': '...', '。': ' ', '‘': '「', '’': '」', '・・・': '...', '···': '...',
        '“': '「', '”': '」', '、': ' ', '~': '～', '!': '！', '?': '？', '　': ' ', '【': '「', '】': '」'}      # 默认要替换的标点

def open_dict():
    with open('biaodian.txt', 'r', encoding='utf-8') as fx:
        lin = fx.readlines()
    for i in range(len(lin)):
        lin[i] = lin[i].replace('\n', '')
    test_dict = {}
    new_dict = {}
    for i in lin:
        tmp_dict = eval(i)
        for key, value in tmp_dict.items():
            test_dict[key] = value
        new_dict[test_dict['想换的标点']] = test_dict['换成的标点']
    return new_dict

def write_dict():
    bd2 = []
    for key, value in biaodian.items():
        tmp = {}
        tmp['想换的标点'] = key
        tmp['换成的标点'] = value
        bd2.append(tmp)
    with open('biaodian.txt', 'w', encoding='utf-8') as fx:
        for i in bd2:
            fx.write(str(i))
            fx.write('\n')

class zhoushen_GUi(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(zhoushen_GUi, self).__init__(parent)
        self.gai_shan_zhou = False
        
        self.setupUi(self)
        self.progressBar.setValue(0)
        # 打开文件
        self.OpenFile.clicked.connect(self.fileopen)
        # 检查要不要连闪轴
        self.radioButton.toggled.connect(lambda :self.rBstate(self.radioButton))
        # 开始锤
        self.StartProgram.clicked.connect(self.kai_shi)

        # 检查并打开符号替换的txt文件
        try:
            self.biaodian = open_dict()
        except FileNotFoundError:
            reply = QMessageBox.question(self, '信息', '没有找到字符替换文件！\n已自动重建',
                QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                write_dict()
                self.biaodian = open_dict()
        except SyntaxError:
            reply = QMessageBox.question(self, '错误', '字符替换文件格式有误！\n是否重建？',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                write_dict()
                self.biaodian = open_dict()
            else:
                os._exit(5)


    def rBstate(self, radioButton):
        if radioButton.isChecked():
            self.textBrowser.append('开启无脑连轴模式！')
            self.gai_shan_zhou = True
        # else:
        #     self.gai_shan_zhou == False

    def fileopen(self):
        self.fileName_path, self.filetype = QFileDialog.getOpenFileName(self,
                "选取文件",
                "./",
                "ASS Files (*.ass)")  #设置文件扩展名过滤,注意用双分号间隔
        if self.fileName_path == '':
            return None
        # 打开文件
        self.textBrowser.append(self.fileName_path)
        self.name = self.fileName_path.split('/')[-1]
        self.path = self.fileName_path[:-len(self.name)]
        with open(self.fileName_path, 'r', encoding='utf-8-sig') as fass:
            self.line, self.header = [], []
            for i in fass.readlines():
                if i[:8] == 'Dialogue':
                    self.line.append(i)
                elif i[:7] == 'Comment':
                    self.line.append(i)
                else:
                    self.header.append(i)
        self.textBrowser.append('ass文件读取成功！')
        self.progress_point = 0
        self.progressBar.setValue(0)
        

    def kai_shi(self):
        # 读取时间和位置
        start, end, location= [], [], []
        for i, l in enumerate(self.line):
            if (not re.search(r",fx,",l)) and l[:7] != 'Comment':
                start.append(l.split(',')[1])
                end.append(l.split(',')[2])
                location.append(i+1)
        # 先检查符号
        self.textBrowser.append('开始字符检查……')
        outlog = '源文件请放心，我一点没动\n\n花寄四人这么可爱，不关注一下吗┏(^ω^)=☞审核群718235402\n\n言归正传，这里是字符检查：\n'    
        # 用于写入txt的内容
        bd1 = ["'", '"', ',', '，']                   # 不知道咋换的标点（逗号是因为可能会有注释）
        
        for i in range(len(self.line)):
            if self.line[i][:7] == 'Comment' or re.search(r",fx,", self.line[i]):      # 跳过注释
                pass
            elif 'ong' in self.line[i].split(',')[9]:
                self.textBrowser.append('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', '')))
                outlog += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', ''))
            elif '???' in self.line[i].split(',')[9]:
                self.textBrowser.append('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', '')))
                outlog += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', ''))
            elif '？？？' in self.line[i].split(',')[9]:
                self.textBrowser.append('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', '')))
                outlog += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', ''))
            elif '校对' in self.line[i].split(',')[9]:
                self.textBrowser.append('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', '')))
                outlog += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9].replace('\n', ''))
            else:
                for j in bd1:
                    if j in self.line[i].split(',')[9]:
                        self.textBrowser.append('第{}行轴标点有问题（不确定怎么改），请注意一下————{}'.format(
                            i+1, self.line[i].split(',')[9]))
                        outlog += '第{}行轴标点有问题（不确定怎么改），请注意一下————{}\n\n'.format(
                            i+1, self.line[i].split(',')[9])
                        break
                for key, value in self.biaodian.items():
                    if key in self.line[i].split(',')[9]:
                        self.line[i] = self.line[i].replace(key, value)
                        self.textBrowser.append("第{}行轴的{}标点有问题，但是我给你换成了{}".format(i+1, key, value))
                        outlog += "第{}行轴的{}标点有问题，但是我给你换成了{}\n\n".format(
                            i+1, key, value)
        self.textBrowser.append('字符检查完成！')
        self.progressBar.setValue(9)
        self.progress_point = 9
        # 开始锤轴啦
        self.textBrowser.append('开始查闪轴……')
        outlog += '这里是锤轴：\n'
        lenth = len(start)              # 总行数
        ckpt = round(lenth / 90)        # 进度条计数器
        # 先找出连轴
        zhou=[]
        for i in range(lenth):
            lianzhou=[]
            lianzhou_flag=False
            for k in zhou:
                if location[i] in k:
                    lianzhou_flag=True
                    break
            if lianzhou_flag:
                continue
            else:
                lianzhou.append(location[i])
                tmp=end[i]
                for j in range(lenth):
                    if start[j]==tmp:
                        tmp=end[j]
                        lianzhou.append(location[j])
                zhou.append(lianzhou)
        # for i in zhou:
        #     self.textBrowser.append(str(i))

        # 查行内的闪轴
        for i in range(lenth):
            if i % ckpt == 0:
                if self.progress_point <= 99:
                    self.progress_point += 1
                    self.progressBar.setValue(self.progress_point)
            shenzhou = False              # 是不是六亲不认轴
            # 先锤行自己的闪轴
            tdelta1 = timedelta(end[i], start[i])                   # 轴的时间
            if tdelta1 <= 0.49 and tdelta1 > 0:
                tneeded = 0.5 - tdelta1                                   # 算出要加的时间
                for j in range(lenth):
                    tdelta2 = timedelta(start[j], end[i])
                    if tdelta2 <= tneeded + 0.3 and tdelta2 > 0:
                        shenzhou = True                                  # 遇到神轴了
                        if self.gai_shan_zhou:
                            self.textBrowser.append(
                                "第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，不过我姑且给你连上了（{}）".format(
                                    location[i], tdelta1*1000, location[j], start[j])
                            )
                            outlog += "第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，不过我姑且给你连上了（{}）\n".format(
                                location[i], tdelta1*1000, location[j], start[j])
                            self.line[location[i]-1] = self.line[location[i]-1].replace(
                                self.line[location[i]-1].split(',')[2], start[j])
                            end[i] = start[j]
                        else:
                            self.textBrowser.append("第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，草这啥神轴啊，你自己看着改吧".format(
                                    location[i], tdelta1*1000, location[j]))
                            outlog += "第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，草这啥神轴啊，你自己看着改吧\n\n".format(
                                location[i], tdelta1*1000, location[j])
                        break
                if not shenzhou:                                     # 没遇到神轴
                    # 看看有没有什么轴和它连着
                    kanguole=False
                    for j in zhou:
                        if location[i] in j and len(j)>1 and location[i]<max(j):
                            self.textBrowser.append("第{}行轴是闪轴（{}ms），但是它和{}行轴是连轴，所以看着改吧".format(
                                location[i], tdelta1*1000, j[j.index(location[i])+1]
                            ))
                            outlog+="第{}行轴是闪轴（{}ms），但是它和{}行轴是连轴，所以看着改吧\n\n".format(
                                location[i], tdelta1*1000, j[j.index(location[i])+1]
                            )
                            kanguole=True
                            break
                    if not kanguole:
                        if self.gai_shan_zhou:
                            tmp = timeplus(end[i], tneeded)
                            self.textBrowser.append("第{}行轴是闪轴（{}ms），但是我给你改好了，以防万一告诉你一下从{}改成了{}".format(
                                location[i], tdelta1*1000, end[i], tmp))
                            outlog += "第{}行轴是闪轴（{}ms），但是我给你改好了\n以防万一告诉你一下从{}改成了{}\n\n".format(
                                location[i], tdelta1*1000, end[i], tmp)
                            self.line[location[i]-1] = self.line[location[i]-1].replace(
                                self.line[location[i]-1].split(',')[2], tmp)
                            end[i] = tmp
                        else:
                            self.textBrowser.append("第{}行轴是闪轴（{}ms），请注意一下".format(location[i], tdelta1*1000))
                            outlog += "第{}行轴是闪轴（{}ms），请注意一下\n\n".format(location[i], tdelta1*1000)
            
            # 再锤行与行之间的闪轴
            # 考虑到联动轴里面可能会有按样式分的情况
            # 打算每次都遍历一遍
            # 再考虑到看的这行轴可能和别的轴之间是连轴
            # 或者你从连轴中间往外看
            # 草联动轴咋这么恶心

            buyongkan=False
            # 先看看现在看的这行轴是不是连轴的一部分
            for j in zhou:
                if location[i] in j and len(j)>1 and location[i]<max(j):        # 看的这行轴是一串连轴的一部分，那就跳过这行轴
                    buyongkan=True
                    break
            if buyongkan:
                continue
            else:                                           # 如果看的不是连轴，就先找找有没有闪轴
                for k in range(lenth):
                    tdelta = timedelta(start[k], end[i])
                    if tdelta < 0.289 and tdelta > 0:   
                        # 发现有闪轴就检查一下这条是不是连轴的一部分 
                        for j in zhou:
                            if location[k] in j and len(j)>1 and min(j)<location[k]<max(j):
                                buyongkan=True
                                break
                        if buyongkan:
                            break
                        else:
                            tdelta = timedelta(start[k], end[i])              # 看看两个轴之间到底差了多少
                            if self.gai_shan_zhou:
                                self.textBrowser.append("第{}行轴和第{}行轴之间是闪轴（{}ms），不过我给你连上了（{}）".format(
                                    location[i], location[k], tdelta*1000, start[k]))
                                outlog+="第{}行轴和第{}行轴之间是闪轴（{}ms），不过我给你连上了（{}）\n".format(
                                                location[i], location[k], tdelta*1000, start[k])
                                self.line[location[i]-1] = self.line[location[i]-1].replace(
                                    self.line[location[i]-1].split(',')[2], start[k])
                                end[i]=start[k]
                            else:
                                tneeded = 0.3-tdelta                            # 看看要改多少
                                candidate = timeminus(end[i], tneeded)
                                self.textBrowser.append('第{}行轴和第{}行轴之间是闪轴（{}ms），建议分开成{}或者连上（{}）'.format(
                                    location[i], location[k], tdelta*1000, candidate, start[k]
                                ))
                                outlog+="第{}行轴和第{}行轴之间是闪轴（{}ms），建议分开成{}或者连上（{}）\n".format(
                                                location[i], location[k], tdelta*1000, candidate, start[k])
        self.progressBar.setValue(100)
        self.textBrowser.append("看完了！")
        outlog += '看完了！\n'
        with open(self.path + '改-' + self.name[:-4] + '.txt', 'w', encoding='utf-8') as ft:
            ft.writelines(outlog)
        with open(self.path + '改-' + self.name, 'w', encoding='utf-8-sig') as fn:
            fn.writelines(self.header)
            fn.writelines(self.line)
        reply = QMessageBox.question(self, '信息', '锤完了！',
                QMessageBox.Ok)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = zhoushen_GUi()
    window.show()
    sys.exit(app.exec_())