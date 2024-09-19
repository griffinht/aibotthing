import os
import discord
import signal
import asyncio

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Setup OpenAI API
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def get_response(channel, content):
    print(channel, content)
    completion = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": content}])
    return completion.choices[0].message.content

@client.event
async def on_message(message):
    if message.author.bot:
        return

    response = await get_response(message.channel.name, message.content)
    if response is None:
        return

    await message.channel.send(response)

# Graceful shutdown handler
async def shutdown():
    print("Shutting down bot gracefully...")
    await client.close()


# Graceful shutdown handler
async def shutdown():
    print("Shutting down bot gracefully...")
    await client.close()

def signal_handler(signal, frame):
    print("attempting to shut bot down...")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown())

signal.signal(signal.SIGINT, signal_handler)

def main():
    # Start the bot
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
