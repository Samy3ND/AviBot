import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import json

# Load environment variables
load_dotenv()

# Get tokens from .env
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# API function
def get_airport_info(icao):
    url = f"http://api.aviationstack.com/v1/airports?access_key={AVIATIONSTACK_API_KEY}&icao_code={icao}"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    data = response.json()
    if not data['data']:
        return None
    airport = data['data'][0]
    city = airport.get('city_iata_code', 'Unknown city')
    if city == 'LON':
        city = 'London'
    return {
        "name": airport.get("airport_name", "Unknown"),
        "icao": airport.get("icao_code", icao),
        "iata": airport.get("iata_code", "N/A"),
        "location": f"{city}, {airport.get('country_name', 'Unknown country')}",
        "timezone": airport.get("timezone", "N/A"),
    }

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def airport(ctx, *, icao_code):
    await ctx.send("🔍 Fetching airport data...")
    data = get_airport_info(icao_code.upper())
    if not data:
        await ctx.send("❌ Airport not found or API error.")
        return
    embed = discord.Embed(
        title=f"{data['name']} ({data['icao']}/{data['iata']})",
        description=f"📍 **Location:** {data['location']}\n🕒 **Timezone:** {data['timezone']}",
        color=0x3498db
    )
    await ctx.send(embed=embed)

# Aircraft data
with open("aircraft_data.json", "r") as file:
    aircraft_data = json.load(file)

@bot.command()
async def aircraft(ctx, code: str):
    code = code.upper()
    if code in aircraft_data:
        data = aircraft_data[code]
        response = (
            f"**{data['name']} ({code})**\n"
            f"🛠️ Manufacturer: {data['manufacturer']}\n"
            f"✈️ Type: {data['type']}\n"
            f"🎯 Role: {data['role']}"
        )
    else:
        response = f"❌ Aircraft code `{code}` not found."
    await ctx.send(response)

bot.run(DISCORD_TOKEN)
