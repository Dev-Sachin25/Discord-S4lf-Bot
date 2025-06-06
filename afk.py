import discord
from discord.ext import commands
import json
import asyncio

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_data = {}
        self.user_cooldowns = {}

    def save_afk_data(self):
        with open("afk_data.json", "w") as f:
            json.dump(self.afk_data, f)

    def load_afk_data(self):
        try:
            with open("afk_data.json", "r") as f:
                self.afk_data = json.load(f)
        except FileNotFoundError:
            self.afk_data = {}

    @commands.command()
    
    async def afk(self, ctx, *, reason="busy so don't ping"):
        user_id = str(ctx.author.id)
        self.afk_data[user_id] = reason
        await ctx.send(f"You are now AFK..")
        self.save_afk_data()

    @commands.command()
    
    async def unafk(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.afk_data:
            del self.afk_data[user_id]
            await ctx.send(f"You are no longer AFK")
            self.save_afk_data()
        else:
            await ctx.send(f"{ctx.author.mention}, you are not AFK")
            
    async def ignore_user_for_duration(self, user_id, duration):
        self.user_cooldowns[user_id] = True
        await asyncio.sleep(duration)
        del self.user_cooldowns[user_id]            

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
            
        if isinstance(message.channel, discord.DMChannel):
            pass  
                    
        for user_id, reason in self.afk_data.items():
            if f"<@{user_id}>" in message.content:
                if message.author.id not in self.user_cooldowns:
                    await message.channel.send(f"{message.author.mention}, I am afk rn., **{reason}**")
                    await self.ignore_user_for_duration(message.author.id, 30)
                break
            elif message.reference and message.reference.cached_message:
                replied_to_user = message.reference.cached_message.author
                if str(replied_to_user.id) == user_id:
                    if message.author.id not in self.user_cooldowns:
                        await message.channel.send(f"{message.author.mention}, I am afk rn., **{reason}**")
                        await self.ignore_user_for_duration(message.author.id, 30)

async def setup(bot):
    cog = AFK(bot)
    cog.load_afk_data()
    await bot.add_cog(cog)
    return True