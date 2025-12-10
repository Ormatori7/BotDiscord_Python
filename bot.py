from dotenv import load_dotenv
load_dotenv()

from discord import app_commands

import random
import discord
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree_commands = app_commands.CommandTree(client)

#/sdv pour avoir le lien
@tree_commands.command(name="sdv", description="Avoir le lien du site supdevinci")
async def sdv_command(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.supdevinci.fr")

#/games pour avoir les 5 jeux
@tree_commands.command(name="games", description="Avoir top 5 jeux")
async def games_command(interaction: discord.Interaction):
    embed = discord.Embed(title=("top 5 des jeux"))
    embed.add_field(name="top1", value="minecraft")
    embed.add_field(name="top1", value="minecraft")
    embed.add_field(name="top1", value="minecraft")
    embed.add_field(name="top1", value="minecraft")
    embed.add_field(name="top1", value="minecraft")
    await interaction.response.send_message(embed=embed)

#generateur de meme
@tree_commands.command(name="meme", description="avoir un meme")
async def meme_command(interaction: discord.Interaction):
    memes = [
        "https://www.dieudogifs.be/thumbs/086372d24b2fad3ac90185181a11699a.jpg"
        
            ]
    meme = random.choice(memes)
    await interaction.response.send_message(meme)

#ban qlq 
@tree_commands.command(name="aurevoir", description="dehors")
async def dehors_command(interaction: discord.Interaction, member: discord.Member):
    await member.send("son gros crane a lui la!")
    await member.kick(reason="ton gros crane la")
    await interaction.response.send_message("arrache ta tete !")

    await interaction.response.send_message("la feinte était tlm puissante qu'il s'est fait ban ")


@client.event
async def on_ready():
    await tree_commands.sync() #synchronise les commandes avec le serveur discord
    print(f'lancement du bot {client.user}')


@client.event
async def on_member_join(member: discord.Member):
    print("nouveau membre a rejoint le discord")
    #envoyer un mesg dans le salon #nouveau membre
    member_channel = client.get_channel(1445360670395596922)
    await member_channel.send("nouveau membre sur le serv")

    #envoyer un dm
    await member.send("bienvenue sur le serveur")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$trkl?'):
        await message.channel.send('Oh bieng!')


#msg interdit
@client.event
async def on_message(message):
        if message.author == client.user:
             return
        
        #anti insulte
        words_blacklist = ["francais", "wee"]

        #recup chaque mot
        for mot in message.content.split():
            if mot in words_blacklist: 
                await message.delete()
                await message.channel.send("ca va te goumer guette bien")
                break

client.run(os.getenv('DISCORD_TOKEN'))
