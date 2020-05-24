# encoding: utf-8
# 作者：HakuRemu
# 在此感谢SK_415为本程序作出的贡献
# 没有他，我的程序不可能如此整齐
# 介绍：运行此程序就自动锤所有ass文件的闪轴和字符问题
# 注意：只能从轴的方面检查，其他问题（吞音，漏轴等）无法检查

import os
from ASS import ASS

if __name__ == "__main__":
    bd2 = {'。。。': '...', '。': ' ', '‘': '「', '’': '」', '・・・': '...', '···': '...',
               '“': '「', '”': '」', '、': ' ', '~': '～', '!': '！', '?': '？', '　': ' ', '【': '「', '】': '」'}      # 默认要替换的标点
    # 找所有文件夹里面的ass然后锤
    try:
        with open('biaodian.txt', 'r+', encoding='utf-8') as f:         # 打开用户自定义的标点替换方案
            biaodian=eval(f.read())

    except FileNotFoundError:
        print('没有找到文件！\n使用默认标点替换方案。。。')
        while True:
            chongjian=input('是否需要重建标点替换的txt文件？(y/n) ')
            if chongjian=='y':
                with open('biaodian.txt', 'w+', encoding='utf-8') as fb:
                    fb.write(str(bd2))
                print('重建成功！将以默认替换方案查轴')
                break
            elif chongjian=='n':
                print('将在不重建txt情况下以默认标点替换方案查轴')
                break

    except SyntaxError:
        print('字典格式有误！\n请检查是否用的英文逗号，英文分号，或者是没有写完！')
        while True:
            chongjian=input('是否需要重建标点替换的txt文件？(y/n) ')
            if chongjian=='y':
                with open('biaodian.txt', 'w+', encoding='utf-8') as fb:
                    fb.write(str(bd2))
                print('重建成功！将以默认替换方案查轴')
                break
            elif chongjian=='n':
                print('将在不重建txt情况下以默认标点替换方案查轴')
                break

    else:
        print('欢迎使用轴审姬！\n')
        while True:
            lian=input('是否需要无脑把闪轴都连上？(y/n) ')
            if lian=='y':
                lian=True
                break
            elif lian=='n':
                lian=False
                break
        for d in os.listdir():
            name, extension = os.path.splitext(d)
            if extension == '.ass' and os.path.isfile(d) and name[0:2] != '改-':
                ass = ASS(name, biaodian, lian)
                ass.out()
