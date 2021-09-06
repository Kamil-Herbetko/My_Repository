import discord, asyncio, time


def token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


messages = joined = 0
token = token()
id = 705131759658074112

client = discord.Client()

async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"""Time: {int(time.time())}, Messages: {messages}, Members joined: {joined}\n""")

            messages = 0
            joined = 0

            await asyncio.sleep(60)
        except Exception as e:
            print(e)

@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server {member.mention}!""")

@client.event
async def on_message(message):
    global messages
    messages += 1
    id = client.get_guild(705131759658074112)
    channels = ["ak"]
    valid_users = ["Kamil Herbetko#7099", "Jakub Radzik
#8825"]

    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content.find("!hello") != -1:
            await message.channel.send("Hi!")
        elif message.content == "!users":
            await message.channel.send(f"""# of members {id.member_count}""")
client.loop.create_task(update_stats())
client.run(token)







































