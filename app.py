import random
from authentication import *
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
    credentials = {
        "user": "admin",
        "password": "Abcd1234"
    }
    try:
        create_account(credentials)
    except Exception as e:
        print(e)
    loop = asyncio.get_event_loop()
    await client.login(token)
    loop.create_task(client.connect())


@app.route("/login", methods=["POST"])
async def login():
    try:
        credentials = await credential_checker()
        btoken = token_generator(credentials.get("user"))
        return btoken
    except Exception as e:
        print(e)
        return "Unauthorized", 401


@app.route("/register", methods=["POST"])
async def register():
    try:
        credentials = await request.json
        create_account(credentials)
        btoken = token_generator(credentials.get("user"))
        return btoken
    except Exception as e:
        print(e)
        return "Unauthorized", 401


@app.route("/guilds", methods=["GET"])
async def choose_guild():
    try:
        await auth_interceptor()
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
        return guilds
    except Exception as e:
        print(f"Except {e}")
        return "Unauthorized", 401


@app.route("/send/<channel_id>", methods=["POST"])
async def send_message(channel_id):
    try:
        await auth_interceptor()
        res: dict = await request.json
        print(res)
        message = res.get("message")
        channel = client.get_channel(int(channel_id))
        await channel.send(message)
        return "OK", 200
    except Exception as e:
        print(f"Except {e}")
        return "Unauthorized", 401


@app.route("/guild/textchannels/<guild_id>", methods=["GET"])
async def get_channel_choice(guild_id):
    try:
        await auth_interceptor()
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
    except Exception as e:
        print(f"Except {e}")
        return "Unauthorized", 401

app.run(host='0.0.0.0', port=5100)
