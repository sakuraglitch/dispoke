import discord
from discord.ext import commands, tasks
import random
from datetime import datetime
import json
import os

# Set up your bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True  # For trading and balance

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None, case_insensitive=True)

import json
import os

# File path where the data is saved
DATA_FILE_PATH = 'bot_data.json'

# Global variable to hold bot data (trainer data, Pokémon, and Pokédex)
bot_data = {
    'user_pokemon_data': {},  # Stores Pokémon data by user ID
    'user_pokedex': {},        # Stores Pokédex entries by user ID (set of Pokémon names)
    'next_pokemon_id': 1       # Tracks the next Pokémon ID to assign globally
}

# Function to load the data from the file
def load_data():
    global bot_data
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, 'r') as file:
                bot_data = json.load(file)
                # Convert lists back to sets for Pokédex
                bot_data['user_pokedex'] = {key: set(value) for key, value in bot_data.get('user_pokedex', {}).items()}
        except (json.JSONDecodeError, KeyError):
            print("⚠️ Error: Corrupted JSON file. Resetting data.")
            bot_data = {'user_pokemon_data': {}, 'user_pokedex': {}, 'next_pokemon_id': 1}
    else:
        bot_data = {'user_pokemon_data': {}, 'user_pokedex': {}, 'next_pokemon_id': 1}

# Function to save data to the file
def save_data():
    global bot_data
    # Convert sets to lists before saving to JSON
    bot_data['user_pokedex'] = {key: list(value) for key, value in bot_data['user_pokedex'].items()}
    
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(bot_data, file, indent=4)

# Load data when the bot starts
load_data()

# All Gen 1 Pokémon with their sprites (image URLs)
pokemon_list = {
    "OG Bulbasaur": "https://img.pokemondb.net/sprites/red-blue/normal/bulbasaur.png",
    "Bulbasaur": "https://img.pokemondb.net/sprites/silver/normal/bulbasaur.png",
    "Shiny Bulbasaur Old": "https://img.pokemondb.net/sprites/silver/shiny/bulbasaur.png",
    "3rd Gen Bulbasaur": "https://img.pokemondb.net/sprites/ruby-sapphire/normal/bulbasaur.png",
    "Shiny Bulbasaur 3rd gen": "https://img.pokemondb.net/sprites/ruby-sapphire/shiny/bulbasaur.png",
    "Bulbasaur HGSS": "https://img.pokemondb.net/sprites/heartgold-soulsilver/normal/bulbasaur.png",
    "Shiny Bulbasaur HGSS": "https://img.pokemondb.net/sprites/heartgold-soulsilver/shiny/bulbasaur.png",
    "Shiny Bulbasaur Animated": "https://img.pokemondb.net/sprites/black-white/anim/shiny/bulbasaur.gif",
    "Bulbasaur XY": "https://img.pokemondb.net/sprites/x-y/normal/bulbasaur.png",
    "Shiny Bulbasaur XY": "https://img.pokemondb.net/sprites/x-y/shiny/bulbasaur.png",
    "Bulbasaur ORAS": "https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/bulbasaur.png",
    "Shiny Bulbasaur ORAS": "https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/shiny/bulbasaur.png",
    "Bulbasaur Home": "https://img.pokemondb.net/sprites/home/normal/bulbasaur.png",
    "Ivysaur": "https://img.pokemondb.net/sprites/red-blue/normal/ivysaur.png",
    "Venusaur": "https://img.pokemondb.net/sprites/red-blue/normal/venusaur.png",
    "Charmander": "https://img.pokemondb.net/sprites/red-blue/normal/charmander.png",
    "Charmeleon": "https://img.pokemondb.net/sprites/red-blue/normal/charmeleon.png",
    "Charizard": "https://img.pokemondb.net/sprites/red-blue/normal/charizard.png",
    "Squirtle": "https://img.pokemondb.net/sprites/red-blue/normal/squirtle.png",
    "Wartortle": "https://img.pokemondb.net/sprites/red-blue/normal/wartortle.png",
    "Blastoise": "https://img.pokemondb.net/sprites/red-blue/normal/blastoise.png",
    "Pikachu": "https://img.pokemondb.net/sprites/red-blue/normal/pikachu.png",
    "Jigglypuff": "https://img.pokemondb.net/sprites/red-blue/normal/jigglypuff.png",
    "Meowth": "https://img.pokemondb.net/sprites/red-blue/normal/meowth.png",
    "Psyduck": "https://img.pokemondb.net/sprites/red-blue/normal/psyduck.png",
    "Eevee": "https://img.pokemondb.net/sprites/red-blue/normal/eevee.png"
}

# Limited edition Pokémon with an expiration date
limited_edition_pokemon = {
    "vaporeon-skitty": {
        "sprite_url": "https://i.ibb.co/QjFXnx67/134-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "yanma-skitty": {
        "sprite_url": "https://i.ibb.co/XxPVR2f6/193-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "girafarig-skitty": {
        "sprite_url": "https://i.ibb.co/wN0518LN/203-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "glaceon-skitty": {
        "sprite_url": "https://i.ibb.co/JFG1zMZ1/272-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "mawile-skitty": {
        "sprite_url": "https://i.ibb.co/ccVdkSdt/300-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "zorua-skitty": {
        "sprite_url": "https://i.ibb.co/JbdwbWH/399-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "liepard-skitty": {
        "sprite_url": "https://i.ibb.co/pB6PjH79/469-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "swirlix-skitty": {
        "sprite_url": "https://i.ibb.co/gZ7KSZ64/491-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "scraggy-skitty": {
        "sprite_url": "https://i.ibb.co/fVMkFxV7/493-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "furfrou-skitty": {
        "sprite_url": "https://i.ibb.co/5x40hLWZ/ADD-ADD.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "skitty": {
        "sprite_url": "https://i.ibb.co/tMpxpCL1/Skitty-Float.png",
        "expiration_date": datetime(2025, 3, 31),  # Set the expiration date (YYYY, MM, DD)
    },
    "Shiny Charizard Gen 2": {
        "sprite_url": "https://img.pokemondb.net/sprites/gold/shiny/charizard.png",
        "expiration_date": datetime(2024, 10, 5),
    },
    "Shiny Bulbasaur Animated": {
        "sprite_url": "https://img.pokemondb.net/sprites/black-white/anim/shiny/bulbasaur.gif",
        "expiration_date": datetime(2024, 3, 31),
    }
}

# Define rarity-based spawn odds using fractions (e.g., 1/101 odds)
rarity = {
    "vaporeon-skitty": 750,  # 1/750 odds
    "glaceon-skitty": 750,  # 1/750 odds
    "yanma-skitty": 500,  # 1/500 odds
    "girafarig-skitty": 500,  # 1/500 odds
    "zorua-skitty": 1000,  # 1/1000 odds
    "yanma-skitty": 500,  # 1/500 odds
    "liepard-skitty": 500,  # 1/500 odds
    "scraggy-skitty": 500,  # 1/500 odds
    "swirlix-skitty": 500,  # 1/500 odds
    "furfrou-skitty": 500,  # 1/500 odds
    "skitty": 100,  # 1/100 odds
    "mawile-skitty": 500,  # 1/500 odds
    "OG Bulbasaur": 100,  # 1/100 odds
    "Bulbasaur": 100,  # 1/100 odds
    "Shiny Bulbasaur Old": 4096,  # 1/4096 odds
    "3rd Gen Bulbasaur": 250,  # 1/250 odds
    "Shiny Bulbasaur 3rd gen": 4096,  # 1/4096 odds
    "Bulbasaur HGSS": 150,  # 1/150 odds
    "Shiny Bulbasaur HGSS": 4096,  # 1/2048 odds
    "Shiny Bulbasaur Animated": 10000,  # 1/10000 odds after
    "Bulbasaur XY": 200,  # 1/200 odds
    "Shiny Bulbasaur XY": 4096,  # 1/4096 odds
    "Bulbasaur ORAS": 150,  # 1/150 odds
    "Shiny Bulbasaur ORAS": 8192,  # 1/4096 odds
    "Bulbasaur Home": 101,  # 1/8192 odds
    "Ivysaur": 100,  # 1/100 odds
    "Venusaur": 75,  # 1/75 odds
    "Charmander": 151,  # 1/151 odds
    "Charmeleon": 100,  # 1/100 odds
    "Charizard": 500,  # 1/500 odds
    "Squirtle": 100,  # 1/100 odds
    "Wartortle": 100,  # 1/100 odds
    "Blastoise": 75,  # 1/75 odds
    "Pikachu": 90,  # 1/90 odds
    "Jigglypuff": 100,  # 1/100 odds
    "Meowth": 100,  # 1/100 odds
    "Psyduck": 85,  # 1/85 odds
    "Eevee": 70,  # 1/70 odds
    "Colored Bulbasaur OG": 1000,  # 1/1000 odds
    "Yellow Bulbasaur BW": 200,  # 1/200 odds
}
# Sample trainer's Pokémon list (Each Pokémon is stored uniquely)
trainer_pokemon = []
caught_pokemon = []
users_data = {}
active_pokemon = {}
spawn_channels = []  # Replace with your channel IDs


# Function to generate random IVs (0-31 for each stat)
def generate_ivs():
    return {
        "HP": random.randint(0, 31),
        "Attack": random.randint(0, 31),
        "Defense": random.randint(0, 31),
        "Sp. Atk": random.randint(0, 31),
        "Sp. Def": random.randint(0, 31),
        "Speed": random.randint(0, 31)
    }
# Function to spawn Pokémon in a random channel
async def spawn_pokemon(ctx):
    # Combine regular and limited edition Pokémon eligible for spawning
    available_pokemon = list(pokemon_list.items())
    
    # Add limited edition Pokémon if they haven't expired
    for name, data in limited_edition_pokemon.items():
        if datetime.now() <= data["expiration_date"]:
            available_pokemon.append((name, data["sprite_url"]))

    # If no Pokémon available (just in case all limited are expired)
    if not available_pokemon:
        print("No available Pokémon to spawn.")
        return

    channel = bot.get_channel(random.choice(spawn_channels))
    if channel is None:
        print("Failed to retrieve channel. Check if the channel ID is correct.")
        return

    # Select random Pokémon to spawn
    pokemon, sprite_url = random.choice(available_pokemon)
    embed = discord.Embed(title=f"A wild {pokemon} appeared!", description="Type `!catch` to catch it!")
    embed.set_image(url=sprite_url)
    message = await channel.send(embed=embed)

    active_pokemon[message.id] = pokemon

    def check(m):
        return m.content.lower() == '!catch' and m.channel == channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        user = msg.author
        if user not in caught_pokemon:
            caught_pokemon[user] = []
        # Add Pokémon with its IVs to the caught list
        ivs = generate_ivs()
        caught_pokemon[user].append({"name": pokemon, "ivs": ivs})
        await channel.send(f"{user.mention} caught {pokemon} with IVs: {ivs}!")
        del active_pokemon[message.id]
    except:
        await channel.send(f"The wild {pokemon} ran away!")
        del active_pokemon[message.id]

# Randomly spawn Pokémon every few minutes
@tasks.loop(minutes=random.randint(1, 5))
async def random_spawn():
    await spawn_pokemon()

# manual spawn command
@bot.command()
async def spawn(ctx):
    spawn_channels = bot_data.get("spawn_channels", [])

    if not spawn_channels:
        await ctx.send("⚠️ No spawn channels are set! Use `!addchannel` first.")
        return

    channel_id = random.choice(spawn_channels)
    channel = bot.get_channel(channel_id)

    if not channel:
        await ctx.send("⚠️ Could not find the selected spawn channel.")
        return

    # Get Pokémon name & image
    pokemon_name, pokemon_image = await spawn_pokemon()

    # Create Embed
    embed = discord.Embed(
        title="A wild Pokémon appeared! 👀",
        description=f"Use `!catch {pokemon_name}` to catch it!",
        color=discord.Color.green()
    )
    embed.set_image(url=pokemon_image)

    await channel.send(embed=embed)
# latency check
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
# Release Command - allows users to release a specific Pokémon
@bot.command()
async def release(ctx, pokemon_name: str):
    user = ctx.author
    if user in caught_pokemon and pokemon_name in caught_pokemon[user]:
        caught_pokemon[user].remove(pokemon_name)
        await ctx.send(f"{user.mention} released {pokemon_name}.")
    else:
        await ctx.send(f"{user.mention}, you don't have {pokemon_name} or it doesn't exist!")

# Initialize an empty dictionary to hold pokedex data for each user
user_pokedex = {}

import random

@bot.command()
async def catch(ctx, pokemon_name: str):
    try:
        # Check if the user has provided a valid Pokémon name
        if not pokemon_name:
            await ctx.send("You need to specify a Pokémon name!")
            return

        # Generate a unique Pokémon ID based on the next available ID
        pokemon_id = bot_data['next_pokemon_id']

        # Increment the next Pokémon ID for future use
        bot_data['next_pokemon_id'] += 1

        # Generate random stats for the Pokémon
        ivs = {
            "HP": random.randint(0, 31),
            "Attack": random.randint(0, 31),
            "Defense": random.randint(0, 31),
            "Sp. Atk": random.randint(0, 31),
            "Sp. Def": random.randint(0, 31),
            "Speed": random.randint(0, 31)
        }
        
        # Set the level for the Pokémon
        level = random.randint(1, 100)

        # Create the caught Pokémon object
        caught_pokemon = {
            "id": pokemon_id,
            "name": pokemon_name,
            "level": level,
            "ivs": ivs
        }

        # Add the Pokémon to the user's data
        user_id = str(ctx.author.id)

        # Initialize user data if not already there
        if user_id not in bot_data['user_pokemon_data']:
            bot_data['user_pokemon_data'][user_id] = []

        bot_data["caught_pokemon"].append(pokemon_name)

        # Add Pokémon name to user's Pokédex
        if user_id not in bot_data['user_pokedex']:
            bot_data['user_pokedex'][user_id] = set()

        bot_data['user_pokedex'][user_id].add(pokemon_name)

        # Convert sets to lists before saving to JSON
        bot_data['user_pokedex'] = {key: list(value) for key, value in bot_data['user_pokedex'].items()}

        # Save data after updating it
        save_data()

        await ctx.send(f"Successfully caught {pokemon_name} (Lvl {level}) with ID: {pokemon_id} and IVs: {ivs}!")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def pokedex(ctx):
    try:
        user_id = str(ctx.author.id)

        if user_id not in bot_data['user_pokedex'] or not bot_data['user_pokedex'][user_id]:
            await ctx.send("You haven't caught any Pokémon yet!")
        else:
            pokedex = bot_data['user_pokedex'][user_id]
            await ctx.send(f"Your Pokédex: {', '.join(pokedex)}")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def team(ctx):
    try:
        user_id = str(ctx.author.id)

        if user_id not in bot_data['user_pokemon_data'] or not bot_data['user_pokemon_data'][user_id]:
            await ctx.send("Your team is empty!")
            return

        response = "**Your Pokémon Team:**\n"
        for i, pokemon in enumerate(bot_data['user_pokemon_data'][user_id], 1):
            ivs_text = ", ".join(f"{stat} {val}" for stat, val in pokemon["ivs"].items())
            response += f"{i}. {pokemon['name']} (Lvl {pokemon['level']}) - IVs: {ivs_text}\n"
        await ctx.send(response)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



# Command to add a channel ID to the bot's list for the guild
@bot.command()
async def addchannel(ctx):
    if ctx.guild is None:
        await ctx.send("This command can only be used in a server (guild).")
        return

    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("You don't have permission to manage channels.")
        return

    channel_id = ctx.channel.id

    # Ensure 'spawn_channels' exists in bot_data
    if "spawn_channels" not in bot_data:
        bot_data["spawn_channels"] = []

    if channel_id not in bot_data["spawn_channels"]:
        bot_data["spawn_channels"].append(channel_id)
        save_data()  # Save changes
        await ctx.send(f"✅ {ctx.channel.mention} has been added to the spawn channels!")
    else:
        await ctx.send(f"⚠️ {ctx.channel.mention} is already in the spawn channels list!")

@bot.command()
async def checkchannels(ctx):
    spawn_channels = bot_data.get("spawn_channels", [])
    if not spawn_channels:
        await ctx.send("⚠️ No spawn channels have been set.")
    else:
        channel_names = [bot.get_channel(cid).mention for cid in spawn_channels if bot.get_channel(cid)]
        await ctx.send(f"📌 Spawn Channels: {', '.join(channel_names)}")


@bot.command()
async def help(ctx, command: str = None):
    if command is None:
        embed = discord.Embed(title="📜 Pokémon Bot Commands", color=discord.Color.blue())
        embed.add_field(name="🔹 `!catch <pokemon_name>`", value="Catch a Pokémon and add it to your team.", inline=False)
        embed.add_field(name="🔹 `!spawn`", value="Spawn a random Pokémon to encounter.", inline=False)
        embed.add_field(name="🔹 `!team`", value="View your current Pokémon team.", inline=False)
        embed.add_field(name="🔹 `!pokedex`", value="View your caught Pokémon in the Pokédex.", inline=False)
        embed.add_field(name="🔹 `!addchannel`", value="Adds the current channel to the bot's spawn list.", inline=False)
        embed.add_field(name="ℹ️ More Info", value="Use `!help <command>` for more details.", inline=False)
        
        await ctx.send(embed=embed)
    else:
        command_details = {
            "catch": "**!catch <pokemon_name>** - Catch a Pokémon and add it to your team.\nExample: `!catch Pikachu`",
            "spawn": "**!spawn** - Spawn a random Pokémon to encounter.\nExample: `!spawn`",
            "team": "**!team** - View your current Pokémon team.\nExample: `!team`",
            "pokedex": "**!pokedex** - View your caught Pokémon in the Pokédex.\nExample: `!pokedex`",
            "addchannel": "**!addchannel** - Adds the current channel to the spawn list.\nExample: `!addchannel`"
        }

        if command.lower() in command_details:
            await ctx.send(command_details[command.lower()])
        else:
            await ctx.send(f"❌ Command `{command}` not found. Use `!help` for a list of available commands.")


# Bot event when it's ready
@bot.event
async def on_ready():
            print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run bot
bot.run('')
