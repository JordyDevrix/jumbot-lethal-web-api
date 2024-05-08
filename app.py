import discord
import asyncio

import quart
from quart import Quart

app = Quart(__name__)
client = discord.Client(intents=discord.Intents.all())

with open("token.txt", "r") as file:
    token: str = file.read()


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await client.login(token)
    loop.create_task(client.connect())


@app.route("/send/<message>", methods=["GET"])
async def send_specific_message(message):
    # wait_until_ready and check for valid connection is missing here
    channel = client.get_channel(1214700522997678157)
    await channel.send(message)
    return 'OK', 200


@app.route("/send", methods=["GET"])
async def send_message():
    return await quart.render_template("index.html")


@app.route("/send", methods=["POST"])
async def send_message_post():
    text = await quart.request.form

    title = text['title']
    content = text['message']
    message = f"# {title}\n{content}"
    print(message)

    channel = client.get_channel(1214700522997678157)
    await channel.send(message)

    return "<p>Message sent</p>"


app.run(host='0.0.0.0', port=5100)
