
import os
import discord
import requests
import time
from datetime import datetime, timedelta
import dateutil.parser
import pytz
import asyncio
from discord.ext import commands
from discord.utils import get
import pytz
from PIL import Image
import requests
import random


utc=pytz.UTC

GUILD = "Redacted"

alreadyPingedEventIDs=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
eventArchivalInProcess=False;

async def setupCommands(bot):
    asyncio.get_event_loop().create_task(lynchRoutine(bot))
    asyncio.get_event_loop().create_task(previousEventRoutine(bot))
    asyncio.get_event_loop().create_task(pingEventRoutine(bot))

    @bot.command(name='cancelAutoEventPing')
    async def cancelAutoEventPing(ctx):
        
        message = ctx.message.clean_content
        options = find_options(message, [])
        
        eventAlreadyPosted = False
        for tempEventId in alreadyPingedEventIDs:
            if(tempEventId == options[0]):
                eventAlreadyPosted = True
                
        if(eventAlreadyPosted):
            await ctx.message.channel.send("Auto event ping was already cancelled for: "+options[0])
        else:
            alreadyPingedEventIDs.append(options[0])
            alreadyPingedEventIDs.pop(0)
            await ctx.message.channel.send("Cancelled auto event ping for: "+options[0])
            
    @bot.command(name='seeAutoEventPing')
    async def seeAutoEventPing(ctx):
        await ctx.message.channel.send("Events that are currently already pinged or have cancelled auto pings: "+str(alreadyPingedEventIDs))
        
    @bot.command(name='pickRandomProfGang')
    async def pickRandomProfGang(ctx):
        print(ctx.message.author.id)
        if(ctx.message.author.id == "Redacted"):
            role = ctx.guild.get_role("Redacted")
            role2 = ctx.guild.get_role("Redacted")
            
            memberList = []
            
            for member in role.members:
                if(member in role2.members):
                    print(member.name +" already chosen remove from list")
                else:
                    memberList.append(member)
                    
            print("Member to be chosen list below")     
            print(memberList)
            
            if(len(memberList) == 0):
                print("no members left to pick")
                for member in role.members:
                    await member.remove_roles(role2)
                    
                await pickRandomProfGang(ctx)
            else:
                memberChosen = random.choice(memberList)
                await memberChosen.add_roles(role2)
                await ctx.message.channel.send(memberChosen.name +" gets to show the next movie!")

    @bot.command(name='changeNameColor')
    async def changeNameColor(ctx):
        
        message = ctx.message.clean_content
        options = find_options(message, [])
        
        colorRoleArray = []
        
        colorRoleArrayNames = []
        
        guildObj = bot.get_guild(GUILD)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)

        for color in guildObj.roles:
            if(color.name[:5] == 'Color'):
                colorRoleArrayNames.append(color.name)
                colorRoleArray.append(color.id)
        
        if len(options) > 0:
            for color in colorRoleArray:
                role_get = get(guildObj.roles, id=color)
                if(role_get in userObj.roles):
                    await userObj.remove_roles(role_get)
                   
            count = 0
            endcount = None
            for colorName in colorRoleArrayNames:
                userOptionReduced = 'color' + options[0].lower()
                userOptionReduced = ''.join(userOptionReduced.split())
                colorNameReduced = colorName.lower()
                colorNameReduced = ''.join(colorNameReduced.split())
                print(userOptionReduced)
                print(colorNameReduced)
                if(userOptionReduced == colorNameReduced):
                    endcount = count         
                count = count + 1
            
            if(endcount is None):
                await ctx.message.channel.send('Bot could not find your desired color, all color roles have now been removed from your account. Please select a color that is available as seen through the bot commands screen.')
            else:
                color_role_get = get(guildObj.roles, id=colorRoleArray[endcount])
                await userObj.add_roles(color_role_get)
                await ctx.message.channel.send('Bot has updated your username with the desired color.')
            
        else:
            await ctx.message.channel.send('Please add an option to select a color. For example !changeNameColor [SeaGreen]')
        
    @bot.command(name='removeNameColor')
    async def removeNameColor(ctx):
        
        colorRoleArray = []
        
        colorRoleArrayNames = []
        
        guildObj = bot.get_guild(GUILD)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)

        for color in guildObj.roles:
            if(color.name[:5] == 'Color'):
                colorRoleArrayNames.append(color.name)
                colorRoleArray.append(color.id)
                
        for color in colorRoleArray:
            role_get = get(guildObj.roles, id=color)
            if(role_get in userObj.roles):
                await userObj.remove_roles(role_get)
        
        await ctx.message.channel.send('Bot removed any color roles it could find attached to your user.')
        
    @bot.command(name='lynch')
    async def lynch(ctx):
        try:
            request = requests.get('https://www.googleapis.com/youtube/v3/search?key=redacted&channelId=UCDLD_zxiuyh1IMasq9nbjrA&part=snippet&order=date')
            print(request.text)
            await ctx.message.channel.send('https://www.youtube.com/watch?v='+str(request.json()["items"][0]["id"]["videoId"]))
            await ctx.message.channel.send('https://www.youtube.com/watch?v='+str(request.json()["items"][1]["id"]["videoId"]))
        except KeyError:
            await botError(ctx)
            return "Could not grab videos from David Lynch"

    @bot.command(name='lynchWeather')
    async def lynchWeather(ctx):
        try:
            request = requests.get('https://www.googleapis.com/youtube/v3/search?key=redacted&channelId=UCDLD_zxiuyh1IMasq9nbjrA&part=snippet&order=date')
            print(request.text)
            await ctx.message.channel.send('https://www.youtube.com/watch?v='+str(request.json()["items"][1]["id"]["videoId"]))
        except KeyError:
            await botError(ctx)
            return "Could not grab videos from David Lynch"
        
    @bot.command(name='lynchNumber')
    async def lynchNumber(ctx):
        try:
            request = requests.get('https://www.googleapis.com/youtube/v3/search?key=redacted&channelId=UCDLD_zxiuyh1IMasq9nbjrA&part=snippet&order=date')
            print(request.text)
            await ctx.message.channel.send('https://www.youtube.com/watch?v='+str(request.json()["items"][0]["id"]["videoId"]))
        except KeyError:
            await botError(ctx)
            return "Could not grab videos from David Lynch"
        
    @bot.command(name='removeMovieNights')
    async def removeMovieNights(ctx):
        movieNightsRoleId=redacted
        guildObj = bot.get_guild(GUILD)
        role_get = get(guildObj.roles, id=movieNightsRoleId)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)
        if(role_get in userObj.roles):
            await userObj.remove_roles(role_get)
            await ctx.message.channel.send('Bot removed the movie nights role!')
        else:
            await ctx.message.channel.send(" you don't have the movie nights role.")
        
    @bot.command(name='addMovieNights')
    async def addMovieNights(ctx):
        movieNightsRoleId=redacted
        guildObj = bot.get_guild(GUILD)
        role_get = get(guildObj.roles, id=movieNightsRoleId)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)
        if(role_get in userObj.roles):
            await ctx.message.channel.send(" you already have the movie nights role.")
        else:
            await userObj.add_roles(role_get)
            await ctx.message.channel.send('Bot added the movie nights role!')
        
    @bot.command(name='addGarlicGamers')
    async def addGarlicGamers(ctx):
        movieNightsRoleId=redacted
        guildObj = bot.get_guild(GUILD)
        role_get = get(guildObj.roles, id=movieNightsRoleId)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)
        if(role_get in userObj.roles):
            await ctx.message.channel.send(" you already have the garlic gamers role.")
        else:
            await userObj.add_roles(role_get)
            await ctx.message.channel.send('Bot added the garlic gamersrole!')
            
    @bot.command(name='removeGarlicGamers')
    async def removeGarticGamers(ctx):
        movieNightsRoleId=redacted
        guildObj = bot.get_guild(GUILD)
        role_get = get(guildObj.roles, id=movieNightsRoleId)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)
        if(role_get in userObj.roles):
            await userObj.remove_roles(role_get)
            await ctx.message.channel.send('Bot removed the garlic gamers role!')
        else:
            await ctx.message.channel.send(" you don't have the garlic gamers role.")
        
    @bot.command(name='addMinecraftRole')
    async def addMinecraftRole(ctx):
        movieNightsRoleId=redacted
        guildObj = bot.get_guild(GUILD)
        role_get = get(guildObj.roles, id=movieNightsRoleId)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)
        if(role_get in userObj.roles):
            await ctx.message.channel.send(" you already have the Minecraft role.")
        else:
            await userObj.add_roles(role_get)
            await ctx.message.channel.send('Bot added the Minecraft role!')
            
    @bot.command(name='removeMinecraftRole')
    async def removeMinecraftRole(ctx):
        movieNightsRoleId=redacted
        guildObj = bot.get_guild(GUILD)
        role_get = get(guildObj.roles, id=movieNightsRoleId)
        userObj = ctx.message.guild.get_member(ctx.message.author.id)
        if(role_get in userObj.roles):
            await userObj.remove_roles(role_get)
            await ctx.message.channel.send('Bot removed the minecraft role!')
        else:
            await ctx.message.channel.send(" you don't have the minecraft role.")
        
    @bot.command(name='getReal')
    async def getReal(ctx):
        await ctx.message.channel.send('Watching movies on your telephone....')
        await ctx.message.channel.send('https://www.youtube.com/watch?v=BcNLEwf2pOw')

    @bot.command(name='pingForEvent')
    async def pingForEvent(ctx):
        try:
            message = ctx.message.clean_content
            options = find_options(message, [])
            
            headerData = {
                'Authorization': 'redacted'
            }
                   
            requestChannelEvents = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events?country_code=US&payment_source_id=redacted&with_user_count=true', headers = headerData)

            if(len(requestChannelEvents.json()) > 0):
                for x in requestChannelEvents.json():
                    if(x["id"] == options[0]):
                        eventDate = dateutil.parser.parse(x["scheduled_start_time"])
                        now = utc.localize(datetime.utcnow())
                        print('now in utc '+now.strftime("%Y-%m-%d %H:%M:%S"))
                        print('event time in utc '+eventDate.strftime("%Y-%m-%d %H:%M:%S"))
                        
                        minutes_diff = "in " + str(int((eventDate - now).total_seconds() / 60)) + " minutes"
                        if(int((eventDate - now).total_seconds() / 60) < 1):
                            minutes_diff = "now"
                        
                        requestEvent = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events/'+x["id"]+'/users?limit=100&with_member=true', headers = headerData)
                        userNameArray = []
                        userIdArray = []
                        for y in requestEvent.json():
                            if(len(requestEvent.json()) > 0):
                                userNameArray.append(y["user"]["username"])
                                userIdArray.append(y["user"]["id"])
                        
                        userPingIDs = ""
                        for tempUserID in userIdArray:
                            userPingIDs = userPingIDs + "<@"+tempUserID+">"+ ", ";
                            
                        userPingIDs = userPingIDs[0:-2]
                            
                        if(len(options) > 1):
                            await ctx.message.channel.send(options[1]+"\n<@&redacted>, "+userPingIDs)
                        else:
                            await ctx.message.channel.send(x["name"]+" starts "+minutes_diff+"\n<@&redacted>, "+userPingIDs)
                        
        except Exception as e:
            await botError(ctx)
            print(e)
            print("manual event ping ran into an issue")
            
    @bot.command(name='pingForEventWithMovieNights')
    async def pingForEventWithMovieNights(ctx):
        try:
            message = ctx.message.clean_content
            options = find_options(message, [])
            
            headerData = {
                'Authorization': 'redacted'
            }
                   
            requestChannelEvents = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events?country_code=US&payment_source_id=redacted&with_user_count=true', headers = headerData)
            if(len(requestChannelEvents.json()) > 0):
                for x in requestChannelEvents.json():
                    if(x["id"] == options[0]):
                        eventDate = dateutil.parser.parse(x["scheduled_start_time"])
                        now = utc.localize(datetime.utcnow())
                        print('now in utc '+now.strftime("%Y-%m-%d %H:%M:%S"))
                        print('event time in utc '+eventDate.strftime("%Y-%m-%d %H:%M:%S"))
                        
                        minutes_diff = "in " + str(int((eventDate - now).total_seconds() / 60)) + " minutes"
                        if(int((eventDate - now).total_seconds() / 60) < 1):
                            minutes_diff = "now"
                        
                        requestEvent = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events/'+x["id"]+'/users?limit=100&with_member=true', headers = headerData)
                        userNameArray = []
                        userIdArray = []
                        for y in requestEvent.json():
                            if(len(requestEvent.json()) > 0):
                                userNameArray.append(y["user"]["username"])
                                userIdArray.append(y["user"]["id"])
                        
                        userPingIDs = ""
                        for tempUserID in userIdArray:
                            userPingIDs = userPingIDs + "<@"+tempUserID+">"+ ", ";
                            
                        userPingIDs = userPingIDs[0:-2]
                        
                        if(len(options) > 1):
                            await ctx.message.channel.send(options[1]+"\n<@&redacted>, "+userPingIDs)
                        else:
                            await ctx.message.channel.send(x["name"]+" starts "+minutes_diff+"\n<@&redacted>, "+userPingIDs)
                        
        except Exception as e:
            await botError(ctx)
            print(e)
            print("manual event ping ran into an issue")
            
    @bot.command(name='getEventIDs')
    async def getEventIDs(ctx):
        try:
            jamchanid = redacted
            
            headerData = {
                'Authorization': 'redacted'
            }
                   
            requestChannelEvents = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events?country_code=US&payment_source_id=redacted&with_user_count=true', headers = headerData)
            if(len(requestChannelEvents.json()) > 0):
                embed=discord.Embed(color=discord.Color(11812188), description="Here are all the available event IDs.")
                for x in requestChannelEvents.json():
                    embed.add_field(name="**"+x["name"]+"**", value="Event ID: " +x["id"], inline=False)
                    
                await ctx.message.channel.send(embed=embed)
            
        except Exception as e:
            print(e)
            print("event ping ran into an issue")
            
    @bot.command(name='startEventArchival')
    async def startEventArchival(ctx):
        global eventArchivalInProcess
        try:
            if(not eventArchivalInProcess):
                await ctx.message.channel.send("Now starting event archival process.")
                eventArchivalInProcess=True;
                print("event routine 2.1")
                channel = bot.get_channel(redacted)
                jamchanid = redacted
                
                headerData = {
                    'Authorization': 'redacted'
                }
                      
                messages = await channel.history(limit=20).flatten()
                       
                requestChannelEvents = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events?country_code=US&payment_source_id=redacted&with_user_count=true', headers = headerData)
                print("event routine 2.2")
                if(len(requestChannelEvents.json()) > 0):
                    for x in requestChannelEvents.json():
                        await asyncio.sleep(2)
                        
                        date = dateutil.parser.parse(x["scheduled_start_time"])
                        #datePlus30Minutes = date + timedelta(minutes=30)
                        
                        #now = datetime.now()
                        
                        #print(now.strftime("%Y-%m-%d %H:%M:%S"))
                        #print(datePlus30Minutes.strftime("%Y-%m-%d %H:%M:%S"))
                        
                        if(x["status"] == 2):
                            print ("Event Is Occuring")
                            messageAlreadyPosted = False
                            print("event routine 2.3")
                            for msg in messages:
                                if("Event ID: " in msg.content):
                                    eventID = msg.content.split("Event ID: ")
                                    if(eventID[1] == x['id']):
                                        print ("Event Already Exists")
                                        messageAlreadyPosted = True
                                        
                            if(messageAlreadyPosted == False):
                                print ("Event Does Not Exist")
                                guild = bot.get_guild(GUILD)
                                user = guild.get_member(int(x["creator"]["id"]))
                                avatar = user.avatar_url
                                author = x["creator"]["username"]
                                
                                img_data = requests.get(avatar).content
                                with open('avatarEvent.webp', 'wb') as handler:
                                    handler.write(img_data)
                                    
                                img = Image.open("avatarEvent.webp")
                                rgb = get_dominant_color(img)
                                
                                embed=discord.Embed(color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]))
                                embed.set_author(name=author+" Hosted", icon_url=avatar)
                                embed.add_field(name="**Event**", value=x["name"], inline=False)
                                embed.add_field(name="**Date**", value=date.strftime("%B %d, %Y"), inline=False)
                                embed.add_field(name="**Description**", value=x["description"], inline=False)
                                
                                if(not(x["id"] is None or x["image"] is None)):
                                    imageLink = "https://cdn.discordapp.com/guild-events/"+x["id"]+"/"+x["image"]+"?size=4096"
                                    embed.set_image(url=imageLink)
            
                                await channel.send("Event ID: "+ x['id'])
                                await channel.send(embed=embed)
                                latestMessage = (await channel.history(limit=1).flatten())[0]
                await ctx.message.channel.send("Event archival process has been completed")    
                eventArchivalInProcess=False;
                
            else:
                await ctx.message.channel.send("Event archival process is in progress please wait until it has finished.")
            
        except Exception as e:
            await botError(ctx)
            print(e)
            print("Bot ran into an issue")
            
async def previousEventRoutine(bot):
    global eventArchivalInProcess
    while True:
        try:
            await asyncio.sleep(700)
            if(not eventArchivalInProcess):
                eventArchivalInProcess=True;
                print("event routine 2.1")
                channel = bot.get_channel(redacted)
                jamchanid = redacted
                
                headerData = {
                    'Authorization': 'redacted'
                }
                      
                messages = await channel.history(limit=20).flatten()
                       
                requestChannelEvents = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events?country_code=US&payment_source_id=redacted&with_user_count=true', headers = headerData)
                print("event routine 2.2")
                if(len(requestChannelEvents.json()) > 0):
                    for x in requestChannelEvents.json():
                        await asyncio.sleep(2)
                        
                        date = dateutil.parser.parse(x["scheduled_start_time"])
                        #datePlus30Minutes = date + timedelta(minutes=30)
                        
                        #now = datetime.now()
                        
                        #print(now.strftime("%Y-%m-%d %H:%M:%S"))
                        #print(datePlus30Minutes.strftime("%Y-%m-%d %H:%M:%S"))
                        
                        if(x["status"] == 2):
                            print ("Event Is Occuring")
                            messageAlreadyPosted = False
                            print("event routine 2.3")
                            for msg in messages:
                                if("Event ID: " in msg.content):
                                    eventID = msg.content.split("Event ID: ")
                                    if(eventID[1] == x['id']):
                                        print ("Event Already Exists")
                                        messageAlreadyPosted = True
                                        
                            if(messageAlreadyPosted == False):
                                print ("Event Does Not Exist")
                                guild = bot.get_guild(GUILD)
                                user = guild.get_member(int(x["creator"]["id"]))
                                avatar = user.avatar_url
                                author = x["creator"]["username"]
                                
                                img_data = requests.get(avatar).content
                                with open('avatarEvent.webp', 'wb') as handler:
                                    handler.write(img_data)
                                    
                                img = Image.open("avatarEvent.webp")
                                rgb = get_dominant_color(img)
                                
                                embed=discord.Embed(color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]))
                                embed.set_author(name=author+" Hosted", icon_url=avatar)
                                embed.add_field(name="**Event**", value=x["name"], inline=False)
                                embed.add_field(name="**Date**", value=date.strftime("%B %d, %Y"), inline=False)
                                embed.add_field(name="**Description**", value=x["description"], inline=False)
                                
                                if(not(x["id"] is None or x["image"] is None)):
                                    imageLink = "https://cdn.discordapp.com/guild-events/"+x["id"]+"/"+x["image"]+"?size=4096"
                                    embed.set_image(url=imageLink)
            
                                await channel.send("Event ID: "+ x['id'])
                                await channel.send(embed=embed)
                                latestMessage = (await channel.history(limit=1).flatten())[0]
                eventArchivalInProcess=False;
                
        except Exception as e:
            print(e)
            print("Bot ran into an issue")
            eventArchivalInProcess=False;
            
async def pingEventRoutine(bot):
    while True:
        try:
            await asyncio.sleep(300)

            print("event routine 3.1")
            channel = bot.get_channel(redacted)
            jamchanid = redacted
            
            headerData = {
                'Authorization': 'redacted'
            }
                   
            requestChannelEvents = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events?country_code=US&payment_source_id=redacted&with_user_count=true', headers = headerData)
            print("event routine 3.2")
            if(len(requestChannelEvents.json()) > 0):
                for x in requestChannelEvents.json():
                    await asyncio.sleep(2)
                    eventDate = dateutil.parser.parse(x["scheduled_start_time"])
                    now = utc.localize(datetime.utcnow())
                    
                    eventDateMinus15Minutes = eventDate - timedelta(minutes=20)
                    
                    if(isNowInTimePeriod(eventDateMinus15Minutes, eventDate, now)):
                        eventAlreadyPosted = False
                        for tempEventId in alreadyPingedEventIDs:
                            if(tempEventId == x["id"]):
                                eventAlreadyPosted = True
                                
                        if(eventAlreadyPosted):
                            print("event already pinged")
                        else:
                            print("event not already pinged")
                            alreadyPingedEventIDs.append(x["id"])
                            alreadyPingedEventIDs.pop(0)
                            print(alreadyPingedEventIDs)
                            
                            minutes_diff = "in " + str(int((eventDate - now).total_seconds() / 60)) + " minutes"
                            if(int((eventDate - now).total_seconds() / 60) < 1):
                                minutes_diff = "now"
                                
                            requestEvent = requests.get('https://discord.com/api/v9/guilds/redacted/scheduled-events/'+x["id"]+'/users?limit=100&with_member=true', headers = headerData)
                            userNameArray = []
                            userIdArray = []
                            for y in requestEvent.json():
                                if(len(requestEvent.json()) > 0):
                                    userNameArray.append(y["user"]["username"])
                                    userIdArray.append(y["user"]["id"])
                            
                            userPingIDs = ""
                            for tempUserID in userIdArray:
                                userPingIDs = userPingIDs + "<@"+tempUserID+">"+ ", ";
                                
                            userPingIDs = userPingIDs[0:-2]
                            
                            print(userPingIDs+"\n"+x["name"]+" starts "+minutes_diff)
                            await channel.send(x["name"]+" starts "+minutes_diff+"\n<@&redacted>, "+userPingIDs)
                        
                    else:
                        print("Do not ping")
                    

        except Exception as e:
            print(e)
            print("event ping ran into an issue") 
        
def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 
            
async def botError(ctx):
    embed=discord.Embed(color=discord.Color(11812188))
    await ctx.message.channel.send("Bot ran into an issue...")
    await ctx.message.channel.send(embed=embed)
    
async def botError2(ctx, errorJam):
    embed=discord.Embed(color=discord.Color(11812188))
    await ctx.message.channel.send(errorJam)
    await ctx.message.channel.send(embed=embed)
    
def find_options(message, options):
    # first index of the first character of the option
    first = message.find('[') + 1
    # index of the last character of the title
    last = message.find(']')
    if (first == 0 or last == -1):
        return options
    options.append(message[first:last])
    message = message[last+1:]
    return find_options(message, options)

def find_options_2(message, options):
    if(message.find('[') == -1):
        messageArray = message.split(" ")
        messageArray.remove(messageArray[0])
        return messageArray
    else:
        # first index of the first character of the option
        first = message.find('[') + 1
        # index of the last character of the title
        last = message.find(']')
        if (first == 0 or last == -1):
            return options
        options.append(message[first:last])
        message = message[last+1:]
        return find_options(message, options)
    
def get_dominant_color(pil_img, palette_size=16):
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    return dominant_color