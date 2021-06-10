import json
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def dmcl(uid,path,haishin_id,mode=1,txtlist=[]):

    lst=requests.get("https://api.matsuri.icu/clip/{}/comments".format(haishin_id),headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',}).json()['data']
    time0=lst[0]['time']
    df=pd.DataFrame(columns=['time','name','chat'])
    dfp=pd.DataFrame(columns=['num'])
    dfpp=pd.DataFrame(columns=['num'])
    for i in lst:
        try:
            chat=i['text']
        except:
            continue
        time=int((i['time']-time0)/1000)
        name=i['username']
        dit={'time':time,'name':name,'chat':chat}
        s=pd.Series(dit)
        df=df.append(s,ignore_index=True)
        
    if mode==1:
        s=2
        sousuo=['草','w','哈','?','(','事故','kksk','awsl','h']
    elif mode==2:
        s=2
        sousuo=txtlist
    elif mode==3:
        s=2
        sousuo=['草','w','哈','?','(','事故','kksk','awsl','h']
        for i in txtlist:
            sousuo.append(i)
    elif mode==4:
        sousuo=txtlist
        s=1
        
    datalist={'0':0}
    relist={'0':0}
    for i in df.values.tolist():
        n=0
        t=int(i[0]/60)
        for k in sousuo:
            if k==i[s]:
                try:
                    relist['{}'.format(str(t))]=relist['{}'.format(t)]+1
                except:
                    relist['{}'.format(str(t))]=1
        try:
            datalist['{}'.format(str(t))]=datalist['{}'.format(t)]+1
        except:
            datalist['{}'.format(str(t))]=1
            
    mean=len(df)/int(list(datalist.keys())[-1])
            
    for i in range(int(list(datalist.keys())[-1])):
        try:
            num1=datalist['{}'.format(str(i))]
        except:
            num1=0
        try:
            num2=relist['{}'.format(str(i))]
        except:
            num2=0
        ditp={'num':num1}
        sp=pd.Series(ditp)
        dfp=dfp.append(sp,ignore_index=True)
        ditp={'num':num2}
        sp=pd.Series(ditp)
        dfpp=dfpp.append(sp,ignore_index=True)
    
    fig, (ax1, ax2) = plt.subplots(2, 1)

    plt.subplots_adjust(wspace=1,hspace=1)
    
    ax1.plot(dfp)
    ax1.set_title('all')
    ax1.set_xlabel('time/(min)')
    ax1.set_ylabel('num/min')
    ax1.grid(True)
    ax1.axhline(mean)

    ax2.set_title('kensaku')
    ax2.plot(dfpp)
    ax2.set_xlabel('time/(min)')
    ax2.set_ylabel('num/min')
    ax2.axhline(mean)
    plt.savefig(path+'123.jpg',dpi=75,bbox_inches = 'tight')
    plt.cla()
    return '123.jpg'
    
        
