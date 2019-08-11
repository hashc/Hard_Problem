try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import copy
import time
import matplotlib.pyplot as plt
import seaborn as sns
import re
import pandas as pd
import pickle
import numpy as np
from datetime import datetime as dt
from collections import defaultdict
import os
from multiprocessing import Pool, cpu_count, current_process

def multifun(mfun,ps):
    pool = Pool(cpu_count()-2)
    multi_res= [pool.apply_async(mfun, (p,)) for p in ps]
    pool.close()
    pool.join()
    return [res.get() for res in multi_res]


def timelogger(func):
    def inner(*args, **kwargs): #1
        start = time.perf_counter()
        print("[start] "+func.__name__,end='\r')
        res = func(*args, **kwargs) 
        print("[finish] %s ==Time %.2f=="%(func.__name__,time.perf_counter()-start),end='\r')
        return func(*args, **kwargs) #2
    return inner
def getDfvalue(df,Id,label=None):
    return df[label][df['Id']==Id].values[0]
@timelogger
def save_pkl(D,fname=None):
    with open(fname,'wb') as f:
        pickle.dump(D,f)
    return 0
@timelogger
def load_pkl(fname=None):
    with open(fname,'rb') as f:
        D = pickle.load(f)
    return D



def str2time(string,Format = '%Y-%m-%dT%H:%M:%S'):
    return dt.strptime(string[:19],Format)
def get_timedelta_secend(time1,time2,Format = '%Y-%m-%dT%H:%M:%S'):
    if Format:
        delta = dt.strptime(time2[:19],Format)-dt.strptime(time1[:19],Format)
    else:
        delta = time2-time1
    return delta.seconds
def get_timedelta(time1,time2,Format = '%Y-%m-%dT%H:%M:%S'):
    if  Format:
        delta = dt.strptime(time2[:19],Format)-dt.strptime(time1[:19],Format)
    else:
        delta = time2-time1
    delta = int(delta.seconds/60)
    return delta
def SortTime(atlst):
    res = sorted(atlst,key=lambda x:x[1])
    return [a for a,t in res]


p1 = re.compile(r'[<](.*?)[>]', re.S)  #最小匹配
def getattrib(string):
    """
    {'Id': '5',
     'PostTypeId': '2',
     'ParentId': '1',
     'CreationDate': '2010-11-02T19:15:20.813',
     'Score': '42',
     'OwnerUserId': '13',
     'LastEditorUserId': '75633',
     'LastEditDate': '2017-12-13T08:24:54.477',
     'LastActivityDate': '2017-12-13T08:24:54.477',
     'CommentCount': '0'}
    
    """
    root = et.fromstring(string)
    attr = root.attrib
    #attr.pop("Body")
    return attr
infoList = ['PostTypeId','Id','OwnerUserId','CreationDate','AcceptedAnswerId','Tags','ParentId',
            "Score","CommentCount","ViewCount","AnswerCount","FavoriteCount",'Title','Body']
def getinfo(attr):
    tmpList = []
    for key in infoList:
        if key in attr:
            tmp = attr[key]
            if key == 'Tags':
                tmp = p1.findall(tmp)
        else:
            tmp = "null"
        tmpList.append(tmp)
    return tmpList
def CalWaitingTime(Data):
    wt = []
    n = 0 
    start = time.perf_counter()
    for i in Data.index:
        n+=1
        if Data.PostTypeId[i]==1 and not np.isnan(Data.AcceptedAnswerId[i]):
            time1 = Data.CreationDate[i][:-4]
            time2 = getDfvalue(data,data.AcceptedAnswerId[i],label="CreationDate")[:-4]
            delta = dt.strptime(time2,'%Y-%m-%dT%H:%M:%S')-dt.strptime(time1,'%Y-%m-%dT%H:%M:%S')
            delta = int(delta.seconds/60)
        else:
            delta = np.NaN
        wt.append(delta)
        if n%100000 == 0:
            elapsed = (time.perf_counter() - start)
            print("===Cal WaitingTime %d   TotalTimeCost %.2f==="%(n,elapsed),end='\r')
    return wt
def CleanData(fname=None,f_csv=None,):
    n=0
    start = time.perf_counter()
    data = {key:[] for key in infoList}
    wait_time = []
    with open(fname,'r') as f:
        for line in f:
            if "row" in line:
                n += 1
                attr = getattrib(line)
                tmpList = getinfo(attr)
                PostTypeId, postid,OwnerUserId,datetime,AcceptedAnswerId,tags,ParentId = tmpList[:7]
                for key,i in zip(infoList,range(len(infoList))):
                    data[key].append(tmpList[i])
            if n%100000 == 0:
                elapsed = (time.perf_counter() - start)
                print("===Data Clean %d   TotalTimeCost %.2f==="%(n,elapsed),end='\r')
    elapsed = (time.perf_counter() - start)
    print("===Data Clean Finish %d   TotalTimeCost %.2f==="%(n,elapsed),end='\r')
    Data = pd.DataFrame(data)
    del data
    wt = CalWaitingTime(Data)
    elapsed = (time.perf_counter() - start)
    print("===Cal WaitingTime %d   TotalTimeCost %.2f==="%(n,elapsed),end='\r')
    Data['WaitingTime']=wt
    Data.to_csv (f_csv, index = None, header=True)
    elapsed = (time.perf_counter() - start)
    print("===Finish %d   TotalTimeCost %.2f==="%(n,elapsed),end='\r')
    return Data
@timelogger
def GetTime(data):
    return {data.Id[i]:str2time(data.CreationDate[i]) for i in data.index}
@timelogger
def getQA(Answer):
    QA = defaultdict(lambda:[])
    for i in Answer.index:
        aid = Answer.Id[i]
        qid = Answer.ParentId[i]
        QA[qid].append(aid)
    return QA
@timelogger
def TeamCal(QA,Question,Time):
    QA_sortbytime={}
    QA_uptoaccept={}
    Q_AcceptTeam=defaultdict(lambda:[])
    Q_TotalTeam = defaultdict(lambda:[])
    n = 0 
    start = time.perf_counter()
    for qid in QA:
        n+=1
        atlst = [(aid,Time[aid]) for aid in QA[qid]]
        QA_sortbytime[qid] = SortTime(atlst)
        aid_accepted = getDfvalue(Question,qid,label='AcceptedAnswerId')
        if not np.isnan(aid_accepted):
            QA_uptoaccept[qid] = [aid  for aid in QA_sortbytime[qid] if Time[aid_accepted]>=Time[aid]]
            tn = len(QA_uptoaccept[qid])
            Q_AcceptTeam[tn].append(qid)
        else:
            tn = len(QA_sortbytime[qid])
            Q_TotalTeam[tn].append(qid)  
        if n%100000 == 0:
            elapsed = (time.perf_counter() - start)
            print("===TeamCal %d / %d  TotalTimeCost %.2f==="%(n,len(QA),elapsed),end='\r')
    elapsed = (time.perf_counter() - start)
    print("===TeamCal Finish %d   TotalTimeCost %.2f==="%(n,elapsed),end='\r')
    return  QA_sortbytime,QA_uptoaccept,Q_AcceptTeam,Q_TotalTeam
def Main(fname,f_csv):
    print("Loading %s"%fname)
    if not os.path.exists(f_csv):
        data = CleanData(fname=fname,f_csv=f_csv)       
    else:
        data = pd.read_csv(f_csv)
    Question = data[data.PostTypeId==1]
    Answer = data[data.PostTypeId==2]
    Time = GetTime(data)
    QA = getQA(Answer)
    if os.path.exists(fname+'.QA.pkl'):
        QAD = load_pkl(fname=fname+'.QA.pkl')
        QA_sortbytime,QA_uptoaccept,Q_AcceptTeam,Q_TotalTeam = QAD['sortbytime'],QAD['uptoaccept'],QAD['AcceptTeam'],QAD['TotalTeam']
    else:
        QA_sortbytime,QA_uptoaccept,Q_AcceptTeam,Q_TotalTeam = TeamCal(QA,Question,Time)
        QAD={'sortbytime':QA_sortbytime,'uptoaccept':QA_uptoaccept,'AcceptTeam':Q_AcceptTeam,'TotalTeam':Q_TotalTeam}
        save_pkl(QAD,fname = fname+'.QA.pkl')
    Ts = sorted(Q_AcceptTeam.keys())
    P=[[len(Q_AcceptTeam[ts]),len(Q_TotalTeam[ts])]  for ts in Ts]
    Ns = [len(Q_TotalTeam[ts]) for ts in Ts]
    print("==[Finish] %s =="%(fname))
    return Ts,P,Ns