import random

import discord
import asyncio

import quart
from quart import Quart, request

app = Quart(__name__)
client = discord.Client(intents=discord.Intents.all())

with open("token.txt", "r") as file:
    token: str = file.read()


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await client.login(token)
    loop.create_task(client.connect())


@app.route("/login", methods=["POST"])
async def login():
    char = "abcdefghijklmnopqrstuvwxyz"
    btoken = ""
    for i in range(32):
        btoken += random.choice((str(random.randint(0, 9)), random.choice(char)))
    return {"Bearer": btoken}


@app.route("/register", methods=["POST"])
async def register():
    char = "abcdefghijklmnopqrstuvwxyz"
    btoken = ""
    for i in range(32):
        btoken += random.choice((str(random.randint(0, 9)), random.choice(char)))
    return {"Bearer": btoken}


@app.route("/guilds", methods=["GET"])
async def choose_guild():
    headers = request.headers
    try:
        bearer = headers.get('Authorization')
        btoken = bearer.split()[1]
        print(btoken)
    except Exception as e:
        print(e)
    client_guild_list = client.guilds
    guilds = []
    for guild in client_guild_list:
        guilds.append(
            {
                "guild_id": str(guild.id),
                "guild_name": guild.name,
                "guild_member_count": int(len(guild.members))
            }
        )
    print(guilds)
    return guilds


@app.route("/guild/textchannels/<guild_id>", methods=["GET"])
async def get_channel_choice(guild_id):
    headers = request.headers
    try:
        bearer = headers.get('Authorization')
        btoken = bearer.split()[1]
        print(btoken)
    except Exception as e:
        print(e)
    client_guild_channel_list = client.get_guild(int(guild_id)).channels
    channels = []
    for channel in client_guild_channel_list:
        if channel.type.value == 0:
            channels.append(
                {
                    "channel_id": str(channel.id),
                    "channel_name": str(
                        channel.name.encode(
                            encoding="ascii",
                            errors="ignore"
                        )
                    )[2:-1].replace("-", " ").strip()
                }
            )
    return channels

app.run(host='0.0.0.0', port=5100)
