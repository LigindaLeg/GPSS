import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='GPSS!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="ГОБС в работе"))

@bot.command(name='add')
async def add(ctx, user_id: int):
    role_id = 1218223814526242896
    role = discord.utils.get(ctx.guild.roles, id=role_id)

    if role in ctx.author.roles:
        with open('ids.txt', 'a') as file:
            file.write(str(user_id) + '\n')
        await ctx.send(f'Пользователь <@{user_id}> Успешно внесён в реестр нарушителей!')
    else:
        await ctx.message.delete()

@bot.command(name='say')
async def say(ctx, *, text):
    role_id = 1218225077133508629
    role = discord.utils.get(ctx.guild.roles, id=role_id)
    
    if role in ctx.author.roles:
        await ctx.send(text)
        await ctx.message.delete()
    else:
        await ctx.message.delete()

@bot.event
async def on_member_update(before, after):
    if after.guild.id == 1218223480387010680:
        guild = bot.get_guild(1218223480387010680)
        member = guild.get_member(after.id)
        if member is not None:
            with open('ids.txt') as file:
                banned_ids = file.read().splitlines()
            await after.add_roles(discord.Object(id=1218274736237187092))
            for role in after.roles:
                if role.id != 1218224584713699389 and role.id != 1218226958110822551:
                    await after.remove_roles(role)
    else:
        with open('ids.txt') as file:
            banned_ids = file.read().splitlines()
        if str(after.id) in banned_ids:
            await after.ban(reason="Замечен ГОБС")
            await after.send("Вы были забанены ГОБС, подать аппеляцию тут - https://discord.gg/vkPQm4M3mT")

bot.run('token')