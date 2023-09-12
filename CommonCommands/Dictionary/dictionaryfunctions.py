import discord
import requests
import random

API_TOKEN_DICTIONARY = 'redacted'
API_TOKEN_THEASAURAS = 'redacted'

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


async def define(ctx, bot):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    try:
        request = requests.get('https://www.dictionaryapi.com/api/v3/references/collegiate/json/'+options[0]+'?key='+API_TOKEN_DICTIONARY, headers = headerData)
        definitionsInfo = request.json()
        #examplesInfo = request.json()[0]["suppl"]["examples"]
        print(str(definitionsInfo))
        #print(str(examplesInfo))

        returnText = ""
        count = 1
        for x in definitionsInfo:
            for y in x["shortdef"]:
                if(not(len(returnText) > 1900)):
                    returnText = returnText + "**Definition " + str(count) + ": **" + y + "\n"
                    count = count + 1
            
        embed=discord.Embed(color=discord.Color(11812188), description=returnText)
        embed.set_author(name="Bot Definitions", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        #embed.add_field(name="Definitions", value="\u200B", inline=False)

        await ctx.message.channel.send("Here are your definitions you cutie <3")
        await ctx.message.channel.send(embed=embed)
            
    except Exception:
        await botError(ctx, "Bot couldnt find the word!")
        return "Something wrong with define function"

async def theasaurus(ctx, bot):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    try:
        request = requests.get('https://www.dictionaryapi.com/api/v3/references/thesaurus/json/'+options[0]+'?key='+API_TOKEN_THEASAURAS, headers = headerData)
        definitionsInfo = request.json()
        #examplesInfo = request.json()[0]["suppl"]["examples"]
        print(str(definitionsInfo))
        #print(str(examplesInfo))

        returnText = "**Synonyms: **"
        count = 1
        for x in definitionsInfo:
            for y in x["meta"]["syns"][0]:
                if(not(len(returnText) > 1900)):
                    returnText = returnText + y + ", "
                    count = count + 1
            
        embed=discord.Embed(color=discord.Color(11812188), description=returnText[0:len(returnText)-2])
        embed.set_author(name="Bot Definitions", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        #embed.add_field(name="Definitions", value="\u200B", inline=False)

        await ctx.message.channel.send("Here are your synonyms you cutie <3")
        await ctx.message.channel.send(embed=embed)
            
    except Exception:
        await botError(ctx, "Bot couldnt find the word!")
        return "Something wrong with define function"
    
async def botError(ctx, errorJam):
    embed=discord.Embed(color=discord.Color(11812188))
    await ctx.message.channel.send(errorJam)
    await ctx.message.channel.send(embed=embed)

