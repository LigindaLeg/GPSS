import discord
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown
import asyncio

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
@bot.command(name='info')
@commands.cooldown(1, 300, commands.BucketType.user)  # Кулдаун на 5 минут
async def info(ctx):
    await ctx.send(
        "Информация о боте <@1218231384024289392>\n"
        "Данный бот автоматизирует блокировку участников, которые когда-либо участвовали в рейдах, ДДОС-Атаках и т.д.\n\n"
        "Этот бот помогает Администраторам Дискорд-Серверов предотвращать рейды и другой возможный ущерб дискорд-серверам, "
        "автоматизируя отбор участников и блокируя их\n\n"
        "Создатель данного бота <@612288780107382795>\n\n"
        "Все вопросы принимаются на нашем дискорд-сервере: https://discord.gg/S4ykbjaRWK"
    )

# Обработка ошибки при попытке использовать команду во время кулдауна
@info.error
async def info_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.message.delete()

# Функция для чтения данных из файла и форматирования строк
def read_ids_from_file(filename):
    with open(filename, 'r') as file:
        ids = file.readlines()
        return [f"<@{id.strip()}>" for id in ids]

# Команда list для вывода данных из файла
@bot.command()
async def list(ctx):
    ids = read_ids_from_file('ids.txt')
    await ctx.send('\n'.join(ids))

# Обработчик события on_message для кулдауна
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Проверяем, если сообщение начинается с префикса и это команда list
    if message.content.startswith('!list'):
        cooldown_seconds = 300  # 5 минут в секундах

        # Проверяем, есть ли кулдаун для этого пользователя
        if not hasattr(bot, 'last_list_command') or bot.last_list_command + cooldown_seconds < message.created_at.timestamp():
            bot.last_list_command = message.created_at.timestamp()
            await bot.process_commands(message)
        else:
            await message.delete()
    await bot.process_commands(message)

bot.run('token')
