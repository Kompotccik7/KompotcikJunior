import discord
import json
from discord.ext import commands
import asyncio

#ladowanie konfiguracji
with open("config.json", "r") as file:
    config = json.load(file)

token = config['token']

#jakies gowno
intents = discord.Intents.default()
intents.message_content = True

#klient
client = commands.Bot(command_prefix='!',intents=intents)

#pomoc
@client.tree.command(name="pomoc", description="pomocy ratunku")
async def help(interaction: discord.Interaction):   
    embed = discord.Embed(
        title="Pomoc",
        color=discord.Color.orange()
    ) 
    embed.add_field(
        name="1. Centrum wsparcia",
        value="https://centrumwsparcia.pl",
        inline=False
    )
    embed.add_field(
        name="2. strona do pomocy nwm",
        value="https://GiveAndGetHelp.com",
        inline=False
    )
    embed.add_field(
        name="3. jak jestes uzalezniony",
        value="https://PoradniaUzaleznienia.pl",
        inline=False
    )
    embed.add_field(
        name="4. Zawsze mozesz zadzwonic po policje albo karetke",
        value='''Pogotowie ratunkowe - 999
        Policja - 997''',
        inline=False
    )
    embed.set_footer(
        text="Mam nadzieje ze wiesz gdzie znalezc pomoc XD"
    )
    await interaction.response.send_message(embed=embed)

#clearowanie
@client.tree.command(name="clear", description="czysci czat")
async def clear(interaction :discord.Interaction, amount:int):
    #czyszczenie
    await interaction.channel.purge(limit=amount)
    #odpowiedz
    await interaction.response.send_message(f"Usunalem {amount} wiadomosci")
    #czekanie i usuwanie
    await asyncio.sleep(2)
    wiadomosc = await interaction.original_response()
    await wiadomosc.delete()

#start
@client.event
async def on_ready():
    print("gotowy")
    #gowno z komendami
    sync = await client.tree.sync()
    

#uruchomienie
client.run(token)