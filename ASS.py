import re
from asstm import *

class ASS:                  # 时轴类
    def __init__(self, name, biaodian, chang, lian=True):
        self.name = name
        self.bd2=biaodian
        self.lian=lian
        self.chang=chang
        # 读入轴的全部内容（包括对话、注释）
        with open(self.name+'.ass', encoding='utf-8-sig') as f:
            self.line, self.header = [], []
            for i in f.readlines():
                if i[:8] == 'Dialogue':
                    self.line.append(i)
                elif i[:7] == 'Comment':
                    self.line.append(i)
                else:
                    self.header.append(i)

    def shijian(self):
        # 读取轴里面的时间
        t1, t2, location= [], [], []
        for i, l in enumerate(self.line):
            if (not re.search(r",fx,",l)) and l[:7] != 'Comment':
                t1.append(l.split(',')[1])
                t2.append(l.split(',')[2])
                location.append(i+1)
            
        return t1, t2, location

    def biaodian(self):
        # 提示对话轴里面出现标点，能换的尽量都换了
        bd1 = ["'", '"', ',', '，']                   # 不知道咋换的标点（逗号是因为可能会有注释）
        chuibiaodian = ''
        lenth = len(self.line)
        for i in range(lenth):
            if self.line[i][:7] == 'Comment' or re.search(r",fx,", self.line[i]):      # 跳过注释
                pass
            elif 'ong' in self.line[i].split(',')[9]:
                print('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9]))
                chuibiaodian += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9])
            elif '???' in self.line[i].split(',')[9]:
                print('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9]))
                chuibiaodian += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9])
            elif '？？？' in self.line[i].split(',')[9]:
                print('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9]))
                chuibiaodian += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9])
            elif '校对' in self.line[i].split(',')[9]:
                print('第{}行可能翻译没听懂，校对请注意一下————{}'.format(
                    i+1, self.line[i].split(',')[9]))
                chuibiaodian += '第{}行可能翻译没听懂，校对请注意一下————{}\n'.format(
                    i+1, self.line[i].split(',')[9])
            else:
                for j in bd1:
                    if j in self.line[i].split(',')[9]:
                        print('第{}行轴标点有问题（不确定怎么改），请注意一下————{}'.format(
                            i+1, self.line[i].split(',')[9]))
                        chuibiaodian += '第{}行轴标点有问题（不确定怎么改），请注意一下————{}\n\n'.format(
                            i+1, self.line[i].split(',')[9])
                        break
                for key, value in self.bd2.items():
                    if key in self.line[i].split(',')[9]:
                        self.line[i] = self.line[i].replace(key, value)
                        print("第{}行轴的{}标点有问题，但是我给你换成了{}".format(i+1, key, value))
                        chuibiaodian += "第{}行轴的{}标点有问题，但是我给你换成了{}\n\n".format(
                            i+1, key, value)
        return chuibiaodian

    def shanzhou(self):
        # 锤闪轴
        chuishanzhou = ''
        start, end, location= self.shijian()
        lenth = len(start)            # 总行数
        # 先找出连轴
        zhou=[]
        for i in range(lenth):
            lianzhou=[]
            lianzhou_flag=False
            for k in zhou:
                if i in k:
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

        # 开始锤轴啦
        for i in range(lenth):
            shenzhou = False              # 是不是六亲不认轴
            # 先锤行自己的闪轴
            if timedelta(end[i], start[i]) > self.chang:
                tdelta = timedelta(end[i], start[i])
                print('第{}行轴是长轴，请注意（{}s）'.format(location[i], tdelta))
                chuishanzhou += '第{}行轴是长轴，请注意（{}s）\n'.format(location[i], tdelta)
            elif timedelta(end[i], start[i]) <= 0.49 and timedelta(end[i], start[i]) > 0:
                tdelta = timedelta(end[i], start[i])                   # 轴的时间
                tneeded = 0.5-tdelta                                   # 算出要加的时间
                for j in range(lenth):
                    if timedelta(start[j], end[i]) <= tneeded+0.3 and timedelta(start[j], end[i]) > 0:
                        shenzhou = True                                  # 遇到神轴了
                        if self.lian:
                            print(
                                "第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，不过我姑且给你连上了（{}）".format(
                                    location[i], tdelta*1000, location[j], start[j])
                            )
                            chuishanzhou += "第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，不过我姑且给你连上了（{}）\n".format(
                                location[i], tdelta*1000, location[j], start[j])
                            self.line[location[i]-1] = self.line[location[i]-1].replace(
                                self.line[location[i]-1].split(',')[2], start[j])
                            end[i] = start[j]
                        else:
                            print("第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，草这啥神轴啊，你自己看着改吧".format(
                                    location[i], tdelta*1000, location[j]))
                            chuishanzhou += "第{}行轴（{}ms）要是不闪就和第{}行轴之间是闪轴了，草这啥神轴啊，你自己看着改吧\n\n".format(
                                location[i], tdelta*1000, location[j])
                        break
                if not shenzhou:                                     # 没遇到神轴
                    # 看看有没有什么轴和它连着
                    kanguole=False
                    for j in zhou:
                        if location[i] in j and len(j)>1 and location[i]<max(j):
                            print("第{}行轴是闪轴（{}ms），但是它和{}行轴是连轴，所以看着改吧".format(
                                location[i], tdelta*1000, j[j.index(location[i])+1]
                            ))
                            chuishanzhou+="第{}行轴是闪轴（{}ms），但是它和{}行轴是连轴，所以看着改吧\n\n".format(
                                location[i], tdelta*1000, j[j.index(location[i])+1]
                            )
                            kanguole=True
                    if not kanguole:
                        tmp = timeplus(end[i], tneeded)
                        print("第{}行轴是闪轴（{}ms），但是我给你改好了，以防万一告诉你一下从{}改成了{}".format(
                            location[i], tdelta*1000, end[i], tmp))
                        chuishanzhou += "第{}行轴是闪轴（{}ms），但是我给你改好了\n以防万一告诉你一下从{}改成了{}\n\n".format(
                            location[i], tdelta*1000, end[i], tmp)
                        self.line[location[i]-1] = self.line[location[i]-1].replace(
                            self.line[location[i]-1].split(',')[2], tmp)
                        end[i] = tmp

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
                    if timedelta(start[k], end[i]) < 0.289 and timedelta(start[k], end[i]) > 0:   
                        # 发现有闪轴就检查一下这条是不是连轴的一部分 
                        for j in zhou:
                            if location[k] in j and len(j)>1 and min(j)<location[k]<max(j):
                                buyongkan=True
                                break
                        if buyongkan:
                            break
                        else:
                            tdelta = timedelta(start[k], end[i])              # 看看两个轴之间到底差了多少
                            if self.lian:
                                print("第{}行轴和第{}行轴之间是闪轴（{}ms），不过我给你连上了（{}）".format(
                                    location[i], location[k], tdelta*1000, start[k]))
                                chuishanzhou+="第{}行轴和第{}行轴之间是闪轴（{}ms），不过我给你连上了（{}）\n".format(
                                                location[i], location[k], tdelta*1000, start[k])
                                self.line[location[i]-1] = self.line[location[i]-1].replace(
                                    self.line[location[i]-1].split(',')[2], start[k])
                                end[i]=start[k]
                            else:
                                tneeded = 0.3-tdelta                            # 看看要改多少
                                candidate = timeminus(end[i], tneeded)
                                print('第{}行轴和第{}行轴之间是闪轴（{}ms），建议分开成{}或者连上（{}）'.format(
                                    location[i], location[k], tdelta*1000, candidate, start[k]
                                ))
                                chuishanzhou+="第{}行轴和第{}行轴之间是闪轴（{}ms），建议分开成{}或者连上（{}）\n".format(
                                                location[i], location[k], tdelta*1000, candidate, start[k])

        print("看完了！")
        chuishanzhou += '看完了！\n'
        return chuishanzhou

    def out(self):
        with open('锤-' + self.name + '.txt', 'w', encoding='utf-8') as f:
            f.write('源文件请放心，我一点没动\n\n')
            f.write('花寄四人这么可爱，不关注一下吗┏(^ω^)=☞审核群718235402\n\n')
            f.write('言归正传，这里是字符检查：\n')
            f.write(self.biaodian()+'\n')
            f.write('这里是锤轴：\n')
            csz = self.shanzhou()
            f.write(csz)
            if csz == '看完了！\n':
                f.write('是强强打轴手，花丸送你一朵小红花！')
            else:
                f.write(
                    '\n字符替换和简单的闪轴修改自动弄完了（保存在改-的那个ass里）\n( >ω<)kira☆')
            
        with open('改-' + self.name + '.ass', 'w', encoding='utf-8-sig') as f:
            f.writelines(self.header)
            f.writelines(self.line)
        return None