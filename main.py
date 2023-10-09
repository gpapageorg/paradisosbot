import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

urlMain = "https://www2.radioparadise.com/rp3-mx.php?n=Music&f=songinfo&song_id=now"

# Intiialize Bot
load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

tokenFile = open("token", "r")
TOKEN = tokenFile.read()

#Play command
@bot.command(name='p', help='To play song')
async def play(ctx, mix):
    global mixString 
    mixString = "Main" if mix=="main" else "Rock"

    if not ctx.message.author.voice:
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        
        if(mix == "main"):
        
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio('https://stream.radioparadise.com/flacm'))
            await ctx.send('**You Are Listening To The Main Mix On Radio Paradise, Thank You For Tuning In**')

        elif(mix == "rock"):
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio('https://stream.radioparadise.com/rock-flac'))
            await ctx.send('**Rock Mix**')

    except:
        await ctx.send("The bot is not connected to a voice channel.")

#Join Command Disabled For now as implemented auto join
#@bot.command(name='j', help='Tells the bot to join the voice channel')
#async def join(ctx):
#    if not ctx.message.author.voice:
#        return
#    else:
#        channel = ctx.message.author.voice.channel
#    await channel.connect()

#Info Now Playing Command
@bot.command(name='np')
async def np(ctx):
    voice_client = ctx.message.guild.voice_client
    html_content = requests.get(urlMain).text

    soup = BeautifulSoup(html_content, 'html.parser') 

    div_bs4 = soup.find('div', id = "title").get_text() 
    info = (div_bs4.strip()).split('\n')
    info[1] = info[1].replace('\r','')

    if voice_client.is_connected() and mixString == 'Main':
        await ctx.send("**Now Playing**")
        await ctx.send("**Mix:** {}".format(mixString))
        await ctx.send("**Title: **"  + info[0])
        await ctx.send("**Artist: **" + info[1])
        await ctx.send("**Album: **" + info[2])
    elif voice_client.is_connected() and mixString == 'Rock':
        await ctx.send("Data Not Available For Rock Mix")
    else:
        pass

#Leave Commad
@bot.command(name='l', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

#Initialization Message
@bot.event
async def on_ready():
    print('Running!')
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await channel.send('Bot Activated!')
        print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))


bot.run(TOKEN)
