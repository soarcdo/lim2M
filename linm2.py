import asyncio
import discord
import math
import time
import random
import threading
import sched
from datetime import datetime, timedelta
from discord.ext import commands, tasks
import os

#1 체르투바 3
#2 켈소스 5
#3 바실라 4
#4 사반 12
#5 여왕개미 6
#6 판드라이드 6
#7 티미트리스 8
#8 탈라킨 5
#9 템페스트 3
#10 펠리스 3
#11 엔쿠라 4
#12 사르카 5
#13 스탄 7
#14 크루마 습지 8
#15 3층크루마 8
#16 6층카탄 10
#17 7층코어 10
#18 판나로드 3.5
#19 마투라 4.5
#20 브래카 2.5
#21 메두사 4
#22 블랙릴리 4
#23 베히모스 6
#24 드래곤비스트 12

bosslist = ["체르투바의 막사(체르투바)","절망의 페허(켈소스)","황무지 남부(바실라)","개미굴 지하2층(사반)","개미굴 지하3층(여왕개미)",
            "디온 구릉지(판드라이드)","플로란 개간지(티미트리스)","반란군 아지트(탈라킨)","시체 처리소(템페스트)","비하이브(펠리스)",
            "디온 목초지(엔쿠라)","델루 리자드맨 서식지(사르카)","거인의 흔적(스탄)","크루마 습지(크루마)","크루마탑 3층(오염된 크루마)",
            "크루마탑 6층(카탄)","크루마탑 7층(코어 수스캡터)","고르곤의 화원(판나로드)","약탈자의 야영지(마투라)","브래카 소굴(브래카)",
            "메두사의 정원(메두사)","죽음의 회랑(블랙 릴리)","용의계곡 북부(베히모스)","안타라스의 동굴 지하6층(드래곤 비스트)"]
checklist = [0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,
             0,0,0,0]
timelist = ["1","2","3","4","5","6","7","8","9","10",
            "11","12","13","14","15","16","17","18","19","20",
            "21","22","23","24"]
app = discord.Client()
token = os.environ["BOT_TOKEN"]
token2 = os.environ["BOT_TOKEN"]
game = discord.Game(name="Chacking", type=8)
discordid = 386533767172456448  # 롤합시다 내 개인서버 테스트용 아이디
discordidlegend = 651046104921800727 #레전드서버 채팅채널아이디
discordboss = 661512467708379148
queues={}

@tasks.loop(seconds=60.0)
async def slow_count():
        await app.wait_until_ready()
        channel = app.get_channel(discordidlegend)
        if alramCheck() == 1:
                await channel.send(embed=alramBoss())        

@slow_count.after_loop
async def after_slow_count():
        print('done!')
        
@app.event
async def on_ready():
        print("다음으로 로그인합니다 : ")
        print(app.user.name)
        print(app.user.id)
        print("===============")
        await app.change_presence(status=discord.Status.online, activity=game)

@app.event
async def on_message(message):
        if message.author.bot:
                return None
        channel6 = app.get_channel(discordidlegend)
        
        strarray = message.content.split(' ')                           
	
        if strarray[0] == "!help" or strarray[0] == "!명령어":
                await message.channel.send("!컷 보스이름 \n!컷 체르 / !컷 켈소스 / !컷 바실라 / !컷 사반 / !컷 여왕 / !컷 판드 / !컷 티미 / !컷 탈라킨 / !컷 템페 / !컷 펠리스 / !컷 엔쿠라 / !컷 사르카 / !컷 스탄 / !컷 습지 / !컷 크3 / !컷 크6 / !컷 크7 / !컷 판나 / !컷 마투라 / !컷 브래카 / !컷 메두사 / !컷 릴리 / !컷 베히 / !컷 비스트\n !보스표 \n !분배(시간나면만들던지말던지)\n !주사위(귀차너)\n !멍 보스이름 )\n!컷시간 보스이름 시간 ")
                
        if strarray[0] == "!컷":
                await message.channel.send(BossCut(strarray[1]))

        if strarray[0] == "!보스":
                await message.channel.send(embed=BossList())

        if strarray[0] == "!컷시간":
                await message.channel.send(SetBossTime(strarray[1], strarray[2]))

        if strarray[0] == "!멍":
                await message.channel.send(SetBossTime(strarray[1], "99:99"))
                                           
        if strarray[0] == "!test":
                await channel6.send(embed=alramBosst())
def alramBosst():
        checkAlarm = 0
        print("알람울리거야")
        now = datetime.now()
        channel6 = app.get_channel(discordid)
        embed=discord.Embed(title="알람", colour=discord.Colour.red())  
        for num in range(24):
                bossstr = bosslist[num] + " 10분전 입니다."
                embed.add_field(name=num, value=bossstr, inline=False)
                
        embed.set_footer(text = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
        print(embed)
        return embed
        
def alramBoss():
        checkAlarm = 0
        #print("알람울리거야")
        now = datetime.now()
        channel6 = app.get_channel(discordid)
        embed=discord.Embed(title="알람", colour=discord.Colour.red())  
        for num in range(24):
                if checklist[num] == 1:
                        fullarray = timelist[num].split(' ')
                        datearray = fullarray[0].split("-")                
                        timearray = fullarray[1].split(':')
                        stime = datetime(int(datearray[0]),int(datearray[1]),int(datearray[2]),int(timearray[0]), int(timearray[1]))
                        tmpmin = (stime-now).seconds / 60
                        print(math.ceil(tmpmin))
                        if math.ceil(tmpmin) == 10:
                                bossstr = bosslist[num] + " 10분전 입니다."
                                print(bossstr)
                                embed.add_field(name=num, value=bossstr, inline=False)
                        if math.ceil(tmpmin) == 5:
                                bossstr = bosslist[num] + " 5분전 입니다."
                                embed.add_field(name=num, value=bossstr, inline=False)                   
                        if math.ceil(tmpmin) == 3:
                                bossstr = bosslist[num] + " 3분전 입니다."
                                embed.add_field(name=num, value=bossstr, inline=False)
                                

        embed.set_footer(text = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
        print(embed)
        return embed

def alramCheck():
        checkAlarm = 0
        now = datetime.now()
        
        for num in range(24):
                if checklist[num] == 1:
                        fullarray = timelist[num].split(' ')
                        datearray = fullarray[0].split("-")                
                        timearray = fullarray[1].split(':')
                        stime = datetime(int(datearray[0]), int(datearray[1]), int(datearray[2]) ,int(timearray[0]), int(timearray[1]))
                        tmpmin = (stime-now).seconds / 60
                        print(math.ceil(tmpmin))
                        if math.ceil(tmpmin) == 10:
                                checkAlarm = 1
                        if math.ceil(tmpmin) == 5:
                                checkAlarm = 1
                        if math.ceil(tmpmin) == 3:
                               checkAlarm = 1

        return checkAlarm

def BossList():
        strlist = []
        now = datetime.now()
        embed=discord.Embed(title="보스 시간 리스트", colour=discord.Colour.blue())  
   
        for num in range(24):
                if checklist[num] == 0:
                        embed.add_field(name=bosslist[num], value="시간 체크 안됨", inline=True)
                else:
                        fullarray = timelist[num].split(' ')
                        embed.add_field(name=bosslist[num], value=fullarray[1], inline=True)
                        
        embed.set_footer(text = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
        
        return embed

def bossNumber(bossname):
        bossnum = 99
        if bossname == "체르":
                bossnum = 0
        if bossname == "켈소스":
                bossnum = 1
        if bossname == "바실라":
                bossnum = 2
        if bossname == "사반":
                bossnum = 3
        if bossname == "여왕":
                bossnum = 4
        if bossname == "판드":
                bossnum = 5
        if bossname == "티미":
                bossnum = 6
        if bossname == "탈라킨":
                bossnum = 7
        if bossname == "템페":
                bossnum = 8
        if bossname == "펠리스":
                bossnum = 9
        if bossname == "엔쿠라":
                bossnum = 10
        if bossname == "사르카":
                bossnum = 11
        if bossname == "스탄":
                bossnum = 12
        if bossname == "습지":
                bossnum = 13
        if bossname == "크3":
                bossnum = 14
        if bossname == "크6":
                bossnum = 15
        if bossname == "크7":
                bossnum = 16
        if bossname == "판나":
                bossnum = 17
        if bossname == "마투라":
                bossnum = 18
        if bossname == "브래카":
                bossnum = 19
        if bossname == "메두사":
                bossnum = 20
        if bossname == "릴리":
                bossnum = 21
        if bossname == "베히":
                bossnum = 22
        if bossname == "비스트":
                bossnum = 23
        return bossnum
        
def SetBossTime(bossname, time):
        chk = 0
        tmpStr = " 컷 시간을 설정하였습니다. 다음 예정시간은 "
        tmptime = " "
        if len(time) != 5 or len(bossname) <= 1:
                return "ex) !컷시간 보스이름 17:05  <<< 시간:분 형식 /// Boss이름 확인"

        if time == "99:99":
                if 99== bossNumber(bossname):
                        return "보스이름을 다시 확인해 주세요"
                tmpStr = " 멍 처리. 다음 예정시간은 "
                fullarray = timelist[bossNumber(bossname)].split(' ')
                datearray = fullarray[0].split("-")                
                timearray = fullarray[1].split(':')
                now = datetime(int(datearray[0]), int(datearray[1]), int(datearray[2]), int(timearray[0]), int(timearray[1]))
                print(timelist[bossNumber(bossname)])
        else:                
                timearray = time.split(':')
                if int(timearray[0]) > 24 or int(timearray[0]) < 0:
                        return "설정 시간을 다시 확인하세요"
                if int(timearray[1]) > 60 or int(timearray[1]) < 0:
                        return "설정 시간을 다시 확인하세요"
                cdate = datetime.now()
                sdate = cdate.strftime("%Y-%m-%d")
                datearry = sdate.split("-")
                now = datetime(int(datearry[0]), int(datearry[1]), int(datearry[2]), int(timearray[0]), int(timearray[1]))
                
        if bossname == "체르":
                tmptime = now + timedelta(hours=3)
                timelist[0] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[0] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "켈소스":
                tmptime = now + timedelta(hours=5)
                timelist[1] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[1] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "바실라":
                tmptime = now + timedelta(hours=4)
                timelist[2] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[2] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "사반":
                tmptime = now + timedelta(hours=12)
                timelist[3] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[3] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "여왕":
                tmptime = now + timedelta(hours=6)
                timelist[4] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[4] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "판드":
                tmptime = now + timedelta(hours=6)
                timelist[5] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[5] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "티미":
                tmptime = now + timedelta(hours=8)
                timelist[6] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[6] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "탈라킨":
                tmptime = now + timedelta(hours=5)
                timelist[7] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[7] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "템페":
                tmptime = now + timedelta(hours=3)
                timelist[8] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[8] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "펠리스":
                tmptime = now + timedelta(hours=3)
                timelist[9] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[9] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "엔쿠라":
                tmptime = now + timedelta(hours=4)
                timelist[10] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[10] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "사르카":
                tmptime = now + timedelta(hours=5)
                timelist[11] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[11] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "스탄":
                tmptime = now + timedelta(hours=7)
                timelist[12] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[12] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "습지":
                tmptime = now + timedelta(hours=8)
                timelist[13] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[13] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "크3":
                tmptime = now + timedelta(hours=8)
                timelist[14] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[14] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "크6":
                tmptime = now + timedelta(hours=10)
                timelist[15] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[15] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "크7":
                tmptime = now + timedelta(hours=10)
                timelist[16] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[16] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "판나":
                tmptime = now + timedelta(hours=3.5)
                timelist[17] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[17] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "마투라":
                tmptime = now + timedelta(hours=4.5)
                timelist[18] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[18] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "브래카":
                tmptime = now + timedelta(hours=2.5)
                timelist[19] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[19] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "메두사":
                tmptime = now + timedelta(hours=4)
                timelist[20] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[20] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "릴리":
                tmptime = now + timedelta(hours=4)
                timelist[21] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[21] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "베히":
                tmptime = now + timedelta(hours=6)
                timelist[22] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[22] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "비스트":
                tmptime = now + timedelta(hours=12)
                timelist[23] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[23] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1

        if chk == 1:
                return bossname+ tmpStr + tmptime + " 입니다."
        else:
                return "설정 실패!! 보스이름을 제대로 입력해 주시기 바랍니다."
                
def BossCut(bossname):
        now = datetime.now()        
        tmpStr = " 컷 시간을 기록하였습니다. 다음예정시간은 "
        tmptime = " "
        chk = 0
        if bossname == "체르":
                tmptime = now + timedelta(hours=3)
                timelist[0] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[0] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
             
        if bossname == "켈소스":
                tmptime = now + timedelta(hours=5)
                timelist[1] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[1] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "바실라":
                tmptime = now + timedelta(hours=4)
                timelist[2] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[2] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "사반":
                tmptime = now + timedelta(hours=12)
                timelist[3] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[3] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "여왕":
                tmptime = now + timedelta(hours=6)
                timelist[4] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[4] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "판드":
                tmptime = now + timedelta(hours=6)
                timelist[5] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[5] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "티미":
                tmptime = now + timedelta(hours=8)
                timelist[6] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[6] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "탈라킨":
                tmptime = now + timedelta(hours=5)
                timelist[7] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[7] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "템페":
                tmptime = now + timedelta(hours=3)
                timelist[8] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[8] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "펠리스":
                tmptime = now + timedelta(hours=3)
                timelist[9] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[9] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "엔쿠라":
                tmptime = now + timedelta(hours=4)
                timelist[10] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[10] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "사르카":
                tmptime = now + timedelta(hours=5)
                timelist[11] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[11] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "스탄":
                tmptime = now + timedelta(hours=7)
                timelist[12] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[12] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "습지":
                tmptime = now + timedelta(hours=8)
                timelist[13] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[13] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "크3":
                tmptime = now + timedelta(hours=8)
                timelist[14] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[14] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "크6":
                tmptime = now + timedelta(hours=10)
                timelist[15] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[15] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "크7":
                tmptime = now + timedelta(hours=10)
                timelist[16] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[16] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "판나":
                tmptime = now + timedelta(hours=3.5)
                timelist[17] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[17] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "마투라":
                tmptime = now + timedelta(hours=4.5)
                timelist[18] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[18] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "브래카":
                tmptime = now + timedelta(hours=2.5)
                timelist[19] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[19] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "메두사":
                tmptime = now + timedelta(hours=4)
                timelist[20] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[20] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "릴리":
                tmptime = now + timedelta(hours=4)
                timelist[21] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[21] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "베히":
                tmptime = now + timedelta(hours=6)
                timelist[22] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[22] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1
        if bossname == "비스트":
                tmptime = now + timedelta(hours=12)
                timelist[23] = tmptime.strftime("%Y-%m-%d %H:%M")
                checklist[23] = 1
                tmptime = tmptime.strftime("%H:%M")
                chk = 1


        if chk == 1:
                return bossname+ tmpStr + tmptime + " 입니다."
        else:
                return "기록 실패!! 보스이름을 제대로 입력해 주시기 바랍니다."
                                        
#def Dice():

slow_count.start()
app.run(access_token)


