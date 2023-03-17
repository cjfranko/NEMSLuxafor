import discord
import requests
import json
import socket
import datetime
import os

client = discord.Client(intents=discord.Intents.default())

# Get the path of the directory containing the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path of the JSON file in the same directory
json_file_path = os.path.join(script_dir, 'config.json')

# Load the JSON data from the file
with open(json_file_path, 'r') as f:
    data = json.load(f)


token = data['token']
LUXAFOR_API_TOKEN = data['luxafor']
COLOR_MAP = {
    "NEMS CRITICAL": "red",
    "NEMS OK": "green",
    "NEMS TESTING": "magenta",
    "NEMS UNKNOWN": "blue",
    "NEMS WARNING": "yellow"
}
dischannelID = data['channelID']
thishost = socket.gethostname()

@client.event
async def on_ready():
    channel = client.get_channel(int(dischannelID))
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{current_time} - CHANNELID: {dischannelID} LUXAFOR ID: {LUXAFOR_API_TOKEN}')
    print(f'{current_time} - Bot Logged in as {client.user.name} to {dischannelID}')
    async def send_gif():
        await channel.send("https://media.tenor.com/-z2KfO5zAckAAAAC/hello-there-baby-yoda.gif")
    await send_gif()
    await channel.send(f'We logged in at {current_time}\nWe are running NEMS Warning Luxafor flag bot on {thishost} \nAnd the Luxafor UserID is {LUXAFOR_API_TOKEN}')
    url = f"https://api.luxafor.com/webhook/v1/actions/pattern"
    data = {
        "userId": LUXAFOR_API_TOKEN,
        "actionFields":{
            "pattern": "white wave"
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        channel = client.get_channel(int(dischannelID))
        print(f'{current_time} - Sent test to Luxafor Flag using set UserID {LUXAFOR_API_TOKEN}')
        await channel.send(f'Logged into Luxafor API Successfully! - Sent Test Pattern')
    else:
        print(f'Failed to set the flag via API, got status code {response.status_code}\n Check the Luxafor Webhook is active and the ID is set correctly')
        await channel.send(f'!!!Failed to set the flag via API, got status code {response.status_code}!!!\n!!!Check the Luxafor Webhook is active and the ID is set correctly!!!')

@client.event
async def on_message(message):
    author_name = str(message.author.name)
    if author_name in COLOR_MAP:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        color = COLOR_MAP[author_name]
        url = f"https://api.luxafor.com/webhook/v1/actions/solid_color"
        data = {
            "userId": LUXAFOR_API_TOKEN,
            "actionFields": {
                "color": color
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        print(f'{current_time} - {author_name} - Sending API FLAG Color: {color} to {LUXAFOR_API_TOKEN}')
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            channel = client.get_channel(int(dischannelID))
        else:
            print(f'{current_time} -Failed to set colour to {color}, got status code {response.status_code}')

client.run(token)
