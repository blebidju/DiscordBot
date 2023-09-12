import discord
import random

def find_options(message, options):
    # first index of the first character of the option
    first = message.find('[') + 1
    # index of the last character of the title
    last = message.find(']')
    if (first == 0 or last == -1):
        if len(options) < 2:
            # TODO: Send a message telling the use how they are using it incorrectly.
            return "Not using the command correctly"
        else:
            return options
    options.append(message[first:last])
    message = message[last+1:]
    return find_options(message, options) 

def find_options_here(message, options):
    # first index of the first character of the option
    first = message.find('[') + 1
    # index of the last character of the title
    last = message.find(']')
    if (first == 0 or last == -1):
        return options
    options.append(message[first:last])
    message = message[last+1:]
    return find_options_here(message, options) 

async def pickRandom(ctx, bot):
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    embed=discord.Embed(color=discord.Color(11812188))
    embed.set_author(name="Bot Random Picker", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
    embed.add_field(name="**"+options[random.randint(0, len(options)-1)]+" wins!!!**", value="\u200B", inline=False)
    await ctx.message.channel.send(embed=embed)

async def flipCoin(ctx, bot):
    message = ctx.message.clean_content

    options = find_options_here(message, [])
    
    isHeads = random.randint(0, 1) 
    
    if(options[0].lower() == "h" or options[0].lower() == "t" or options[0].lower() == "heads" or options[0].lower() == "tails" or options[0].lower() == "tail" or options[0].lower() == "head"):
        if(isHeads == 1):
            print("flipped coin was heads")
            print("option was "+ options[0])
            await ctx.message.channel.send("Coin flip was heads.")
            if(options[0].lower() == "h" or options[0].lower() == "heads" or options[0].lower() == "head"):
                await ctx.message.channel.send("You flipped correctly!")
            
            else:
                await ctx.message.channel.send("You flipped incorrectly...")
        else:
            print("flipped coin was tails")
            print("option was "+ options[0])
            await ctx.message.channel.send("Coin flip was tails.")
            if(options[0].lower() == "t" or options[0].lower() == "tails" or options[0].lower() == "tail"):
                await ctx.message.channel.send("You flipped correctly!")
            else:
                await ctx.message.channel.send("You flipped incorrectly...")   
    else:
        await ctx.message.channel.send("Acceptable flips are heads, tails, head, tail, h, or t.")
            
    
    