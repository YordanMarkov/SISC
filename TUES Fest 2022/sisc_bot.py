import discord
from discord.ext import commands, tasks
import os
import time

TOKEN = 'SECRET' # Personal information
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


CAMERA_FILE = "/home/pi/SISC/analyzed_camera_snapshot.jpg"
  
@client.event
async def on_ready():
    print("Bot is ready.") # Console information
    background_task.start()

@client.command()
async def help(ctx):
    await ctx.send('*-=* **SISC** *=-* \n \* !help - Shows this message. \n \* !pic - Takes an instant picture. \n \* !start - Starts SISC. \n \* !stop - Stops SISC.')

@client.command()
async def start(ctx):
    os.system("systemctl start sisc.service")
    await ctx.send('SISC has started.')


@client.command()
async def stop(ctx):
    os.system("systemctl stop sisc.service")
    await ctx.send('SISC has stopped.')
 
@client.command()
async def pic(ctx):
    os.system("python3 /home/pi/SISC/quick_scan.py")
    await ctx.send('Taking a picture...')

@tasks.loop(seconds=5)
async def background_task():
    if os.path.exists('/home/pi/SISC/message.txt') and os.path.exists(CAMERA_FILE):
        message = open('/home/pi/SISC/message.txt').read()
        user = client.get_user('SECRET') # Personal information
        await user.send(message, file=discord.File(CAMERA_FILE))
        os.remove(CAMERA_FILE)
        os.remove('/home/pi/SISC/message.txt')
    if os.path.exists('/home/pi/SISC/pic.txt') and os.path.exists('/home/pi/SISC/pic.jpg'):
        message = open('/home/pi/SISC/pic.txt').read()
        user = client.get_user(283145272639488000)
        await user.send(message, file=discord.File('/home/pi/SISC/pic.jpg'))
        os.remove('/home/pi/SISC/pic.jpg')
        os.remove('/home/pi/SISC/pic.txt')

client.run(TOKEN)