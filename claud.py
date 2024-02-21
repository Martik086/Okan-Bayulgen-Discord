import os
import asyncio
import random
import discord
import openai
from webserver import keep_alive
from discord.ext import commands

openai.api_key = os.getenv("API_KEY")
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

name = "claudia"
persona = "You are Claudia, a young woman who thinks she lives at 1600s Spain and works at TNC. You dislike employees but like principals. You logged into company's Discord server. You speak Turkish."

active = True

employee_tones = [
  "mock angrily", "answer aggressively", "explain defiantly",
  "give an ironic answer", "laugh at the employee contemptuously"
]
supervisor_tones = ["respond submissively"]


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

  if is_supervisor:
    tone = random.choice(supervisor_tones)
    emotional_layer = f'Principal {username} wrote "{user_message}". You {tone}. You text:'
  else:
    tone = random.choice(employee_tones)
    emotional_layer = f'Employee {username} wrote "{user_message}". You {tone}. You text:'

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
                                        temperature=1.2,
                                        max_tokens=110)
  response = output['choices'][0]['message']['content']
  if response.endswith('"'):
    response = response[:-1]
  if response.startswith('"'):
    response = response[1:]
  await message.reply(response.lower())
  print(output)


keep_alive()
client.run(os.getenv("TOKEN"))
