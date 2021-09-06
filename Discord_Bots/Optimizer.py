import discord, asyncio, time, random, os, youtube_dl
from discord.ext import commands, tasks
from itertools import cycle



def token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = token()
id = 705131759658074112


bot = commands.Bot(command_prefix='$')
status = cycle(["Optimizing your feelings!", "Busy making this server great!"])


@bot.event
async def on_ready():
    change_status.start()
    print("Bot is ready")

@bot.event
async def on_member_join(member):
    for channel in member.server.channels:
        if str(channel) == "general":
            await bot.send_message(f"""Welcome to the server {member.mention}!""")

@bot.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if str(channel) == "general":
            await bot.send_message(f"""Goodbye {member.mention}!""")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments!")




@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount + 1)


@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.send(f"You have been kicked from the server {bot.get_guild(id).name}. Reason: {reason}")
    await member.kick(reason=reason)
    await ctx.send(f"User {member.mention} has been successfully kicked.")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send(f"You have been banned from the server {bot.get_guild(id).name}. Reason: {reason}")
    await member.ban(reason=reason)
    await ctx.send(f"User {member.mention} has been successfully banned.")

@bot.command()
async def unban(ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_number = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_number):
            await ctx.guild.unban(user)
            await user.send(f"You have been unbanned from the server {bot.get_guild(id).name}.")
            await ctx.send(f"User {user.mention} has been successfully unbanned.")
            return

    await ctx.send(f"User {member} isn't banned from the server.")

@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(f'cogs.{extension}')
    except Exception as e:
        print(e)

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Successfully reloaded {extension}")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify an amount of messages to delete!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(seconds=900)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

bot.run(token)



