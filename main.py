# -*- coding: UTF-8 -*-
'''
.__         .__  .__.__  .__        
|  |   ____ |  | |__|  | |__| ____  
|  |  /  _ \|  | |  |  | |  |/    \ 
|  |_(  <_> )  |_|  |  |_|  |   |  \
|____/\____/|____/__|____/__|___|  /
                                 \/ 
Magic Bot(KOOK) by lolilin(白澪)
project: Minecraft hypixel Bot 
github project: https://github.com/lolilin/hypixel-Info-KOOK
'''

##加载普通拓展( •̀ ω •́ )✧

from ensurepip import version
from sqlite3 import Timestamp
import time
from gevent import config
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
with open('./player/config.json', 'r', encoding='utf-8') as f:
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
version = 'Alpha 22a27a'

if msg.ctx.channel.id != "id":
    return
##Hypixel当前信息
@bot.command(name= 'hyp')
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
    
    elif type == 'about':
        cm = CardMessage()
        c1 = Card(Module.Header('关于 hypixel Info 机器人'), theme=Types.Theme.NONE)
        c1.append(Module.Section('这是一个可以查询hypixel信息的机器人'))
        c1.append(Module.Section(f'版本: {version}'))
        c1.append(Module.Section('github: https://github.com/lolilin/hypixel-Info-KOOK', Element.Button('link button', 'https://github.com/lolilin/hypixel-Info-KOOK', Types.Click.LINK)))
        cm.append(c1)

        c2 = Card(theme=Types.Theme.NONE) 
        c2.append(Module.Context('Powered by lolilin(白澪)'))
        cm.append(c2)  
        await msg.reply(cm)

    elif type == 'help' or type == '帮助':
        cm = CardMessage()
        c1 = Card(Module.Header('帮助文档'), theme=Types.Theme.NONE)
        c1.append(Module.Context('使用 "/hyp about" 来获取关于信息'))
        c1.append(Module.Divider())
        c1.append(Module.Header('快速命令'))
        c1.append(Module.Section('使用 "/hyp" 来获取服务器信息'))
        c1.append(Module.Section('使用 "/hi <玩家名>" 来获取玩家信息'))
        c1.append(Module.Header('如何使用 "/hyp <类型> <玩家名>"'))
        c1.append(Module.Section('类型=server 或 服务器: 获取hypixel服务器信息(无须填写玩家名'))
        c1.append(Module.Section('类型=player 或 玩家: 获取hypixel玩家信息'))
        c1.append(Module.Section('类型=hyp game(比如 skywars , 空岛战争): 获取指定游戏排行榜及信息(无须填写玩家名)[开发中]'))
        c1.append(Module.Section('类型=hyp game(比如 skywars , 空岛战争): 获取指定游戏玩家信息(填写玩家名)[开发中]'))
        c1.append(Module.Section('类型=ban 或 黑名单: 获取hypixel封禁玩家信息[开发中]'))
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
            c1 = Card(Module.Header(f'"{playername}" 语法错误'), color='#b20000') 
            c1.append(Module.Section(f'使用 "/hyp 帮助" 来获取帮助'))
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
                time_local = time.localtime(int(hyp1player.get('firstLogin')/1000))
                dt = time.strftime("%Y年%m月%d日 %H时%M分%S秒",time_local)
                firstlogin = dt
                time_local = time.localtime(int(hyp1player.get('lastLogin')/1000))
                dt = time.strftime("%Y年%m月%d日 %H时%M分%S秒",time_local)
                lastlogin = dt
                time_local = time.localtime(int(hyp1player.get('lastLogout')/1000))
                dt = time.strftime("%Y年%m月%d日 %H时%M分%S秒",time_local)
                lastlogout = dt


                ##在线部分
                mode = hyp1session.get('mode')
                gametype = hyp1session.get('gameType')

                if mode == 'LOBBY':
                    mode = '大厅'
                elif mode == 'dynamic':
                    mode = '游戏中'
                elif mode == 'hub':
                    mode = '空岛大厅'
                elif mode == 'PIT':
                    mode = '天坑乱斗'


                if gametype == 'DUELS':
                    gametype = '决斗游戏'
                elif gametype == 'BEDWARS':
                    gametype = '起床战争'
                elif gametype == 'SKYWARS':
                    gametype = '空岛战争'
                elif gametype == 'WOOL_GAMES':
                    gametype = '羊毛战争'
                elif gametype == 'SKYBLOCK':
                    gametype = '空岛生存'
                elif gametype == 'PROTOTYPE':
                    gametype = '测试游戏'
                elif gametype == 'MURDER_MYSTERY':
                    gametype = '密室杀手'
                elif gametype == 'HOUSING':
                    gametype = '家园世界'
                elif gametype == 'TNTGAMES': 
                    gametype = '掘战游戏'
                elif gametype == 'ARCADE':
                    gametype = '街机游戏'
                elif gametype == 'BUILD_BATTLE':
                    gametype = '建筑大师'
                elif gametype == 'MCGO':
                    gametype = '警匪大战'
                elif gametype == 'LEGACY':
                    gametype = '经典游戏'
                elif gametype == 'WALLS3':
                    gametype = '超级战墙'
                elif gametype == 'PIT':
                    gametype = '天坑乱斗'
                elif gametype == 'MAIN':
                    gametype = '主大厅'
                elif gametype == 'SUPER_SMASH':
                    gametype = '星碎英雄'
                elif gametype == 'BATTLEGROUND':
                    gametype = '领主战争'
                elif gametype == 'SURVIVAL_GAMES':
                    gametype = '闪电饥饿游戏'
                elif gametype == 'TOURNAMENT':
                    gametype = '竞赛殿堂'
                

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

                if rank == 'SUPERSTAR':
                    rank = 'MVP++'
                elif rank == 'MVP_PLUS':
                    rank = 'MVP+'
                elif rank == 'VIP_PLUS':
                    rank = 'VIP+'

                ##查询等级部分
                exp = hyp1player['networkExp']
                level = round((hyplv(exp)), 2)

                ##回复信息
                if online == True:
                    ocolor = '#c3dd70'
                    oonline = f'在线'
                else:
                    ocolor = '#8d8d8d'
                    oonline = f'离线[{lastlogout}]'

                cm = CardMessage()
                c1 = Card(Module.Header(f'{playername} 的hypixel信息'), color= f'{ocolor}')
                c1.append(Module.Context(f'{mcuuid}'))
                c1.append(Module.Divider())
                if rank == None:
                    c1.append(Module.Section(f'{playername} \nhypixel等级: {level} | 人品值: {hyp1player["karma"]}' , Element.Image(f'https://crafatar.com/avatars/{mcuuid}?size='), Types.SectionMode.LEFT))
                else:
                    c1.append(Module.Section(f'[{rank}]{playername} \nhypixel等级: {level} | 人品值: {hyp1player["karma"]}' , Element.Image(f'https://crafatar.com/avatars/{mcuuid}?size='), Types.SectionMode.LEFT))
                c1.append(Module.Divider())
                c1.append(Module.Section(f'状态: {oonline}'))
                if online == True:
                    c1.append(Module.Section(f'所在位置: {mode} [{gametype}]'))
                else:
                    c1.append(Module.Section(f'最后登陆: {lastlogin}'))
                cm.append(c1)

                c2 = Card(theme=Types.Theme.NONE) 
                c2.append(Module.Context('Powered by lolilin(白澪)'))
                cm.append(c2)  
                await msg.reply(cm)

##玩家基本信息(快速)
@bot.command(name = 'hi')
async def player_info(msg: Message, playername: str):
    ##判断玩家语法名
    grammar = is_valid_minecraft_username(f'{playername}')
    if grammar == False:

        cm = CardMessage()
        c1 = Card(Module.Header(f'"{playername}" 语法错误'), color='#b20000') 
        c1.append(Module.Section(f'使用 "/hyp 帮助" 来获取帮助'))
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
            time_local = time.localtime(int(hyp1player.get('firstLogin')/1000))
            dt = time.strftime("%Y年%m月%d日 %H时%M分%S秒",time_local)
            firstlogin = dt
            time_local = time.localtime(int(hyp1player.get('lastLogin')/1000))
            dt = time.strftime("%Y年%m月%d日 %H时%M分%S秒",time_local)
            lastlogin = dt
            time_local = time.localtime(int(hyp1player.get('lastLogout')/1000))
            dt = time.strftime("%Y年%m月%d日 %H时%M分%S秒",time_local)
            lastlogout = dt


            ##在线部分
            mode = hyp1session.get('mode')
            gametype = hyp1session.get('gameType')

            if mode == 'LOBBY':
                mode = '大厅'
            elif mode == 'dynamic':
                mode = '游戏中'
            elif mode == 'hub':
                mode = '空岛大厅'
            elif mode == 'PIT':
                mode = '天坑乱斗'


            if gametype == 'DUELS':
                gametype = '决斗游戏'
            elif gametype == 'BEDWARS':
                gametype = '起床战争'
            elif gametype == 'SKYWARS':
                gametype = '空岛战争'
            elif gametype == 'WOOL_GAMES':
                gametype = '羊毛战争'
            elif gametype == 'SKYBLOCK':
                gametype = '空岛生存'
            elif gametype == 'PROTOTYPE':
                gametype = '测试游戏'
            elif gametype == 'MURDER_MYSTERY':
                gametype = '密室杀手'
            elif gametype == 'HOUSING':
                gametype = '家园世界'
            elif gametype == 'TNTGAMES': 
                gametype = '掘战游戏'
            elif gametype == 'ARCADE':
                gametype = '街机游戏'
            elif gametype == 'BUILD_BATTLE':
                gametype = '建筑大师'
            elif gametype == 'MCGO':
                gametype = '警匪大战'
            elif gametype == 'LEGACY':
                gametype = '经典游戏'
            elif gametype == 'WALLS3':
                gametype = '超级战墙'
            elif gametype == 'PIT':
                gametype = '天坑乱斗'
            elif gametype == 'MAIN':
                gametype = '主大厅'
            elif gametype == 'SUPER_SMASH':
                gametype = '星碎英雄'
            elif gametype == 'BATTLEGROUND':
                gametype = '领主战争'
            elif gametype == 'SURVIVAL_GAMES':
                gametype = '闪电饥饿游戏'
            elif gametype == 'TOURNAMENT':
                gametype = '竞赛殿堂'
            

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

            if rank == 'SUPERSTAR':
                rank = 'MVP++'
            elif rank == 'MVP_PLUS':
                rank = 'MVP+'
            elif rank == 'VIP_PLUS':
                rank = 'VIP+'

            ##查询等级部分
            exp = hyp1player['networkExp']
            level = round((hyplv(exp)), 2)

            ##回复信息
            if online == True:
                ocolor = '#c3dd70'
                oonline = f'在线'
            else:
                ocolor = '#8d8d8d'
                oonline = f'离线[{lastlogout}]'

            cm = CardMessage()
            c1 = Card(Module.Header(f'{playername} 的hypixel信息'), color= f'{ocolor}')
            c1.append(Module.Context(f'{mcuuid}'))
            c1.append(Module.Divider())
            if rank == None:
                c1.append(Module.Section(f'{playername} \nhypixel等级: {level} | 人品值: {hyp1player["karma"]}' , Element.Image(f'https://crafatar.com/avatars/{mcuuid}?size='), Types.SectionMode.LEFT))
            else:
                c1.append(Module.Section(f'[{rank}]{playername} \nhypixel等级: {level} | 人品值: {hyp1player["karma"]}' , Element.Image(f'https://crafatar.com/avatars/{mcuuid}?size='), Types.SectionMode.LEFT))
            c1.append(Module.Divider())
            c1.append(Module.Section(f'状态: {oonline}'))
            if online == True:
                c1.append(Module.Section(f'所在位置: {mode} [{gametype}]'))
            else:
                c1.append(Module.Section(f'最后登陆: {lastlogin}'))
            cm.append(c1)

            c2 = Card(theme=Types.Theme.NONE) 
            c2.append(Module.Context('Powered by lolilin(白澪)'))
            cm.append(c2)  
            await msg.reply(cm)





#一切都结束了，开始运行吧(＠_＠;)
bot.run()