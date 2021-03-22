"""
certain commands havent been uploaded here yet due to high unstability or deprecation over the discord version, will be updated soon
1. On_message command has no ping monitoring yet
2. lock and unlock commands
"""

from time import sleep
import os
import discord
from discord.utils import get
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import sys
from datetime import date
import random
from discord import FFmpegPCMAudio #for audio output by connecting to the voice, not suggested and system specififc
#needs FFmpegPCMAudio to be downloaded and also needs the corresponding mp3 file in the downloaded form
from discord_slash import SlashCommand
from discord_slash.model import SlashContext
#the necessary import and dependencies can be found in requirements.txt
intents = discord.Intents().all()

TOKEN = "insert your token here"
#The bot can only access and understand the messages prefixed with '+'
bot = commands.Bot(command_prefix='+', intents=intents)

BOT_LOGS = 749473757843947671 #channel id of the logs channel
GOD = 718845827413442692 #user id of the GOD, to avoid powerful commands from being abused by others
@bot.event
async def on_ready():
    #greet in a channel on coming online
    onlineEmbed = discord.Embed(title = "I am back", color = 0x48bf91)
    await bot.get_channel(BOT_LOGS).send(embed = onlineEmbed)

@bot.event
async def on_member_remove(user):
    #send as soon as a user leaves server
    await bot.get_channel(BOT_LOGS).send(str(user.mention) +' just left.')

@bot.event
async def on_command_error(ctx, error):
    #error handling, in case of an error the error message will be put up in the channel
   await ctx.send("Exception raised")
   await ctx.send("```" + str(error) + "```")


@bot.command(aliases = ['ping', 'Ping'])
async def _ping(ctx):
    string = 'Pong!!!\nPing = 69.420ms'
    await ctx.send(string)


@bot.command(aliases = ['list'])
async def listing(ctx, *roleName):
    #to generate a file of all people with a particular role
    #syntax - `+list GOD` -> generates a file of all user with rolename GOD

    #NOTE - this generates a file in the place of hosting, so running from server will generate there and will not be sent
    if ctx.message.author.id == GOD:
        roleName = ' '.join(roleName)
        thisRole = discord.utils.get(ctx.guild.roles, name=roleName)
        file = open('list.csv', 'w')
        for guild in bot.guilds:
            await ctx.send(str(guild))
            for member in guild.members:
                try:
                    if thisRole in member.roles:
                        file.write(member.name + ',' + str(member.id) + '\n')
                except UnicodeEncodeError as E:
                    #exisatnce of emojis/noisy characters/obscure languages affects the code 
                    #and such files wont be compatible in all file readers, so we skip such names
                    await ctx.send(member.name + 'is someone whose name has a non utf-8 character')
                    continue
        await ctx.send("done")
    else:
        await ctx.send("You dont even know what this command is, stfu")

@bot.command(aliases = ['contribute'])
async def _support(ctx, *params):
    Embeds = discord.Embed(title="Contributions", color=0x00ff00)
    Embeds.add_field(name="Github repo", value="https://github.com/ArvindAROO/J.A.R.V.I.S",inline = False)
    await ctx.send(embed=Embeds)

@bot.command(aliases = ['c', 'count'])
async def _count(ctx, *roleName):
    #syntax - `+c GOD & mod` returns the count of members having role 'GOD' and 'mod
    roleName = ' '.join(roleName)
    #convert it back into string and split it at '&' and strip the individual roles
    try:
        roleName = roleName.split('&')
    except:
        pass
    temp = []
    for i in roleName:
        temp.append(i.strip())
    roleName = temp
    await ctx.send("Got request for role " + str(roleName))
    #A command to get number of users in a role
    if roleName == ['']:
        for guild in bot.guilds:
            await ctx.send("We have {} people here, wow!!".format(len(guild.members)))
    else:
        thisRole = []
        #make a list of all roles in terms of role-id
        for roles in roleName:
            thisRole.append(discord.utils.get(ctx.guild.roles, name=roles))
        for guild in bot.guilds:
            await ctx.send("Currently in "+str(guild))
            count = 0
            for member in guild.members:
                boolean = True
                #bool will be true only if all the roles passed as args are present
                for roles in thisRole:
                    if roles not in member.roles:
                        boolean = False
                if boolean:    
                    count += 1
        await ctx.send(str(count) + " people has role " + str(thisRole))

@bot.command(aliases = ['l'])
async def leave(ctx):
    #command to make the bot leave the VC, deprecated and not suggested
    channel = ctx.message.author.voice.channel
    try:
        voice = await channel.connect()
        await voice.disconnect()
    except Exception as E:
        await ctx.send("Got exception" + str(E))
    await channel.disconnect()

@bot.command(aliases = ['TruePing', 'trueping', 'tp'])
async def true_ping(ctx):
    #generate the actual ping of the bot
    await ctx.send("Ping is " + str(round(bot.latency * 1000)) + "ms")
	
@bot.command(aliases = ['sayit'])
async def pingeveryone(ctx):
    #A function to mention @everyone
    if ctx.message.author.id == GOD:
        await ctx.send("@everyone")
    else:
        await ctx.send("You dont have access to this command" )

@bot.command(aliases = ['Spam'])
async def spam(ctx, user: discord.Member,count):
    #syntax - `+Spam @Stark 20` pings 20 times
    #spam function to spam ping someone as many times as required
    if ctx.message.author.id == GOD:
        for i in range(int(count)):
            await ctx.send(user.mention)
    else:
        await ctx.send("Nah")

@bot.command(aliases = ['e', 'echo'])
async def _echo(ctx, channel,*message):
    #! still under testing, doesnt workas reply for other channels becase the ctx(context) object has info about only current channel
    #syntax - without reply - `+e #channelname whatever msg` -> just echoes whatever you have said
    #with reply - currently works only in the same channel - `+e #channelname msg <message id as int>` - send the message as a reply to the message in the id
    guild = 742797665301168220
    if ctx.author.id == GOD:    
        try:
            message = list(message)
            msg_id = int(message[-1])
            message = message[0:-1]
            channel = str(channel)
            newChannel = ''
            for i in channel:
                if i in "1234567890":
                    newChannel += i
            newChannel = int(newChannel)
            channelObj = bot.get_channel(newChannel)
            msgObj = await ctx.fetch_message(msg_id)
            await msgObj.reply(' '.join(message))
            return
        except Exception as E:
            pass
    else:
        ctx.send("I dont respond to you")

@bot.command(aliases = ['sleep'])
async def ByeBye(ctx):
    #command to close/shutdown the bot from the discord client
    #syntax - `+sleep`
    if ctx.author.id == GOD:
        await ctx.send("GG WP, i am dead")
        sys.exit(0)
    
    else:
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        member = ctx.author
        await ctx.author.add_roles(muted)
        mute_embed.add_field(name="muted user", value=mute_user)
        await ctx.send("Ayy lawda, how dare you try that, take a 30s mute")
        await asyncio.sleep(30)
        if (muted in member.roles):
            await member.remove_roles(muted)
            await ctx.send("Welcome back {}, dont you dare try that again".format(member.mention))

@bot.command(aliases = ['p', 'purge'])
async def _clear(ctx, amt=0):
    #syntax - `+purge 10` - removes last 10 messages in that channel
    if ctx.message.author.id == GOD:
        if amt > 0:    
            await ctx.channel.purge(limit=amt)
        else:
            await ctx.send("how much do you wanna purge")
    else:
        await ctx.send("You dont have the perms to do that" )
        




@bot.command(aliases = ['remainder', 'r'])
async def rem(ctx, *time):
    #just a remainder function - `+r 10 m`
    possibleUnits = ['s', 'm', 'h']
    unit = time[-1]
    time = time[0]
    try:
        time = int(time)
        if unit in possibleUnits:
            timeInSec = 0
            if unit == 'm':
                timeInSec = time*60
            elif  unit == 'h':
                timeInSec = time*60*60
            else:
                timeInSec = time

            await ctx.send("Timer started for {} seconds".format(timeInSec))
            await asyncio.sleep(timeInSec)
            await ctx.send(ctx.author.mention)
            await ctx.send("Sup bitch, times up")
        else:
            await ctx.send("Need either s, m, h as time units")
    except ValueError as V:
        await ctx.send("Need number as time value")

@bot.command(aliases = ['play'])
async def wake(ctx):
    #to play a mp3 file in a VC
    #! deprecated and highly inefficient and needs ffmpeg to be downloaded
    channel = ctx.message.author.voice.channel
    try:
        voice = await channel.connect()
    except:
        pass
    voice.play(FFmpegPCMAudio(executable = 'ffmpeg-N-99890-g7e8306dd2d-win64-gpl-shared\\bin\\ffmpeg.exe', source = 'Believer.mp3'))

@bot.command(aliases = ['mute'])
async def _mute(ctx, member, time, reason="no reason given"):
    #command to mute a member, the perms for such a role must be set as per convenience
    #syntax - `+mute @Stark 5h <whatever reason>`
    muted = discord.utils.get(ctx.guild.roles, name="Muted")

    if (ctx.author.id == GOD):
        if '@' in str(member):
            member = str(member)
            id = ''
            for i in member:
                if i in '1234567890':
                    id += i
            member = int(id) #get their id
            member = ctx.message.guild.get_member(member)  
            # await ctx.send(str(type(member)) + str(member))
            
            seconds=0
            if time.lower().endswith("d"):
                seconds += int(time[:-1]) * 60 * 60 * 24
            if time.lower().endswith("h"):
                seconds += int(time[:-1]) * 60 * 60
            elif time.lower().endswith("m"):
                seconds += int(time[:-1]) * 60
            elif time.lower().endswith("s"):
                seconds += int(time[:-1])
            
            if seconds <= 0:
                await ctx.channel.send(f"{ctx.author.mention}, please enter a valid amount of time")
            else:
                if (muted in member.roles):
                    await ctx.channel.send("Lawda he's already muted means how much more you'll do")
                else:
                    await member.add_roles(muted)
                    mute_embed = discord.Embed(title="Mute", color=0xff0000)
                    mute_user = f"{member.mention} was muted"
                    mute_embed.add_field(name="muted user", value=mute_user)
                    await ctx.channel.send(embed=mute_embed)
                    mute_embed_logs = discord.Embed(title="Mute", color=0xff0000)
                    mute_details_logs = f"{member.mention}\t Time: {time}\n Reason: {reason}\n Moderator: {ctx.author.mention}"
                    mute_embed_logs.add_field(name="muted user details logs", value=mute_details_logs)
                    await bot.get_channel(BOT_LOGS).send(embed=mute_embed_logs)
                    await asyncio.sleep(seconds)
                    if (muted in member.roles):
                        unmute_embed = discord.Embed(title="Unmute", color=0x00ff00)
                        unmute_user = f"{member.mention} welcome back"
                        unmute_embed.add_field(name="unmuted user", value=unmute_user)
                        await ctx.channel.send(embed=unmute_embed)
                        unmute_embed_logs = discord.Embed(title="Unmute", color=0x00ff00)
                        unmute_details_logs = f"{member.mention}\n Moderator: Auto"
                        unmute_embed_logs.add_field(name="unmuted user details logs", value=unmute_details_logs)
                        await bot.get_channel(BOT_LOGS).send(embed=unmute_embed_logs)
                        await member.remove_roles(muted)
        else:
            await ctx.channel.send(f"{ctx.author.mention}, mention the user, not just the name")
    else:
        await ctx.channel.send("You dont have perms for that")

    
@bot.command(aliases = ['unmute'])
async def _unmute(ctx, member: discord.Member):
    muted = discord.utils.get(ctx.guild.roles, name="Muted")
    if ctx.author.id == GOD:
        if (muted not in member.roles):
            await ctx.channel.send("The user isn't muted")
        else:
            unmute_embed = discord.Embed(title="Unmute", color=0x00ff00)
            unmute_user = f"{member.mention} welcome back"
            unmute_embed.add_field(name="unmuted user", value=unmute_user)
            await ctx.channel.send(embed=unmute_embed)
            unmute_embed_logs = discord.Embed(title="Unmute", color=0x00ff00)
            unmute_details_logs = f"{member.mention}\n Moderator: {ctx.author.mention}"
            unmute_embed_logs.add_field(name="unmuted user details logs", value=unmute_details_logs)
            await bot.get_channel(BOT_LOGS).send(embed=unmute_embed_logs)
            await member.remove_roles(muted)
    else:
        await ctx.channel.send("You dont have perms for that")

#! slash commands are a kind of commands like `/tableflip` which work without bot specific prefix
#! not recommended as its kind of unstable and slow and also activating stops all non-slash bot commands
# slash = SlashCommand(bot,  auto_register=True)
# @slash.slash(name="test")
# async def _test(ctx: SlashContext):
#     embed = discord.Embed(title="embed test")
#     await ctx.send(content="test", embeds=[embed])


# @slash.slash(name="hmm", description="Testing description")
# async def _hmm(ctx:SlashContext):
#     embed = discord.Embed(title="embed test")
#     await ctx.send(content=":ThinkLikeLawda:", embeds=[embed])



@bot.event
async def on_message(message):
    if message.author.bot:
        pass
    else:
        await bot.process_commands(message)
    




@bot.command(aliases = ['kick'])
async def _kick(ctx, member, *reason):
    #to kick a user out of the server
    #syntax - `+kick @Stark <>reason here`
    reason=list(reason)
    reason=" ".join(reason)
    if (reason==""):
        reason = "no reason given"
    if '@' in str(member):
            member = str(member)
            id = ''
            for i in member:
                if i in '1234567890':
                    id += i
            member = int(id) #get their id
            member = ctx.message.guild.get_member(member)
    else:
        await ctx.send("Mention the user and not just the name")
        return
    if (ctx.author.id == GOD):
        await ctx.guild.kick(member)
        await ctx.send(f"{str(member)} was kicked")
        try:
            #Dm the user saying he/she has been kicked from the server
            await member.send(f"You were kicked from the server\n Reason: {reason}")
        except:
            await ctx.send("DM failed, the users has DMs disabled")
    else:
        await ctx.channel.send("Who do you think you are to run this command")
    


bot.run(TOKEN)