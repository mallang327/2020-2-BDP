#!/usr/bin/env python
# coding: utf-8

# # 기말프로젝트: Best player for you
# 20151496 정 원

# In[1]:


import hangul_font
import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib
import matplotlib.pyplot as plt
import re
import numpy as np
import time as tm


class Questions:
    
    col = ["순","이름","팀","WAR","G","타석","타수","득점",'안타',
          '2타','3타','홈런','루타','타점','도루','도실','볼넷',
          '사구','고4','삼진','병살','희타','희비']
    df = pd.DataFrame(columns=col)
    
    def __init__(self,Q_Num):
        self.Q_Num=Q_Num;
    
    def checkTime(func):
        def new_func(*args, **kwargs):

            start_time = tm.time()

            func(*args, **kwargs)

            end_time = tm.time()
            print('실행시간:',end_time - start_time)        
        return new_func
    
    def get_info():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless') # 웹 브라우저를 띄우지 않는 headless 
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chromeDriver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

        chromeDriver.get("http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&"
                         "ys=2020&ye=2020&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&"
                         "ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&"
                         "tr=&cv=&ml=1&sn=380&si=&cn=")
        #URL 주소

        html = chromeDriver.page_source
        stat_page = BeautifulSoup(html, 'html.parser')
        #stat_page = 크롤링한 정보
        temp = stat_page.find_all("table")[1]
            
        templen = len(temp.find_all("tr"))
            # Dataframe 작성

        df_all = Questions.df.copy()
        for i in range(2, templen):

            tempTr = temp.find_all("tr")[i]
            if(tempTr.find("th") is not None):
                continue
            row = {}
            column_idx = 0
            for j in range(23): # 0~22
                tTd = tempTr.find_all("td")[j]
                tempTd = tTd.text
                if j == 2:
                    result = re.search('(?<=20)\w',tempTd)
                    test = result.group()
                    if test == 'K':
                        res_color = re.search('(?<=background:)\W',str(tTd))
                        if res_color == None:
                            res_color = re.search('(?<=background:)\w+',str(tTd))
                        test2 = res_color.group()
                        if test2 == '#':
                            tempTd = 'Kia'
                        elif test2 == 'black':
                            tempTd = 'KT'
                    elif test == 'N':
                        tempTd = 'NC'
                    elif test == '키':
                        tempTd = '키움'
                    elif test == 'L':
                        tempTd = 'LG'
                    elif test == '롯':
                        tempTd = '롯데'
                    elif test == '삼':
                        tempTd = '삼성'
                    elif test == '한':
                        tempTd = '한화'
                    elif test == '두':
                        tempTd = '두산'
                    elif test == 'S':
                        tempTd = 'SK'

                row[Questions.col[column_idx]] = tempTd
                column_idx += 1
            df_all = df_all.append(row,ignore_index=True)
        return df_all
    
    def get_validdata():
        df_f = df_all.copy()
        df_f = df_all[["WAR","G","타석","타수","득점",'안타',
                           '2타','3타','홈런','루타','타점','도루',
                           '도실','볼넷','사구','고4','삼진','병살',
                           '희타','희비']].astype(float)
        df_f[['순','이름','팀']] = df_all[['순','이름','팀']]
        df_f = pd.DataFrame(df_f, columns = Questions.col)
        df72 = df_f['G'] >= 72
        df_72 = df_f[df72]
        

        return df_72

    
    def input_question():
        while True:
            try:
                
                Q_Num = int(input("1.선수 기록 찾기 2.나의 Best선수 찾기 0. 종료\n원하는 항목을 선택하세요 "))
                if Q_Num < 0 or Q_Num > 3:
                    raise ScoreException('0, 1, 2 세 가지 값 중에서 입력해주세요')
                else:
                    return Q_Num
                    break
            except IndexError:
                print('잘못 입력하셨습니다. 다시 입력하세요.')
            except ValueError:
                print('잘못 입력하셨습니다. 다시 입력하세요.')
                
            except KeyboardInterrupt:
                print('잘못 입력하셨습니다. 다시 입력하세요.')
                


class Question_1(Questions):

    col_1 = ["순","이름","팀","WAR","G","타석","타수","득점",'안타',
          '2타','3타','홈런','루타','타점','도루']
    df_1 = pd.DataFrame(columns = col_1)
    def __init__(self, Q_num):
        Questions.__init__(self, Q_Num)
        
    def get_Player():
                        # Dataframe 작성

        while True:
            Name = input("찾고싶은 선수 이름을 입력하세요: ")
            df_tt = Question_1.df_1.copy()
            for i in range(len(df_all)):
                if df_all.iloc[i][1] == Name:
                    temp_info = df_all.iloc[i][:15]
                    df_tt = df_tt.append(temp_info,ignore_index=True)
                    break
                else:
                    continue
            if df_tt.empty == True:
                print('\n잘못 입력하셨습니다, 다시 입력하세요\n')
                continue
            else:
                break
            
        return df_tt
    
    def get_Mean():
        df_72 = Questions.get_validdata()
        
        df_float2 = df_72[["WAR","G","타석","타수","득점",'안타',
           '2타','3타','홈런','루타','타점','도루']].astype(float)

        df_mean = df_float2.mean()
        df_mean['이름'] = '평균'
        return df_mean
    
    def get_Graphs():
        df_graph = Question_1.df_1.copy()
        df_graph = df_graph.append(df_tt,ignore_index=True)
        df_graph = df_graph.append(df_mean,ignore_index=True)
        df2_graph = df_graph.set_index("이름")
        df2_num = df2_graph[["WAR","G","타석","타수","득점",'안타',
                             '2타','3타','홈런','루타','타점','도루']].astype(float)
        df2_numT = df2_num.T
        return df2_numT
        
        
class Question_2(Questions):
    col_2 = ["순","이름","팀","WAR","G","타석","타수","득점",'안타',
          '2타','3타','홈런','루타','타점','도루','도실','볼넷',
          '사구','고4','삼진','병살','희타','희비']
    df_2 = pd.DataFrame(columns=col_2)
    def __init__(self, Q_num,style1,style2,style3,style4):
        Questions.__init__(self, Q_Num)
    
    
    def my_stat():
        col_stat = ["순","이름","팀","WAR","G","타석","타수","득점",'안타',
        '2타','3타','홈런','루타','타점','도루','도실','볼넷',
        '사구','고4','삼진','병살','희타','희비','파워','스피드','정교함','선구안']

        df_72 = Questions.get_validdata()
        df_temp = df_72.copy()
        df_temp2 = df_temp[["WAR","G","타석","타수","득점",'안타',
                            '2타','3타','홈런','루타','타점','도루',
                            '도실','볼넷','사구','고4','삼진','병살',
                            '희타','희비']].astype(float)
        df_temp2[['순','이름','팀']] = df_temp[['순','이름','팀']]

        df_temp2 = pd.DataFrame(df_temp2,columns=Question_2.col_2)
        
        df_temp2['타율'] = df_temp2['안타']/df_temp2['타수']
        df_temp2['단타'] = df_temp2['안타'] - (df_temp2['2타'] + df_temp2['3타'] + df_temp2['홈런'])
        df_temp2['파워'] = (df_temp2['단타'] + df_temp2['2타']*2 + df_temp2['3타']*2 + df_temp2['홈런']*5)/df_temp2['타수']
        df_temp2['스피드'] = (df_temp2['도루']*3 - df_temp2['도실']/2)*df_temp2['타율']
        
        df_temp2['정교함'] = (df_temp2['안타'] - df_temp2['삼진']/3) / df_temp2['타수']
        df_temp2['선구안'] = (df_temp2['볼넷'] + df_temp2['사구']) / df_temp2['삼진'] * df_temp2['볼넷']
    
        # norm_info
        scaler = MinMaxScaler()
        df_norm = df_temp2[["WAR","G","타석","타수","득점",'안타',
                   '2타','3타','홈런','타점','도루',
                   '도실','볼넷','사구','고4','삼진','파워','스피드','정교함','선구안']].astype(float)

        df_norm[['파워','스피드',
                 '정교함','선구안']] = scaler.fit_transform(df_norm[['파워','스피드',
                                                                          '정교함','선구안']])
        
        df_norm[['순','이름','팀']] = df_temp[['순','이름','팀']]
        df_norm = pd.DataFrame(df_norm, columns = col_stat)
        return df_norm
    # 야구 고수 질문  
    def input_attr():
        df_attr = df_norm.copy()
        list = []
        df_attr['res'] = 0
        while len(list) < 4:
            styles = int(input("1.파워(홈런) 2.스피드(도루) 3.정교함(타율) 4.선구안(볼넷)\n선호하는 스타일 번호를 순서대로 입력하세요 : "))
            if styles == 1:
                list.append('파워')
                df_attr['res'] = df_attr['res'] + df_attr['파워']*(8-2*(len(list)))
            elif styles == 2:
                list.append('스피드')
                df_attr['res'] = df_attr['res'] + df_attr['스피드']*(8-2*(len(list)))
            elif styles == 3:
                list.append('정교함')
                df_attr['res'] = df_attr['res'] + df_attr['정교함']*(8-2*(len(list)))
            elif styles == 4:
                list.append('선구안')
                df_attr['res'] = df_attr['res'] + df_attr['선구안']*(8-2*(len(list)))
            else:
                print('잘못 입력하셨습니다, 다시 입력하세요')
                continue
            print('\n')
        test = df_attr.sort_values(ascending = False,by = 'res')
        return test    
    # 야구 초보자 질문        
    def input_attr2():
        df_attr2 = df_norm.copy()
        list = []
        df_attr2['res'] = 0
        while len(list) < 4:
            
            styles = int(input("1.힘 센 선수(홈런) 2.빠른 선수(도루) 3.다재다능한 선수 4.동체시력 최고! 삼진 안 당하는 선수(볼넷)\n선호하는 스타일 번호를 순서대로 입력하세요 : "))
            if styles == 1:
                list.append('파워')
                df_attr2['res'] = df_attr2['res'] + df_attr2['파워']*(8-2*(len(list)))
            elif styles == 2:
                list.append('스피드')
                df_attr2['res'] = df_attr2['res'] + df_attr2['스피드']*(8-2*(len(list)))
            elif styles == 3:
                list.append('정교함')
                df_attr2['res'] = df_attr2['res'] + df_attr2['정교함']*(8-2*(len(list)))
            elif styles == 4:
                list.append('선구안')
                df_attr2['res'] = df_attr2['res'] + df_attr2['선구안']*(8-2*(len(list)))
            else:
                print('잘못 입력하셨습니다, 다시 입력하세요')
                continue
            print('\n')
        test2 = df_attr2.sort_values(ascending = False,by = 'res')
        return test2    

#Main 함수부분    
if __name__ == "__main__":
    print("KBO 선수 정보를 불러옵니다\n잠시만 기다려주세요")
    df_all = Questions.get_info()
    print('불러오기 완료\n')
   
    try:
        Q_Num = Questions.input_question()
    except ScoreException as e:
        print(e.args[0])
    else:

        if Q_Num == 1:
            Find_Player = Question_1(Q_Num)
            df_tt = Question_1.get_Player()
            df_mean = Question_1.get_Mean()
            df2_numT = Question_1.get_Graphs()

            df2_numT.plot(kind='bar')
            tm.sleep(0.5)
            print('원하는 선수의 정보를 찾았습니다!')


        elif Q_Num == 2:
            list2 = []
            level = int(input("1.야잘알(야구 고수!) 2.야알못(야구 몰라요)\n당신은 야알못? 야잘알? 번호를 입력하세요 : "))
            while len(list2) < 1:
                if level == 1:
                    list2.append('야잘알')
                    df_norm = Question_2.my_stat()
                    test = Question_2.input_attr()
                    print("당신이 찾는 선수는\n")
                    print(test[:3].iloc[:][['이름','팀']])
                    print("입니다!")
                elif level == 2:
                    list2.append('야알못')
                    df_norm = Question_2.my_stat()
                    test2 = Question_2.input_attr2()
                    print("당신이 찾는 선수는\n")
                    print(test2[:3].iloc[:][['이름','팀']])
                    print("입니다!")
                else:
                    print('잘못 입력하셨습니다, 다시 입력하세요')
                    continue

        elif Q_Num == 0:
            print('프로그램을 종료합니다.')

            
if __name__ == "__main__":
    print("KBO 선수 정보를 불러옵니다\n잠시만 기다려주세요")
    df_all = Questions.get_info()
    print('불러오기 완료\n')
   

    Q_Num = Questions.input_question()
    if Q_Num == 1:
        Find_Player = Question_1(Q_Num)
        df_tt = Question_1.get_Player()
        df_mean = Question_1.get_Mean()
        df2_numT = Question_1.get_Graphs()

        df2_numT.plot(kind='bar')
        time.sleep(0.5)
        print('원하는 선수의 정보를 찾았습니다!')


    elif Q_Num == 2:
        list2 = []
        level = int(input("1.야잘알(야구 고수!) 2.야알못(야구 몰라요)\n당신은 야알못? 야잘알? 번호를 입력하세요 : "))
        while len(list2) < 1:
            if level == 1:
                list2.append('야잘알')
                df_norm = Question_2.my_stat()
                test = Question_2.input_attr()
                print("당신이 찾는 선수는\n")
                print(test[:3].iloc[:][['이름','팀']])
                print("입니다!")
            elif level == 2:
                list2.append('야알못')
                df_norm = Question_2.my_stat()
                test2 = Question_2.input_attr2()
                print("당신이 찾는 선수는\n")
                print(test2[:3].iloc[:][['이름','팀']])
                print("입니다!")
            else:
                print('잘못 입력하셨습니다, 다시 입력하세요')
                continue

    elif Q_Num == 0:
        print('프로그램을 종료합니다.')


# In[ ]:




