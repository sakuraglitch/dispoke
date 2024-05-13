import discord
import random
from discord.ext import commands
from commands import MyCommands
# Define the Pokemon data
all_pokemons = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard",
    "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree",
    "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot",
    "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok",
    "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina",
    "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable",
    "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat",
    "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat",
    "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck",
    "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag",
    "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop",
    "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool",
    "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash",
    "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo",
    "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder",
    "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee",
    "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute",
    "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung",
    "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela",
    "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu",
    "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar",
    "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto",
    "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte",
    "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno",
    "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew"
]
MyCommands = MyCommands(commands.Cog)
# Dictionary to store caught Pokémon and their stats
caught_pokemons = {}

# Dictionary to store user balances (Pokeyen)
user_balances = {}

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

shiny_odds = 8192  # Shiny odds
trading = False  # Variable to track if a trade is ongoing

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!start'):
        if message.author.id not in caught_pokemons:
            caught_pokemons[message.author.id] = {}  # Initialize the dictionary for the user if not present
        if message.author.id not in user_balances:
            user_balances[message.author.id] = 0
        await message.channel.send('Your Pokémon journey begins!')

    if message.content.startswith('!catch'):
        if message.author.id not in caught_pokemons:
            caught_pokemons[message.author.id] = {}  # Initialize the dictionary for the user if not present
            await message.channel.send('Please use the `!start` command to begin your journey!')
            return

        "legendary" if is_legendary else ""
    pokemon = random.choice(all_pokemons)
    is_legendary = random.random() < 0.005  # 0.5% chance for legendary
    shiny = random.randint(1, shiny_odds) == 1
    if pokemon not in caught_pokemons[message.author.id]:
        caught_pokemons[message.author.id][pokemon] = {
            'shiny': shiny,
            'legendary': is_legendary,
            'stats': {
                'hp': random.randint(0, 31),
                'attack': random.randint(0, 31),
                'defense': random.randint(0, 31),
                'sp_atk': random.randint(0, 31),
                'sp_def': random.randint(0, 31),
                'speed': random.randint(0, 31)
            }
        }
    else:
        caught_pokemons[message.author.id][pokemon]['stats']['hp'] = random.randint(0, 31)

    if message.content.startswith('!pokemon') or message.content.startswith('!p'):
        if message.author.id not in caught_pokemons or not caught_pokemons[message.author.id]:
            await message.channel.send('You have not caught any Pokémon yet!')
            return
        await message.channel.send('You caught a shiny') if shiny else await message.channel.send('')

        pokemon_list = ', '.join(caught_pokemons[message.author.id].keys())
        await message.channel.send(f'Pokémons you have caught: {pokemon_list}')

    if message.content.startswith('!info') or message.content.startswith('!i'):
        if message.author.id not in caught_pokemons or not caught_pokemons[message.author.id]:
            await message.channel.send('You have not caught any Pokémon yet!')
            return

        if 'latest' in message.content:
            pokemon_name = list(caught_pokemons[message.author.id].keys())[-1]
        else:
            pokemon_id = int(message.content.split(' ')[1])
            if pokemon_id > len(caught_pokemons[message.author.id]) or pokemon_id < 1:
                await message.channel.send('Invalid Pokémon ID!')
                return
            pokemon_name = list(caught_pokemons[message.author.id].keys())[pokemon_id - 1]

        pokemon_data = caught_pokemons[message.author.id][pokemon_name]
        shiny_str = "Shiny" if pokemon_data['shiny'] else "Not shiny"
        legendary_str = "Legendary" if pokemon_data['legendary'] else "Not legendary"
        stats_str = f"HP: {pokemon_data['stats']['hp']}\nAttack: {pokemon_data['stats']['attack']}\nDefense: {pokemon_data['stats']['defense']}\nSpecial Attack: {pokemon_data['stats']['sp_atk']}\nSpecial Defense: {pokemon_data['stats']['sp_def']}\nSpeed: {pokemon_data['stats']['speed']}"
        await message.channel.send(f'{pokemon_name} ({shiny_str}, {legendary_str})\nStats:\n{stats_str}')

    elif message.content.startswith('!bal') or message.content.startswith('!balance'):
        if message.author.id not in user_balances:
            await message.channel.send('You have not started your journey yet!')
            return

        balance = user_balances[message.author.id]
        await message.channel.send(f'Your balance (Pokeyen): {balance}')

    elif message.content.startswith('!sel') or message.content.startswith('!select'):
        # Check if the message is during a trade
        # Handle selecting a Pokémon for trade
        pass

    elif message.content.startswith('!givemoney') or message.content.startswith('!gm'):
        # Check if the message is during a trade
        # Handle giving money during a trade
        pass

client.run('token')