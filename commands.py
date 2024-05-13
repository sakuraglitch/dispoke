import discord
from discord.ext import commands
import random

from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)


class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

        @commands.command()
        async def start(message, caught_pokemons, user_balances):
                if message.author.id not in caught_pokemons:
                    caught_pokemons[message.author.id] = {}
                if message.author.id not in user_balances:
                    user_balances[message.author.id] = 0
                await message.channel.send('Your Pokémon journey begins!')

    @commands.command()
    async def catch(message, caught_pokemons, all_pokemons, shiny_odds):
        if message.author.id not in caught_pokemons:
            caught_pokemons[message.author.id] = {}
            await message.channel.send('Please use the `!start` command to begin your journey!')

            pokemon = random.choice(all_pokemon)
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
            await message.channel.send('You caught a shiny') if shiny else \
                await message.channel.send('')

            return

        @commands.command()
        async def pokemon(self, ctx):
            if message.content.startswith('!pokemon') or message.content.startswith('!p'):
                if message.author.id not in caught_pokemons or not caught_pokemons[message.author.id]:
                    await message.channel.send('You have not caught any Pokémon yet!')
                return

            pokemon_list = ', '.join(caught_pokemons[message.author.id].keys())

            @commands.command()
            async def pokemon(self, ctx):
                message.content.startswith('!info') or message.content.startswith('!i')
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

            @commands.command()
            async def pokemon(self, ctx):
                pokemon_data = caught_pokemons[message.author.id][pokemon_name]
            shiny_str = "Shiny" if pokemon_data['shiny'] else "Not shiny"
            legendary_str = "Legendary" if pokemon_data['legendary'] else "Not legendary"
            stats_str = "HP: {pokemon_data['stats']['hp']}\nAttack: {pokemon_data['stats']['attack']}\nDefense: {pokemon_data['stats']['defense']}\nSpecial Attack: {pokemon_data['stats']['sp_atk']}\nSpecial Defense: {pokemon_data['stats']['sp_def']}\nSpeed: {pokemon_data['stats']['speed']}"
            await message.channel.send(f'{pokemon_name} ({shiny_str}, {legendary_str})\nStats:\n{stats_str}')