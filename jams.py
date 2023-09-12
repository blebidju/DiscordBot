# bot.py
import os
import discord

from ServerSpecificFunctions.Test import testServer
from ServerSpecificFunctions.JAMS import jamsServer

from ServerSpecificFunctions.Test import testCommands
from ServerSpecificFunctions.JAMS import jamsCommands
from CommonCommands import commonCommands

from discord.ext import commands
from dotenv import load_dotenv

#import urllib.request
from PIL import Image
import requests

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
count = 0
pincount = 0
insultcount = 0
#jamsCommands.setupCommands();

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await testCommands.setupCommands(bot);
    await jamsCommands.setupCommands(bot);
    await commonCommands.setupCommands(bot);
    
@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    
    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name="Mods")
    member = guild.get_member(payload.user_id)
    
    if role in member.roles:
        if str(payload.emoji) == '📌':
            await doesPinMessageExistThenPin(bot, message)
    
@bot.event   
async def on_member_join(member):
    server = await pick_correct_server_by_member(member)
    await server.member_join(member, bot)

@bot.event
async def on_message(message):
    global insultcount

    if message.content[0] == "!":
        randomInsult = random.randint(0, 500)
        insultcount = insultcount + 1
        if(randomInsult == 1 or insultcount > 300):
            insults = []
            
            await message.reply(random.choice(insults))
            insultcount = 0
        else:
            await bot.process_commands(message)
    
    announcementsChannelID = redacted
    movieNightsRoleID = "<@&redacted>"
    evenPingsRoleID = "<@&redacted>"
    minecraftPingsRoleID = "<@&redacted>"

    channel = bot.get_channel(announcementsChannelID)
    
    author = message.author.name
    messageText = message.content
    avatar = message.author.avatar_url
    returnText = "**" +messageText+"**"
     
    #urllib.request.urlretrieve(avatar, "local-filename.webp")
    img_data = requests.get(avatar).content
    with open('avatar.webp', 'wb') as handler:
        handler.write(img_data)
        
    img = Image.open("avatar.webp")
    rgb = get_dominant_color(img)
    
    if movieNightsRoleID in messageText:
        embed=discord.Embed(color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]), description=returnText)
        embed.set_author(name=author+" Announced", icon_url=avatar, url=message.jump_url)
        await channel.send(embed=embed)
        
    if evenPingsRoleID in messageText:
        embed=discord.Embed(color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]), description=returnText)
        embed.set_author(name=author+" Announced", icon_url=avatar, url=message.jump_url)
        await channel.send(embed=embed)
        
    if minecraftPingsRoleID in messageText:
        embed=discord.Embed(color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]), description=returnText)
        embed.set_author(name=author+" Announced", icon_url=avatar, url=message.jump_url)
        await channel.send(embed=embed)
    
    global count
    
    random1 = 0
    if message.author.id != redacted:
        count = count + 1
        random1 = random.randint(0, 1000)
        #print('random number 1')
        #print(random1)
    
    if(random1 == 1 or count > 1000):
        count = 0
        
        random2 = random.randint(0, 5)
        #print('random number 2')
        #print(random2)
        
        if(random2 == 0):
            await message.add_reaction(redacted)
        elif(random2 == 1):
            await message.add_reaction(redacted)
        elif(random2 == 2):
            await message.add_reaction(redacted)
        elif(random2 == 3):
            await message.add_reaction(redacted)
        elif(random2 == 4):
            await message.add_reaction(redacted)
        elif(random2 == 5):
            await message.add_reaction(redacted)
    
    randomPin = random.randint(0, 70000)
    
    global pincount
    
    pincount = pincount + 1
    if(randomPin == 1 or pincount > 70000):
        if message.author != bot.user:
            pincount = 0
            await message.add_reaction('📌')
        else:
            pincount = 100001

async def doesPinMessageExistThenPin(bot, message):
    pinChannelID = redacted;
    channel = bot.get_channel(pinChannelID)
    
    if str(message.channel.id) != str(pinChannelID):
        messages = await channel.history(limit=99999).flatten()
        messageAlreadyPosted = False
        
        for msg in messages:
            if msg.embeds:
                if(msg.embeds[0].author.url == 'https://discord.com/channels/{0}/{1}/{2}'.format(message.guild.id, message.channel.id, message.id)):
                    print ("Message Exists So Do Not Pin")
                    messageAlreadyPosted = True
                    
        if not messageAlreadyPosted:
            print ("Message Does Not Exist So Pin")
            await pinMessageForReal(bot, message)
    
async def pinMessageForReal(bot, message):
    headers = ["https://cdn.discordapp.com/attachments/redacted/redacted/redacted.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/unknown.png","https://cdn.discordapp.com/attachments/redacted/redacted/unknown.png","https://cdn.discordapp.com/attachments/redacted/redacted/space1.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/space2.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/space3.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/space4.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/space5.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/space6.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/space7.png?size=4096","https://cdn.discordapp.com/attachments/redacted/redacted/space8.png?size=4096"]
    
    """Forwards a message to the archive channel."""
    pinChannelID = redacted;
    channel = bot.get_channel(pinChannelID)
    
    avatar = message.author.avatar_url
     
    #urllib.request.urlretrieve(avatar, "local-filename.webp")
    img_data = requests.get(avatar).content
    with open('avatar.webp', 'wb') as handler:
        handler.write(img_data)
        
    img = Image.open("avatar.webp")
    rgb = get_dominant_color(img)
    
    try:
        await channel.send(random.choice (headers))
        
        name = message.author.display_name 
        avatar = message.author.avatar_url
        pin_content = message.content
        server = message.guild.id 
        
        emb = discord.Embed( 
            description=pin_content, 
            color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]))  # Initalizes embed with description pin_content. 
        emb.set_author( 
            name=name, 
            icon_url=avatar, 
            url='https://discord.com/channels/{0}/{1}/{2}'.format( 
                server, message.channel.id, message.id) 
            )  # Sets author and avatar url of the author of pinned message. 
 
        # Sets footer as the channel the message was sent and pinned in. 
        emb.set_footer(text='Sent in #{}'.format(message.channel)) 

        await channel.send(embed=emb)
        
        """if message.attachments:
            await channel.send('Attachments:')"""
        for attachments in message.attachments:
            await channel.send(attachments)
            
        
    except discord.errors.Forbidden: 
        print('Something went wrong')
    
async def pick_correct_server_by_member(member):
    print(member.guild.id)
    if member.guild.id == int(os.getenv('TEST_GUILD')):
        return testServer
    elif member.guild.id == int(os.getenv('JAMS_GUILD')):
        return jamsServer

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

bot.run(TOKEN)
