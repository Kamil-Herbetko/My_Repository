import discord, asyncio, youtube_dl
from discord.ext import commands
from functools import partial
from Discord_Bots.cogs.project_utils.Queue import Queue

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester, volume=0.5):
        super().__init__(source, volume)
        self.requester = requester

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable="C:/ffmpeg/bin/ffmpeg.exe"), data=data)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'```ini\n[Added {data["title"]} to the Queue.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source, **ffmpeg_options, executable="C:/ffmpeg/bin/ffmpeg.exe"), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url'], **ffmpeg_options, executable="C:/ffmpeg/bin/ffmpeg.exe"), data=data, requester=requester)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = Queue(40)

    @commands.command()
    async def join(self, ctx):

        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return
        else:
            channel = ctx.message.author.voice.channel
            await ctx.send(f'Connected to ``{channel}``')
        await channel.connect()
        if ctx.voice_client.is_connected():
            await ctx.voice_client.move_to(channel)


    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, search):
        try:
            if not ctx.voice_client:
                await ctx.send("Connect me to the voice channel!")
                return


            async with ctx.typing():
                player = await YTDLSource.regather_stream(await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False), loop=self.bot.loop)
                if self.queue.isEmpty() and not ctx.voice_client.is_playing():

                    await ctx.send(
                        f':mag_right: **Searching for** ``' + search + '``\n<:youtube:763374159567781890> **Now Playing:** ``{}'.format(
                            player.title) + "``")

                    await self.start_playing(ctx.voice_client, player)


                else:

                    self.queue.enqueue(player)

                    await ctx.send(
                        f':mag_right: **Searching for** ``' + search + '``\n<:youtube:763374159567781890> **Added to queue:** ``{}'.format(
                            player.title) + "``")

                    asyncio.create_task(self.start_playing(ctx.voice_client, player))




        except Exception as e:
            print(e)
            await ctx.send("Somenthing went wrong - please try again later!")



    @commands.command(name="play-url")
    async def play_url(self, ctx, *, url):

        try:
            if not ctx.voice_client:
                await ctx.send("Connect me to the voice channel!")
                return
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

                if self.queue.isEmpty() and not ctx.voice_client.is_playing():

                    await ctx.send(
                        f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Now Playing:** ``{}'.format(
                            player.title) + "``")

                    await self.start_playing(ctx.voice_client, player)


                else:

                    self.queue.enqueue(player)

                    await ctx.send(
                        f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Added to queue:** ``{}'.format(
                            player.title) + "``")

                    asyncio.create_task(self.start_playing(ctx.voice_client, player))

        except Exception as e:
            print(e)
            await ctx.send("Somenthing went wrong - please try again later!")

    async def start_playing(self, voice_client, player):

        if self.queue.isEmpty():
            self.queue.enqueue(player)

        while not self.queue.isEmpty():
            await asyncio.sleep(0.1)
            try:
                if not voice_client.is_playing():
                    voice_client.play(self.queue.dequeue(), after=lambda e: print('Player error: %s' % e) if e else None)

            except:
                pass

    @commands.command(name="clear-queue")
    async def clear_queue(self, ctx):
        self.queue.clear()


def setup(bot):
    bot.add_cog(Music(bot))
