import os
import json
import string
from discord.ext import commands
import discord
import requests
from colorama import Fore, init
import asyncio
import sys
import random
from flask import Flask
from threading import Thread
import time
import urllib.parse
import urllib.request
import re
from pystyle import Center, Colorate, Colors
import io
import webbrowser
from bs4 import BeautifulSoup
import datetime
import status_rotator
from pyfiglet import Figlet
import openai
from config import TOKEN
import afk
import automessage
import platform
import socket
import aiohttp

# Initialize colorama for cross-platform colored output
init()

# Bot initialization with anti-detection
sachin = commands.Bot(
    description='SELFBOT CREATED BY SACHIN',
    command_prefix='.',
    self_bot=True
)
status_task = None

# Remove default help command
sachin.remove_command('help')

# Bot configuration
sachin.whitelisted_users = {}
sachin.antiraid = False

# Color constants
red = "\033[91m"
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[94m"
pretty = "\033[95m"
magenta = "\033[35m"
lightblue = "\033[36m"
cyan = "\033[96m"
gray = "\033[37m"
reset = "\033[0m"
pink = "\033[95m"
dark_green = "\033[92m"
yellow_bg = "\033[43m"
clear_line = "\033[K"

# Anti-Ban Protection System
ANTI_BAN_CONFIG = {
    'enabled': False,
    'webhook_url': None,
    'backup_servers': [],
    'trusted_users': set(),
    'safe_mode': False
}

# Update the HELP_CATEGORIES with more detailed descriptions
HELP_CATEGORIES = {
    "COMMON": {
        "emoji": "⚙️",
        "description": "Common Commands",
        "commands": {
            ".help": {"desc": "Show all commands", "usage": ".help [command]", "example": ".help antiban"},
            ".csrv": {"desc": "Clone server to another server", "usage": ".csrv <source_id> <target_id>", "example": ".csrv 123456789 987654321"},
            ".checkpromo": {"desc": "Check Discord promo status", "usage": ".checkpromo <link>", "example": ".checkpromo discord.com/promo/..."},
            ".spam": {"desc": "Spam a message multiple times", "usage": ".spam <amount> <message>", "example": ".spam 5 hello"},
            ".clear": {"desc": "Clear your messages", "usage": ".clear <amount>", "example": ".clear 10"}
        }
    },
    "AFK": {
        "emoji": "💤",
        "description": "AFK System Commands",
        "commands": {
            ".afk": {"desc": "Set AFK status with reason", "usage": ".afk <reason>", "example": ".afk brb in 10 mins"},
            ".unafk": {"desc": "Remove AFK status", "usage": ".unafk", "example": ".unafk"}
        }
    },
    "AUTO": {
        "emoji": "🤖",
        "description": "Automation Commands",
        "commands": {
            ".addar": {"desc": "Add auto response", "usage": ".addar <trigger>, <response>", "example": ".addar hi, hello!"},
            ".removear": {"desc": "Remove auto response", "usage": ".removear <trigger>", "example": ".removear hi"},
            ".auto": {"desc": "Set auto message", "usage": ".auto <time> true <channel> <msg>", "example": ".auto 60 true #general Hello!"},
            ".stopauto": {"desc": "Stop auto message", "usage": ".stopauto <msg_id>", "example": ".stopauto 123456789"}
        }
    },
    "PAYMENT": {
        "emoji": "💰",
        "description": "Payment Related Commands",
        "commands": {
            ".upi": {"desc": "Show UPI payment details", "usage": ".upi", "example": ".upi"},
            ".qr": {"desc": "Show payment QR code", "usage": ".qr", "example": ".qr"},
            ".addy": {"desc": "Show LTC address", "usage": ".addy", "example": ".addy"}
        }
    },
    "CRYPTO": {
        "emoji": "🪙",
        "description": "Cryptocurrency Commands",
        "commands": {
            ".send": {"desc": "Send LTC to address", "usage": ".send <address> <amount>", "example": ".send Lt... 0.5"},
            ".bal": {"desc": "Check LTC balance", "usage": ".bal <address>", "example": ".bal Lt..."},
            ".mybal": {"desc": "Check your LTC balance", "usage": ".mybal", "example": ".mybal"},
            ".ltcprice": {"desc": "Check current LTC price", "usage": ".ltcprice", "example": ".ltcprice"}
        }
    },
    "STATUS": {
        "emoji": "🎮",
        "description": "Status Commands",
        "commands": {
            ".stream": {"desc": "Set streaming status", "usage": ".stream <title>", "example": ".stream Playing Games"},
            ".play": {"desc": "Set playing status", "usage": ".play <title>", "example": ".play Minecraft"},
            ".watch": {"desc": "Set watching status", "usage": ".watch <title>", "example": ".watch Netflix"},
            ".listen": {"desc": "Set listening status", "usage": ".listen <title>", "example": ".listen Spotify"},
            ".stopactivity": {"desc": "Stop all activities", "usage": ".stopactivity", "example": ".stopactivity"}
        }
    },
    "PROTECTION": {
        "emoji": "🛡️",
        "description": "Protection Commands",
        "commands": {
            ".antiban": {"desc": "Toggle anti-ban protection", "usage": ".antiban <on/off>", "example": ".antiban on"},
            ".safemode": {"desc": "Toggle safe mode", "usage": ".safemode <on/off>", "example": ".safemode on"},
            ".trust": {"desc": "Add trusted user", "usage": ".trust <user_id>", "example": ".trust 123456789"},
            ".untrust": {"desc": "Remove trusted user", "usage": ".untrust <user_id>", "example": ".untrust 123456789"},
            ".backupserver": {"desc": "Add backup server", "usage": ".backupserver <server_id>", "example": ".backupserver 123456789"},
            ".webhook": {"desc": "Set webhook for notifications", "usage": ".webhook <url>", "example": ".webhook https://discord.com/api/webhooks/..."}
        }
    },
    "CALCULATOR": {
        "emoji": "🧮",
        "description": "Calculator Commands",
        "commands": {
            ".math": {"desc": "Calculate expression", "usage": ".math <expression>", "example": ".math 2 + 2"},
            ".i2c": {"desc": "Convert INR to Crypto", "usage": ".i2c <amount>", "example": ".i2c 1000"},
            ".c2i": {"desc": "Convert Crypto to INR", "usage": ".c2i <amount>", "example": ".c2i 50"}
        }
    }
}

@sachin.command(name='help')
async def help_cmd(ctx, command: str = None):
    """Horizontal help command"""
    try:
        if command:
            # Show help for specific command
            for category, data in HELP_CATEGORIES.items():
                if command in [cmd.replace(".", "") for cmd in data["commands"].keys()]:
                    cmd_info = data["commands"][f".{command}"]
                    msg = f"**{cmd_info['desc']}**\n`{cmd_info['usage']}`"
                    await ctx.send(msg)
                    return
            await ctx.send("❌ Command not found")
            return

        # Show horizontal help menu
        help_text = "```\n"
        help_text += "╔══════════════════════════════ S A C H I N C O R D ═══════════════════════════╗\n"
        help_text += "║                                                                              ║\n"
        
        # Common Commands
        help_text += "║  ⚙️ COMMON         ┃ 🎮 STATUS       ┃ 💰 PAYMENT        ┃ 🤖 AUTO           ║\n"
        help_text += "║  .help             ┃ .stream          ┃ .upi              ┃ .auto            ║\n"
        help_text += "║  .csrv             ┃ .play            ┃ .qr               ┃ .stopauto        ║\n"
        help_text += "║  .spam             ┃ .watch           ┃ .addy             ┃ .addar           ║\n"
        help_text += "║  .clear            ┃ .listen          ┃ .ltcprice         ┃ .removear        ║\n"
        help_text += "║                    ┃ .stopactivity    ┃ .send             ┃ .lister          ║\n"
        help_text += "║──────────────────────────────────────────────────────────────────────────────║\n"
        
        # Second row of categories
        help_text += "║  💤 AFK            ┃ 🧮 CALC         ┃ 🛡️ PROTECTION     ┃ 💱 CRYPTO        ║\n"
        help_text += "║  .afk              ┃ .math            ┃ .antiban          ┃ .send            ║\n"
        help_text += "║  .unafk            ┃ .i2c             ┃ .safemode         ┃ .bal             ║\n"
        help_text += "║                    ┃ .c2i             ┃ .trust            ┃ .mybal           ║\n"
        help_text += "║                    ┃                  ┃ .untrust          ┃ .ltcprice        ║\n"
        help_text += "║                    ┃                  ┃ .backupserver     ┃                  ║\n"
        help_text += "║──────────────────────────────────────────────────────────────────────────────║\n"
        help_text += "║  Use .help <command> for detailed information about a specific command       ║\n"
        help_text += "╚══════════════════════════════════════════════════════════════════════════════╝\n"
        help_text += "```"
        
        await ctx.send(help_text)

    except Exception as e:
        print(f"Help command error: {str(e)}")

    try:
        await ctx.message.delete()
    except:
        pass

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
Qr = config.get("Qr")
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

time_rn = get_time_rn()

@sachin.event
async def on_message(message):
    if message.author.bot:
        return

    # Auto-response handling
    with open('auto_responses.json', 'r') as file:
        auto_responses = json.load(file)

    if message.content in auto_responses:
        await message.channel.send(auto_responses[message.content])

    await sachin.process_commands(message)

@sachin.command()
async def upi(ctx):
    message = (f"{Upi}")
    message2 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}UPI SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@sachin.command()
async def qr(ctx):
    message = (f"{Qr}")
    message2 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}QR SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@sachin.command()
async def addy(ctx):
    message = (f"<a:ltcan:1238717949968257034> <a:ltcan:1238717949968257034> <a:ltcan:1238717949968257034> <a:ltcan:1238717949968257034> **LTC ADDY** <a:ltcan:1238717949968257034> <a:ltcan:1238717949968257034> <a:ltcan:1238717949968257034> <a:ltcan:1238717949968257034> ")
    message2 = (f"{LTC}")
    message3 = (f"**MUST SEND SCREENSHOT AND BLOCKCHAIN AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}ADDY SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
# MATHS
api_endpoint = 'https://api.mathjs.org/v4/'
@sachin.command()
async def math(ctx, *, equation):
    # Send the equation to the math API for calculation
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.reply(f'`-` **RESULT**: `{result}`')
    else:
        await ctx.reply('`-` **FAILED**')
        
@sachin.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def i2c(ctx, amount: str):
    amount = float(amount.replace('₹', ''))
    inr_amount = amount / I2C_Rate
    await ctx.reply(f"`-` **AMOUNT IS** : `${inr_amount:.2f}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}I2C DONE ✅ ")
    
@sachin.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def c2i(ctx, amount: str):
    amount = float(amount.replace('$', ''))
    usd_amount = amount * C2I_Rate
    await ctx.reply(f"`-` **AMOUNT IS** : `₹{usd_amount:.2f}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}C2I DONE ✅ ")
    
spamming_flag = True
# SPAM 
@sachin.command()
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)      
    print("{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN}SPAMMING SUCCESFULLY✅ ")
    
@sachin.command(aliases=[])
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{LTC}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("- `FAILED`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("- `FAILED`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price

    message = f"**CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD`\n"
    message += f"**TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD`\n"
    message += f"**UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD`\n\n"

    await ctx.reply(message)
    
@sachin.command(aliases=['ltcbal'])
async def bal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("- `FAILED`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("- `FAILED`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price

    message = f"**CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD`\n"
    message += f"**TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD`\n"
    message += f"**UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD`\n\n"

    await ctx.reply(message)
          
@sachin.command(aliases=["streaming"])
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/https://Wallibear",
    )
    await sachin.change_presence(activity=stream)
    await ctx.send(f"`-` **STREAM CREATED** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STREAM SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@sachin.command(aliases=["playing"])
async def play(ctx, *, message):
    game = discord.Game(name=message)
    await sachin.change_presence(activity=game)
    await ctx.send(f"`-` **STATUS FOR PLAYZ CREATED** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PLAYING SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@sachin.command(aliases=["watch"])
async def watching(ctx, *, message):
    await sachin.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=message,
    ))
    await ctx.send(f"`-` **WATCHING CREATED**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}WATCH SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@sachin.command(aliases=["listen"])
async def listening(ctx, *, message):
    await sachin.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    await ctx.reply(f"`-` **LISTENING CREATED**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STATUS SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@sachin.command(aliases=[
    "stopstreaming", "stopstatus", "stoplistening", "stopplaying",
    "stopwatching"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await sachin.change_presence(activity=None, status=discord.Status.dnd)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED}STREAM SUCCESFULLY STOPED⚠️ ")
    
@sachin.command()
async def checkpromo(ctx, *, promo_links):
    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:
        for link in links:
            promo_code = extract_promo_code(link)
            if promo_code:
                result = await check_promo(session, promo_code)
                await ctx.send(result)
            else:
                await ctx.send(f'**INVALID LINK** : `{link}`')


async def check_promo(session, promo_code):
    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    async with session.get(url) as response:
        if response.status in [200, 204, 201]:
            data = await response.json()
            if data["uses"] == data["max_uses"]:
                return f'- `ALREADY CLAIMED {promo_code}`'
            else:
                try:
                    now = datetime.datetime.utcnow()
                    exp_at = data["expires_at"].split(".")[0]
                    parsed = parser.parse(exp_at)
                    days = abs((now - parsed).days)
                    title = data["promotion"]["inbound_header_text"]
                except Exception as e:
                    print(e)
                    exp_at = "- `FAILED TO FETCH`"
                    days = ""
                    title = "- `FAILED TO FETCH`"
                return f'**VALID** : __`{promo_code}`__ \n`-` **DAYS LEFT IN EXPIRATION** : `{days}`\n`-` **EXPIRES AT** : `{exp_at}`\n`-` **TITLE** : `{title}`\n\n`-` **ASKED BY** : `sachin.user.name`**'
                
        elif response.status == 429:
            return f'**RARE LIMITED**`'
        else:
            return f'**INVALID CODE** : {promo_code}`'


def extract_promo_code(promo_link):
    promo_code = promo_link.split('/')[-1]
    return promo_code
    
@sachin.command()
async def exch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} LEGIT | EXCHANGED {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')

@sachin.command()
async def vouch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} LEGIT SELLER | GOT {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    await ctx.send(f'**NO VOUCH NO WARRANTY OF PRODUCT**')
    
@sachin.command(aliases=['cltc'])
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"**THE CURRENT PRICE OF LITECOIN IN MARKET IS :** `{price:.2f}`")
    else:
        await ctx.send("**FAILED TO FETCH**")
        
@sachin.command()
async def addar(ctx, *, trigger_and_response: str):
    # Split the trigger and response using a comma (",")
    trigger, response = map(str.strip, trigger_and_response.split(','))

    with open('auto_responses.json', 'r') as file:
        data = json.load(file)

    data[trigger] = response

    with open('auto_responses.json', 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'**AUTO-RESPONSE ADDED.. !** **{trigger}** - **{response}**')



@sachin.command()
async def removear(ctx, trigger: str):
    with open('auto_responses.json', 'r') as file:
        data = json.load(file)

    if trigger in data:
        del data[trigger]

        with open('auto_responses.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(f'**AUTO-RESPONSE REMOVED** **{trigger}**')
    else:
        await ctx.send(f'**AUTO-RESPONSE NOT FOUND** **{trigger}**')
        
@sachin.command()
async def lister(ctx):
    with open('auto_responses.json', 'r') as file:
        data = json.load(file)
    responses = '\n'.join([f'**{trigger}** - **{response}**' for trigger, response in data.items()])
    await ctx.send(f'**AUTO_RESPONSE LIST** :\n{responses}')

@sachin.command()
async def csrv(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = sachin.get_guild(source_guild_id)
    target_guild = sachin.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await ctx.send("`-` **GUILD NOT FOUND**")
        return

    # Delete all channels in the target guild
    for channel in target_guild.channels:
        try:
            await channel.delete()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN DELETED ON THE TARGET GUILD")
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING CHANNEL {channel.name}: {e}")

    # Delete all roles in the target guild except for roles named "here" and "@everyone"
    for role in target_guild.roles:
        if role.name not in ["here", "@everyone"]:
            try:
                await role.delete()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ROLE {role.name} HAS BEEN DELETED ON THE TARGET GUILD")
                await asyncio.sleep(0)
            except Exception as e:
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING ROLE {role.name}: {e}")

    # Clone roles from source to target
    roles = sorted(source_guild.roles, key=lambda role: role.position)

    for role in roles:
        try:
            new_role = await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} {role.name} HAS BEEN CREATED ON THE TARGET GUILD")
            await asyncio.sleep(0)

            # Update role permissions after creating the role
            for perm, value in role.permissions:
                await new_role.edit_permissions(target_guild.default_role, **{perm: value})
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING ROLE {role.name}: {e}")

    # Clone channels from source to target
    text_channels = sorted(source_guild.text_channels, key=lambda channel: channel.position)
    voice_channels = sorted(source_guild.voice_channels, key=lambda channel: channel.position)
    category_mapping = {}  # to store mapping between source and target categories

    for channel in text_channels + voice_channels:
        try:
            if channel.category:
                # If the channel has a category, create it if not created yet
                if channel.category.id not in category_mapping:
                    category_perms = channel.category.overwrites
                    new_category = await target_guild.create_category_channel(name=channel.category.name, overwrites=category_perms)
                    category_mapping[channel.category.id] = new_category

                # Create the channel within the category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await new_category.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    # Check if the voice channel already exists in the category
                    existing_channels = [c for c in new_category.channels if isinstance(c, discord.VoiceChannel) and c.name == channel.name]
                    if existing_channels:
                        new_channel = existing_channels[0]
                    else:
                        new_channel = await new_category.create_voice_channel(name=channel.name)

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

                # Update channel permissions after creating the channel
                for overwrite in channel.overwrites:
                    if isinstance(overwrite.target, discord.Role):
                        target_role = target_guild.get_role(overwrite.target.id)
                        if target_role:
                            await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                    elif isinstance(overwrite.target, discord.Member):
                        target_member = target_guild.get_member(overwrite.target.id)
                        if target_member:
                            await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                await asyncio.sleep(0)  # Add delay here
            else:
                # Create channels without a category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await target_guild.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    new_channel = await target_guild.create_voice_channel(name=channel.name)

                    # Update channel permissions after creating the channel
                    for overwrite in channel.overwrites:
                        if isinstance(overwrite.target, discord.Role):
                            target_role = target_guild.get_role(overwrite.target.id)
                            if target_role:
                                await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                        elif isinstance(overwrite.target, discord.Member):
                            target_member = target_guild.get_member(overwrite.target.id)
                            if target_member:
                                await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                    await asyncio.sleep(0)  # Add delay here

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING CHANNEL {channel.name}: {e}")
            
@sachin.command(aliases=["pay", "sendltc"])
async def send(ctx, addy, value):
    try:
        value = float(value.strip('$'))
        message = await ctx.send(f"Sending {value}$ To {addy}")
        url = "https://api.tatum.io/v3/litecoin/transaction"
        
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=usd&vs_currencies=ltc")
        r.raise_for_status()
        usd_price = r.json()['usd']['ltc']
        topay = usd_price * value
        
        payload = {
        "fromAddress": [
            {
                "address": ltc_addy,
                "privateKey": ltc_priv_key
            }
        ],
        "to": [
            {
                "address": addy,
                "value": round(topay, 8)
            }
        ],
        "fee": "0.00005",
        "changeAddress": ltc_addy
    }
        headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        await message.edit(content=f"**Successfully Sent {value}$ To {addy}**\nhttps://live.blockcypher.com/ltc/tx/{response_data["txId"]}")
    
    except requests.RequestException as e:
        await ctx.send(f"**Failed to send LTC. Error: {e}**")
    except ValueError:
        await ctx.send("**Invalid amount. Please provide a valid number.**")

@sachin.command(aliases=['purge, clear'])
async def clear(ctx, times: int):
    channel = ctx.channel

    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id

    
    messages = await channel.history(limit=times + 1).flatten()

    
    bot_messages = filter(is_bot_message, messages)

    
    for message in bot_messages:
        await asyncio.sleep(0.55)  
        await message.delete()

    await ctx.send(f"`-` **DELETED {times} MESSAGES**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PURGED SUCCESFULLY✅ ")


# AUTO MSG
async def setup_extensions():
    """Load all extensions"""
    try:
        await sachin.load_extension("automessage")
        await sachin.load_extension("afk")
        await sachin.load_extension("status_rotator")
        print("Made By SACHIN With ❤️")
    except Exception as e:
        print(f"Error loading extensions: {e}")

# Anti-Detection Features
@sachin.event
async def on_command(ctx):
    random_delay, simulate_typing = setup_anti_detection()
    await random_delay()
    await simulate_typing()

@sachin.event
async def on_command_completion(ctx):
    await asyncio.sleep(random.uniform(0.5, 1.5))

@sachin.event
async def on_command_error(ctx, error):
    print(f"{red}[ERROR] Command error occurred: {str(error)}{reset}")

# Anti-Detection Event Handlers
@sachin.event
async def on_guild_ban(guild, user):
    """Handle ban events for protection"""
    if ANTI_BAN_CONFIG['enabled'] and user.id == sachin.user.id:
        if ANTI_BAN_CONFIG['webhook_url']:
            # Send webhook notification
            webhook = discord.Webhook.from_url(ANTI_BAN_CONFIG['webhook_url'], adapter=discord.RequestsWebhookAdapter())
            webhook.send(f"⚠️ Ban detected in {guild.name} ({guild.id})")
        
        if ANTI_BAN_CONFIG['safe_mode']:
            # Leave all mutual guilds for safety
            for guild in sachin.guilds:
                if guild.id not in ANTI_BAN_CONFIG['backup_servers']:
                    await guild.leave()

@sachin.event
async def on_guild_join(guild):
    """Handle guild join events"""
    if ANTI_BAN_CONFIG['safe_mode']:
        # Check if any banned users are in the guild
        banned_users = await guild.bans()
        if any(ban.user.id == sachin.user.id for ban in banned_users):
            await guild.leave()
            if ANTI_BAN_CONFIG['webhook_url']:
                webhook = discord.Webhook.from_url(ANTI_BAN_CONFIG['webhook_url'], adapter=discord.RequestsWebhookAdapter())
                webhook.send(f"🚫 Avoided joining {guild.name} ({guild.id}) - Previous ban detected")

def print_starting_animation():
    animation = [
        "[■□□□□□□□□□]",
        "[■■□□□□□□□□]",
        "[■■■□□□□□□□]",
        "[■■■■□□□□□□]",
        "[■■■■■□□□□□]",
        "[■■■■■■□□□□]",
        "[■■■■■■■□□□]",
        "[■■■■■■■■□□]",
        "[■■■■■■■■■□]",
        "[■■■■■■■■■■]"
    ]
    
    print(
        Center.XCenter(
            Colorate.Vertical(
                Colors.blue_to_purple,
                r"""
    _____ ___   ________  _______   __   __________  ____  ____ 
   / ___//   | / ____/ / / /  _/ | / /  / ____/ __ \/ __ \/ __ \
   \__ \/ /| |/ /   / /_/ // //  |/ /  / /   / / / / /_/ / / / /
  ___/ / ___ / /___/ __  // // /|  /  / /___/ /_/ / _, _/ /_/ / 
 /____/_/  |_\____/_/ /_/___/_/ |_/   \____/\____/_/ |_/_____/           
                """,
                1,
            )
        )
    )
    
    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + Center.XCenter(f"{cyan}Starting Sachin Cord... {animation[i]} {reset}"))
        sys.stdout.flush()
    print("\n")

@sachin.event
async def on_ready():
    print_starting_animation()
    print(
        Center.XCenter(
            Colorate.Vertical(
                Colors.blue_to_purple,
            f"""[+] -------------------------------- ] | [ S A C H I N C O R D - {sachin.user.name}  ] | [ ------------------------------------ [+]
""",
                1,
            )
        )
    )
    # Load extensions
    await setup_extensions()
    print(Center.XCenter(f"{green}Bot Started Successfully ✅{reset}"))

if __name__ == "__main__":
    token = TOKEN
    try:
        # Create event loop before running the bot
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the selfbot with user token
        sachin.run(token, log_handler=None)
    except discord.LoginFailure:
        print(f"{red}[ERROR] Invalid token. Please check your user token in config.py{reset}")
        print(f"{yellow}Make sure you're using your USER token, not a bot token!{reset}")
    except Exception as e:
        print(f"{red}[ERROR] An error occurred: {str(e)}{reset}")
    finally:
        try:
            if loop and not loop.is_closed():
                loop.close()
        except:
            pass