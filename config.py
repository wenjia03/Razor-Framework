ANTI_DETECT = False
ANTI_DETECT_TIME = 1
QUESTION_PATH = 'D:\\工程\\JSU-安全教育自动考试\\tiku2.csv'#题库链接
SYSTEM_LINK = 'http://210.43.64.99:8080/'#考试系统链接
IS_CHANGEBUTTON_CHANGE = True#上一页下一页按钮变换,即第一页为下一页，第二页为上一页
#XPATH
ANAYSTIC_ELEMENT_XPATH = '/html/body/div/div[3]/div[2]/div[2]/div/div'#特征元素，用来检测是否处于答题页面
ANASTIC_STATUS_XPATH = '//*[@id="dati"]/div[26]'#检测当前题目状态
QUESTION_FRONT = '//*[@id="dati"]/div['#题目前的xpath
QUESTION_BACK = ']/h3'##题目后的xpath
#//*[@id="dati"]/div[题号变量]/h3
UP_BUTTON = '//*[@id="dati"]/div[26]/input[1]'#上一页
DOWN_BUTTON = '//*[@id="dati"]/div[26]/input[2]'#下一页
SETECTER = '//*[@id="runpage"]'
#答题系统需要自行开发，位于函数answerq