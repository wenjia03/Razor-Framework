from numpy import true_divide
from numpy.lib.function_base import select
import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os,config
import random
import webbrowser
from dateutil.parser import parse
import pandas as pd
browser = webdriver.Chrome()
Question = []#存储试题集
Answer = []#存储试题答案 常数 0=错误/A 1=正确/B 2=C 3=D
Qtypes = []#存储试题类型 0=判断题（2个Radio）1=选择题（4个Radio）
Qanswer = []#题面答案
Qtest = []#题面
def readquestion():
    path = config.QUESTION_PATH#os.getcwd()+'\\test1.csv'
    f = open(path, encoding='utf-8')
    data = pd.read_csv(f)
    lists = data.values.tolist()
    l = len(lists)
    print('读取完成，正在解析......')
    i = 0
    s = []
    while i < l:
        s = lists[i]
        Question.append(s[0])
        Qtypes.append(s[1])
        Answer.append(s[2])
        i = i + 1
        print(f'当前正在解析 {i+1} 项，共计有 {l} 项。')

    print('解析完成')

def search(questions):#解析题目的重复水平 题目重复返回该题位置，题目不重复返回-1
    l = len(Question)
    i = 0
    code = -1
    while i < l:
        if Question[i] == questions:
            code = i
            break
        i = 1 + i
    
    return code        
        
    
    


def reWord(xpath):#返回一个字符串
    subinfo = browser.find_element_by_xpath(xpath)
    info = subinfo.text
    return str(info)

def sleep(t):
    time.sleep(t)

def isElementExist(xpath):
    try:
        browser.find_element_by_xpath(xpath)
        return True
    except:
        return False

def pause():
    os.system('pause')

def status(words):#检测系统现在状态详情
    a = words.find("共有")
    b = words.find('题')
    c = words.find('第')
    d = words.find("/")
    e = words.find('页')
    lens = len(words)
    que = words[a+2:b-1]#共计题目数量
    now = words[c+1:d-1]#当前页
    pages =  words[d+2:e-1]#总共页数
    return [int(que),int(now),int(pages)]#状态详情

def RMain(words):
    a = words.find('、')
    return words[a + 1:]

def answerq(sum,q):#题号，答案
    browser.find_element_by_xpath(f'//*[@id="ti_{sum}_{q}"]').click()

readquestion()
print("TESTING……:)")
Print('Base On Razor Framework Designed By wenjia Chen Powered By Ferrum Fondation')
browser.get(config.SYSTEM_LINK)
print('Pls Login Your Account and start test.')
pause()
print("Checking……")
if isElementExist(config.ANAYSTIC_ELEMENT_XPATH) == True:
    print('Success!')
    print('Reading……')
    buttonword = reWord(config.ANASTIC_STATUS_XPATH)
    datas = status(buttonword)
    print(f"All:{datas[0]} NowPages:{datas[1]} ALLPages:{datas[2]}")
    i = 1
    sum = 1
    total = datas[0]
    while True:#读取题目进程
        if isElementExist(f'{config.QUESTION_FRONT}{i}{config.QUESTION_BACK}') != False:#检测当前题目是否存在
            Qtest.append(RMain(reWord(f'{config.QUESTION_FRONT}{i}{config.QUESTION_BACK}')))
            print(f"正在读取第{sum}题")
            if isElementExist(f'{config.QUESTION_FRONT}{i+1}{config.QUESTION_BACK}') == False:#检测是否存在下一题
                if sum >= datas[0]:#sum>=总数，即尾页
                    print('全部读取完成')
                    break
                else:#不满足，即不是尾页，清空计数器
                    i = 1
                    sum = sum + 1
                    while True:
                        try:
                            print('本页全部读取完成，准备换页')
                            buttonword = reWord(config.ANASTIC_STATUS_XPATH)
                            datas = status(buttonword)
                            if datas[1] == 1 and config.IS_CHANGEBUTTON_CHANGE == True:
                                browser.find_element_by_xpath(config.UP_BUTTON).click()#点击换页
                            else:
                                browser.find_element_by_xpath(config.DOWN_BUTTON).click()#点击换页
                            sleep(2)
                            break
                        except:
                            print("233")
            else:#不是最后一题，双数加一
                i = i + 1
                sum = sum +1
        else:
            break
    
    j = 0
    while j < total:#解题进程
        code = search(Qtest[j])
        if code != -1:#如果该题目存在
            Qanswer.append(int(Answer[code]))
            print(f'正在解第 {j} 题')
        else:
            print(f'题库中不存在该题：{Qtest[j]}')
            nowanswer = int(input('请回答：常数 0=正确/A 1=错误/B 2=C 3=D'))
            Qanswer.append(int(nowanswer))

        j = j + 1

    pageselecter = Select(browser.find_element_by_xpath(config.SETECTER))
    pageselecter.select_by_visible_text("1")

    i = 1
    sum = 1
    while i <= total:
        if isElementExist(f'{config.QUESTION_FRONT}{i}{config.QUESTION_BACK}') != False:#检测当前题目是否存在
            while True:
                try:
                    print(f"正在答第{sum}题")
                    q = int(Qanswer[sum-1])
                    answerq(sum,q)
                    if config.ANTI_DETECT == True:
                        sleep(config.ANTI_DETECT_TIME)
                    break
                except:
                    print('出现意外情况')
                    print('恶心算法保护已启动')
            
            if isElementExist(f'{config.QUESTION_FRONT}{i+1}{config.QUESTION_BACK}') == False:#检测是否存在下一题
                if sum >= datas[0]:#sum>=总数，即尾页
                    print('全部答题完成')
                    break
                else:#不满足，即不是尾页，清空计数器
                    i = 1
                    sum = sum + 1
                    print('本页全部答题完成，准备换页')
                    sleep(2)
                    while True:
                        try:
                            buttonword = reWord(config.ANASTIC_STATUS_XPATH)
                            datas = status(buttonword)
                            if datas[1] == 1 and config.IS_CHANGEBUTTON_CHANGE == True:
                                browser.find_element_by_xpath(config.UP_BUTTON).click()#点击换页
                            else:
                                browser.find_element_by_xpath(config.DOWN_BUTTON).click()#点击换页
                            sleep(2)
                            break
                        except:
                            print('233')
            else:#不是最后一题，双数加一
                i = i + 1
                sum = sum +1
        else:
            break
    pause()

