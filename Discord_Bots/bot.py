import discord


def token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = token()
id = 705131759658074112

client = discord.Client()

@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server {member.mention}!""")

@client.event
async def on_message(message):
    id = client.get_guild(705131759658074112)
    channels = ["ak"]
    valid_users = ["Kamil Herbetko#7099", "Jakub Radzik
#8825"]

    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content.find("!hello") != -1:
            await message.channel.send("Hi!")
        elif message.content == "!users":
            await message.channel.send(f"""# of members {id.member_count}""")
client.run(token)







































