'''
.__         .__  .__.__  .__        
|  |   ____ |  | |__|  | |__| ____  
|  |  /  _ \|  | |  |  | |  |/    \ 
|  |_(  <_> )  |_|  |  |_|  |   |  \
|____/\____/|____/__|____/__|___|  /
                                 \/ 
Magic Bot(kaiheila.cn) by lolilin(白澪)
project: Minecraft hypixel Bot 
github project: None
'''

##加载普通拓展( •̀ ω •́ )✧

from sqlite3 import Timestamp
import time
import requests
import json
import random
import datetime


from msilib.schema import Error
from mcuuid import MCUUID
from mcuuid.tools import is_valid_minecraft_username


##加载开黑啦机器人拓展ヾ(≧▽≦*)o
from khl import Bot, Message, EventTypes, Event
from khl.card import CardMessage, Card, Module, Element, Types, Struct
from khl.command import Rule


##加载配置文件(●'◡'●)
with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
bot = Bot(token=config['token']) #加载魔偶token


##函数
def hyplv(xp):
    ##计算hypixel经验到等级
    prefix = -3.5
    const = 12.25
    divides = 0.0008
    return (divides*xp+const)**0.5+prefix+1


##变量设置φ(゜▽゜*)♪



##关于
@bot.command(name = 'hyp-about')
async def about(msg: Message):
    cm = CardMessage
    c1 = Card(Module.Header('About hypixel Info Bot'), theme=Types.Theme.NONE)
    c1.append(Module.Section('hypixel Info Bot'))
    c1.append(Module.Section('github:' ))
    cm.append(c1)

    c2 = Card(theme=Types.Theme.NONE) 
    c2.append(Module.Context('Powered by lolilin(白澪)'))
    cm.append(c2)  
    await msg.reply(cm)

@bot.command(name = 'hyp-help')
async def help(msg: Message):
    cm = CardMessage
    c1 = Card(Module.Header('Help Word'), theme=Types.Theme.NONE)
    c1.append(Module.Context('use "/hyp-about" get about hypixel info'))
    c1.append(Module.Divider())
    c1.append(Module.Section('use "/hyp-info" to fast get server info'))
    c1.append(Module.Section('use "/hyp <name>" to fast get player info'))
    c1.append(Module.Header('How to use "/hyp-info <type> <name>"'))
    c1.append(Module.Section('type=server: get hypixel server info(No playername'))
    c1.append(Module.Section('type=player: to get player hypixel info'))
    c1.append(Module.Section('type=hypixel game(as skywars): to get that game info(No playername)'))
    c1.append(Module.Section('type=hypixel game(as skywars): to get that game player info(have playername)[In production]'))
    cm.append(c1)

    c2 = Card(theme=Types.Theme.NONE) 
    c2.append(Module.Context('Powered by lolilin(白澪)'))
    cm.append(c2)  
    await msg.reply(cm)


##Hypixel当前信息
@bot.command(name= 'hyp-info')
async def hyp_info(msg: Message, type: str = 'None', playername: str = 'None'):

    ##判断需要查询的类型
    if type == 'None' or type == 'server':

        ##查询服务器信息
        serverip = 'mc.hypixel.net'
        
        serverdata = requests.get(
                url= f'https://list.fansmc.com/api/{serverip}'
            ).json()
        motd = serverdata['motd']
        p = serverdata['p']
        mp = serverdata['mp']

        ##卡片信息
        cm = CardMessage()
        c1 = Card(Module.Header(f'{serverip}                                {p}/{mp}'), theme=Types.Theme.NONE) 
        # c1.append(Module.Container(Element.Image('https://texture.namemc.com/ad/bf/adbf2b8031965b50.png')))
        c1.append(Module.Section(f'{motd}',Element.Image('https://texture.namemc.com/ad/bf/adbf2b8031965b50.png'),Types.SectionMode.LEFT))
        cm.append(c1)
        c2 = Card(theme=Types.Theme.NONE) 
        c2.append(Module.Context('Powered by lolilin(白澪)'))
        cm.append(c2)  
        await msg.reply(cm)


    elif type == 'player' or type == '玩家':
        
        ##判断玩家语法名
        grammar = is_valid_minecraft_username(f'{playername}')
        if grammar == False:

            cm = CardMessage()
            c1 = Card(Module.Header(f'"{playername}" is not a correct Minecraft name'), color='#b20000') 
            c1.append(Module.Section(f'pls "/hyp <playername>" or \n"/hyp-info player <playername>" thx'))
            cm.append(c1)
            c2 = Card(theme=Types.Theme.NONE) 
            c2.append(Module.Context('Powered by lolilin(白澪)'))
            cm.append(c2)  
            await msg.reply(cm)
            

        else:

            ##请求uuid
            mcdata = requests.get(
                url= f'https://api.mojang.com/users/profiles/minecraft/{playername}'
            ).json()
            mcuuid = mcdata.get('id')
            
            ##请求hyp信息
            hyp1data = requests.get(    ##hyp1data变量为hypixel api的读取数据
                url = "https://api.hypixel.net/player",
                params = {
                    "key": {config['api_key']['hypixel']},
                    "uuid": {mcuuid}   
                }
            ).json()
            hyp1player = hyp1data.get("player")
            name = hyp1player.get("playername")
            hyp1status = requests.get(
                url = "https://api.hypixel.net/status",
                params = {
                    "key": {config['api_key']['hypixel']},
                    "uuid": {mcuuid}   
                }
            ).json()
            hyp1session = hyp1status.get("session")

            ##判断是否出错
            if hyp1player == None:
                return

            else:
                ##判断是否在线
                online = hyp1session.get("online")

                ##时间换算
                firstlogin = datetime.datetime.fromtimestamp(int(hyp1player.get('firstLogin')/1000))
                

                lastlogin = datetime.datetime.fromtimestamp(int(hyp1player.get('lastLogin')/1000))

                lastlogout = datetime.datetime.fromtimestamp(int(hyp1player.get('lastLogout')/1000))

                ##在线部分
                mode = hyp1session.get('mode')
                gametype = hyp1session.get('gameType')

                ##查询Rank部分
                hyp1rank = hyp1player.get("rank")
                hyp1monthlyPackageRank = hyp1player.get("monthlyPackageRank")
                hyp1newPackageRank = hyp1player.get("newPackageRank")

                if hyp1rank != None and hyp1rank != "NORMAL":
                    rank = hyp1data["player"]["rank"]
                elif hyp1monthlyPackageRank != None and hyp1monthlyPackageRank != "NONE":
                    rank = hyp1data["player"]["monthlyPackageRank"]
                elif hyp1newPackageRank != None:
                    rank = hyp1data["player"]["newPackageRank"]
                else:
                    rank = None
            
                ##查询等级部分
                exp = hyp1player['networkExp']
                level = round((hyplv(exp)), 2)

                ##回复信息
                if online == True:
                    ocolor = '#c3dd70'
                    online = f'{online}'
                else:
                    ocolor = '#8d8d8d'
                    online = f'{online}[{lastlogout}]'

                cm = CardMessage()
                c1 = Card(Module.Header(f'{playername} hypixel Info'), color= f'{ocolor}')
                c1.append(Module.Context(f'{mcuuid}'))
                c1.append(Module.Divider())
                c1.append(Module.Section(f'[{rank}]{name} \nlevel: {level} | karma: {hyp1player["karma"]}' , Element.Image(f'https://crafatar.com/avatars/{mcuuid}?size='), Types.SectionMode.LEFT))
                c1.append(Module.Divider())
                c1.append(Module.Section(f'online: {online}'))
                c1.append(Module.Section(f'lastlogin: {lastlogin} | firstlogin{firstlogin}'))
                c1.append(Module.Section(f'mode: {mode} [{gametype}]'))
                cm.append(c1)

                c2 = Card(theme=Types.Theme.NONE) 
                c2.append(Module.Context('Powered by lolilin(白澪)'))
                c2.append(c2)  
                await msg.reply(cm)

##玩家基本信息(快速)
@bot.command(name = 'hyp')
async def player_info(msg: Message, playername: str):
    ##判断玩家语法名
    grammar = is_valid_minecraft_username(f'{playername}')
    if grammar == False:

        cm = CardMessage()
        c1 = Card(Module.Header(f'"{playername}" is not a correct Minecraft name'), color='#b20000') 
        c1.append(Module.Section(f'pls "/hyp <playername>" or \n"/hyp-info player <playername>" thx'))
        cm.append(c1)
        c2 = Card(theme=Types.Theme.NONE) 
        c2.append(Module.Context('Powered by lolilin(白澪)'))
        cm.append(c2)  
        await msg.reply(cm)
        

    else:

        ##请求uuid
        mcdata = requests.get(
            url= f'https://api.mojang.com/users/profiles/minecraft/{playername}'
        ).json()
        mcuuid = mcdata.get('id')
        
        ##请求hyp信息
        hyp1data = requests.get(    ##hyp1data变量为hypixel api的读取数据
            url = "https://api.hypixel.net/player",
            params = {
                "key": {config['api_key']['hypixel']},
                "uuid": {mcuuid}   
            }
        ).json()
        hyp1player = hyp1data.get("player")
        name = hyp1player.get("playername")
        hyp1status = requests.get(
            url = "https://api.hypixel.net/status",
            params = {
                "key": {config['api_key']['hypixel']},
                "uuid": {mcuuid}   
            }
        ).json()
        hyp1session = hyp1status.get("session")

        ##判断是否出错
        if hyp1player == None:
            return

        else:
            ##判断是否在线
            online = hyp1session.get("online")

            ##时间换算
            firstlogin = datetime.datetime.fromtimestamp(int(hyp1player.get('firstLogin')/1000))
            

            lastlogin = datetime.datetime.fromtimestamp(int(hyp1player.get('lastLogin')/1000))

            lastlogout = datetime.datetime.fromtimestamp(int(hyp1player.get('lastLogout')/1000))

            ##在线部分
            mode = hyp1session.get('mode')
            gametype = hyp1session.get('gameType')

            ##查询Rank部分
            hyp1rank = hyp1player.get("rank")
            hyp1monthlyPackageRank = hyp1player.get("monthlyPackageRank")
            hyp1newPackageRank = hyp1player.get("newPackageRank")

            if hyp1rank != None and hyp1rank != "NORMAL":
                rank = hyp1data["player"]["rank"]
            elif hyp1monthlyPackageRank != None and hyp1monthlyPackageRank != "NONE":
                rank = hyp1data["player"]["monthlyPackageRank"]
            elif hyp1newPackageRank != None:
                rank = hyp1data["player"]["newPackageRank"]
            else:
                rank = None
        
            ##查询等级部分
            exp = hyp1player['networkExp']
            level = round((hyplv(exp)), 2)

            ##回复信息
            if online == True:
                ocolor = '#c3dd70'
                online = f'{online}'
            else:
                ocolor = '#8d8d8d'
                online = f'{online}[{lastlogout}]'

            cm = CardMessage()
            c1 = Card(Module.Header(f'{playername} hypixel Info'), color= f'{ocolor}')
            c1.append(Module.Context(f'{mcuuid}'))
            c1.append(Module.Divider())
            c1.append(Module.Section(f'[{rank}]{name} \nlevel: {level} | karma: {hyp1player["karma"]}' , Element.Image(f'https://crafatar.com/avatars/{mcuuid}?size='), Types.SectionMode.LEFT))
            c1.append(Module.Divider())
            c1.append(Module.Section(f'online: {online}'))
            c1.append(Module.Section(f'lastlogin: {lastlogin} | firstlogin{firstlogin}'))
            c1.append(Module.Section(f'mode: {mode} [{gametype}]'))
            cm.append(c1)

            c2 = Card(theme=Types.Theme.NONE) 
            c2.append(Module.Context('Powered by lolilin(白澪)'))
            c2.append(c2)  
            await msg.reply(cm)




#一切都结束了，开始运行吧(＠_＠;)
bot.run()