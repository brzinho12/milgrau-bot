import discord
from discord.ext import commands
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import ConnectEvent, DisconnectEvent
import asyncio

TOKEN = "1444870821096063066"

CANAL_BEM_VINDO = https://discord.com/channels/1444865299378733096/1444865300108415029
CANAL_LIVES = https://discord.com/channels/1444865299378733096/1444869414796263584

# USUÁRIOS DO TIKTOK QUE O BOT VAI MONITORAR
USUARIOS_TIKTOK = ["bonza_019", "_eothur7", "eo_br_crlh", "eojonjomkrlh2"]

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot ligado como {bot.user}")
    bot.loop.create_task(monitorar_tiktok())

@bot.event
async def on_member_join(member):
    canal = bot.get_channel(CANAL_BEM_VINDO)
    if canal:
        await canal.send(f"👋 Olá {member.mention}, bem-vindo(a) à **Cordeiro House**!")

@bot.event
async def on_presence_update(before, after):
    if after.activity and after.activity.type == discord.ActivityType.streaming:
        canal = bot.get_channel(CANAL_LIVES)
        if canal:
            await canal.send(
                f"🔴 **{after.name} entrou em live agora!**\n"
                f"{after.activity.url}"
            )

# =========================
# MONITORAMENTO DO TIKTOK
# =========================
async def monitorar_tiktok():
    await bot.wait_until_ready()

    for user in USUARIOS_TIKTOK:
        client = TikTokLiveClient(unique_id=user)

        @client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            canal = bot.get_channel(CANAL_LIVES)
            if canal:
                await canal.send(
                    f"🔴 **{user} entrou em live no TikTok!**\n"
                    f"https://www.tiktok.com/@{user}/live"
                )

        @client.on(DisconnectEvent)
        async def on_disconnect(event: DisconnectEvent):
            print(f"{user} saiu da live.")

        asyncio.create_task(client.start())

bot.run(TOKEN)
