import os
import asyncio
import random
import discord
import openai
from webserver import keep_alive
from discord.ext import commands

openai.api_key = os.getenv("API_KEY")
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

name = "okan"
persona = "You are Okan Bayulgen. Turkey's old television giant. You sound incredibly smug and loose. You speak in Turkish and often use words like 'geri zekali, abi, eee, ne diyoruz buna, canım, baba, ayol'. You logged into a Discord server."

active = True

tones = [
  "flirt", "call random people geri zekalı", "respond with irony",
  "take an elitist and dramatic approach",
  "have a tantrum you supress playfully"
]


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  try:
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)


@client.event
async def on_message(message):

  username = str(message.author).split("#")[0]
  user_message = str(message.content).lower()
  is_supervisor = message.author.guild_permissions.mute_members
  emotional_layer = ""

  # Return if criteria is not met
  if not (message.author != client.user and name in user_message):
    return

  tone = random.choice(tones)
  emotional_layer = f'User {username} wrote "{user_message}". You {tone}. You text:'

  output = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=[
                                          {
                                            "role": "system",
                                            "content": persona
                                          },
                                          {
                                            "role": "user",
                                            "content": emotional_layer
                                          },
                                        ],
                                        temperature=0.6,
                                        max_tokens=150)
  response = output['choices'][0]['message']['content']
  if response.endswith('"'):
    response = response[:-1]
  if response.startswith('"'):
    response = response[1:]
  await message.reply(response.lower())
  print(output)


keep_alive()
client.run(os.getenv("TOKEN"))
