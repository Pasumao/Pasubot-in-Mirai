from nonebot.plugin import on_keyword,on_command
from nonebot.rule import startswith
from nonebot.typing import T_State
from nonebot.adapters import MessageSegment,Message
from nonebot.adapters.mirai import Bot, MessageEvent
from nonebot.adapters.mirai.message import MessageSegment,MessageChain
import os
import pandas as pd
import requests
import xlwt
from danmuchuli import dmcl
import time

kk = on_keyword({"看看"}, rule=startswith("看看"))
dy = on_command("订阅", rule=startswith("订阅"))

@kk.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: T_State):
    #state['asd']=0
    try:
        group_id=event.get_session_id().split('_')[1]
        state['asd']=0
    except:
        group_id=event.get_user_id()
        state['asd']=0
    args = str(event.get_plaintext()).strip()
    state["group_id"]=group_id
    if args[:2]=='看看':
        state["mono"] = args[2:] # 如果用户发送了参数则直接赋值
        


@kk.got("mono", prompt="你想看什么？")
async def handle_mono(bot: Bot, event: MessageEvent, state: T_State):
    asd=state['asd']
    if asd==0:
        txtlist=[]
        mode='1'
        mono = state["mono"]
        group_id=state["group_id"]
        abs_path=os.path.abspath('.')+"\\awesome_bot\\plugins\\"
        canshu=''
        if ',' in mono:
            canshu=mono.split('，')[1:]
        elif ' ' in mono:
            canshu=mono.split(' ')[1:]
        if "帮助" in mono:
            if canshu=='':
                await kk.finish("可以输入\n1.看看帮助 仓库\n2.看看帮助 ass\n3.看看帮助 订阅\n4.看看帮助 游戏\n5.看看帮助 涩图\n空格可换成全角逗号\n指令中[]为非必要参数，{}为必要参数")
            elif canshu[0]=='仓库':
                await kk.finish(msgmake("仓库：\n,指令：看看仓库\n,可以查看近10次的弹幕记录\n,如果想看数据统计请看看看帮助 ass"))
            elif canshu[0]=='ass':
                await kk.finish(msgmake("ass：\n,指令：如果群订阅了多个频道-看看ass [{模式号} [直播序列号] [用「/」隔开的检索词列表]]\n,有四种模式：\n,模式1：正常检索\n,模式2：定向检索文本\n,模式3：在正常模式的基础上添加检索文本\n,模式4：定向检索用户名"))
            elif canshu[0]=='订阅':
                await kk.finish(msgmake("订阅：\n,指令：看看订阅\n,查看当前群聊中订阅了哪些频道\n,订阅方式：订阅{uid}\n,取消订阅方式：订阅{uid} 取消"))
            elif canshu[0]=='游戏':
                await kk.finish(msgmake("还没写呢"))
            elif canshu[0]=='涩图':
                await kk.finish(msgmake("还没写呢"))
        elif "仓库" in mono:
            if len(canshu)==0 and len(uidlist(group_id))==1:
                await kk.finish(msgmake('当前仓库：\n,'+ck(group_id)))
            elif len(uidlist(group_id))==1:
                await kk.finish(msgmake('当前仓库：\n,'+ck(group_id)))
        elif "ass" in mono:
            num_id=1
            if len(uidlist(group_id))==0:
                await kk.finish(msgmake("你还没有订阅过"))
            try:
                if len(canshu)==1:
                    mode=int(canshu[0])
                elif len(canshu)==0:
                    mode=1
                elif len(canshu)==2:
                    mode=int(canshu[0])
                    num_id=int(canshu[1])
                else:
                    mode=int(canshu[0])
                    txtlist=canshu[2].split('/')
            except:
                await kk.finish(msgmake("出错了"))
            jpgstr,i=ass_num(group_id,abs_path,num_id,mode,txtlist)
            if i==0:
                await kk.finish(msgmake(jpgstr))
            await kk.send(msgmake("最近一次直播的数据如下：\n,{}".format(jpgstr)))
        elif "订阅" in mono:
            await kk.finish(msgmake("当前订阅:\n{}".format(vnamestr(group_id))))
    else:
        pass
    
@dy.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: T_State):
    try:
        group_id=event.get_session_id().split('_')[1]
        state['asd']=0
    except:
        group_id=event.get_user_id()
        state['asd']=0
    args = str(event.get_plaintext()).strip()
    state["group_id"]=group_id
    if args:
        state["uid"] = args[2:]  # 如果用户发送了参数则直接赋值


@dy.got("uid", prompt="请输入待订阅的B站用户名")
async def handle_vname(bot: Bot, event: MessageEvent, state: T_State):
    asd=state['asd']
    if asd==0:
        uid = state["uid"]
        group_id=state["group_id"]
        canshu=''
        if ',' in uid:
            canshu=uid.split('，')[1:]
        elif ' ' in uid:
            canshu=uid.split(' ')[1:]
        if canshu=='':
            try:
                abs_path=os.path.abspath('.')+"\\awesome_bot\\plugins\\v\\"
                group_id2vname_df=pd.read_excel(abs_path+'dylist.xls')
                for i in group_id2vname_df.values.tolist():
                    if str(i[0])==group_id and str(i[2])==uid:
                        await kk.finish(msgmake("请不要重复订阅同一个频道"))
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',}
                cnldata=requests.get('https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(uid),headers=headers,).json()
                vname=cnldata['data']['name']
                roomid=cnldata['data']['live_room']['roomid']
                dit={'group_id':group_id,'vname':vname,'uid':uid,'roomid':roomid}
                group_id2vname_df=group_id2vname_df.append(dit,ignore_index=True)
                group_id2vname_df.to_excel(abs_path+'dylist.xls',index=0,encoding = 'utf-8')
                await kk.send(msgmake("订阅成功,1.jpg"))
            except:
                pass
        elif canshu[0]=="取消":
            await kk.send(msgmake("没写完呢"))
    else:
        pass
            
def msgmake(msgstr: str):
    msgdit={}
    msg=Message(message=None)
    for i in msgstr.split(","):
        if ('.jpg' in i) or ('.png' in i):
            msg.append(MessageSegment.image(path=i))
        else:
            msg.append(MessageSegment.plain(i))
    return msg

def ass_num(group_id,abs_path,canshu,mode=1,txtlist=[]):
    idlist=[]
    canshu=canshu-1
    uid=uidlist(group_id)[0][2]
    try:
        lst=requests.get(r'https://api.matsuri.icu/channel/{}/clips'.format(uid),headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',}).json()['data']
    except:
        return '无法查看，等会再查',0
    for i in range(5):
        idlist.append(lst[i]['id'])
    try:
        return dmcl(uid,'..\\Mirai\\data\\net.mamoe.mirai-api-http\\images\\',idlist[canshu],mode,txtlist),1
    except:
        return "出错了或者还在播",0
    pass

def vnamestr(group_id):
    vnamestr=''
    n=0
    abs_path=os.path.abspath('.')+"\\awesome_bot\\plugins\\v\\"
    group_id2vname_df=pd.read_excel(abs_path+'dylist.xls')
    for i in group_id2vname_df.values.tolist():
        if str(i[0])==group_id:
            vnamestr=vnamestr+i[1]+r' 空间：space.bilibili.com/{} 直播间:live.bilibili.com/{}'.format(str(i[2]),str(i[3]))+'\n,'
    return vnamestr

def uidlist(group_id):
    uidlist=[]
    abs_path=os.path.abspath('.')+"\\awesome_bot\\plugins\\v\\"
    group_id2vname_df=pd.read_excel(abs_path+'dylist.xls')
    for i in group_id2vname_df.values.tolist():
        if str(i[0])==group_id:
            uidlist.append(i)
    return uidlist

def list2msg(lst):
    msgstr=''
    n=0
    for i in lst:
        n=n+1
        msgstr=msgstr+str(n)+'.'+i+'\n,'
    return msgstr

def ck(group_id):
    datalist=[]
    uid=uidlist(group_id)[0][2]
    try:
        lst=requests.get(r'https://api.matsuri.icu/channel/{}/clips'.format(uid),headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',}).json()['data']
    except:
        return '无法查看，等会再查'
    for i in range(5):
        datalist.append('标题:'+lst[i]['title']+'，开始时间:'+str(int((int(time.time())-int(str(lst[i]['start_time'])[:-3]))/60))+'前，总弹幕数:'+str(lst[i]['total_danmu'])+'，观看人数:'+str(lst[i]['views']))
    return list2msg(datalist)












