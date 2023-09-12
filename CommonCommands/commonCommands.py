import discord

from CommonCommands.StrawPoll import strawpollfunctions
from CommonCommands.PickRandom import pickrandomfunctions
from CommonCommands.MovieAPI import movieapifunctions
from CommonCommands.PinArchive import pinarchive
from CommonCommands.Dictionary import dictionaryfunctions
import requests
import random

async def setupCommands(bot):
    @bot.command(name='strawPoll')
    async def makeStrawpoll(ctx):    
        await strawpollfunctions.makeStrawpoll(ctx, bot)
        
    @bot.command(name='pickRandom')
    async def pickRandom(ctx):   
        await pickrandomfunctions.pickRandom(ctx, bot)
        
    @bot.command(name='getMedia')
    async def findmedia(ctx):   
        await movieapifunctions.mediaSearch(ctx, bot)
        
    @bot.command(name='pin')
    async def findmedia(ctx):   
        await pinarchive.pinMessage(ctx, bot)
        
    @bot.command(name='getMediaIndex')
    async def findmediaid(ctx):   
        await movieapifunctions.findMediaID(ctx, bot)
        
    @bot.command(name='getCredits')
    async def findcredits(ctx):   
        await movieapifunctions.getCredits(ctx)
        
    @bot.command(name='getTrailer')
    async def findtrailer(ctx):   
        await movieapifunctions.getTrailer(ctx)
    
    @bot.command(name='getStreamSites')
    async def findstreamingsites(ctx):   
        await movieapifunctions.getStreamSites(ctx)
        
    @bot.command(name='randomMovie')
    async def randommovie(ctx):   
        await movieapifunctions.getMovieInfoRandom(ctx)
        
    @bot.command(name='randomMopie')
    async def randommopie(ctx):
        if(ctx.message.author.id == redacted):
            await movieapifunctions.getMovieInfoRandom(ctx)
        else:
            await ctx.message.channel.send('')
        
    @bot.command(name='define')
    async def define(ctx):   
        await dictionaryfunctions.define(ctx, bot)
        
    @bot.command(name='synonym')
    async def wordLike(ctx):   
        await dictionaryfunctions.theasaurus(ctx, bot)
    
    @bot.command(name='flip')
    async def makeStrawpoll(ctx):    
        await pickrandomfunctions.flipCoin(ctx, bot)

    @bot.command(name='flipTable')
    async def flipTable(ctx):   
        await ctx.message.channel.send('(╯°□°)╯︵ ┻━┻')
        
    @bot.command(name='putTableBack')
    async def putTableBack(ctx):   
        await ctx.message.channel.send('┬─┬ノ( º _ ºノ)')
        
    @bot.command(name='talk')
    async def talk(ctx):
        if(ctx.message.author.id == redacted):
            message = ctx.message.clean_content
            headerData = {
                'Content-Type': 'application/json'
            }
            options = find_options(message, [])
            
            splitmessage = options[1].split("/")
            guildid = splitmessage[4]
            channelid = splitmessage[5]
            messageid = splitmessage[6]
            
            channel = bot.get_channel(int(channelid))
            await channel.send(options[0])
        else:
            await ctx.message.channel.send("")
        
    @bot.command(name='reply')
    async def reply(ctx):
        if(ctx.message.author.id == redacted):
            message = ctx.message.clean_content
            headerData = {
                'Content-Type': 'application/json'
            }
            options = find_options(message, [])
            splitmessage = options[1].split("/")
            
            guildid = splitmessage[4]
            channelid = splitmessage[5]
            messageid = splitmessage[6]
            
            channel = bot.get_channel(int(channelid))
            message = await channel.fetch_message(int(messageid))
            
            await message.channel.send(options[0], reference=message)
        else:
            await ctx.message.channel.send("")
        
    @bot.command(name='commandsMarmalade')
    async def commandListMarmalade(ctx):
        await ctx.message.channel.send(embed=await buildMarmaldeEmbed())
    
    @bot.command(name='commands')
    async def commandList(ctx):
        await ctx.message.channel.send("Here are my list of commands. if you see an optional parameter you can either include it or not. For example in get media these are both valid uses !getMedia [django], !getMedia [django] [1]")
        await ctx.message.channel.send(embed=await buildEventCommands())
        await ctx.message.channel.send(embed=await buildRoleCommands())
        await ctx.message.channel.send(embed=await buildNameColorCommands())
        await ctx.message.channel.send(embed=await buildMovieDBCommands())
        await ctx.message.channel.send(embed=await buildDecideCommands())
        await ctx.message.channel.send(embed=await buildDictionaryCommands())
        await ctx.message.channel.send(embed=await buildEntertainCommands())
        await ctx.message.channel.send(embed=await buildLynchCommands())
        await ctx.message.channel.send(embed=await buildOtherCommands())

    @bot.command(name='updateCommands')
    async def updateCommands(ctx):
        channel = bot.get_channel(934226056997654559)
        await channel.purge(limit=15)
        await channel.send("Here are my list of commands. if you see an optional parameter you can either include it or not. For example in get media these are both valid uses !getMedia [django], !getMedia [django] [1]")
        await channel.send(embed=await buildEventCommands())
        await channel.send(embed=await buildRoleCommands())
        await channel.send(embed=await buildNameColorCommands())
        await channel.send(embed=await buildMovieDBCommands())
        await channel.send(embed=await buildDecideCommands())
        await channel.send(embed=await buildDictionaryCommands())
        await channel.send(embed=await buildEntertainCommands())
        await channel.send(embed=await buildLynchCommands())
        await channel.send(embed=await buildOtherCommands())
        await channel.send(embed=await buildMarmaldeEmbed())
        

    async def buildMarmaldeEmbed():  
        marEmbed = discord.Embed(
            description="Here are my list of commands.",
            color=discord.Color(12021036))
        
        marEmbed.set_author(name="Marmalade Command List", icon_url="https://cdn.discordapp.com/avatars/redacted/c7ab51219dd1aea0ea7569813cfadc5c.webp?size=160")
        marEmbed.add_field(name="**!guess guess**", value="Lets you play competitive wordle with friends! Just guess a 5 letter word and away you go!", inline=False)
        marEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return marEmbed
    
    async def buildEventCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Event Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!pingForEvent [event ID] [optional custom message]**", value="Ping everyone for an event along with how much longer till the event. This will not ping movie nights like the auto ping does. You can grab the event ID by using discord dev tools or by using the !getEventIDs command You can also use a custom message by adding in the last parameter.", inline=False)
        jamEmbed.add_field(name="**!pingForEventWithMovieNights [event ID] [optional custom message]**", value="Ping everyone for an event along with how much longer till the event. This will ping movie nights like the auto ping does. You can grab the event ID by using discord dev tools or by using the !getEventIDs command You can also use a custom message by adding in the last parameter.", inline=False)
        jamEmbed.add_field(name="**!getEventIDs**", value="Grab event IDs for all events in the server", inline=False)
        jamEmbed.add_field(name="**!cancelAutoEventPing [event ID]**", value="Cancel auto ping for event that happens 5 to 15 min before an event takes place, this is experimental functionality and may not work under certain circumstances. This is reccomended only to be used the same day an event takes place because it can be wiped out by other event pings or the bot being restarted.", inline=False)
        jamEmbed.add_field(name="**!seeAutoEventPing**", value="See events that will no longer auto ping.", inline=False)
        jamEmbed.add_field(name="**!startEventArchival**", value="Start event archival process that usually runs every few minutes. You may get an error message if it is already being run via the routine or someone else used this command recently.", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildRoleCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Role Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!addMovieNights**", value="Gives you the movie nights role.", inline=False)
        jamEmbed.add_field(name="**!removeMovieNights**", value="Removes the movie nights role.", inline=False)
        jamEmbed.add_field(name="**!addMinecraftRole**", value="Gives you the minecraft role.", inline=False)
        jamEmbed.add_field(name="**!removeMinecraftRole**", value="Removes the minecraft role.", inline=False)
        jamEmbed.add_field(name="**!addGarlicGamers**", value="Gives you the gartic gamers role.", inline=False)
        jamEmbed.add_field(name="**!removeGarlicGamers**", value="Removes the gartic gamers role.", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildNameColorCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Name Color Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        
        colorRoleArrayNames = ''
        guildObj = bot.get_guild(redacted)

        for color in guildObj.roles:
            if(color.name[:5] == 'Color'):
                colorRoleArrayNames = colorRoleArrayNames + color.name[6:] + ', '
                
        jamEmbed.add_field(name="**!changeNameColor [color]**", value="Change the color of your username. List of colors are " +colorRoleArrayNames[:len(colorRoleArrayNames)-2], inline=False)
        jamEmbed.add_field(name="**!removeNameColor**", value="Removes all color roles from your username.", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildMovieDBCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Movie DB Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!getMedia [title/persons name] [optional index]**", value="Multisearch function for movies, tv, and actors/actresses. If you want a specific index use !findMediaIndex to get it.", inline=False)
        jamEmbed.add_field(name="**!getCredits [movie title] [optional index]**", value="Gets movie credits for a specific movie. If you want a specific index use !findMediaIndex to get it.", inline=False)
        jamEmbed.add_field(name="**!getTrailer [movie title] [optional index]**", value="Gets a random movie trailer for a specific movie. If you want a specific index use !findMediaIndex to get it.", inline=False)
        jamEmbed.add_field(name="**!getStreamSites [movie title] [2 letter country code ie US] [optional index]**", value="Shows all the places you can either stream, rent, or buy the movie. If you want a specific index use !findMediaIndex to get it.", inline=False)
        jamEmbed.add_field(name="**!getMediaIndex [title/persons name]**", value="If you cant find the media information you are looking for you can use this function to get the index and input it into the index field in !findMedia.", inline=False)
        jamEmbed.add_field(name="**!randomMovie**", value="Picks a random movie to watch.", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildDecideCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Decide Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!strawPoll {title} [Option1] [Option2] [Option3]**", value="Creates a strawpoll with as many options as you want. 2 is the minimum.", inline=False)
        jamEmbed.add_field(name="**!pickRandom [Option1] [Option2] [Option3]**", value="Choses a random option using as many options as you want. 2 is the minimum.", inline=False)
        jamEmbed.add_field(name="**!flip [Option1]**", value="Use heads, tails, head, tail, h, or t. Flip a coin, test your fate.....", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildDictionaryCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Dictionary Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!define [Option1]**", value="Get definition of a word.", inline=False)
        jamEmbed.add_field(name="**!synonym [Option1]**", value="Get a word similar to the one you provided.", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildEntertainCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Entertain Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!joke**", value="Tell a tame joke!", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildLynchCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Lynch Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!getReal**", value="Watching movies on your telephone....", inline=False)
        jamEmbed.add_field(name="**!lynchWeather**", value="Posts the latest weather report from the david lynch youtube channel.", inline=False)
        jamEmbed.add_field(name="**!lynchNumber**", value="Posts the latest number of the day from the david lynch youtube channel.", inline=False)
        jamEmbed.add_field(name="**!lynch**", value="Posts the latest number of the day and weather vid from the david lynch youtube channel.", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def buildOtherCommands():
        jamEmbed = discord.Embed(color=discord.Color(11812188))
        
        jamEmbed.set_author(name="Other Commands", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        jamEmbed.add_field(name="**!pickRandomProfGang**", value="Picks random user from prof gang role. Only works for akira", inline=False)
        jamEmbed.add_field(name="**!updateCommands**", value="Updates the bot commands channel with any new commands.", inline=False)
        jamEmbed.add_field(name="**!flipTable**", value="(╯°□°)╯︵ ┻━┻", inline=False)
        jamEmbed.add_field(name="**!putTableBack**", value="┬─┬ノ( º _ ºノ)", inline=False)
        jamEmbed.add_field(name="**!getReal**", value="Watching movies on your telephone....", inline=False)
        jamEmbed.set_footer(text="\n‎                                                                                                                                ‎                                                       ‎                                     \n")
        
        return jamEmbed
    
    async def botError(ctx):
        embed=discord.Embed(color=discord.Color(11812188))
        await ctx.message.channel.send("Bot ran into an issue...")
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
        
