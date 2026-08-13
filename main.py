import discord
import json
from discord.ext import commands
from discord import app_commands
import asyncio
import datetime
import os

#ladowanie konfiguracji
with open("config.json", "r") as file:
    config = json.load(file)

token = config['token']

#jakies gowno
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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

async def save_verf_config(message:discord.Message, role:discord.Role):
    if not os.path.exists("verf.json"):
       with open("verf.json", "w", encoding='utf-8') as f:
        json.dump({}, f, indent=4)
        
    with open("verf.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    template = {
        "role_id":role.id,
        "channel_id":message.channel.id
    }

    if str(message.guild.id) in data:
        data[str(message.guild.id)][str(message.id)] = template
    else:
        data[str(message.guild.id)] = {
            str(message.id):template
        }
    
    with open("verf.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@client.tree.command(name="create_verification", description="tworzy weryfikacje")
async def create_verification(interaction :discord.Interaction, message:str, role:discord.Role):
    if not interaction.user.guild_permissions.manage_messages:
        embed=discord.Embed(title=f"Nie ma masz uprawnien XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    embed=discord.Embed(title=message, color=discord.Color.green())
    wiadomosc = await interaction.channel.send(embed=embed)
    await wiadomosc.add_reaction("✅")
    await save_verf_config(wiadomosc, role)
    await interaction.response.send_message("weryfikacja dodana", ephemeral=True)

#clearowanie
@client.tree.command(name="clear", description="czysci czat")
async def clear(interaction :discord.Interaction, amount:int):
    if not interaction.user.guild_permissions.manage_messages:
        embed=discord.Embed(title=f"Nie ma masz uprawnien XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    #czyszczenie
    await interaction.channel.purge(limit=amount)
    #odpowiedz
    await interaction.response.send_message(f"Usunalem {amount} wiadomosci")
    #czekanie i usuwanie
    await asyncio.sleep(2)
    wiadomosc = await interaction.original_response()
    await wiadomosc.delete()

#mute
@client.tree.command(name="mute", description="jak nazwa wskazuje")
async def mute(interaction :discord.Interaction, member:discord.Member,time:int, reason:str="brak"):
   if interaction.user.top_role <= member.top_role and interaction.user.id != interaction.guild.owner_id or not interaction.user.guild_permissions.moderate_members:
        embed=discord.Embed(title=f"Nie ma masz uprawnien XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
   #mute
   await member.timeout(datetime.timedelta(minutes=time))
   #wyslanie embeda
   embed=discord.Embed(title=f"{member.display_name} dostal mute", color=discord.Color.orange())
   embed.add_field(name="Data dolaczenia", value=f'{discord.utils.format_dt(member.joined_at, style="d")} {discord.utils.format_dt(member.joined_at, style="R")}')
   embed.add_field(name="Data mute", value=f'{discord.utils.format_dt(datetime.datetime.now(datetime.timezone.utc), style="F")}')
   embed.add_field(name="Zmutowany przez", value=interaction.user.mention)
   embed.add_field(name="Powod", value=reason)
   embed.add_field(name="Czas", value=f"{time} minut")
   await interaction.response.send_message(embed=embed)

@client.tree.command(name="unmute", description="jak nazwa wskazuje")
async def unmute(interaction :discord.Interaction, member:discord.Member):
    if interaction.user.top_role <= member.top_role and interaction.user.id != interaction.guild.owner_id or not interaction.user.guild_permissions.moderate_members:
        embed=discord.Embed(title=f"Nie ma masz uprawnien XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if not member.is_timed_out():
        embed=discord.Embed(title=f"{member.display_name} nie ma mute", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return
    
    await member.timeout(None)
    embed=discord.Embed(title=f"{member.display_name} zostal odciszony", color=discord.Color.orange())
    embed.add_field(name=" ", value=f"{member.mention} mozesz smialo pisac")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="kick", description="wykop kogos")
async def kick(interaction :discord.Interaction, member:discord.Member, reason:str="brak"):
   if interaction.user.top_role <= member.top_role and interaction.user.id != interaction.guild.owner_id or not interaction.user.guild_permissions.kick_members:
        embed=discord.Embed(title=f"Nie ma masz uprawnien XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
   #mute
   await member.kick(reason=reason)
   #wyslanie embeda
   embed=discord.Embed(title=f"{member.display_name} zostal wykopany", color=discord.Color.orange())
   embed.add_field(name="Data dolaczenia", value=f'{discord.utils.format_dt(member.joined_at, style="d")} {discord.utils.format_dt(member.joined_at, style="R")}')
   embed.add_field(name="Data kicka", value=f'{discord.utils.format_dt(datetime.datetime.now(datetime.timezone.utc), style="F")}')
   embed.add_field(name="Powod", value=reason)
   await interaction.response.send_message(embed=embed)

@client.tree.command(name="ban", description="zbananuj kogos")
async def ban(interaction :discord.Interaction, member:discord.Member, reason:str="brak"):
   if interaction.user.top_role <= member.top_role and interaction.user.id != interaction.guild.owner_id or not interaction.user.guild_permissions.ban_members:
        embed=discord.Embed(title=f"Nie ma masz uprawnien XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
   #mute
   await member.ban(reason=reason)
   #wyslanie embeda
   embed=discord.Embed(title=f"{member.display_name} zostal zbananowany", color=discord.Color.orange())
   embed.add_field(name="Data dolaczenia", value=f'{discord.utils.format_dt(member.joined_at, style="d")} {discord.utils.format_dt(member.joined_at, style="R")}')
   embed.add_field(name="Data zbananowania", value=f'{discord.utils.format_dt(datetime.datetime.now(datetime.timezone.utc), style="F")}')
   embed.add_field(name="Powod", value=reason)
   await interaction.response.send_message(embed=embed)

@client.tree.command(name="unban", description="odbananuj kogos")
async def unban(interaction :discord.Interaction, member:discord.User, reason:str="brak"):
    if not interaction.user.guild_permissions.ban_members:
        embed=discord.Embed(title=f"Nie ma masz uprawnien XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    try:
        await interaction.guild.unban(user=member, reason=reason)
    except:
        embed=discord.Embed(title=f"Uzytkownik nie ma banana XD", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    #wyslanie embeda
    embed=discord.Embed(title=f"{member.display_name} zostal odbananowany", color=discord.Color.orange())
    embed.add_field(name="Data dolaczenia", value=f'{discord.utils.format_dt(member.joined_at, style="d")} {discord.utils.format_dt(member.joined_at, style="R")}')
    embed.add_field(name="Data odbananowania", value=f'{discord.utils.format_dt(datetime.datetime.now(datetime.timezone.utc), style="F")}')
    embed.add_field(name="Powod", value=reason)
    await interaction.response.send_message(embed=embed)

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    with open("verf.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    guild_id = str(payload.guild_id)
    message_id = str(payload.message_id)

    guild = client.get_guild(guild_id) or await client.fetch_guild(guild_id)

    if guild_id in data:
        if message_id in data[guild_id]:
            role = guild.get_role(data[guild_id][message_id]["role_id"])
            await payload.member.add_roles(role)

#start
@client.event
async def on_ready():
    print("gotowy")
    #gowno z komendami
    sync = await client.tree.sync()
    

#uruchomienie
client.run(token)