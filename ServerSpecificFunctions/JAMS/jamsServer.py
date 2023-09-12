import os
import discord

GUILD = redacted

async def member_join(member, bot):
    print(f'{member.name} has joined the server!')
    guild = bot.get_guild(GUILD)
    movieRole = discord.utils.get(guild.roles, name="movie nights")
    await member.add_roles(movieRole)
    
    
    
    
    