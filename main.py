"""CTIH's Antigrief"""
import discord
from discord import commands
import config
import asyncio
import json

TOKEN = config.token
blocked_words = config.blocked_words
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

story = {}


@bot.event
async def on_ready():
    
    print(f"Logged in as {bot.user}")
    with open("channels.txt","r") as f:
        channels = f.readlines()
    for channel__ in channels:
        print(channel__)
        story[str(channel__.strip())] = ""
    while True:
        await asyncio.sleep(2)
        print(story)
@bot.event
async def on_message(message):
    user = message.author
    with open("channels.txt","r") as f:
        channels_ = f.readlines()
 
    if user.bot == True:
        return
    if f"{message.channel.id}\n" not in channels_:
        return
    if " " in message.content:
        await message.channel.send("Sinun pitää laittaa **yksi** **sana**")
        return
    story[str(message.channel.id)] += f"{str(message.content)} "


@bot.command(description="Adds a story channel.")
async def add_channel(ctx, channel_:discord.TextChannel):
    await ctx.respond(f"Added channel <#{channel_.id}>!")
    with open("channels.txt","a") as f:
        f.write(f"{channel_.id}\n")
    story[str(channel_.id)] = ""
        
        
@bot.command(description="Removes a story channel.")
async def remove_channel(ctx, channel_:discord.TextChannel):
    await ctx.respond(f"Removed channel <#{channel_.id}>!")
    with open("channels.txt","r") as f:
            channels = f.readlines()
    channels.remove(f"{channel_.id}\n")
    with open("channels.txt","w") as f:
        f.writelines(channels)
       
        
@bot.command(description="Displays the current story.")
async def story(ctx):
    await ctx.respond(story[str(ctx.channel.id)])    
    
async def create_properties(server_id):

    with open("server_settings.json","r") as f:
        settings = json.load(f)
    if str(server_id) in settings:
        return True
    else:
        settings[str(server_id)] = {}
        settings[str(server_id)]["allow_space"] = False
        with open("server_settings.json","w") as f:
            settings = json.dump(settings,f)
        return False
    
async def change_properties(server_id, setting, mode):
    create_properties(server_id=server_id)
    with open("server_settings.json","r") as f:
        settings = json.load(f)
    
    settings[str(server_id)][str(setting)] = bool(mode)
    with open("server_settings.json","w") as f:
        settings = json.dump(settings,f)

@bot.command(description="None")
async def allow_spaces(ctx,bool:bool):
    
    guild = ctx.guild.id
    print(guild)
    settings = await change_properties(server_id = guild,setting="allow_spaces",mode=True)
    print(settings)
bot.run(TOKEN)
