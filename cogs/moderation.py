import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client 
        

    @app_commands.command(name="aurevoir", description="dehors")
    async def dehors_command(interaction: discord.Interaction, member: discord.Member):
        await member.send("Dehors !")
        await member.kick(reason="python")
        await interaction.response.send_message("Dehors ! {member.mention}")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        word_blacklist = {'tg', 'fdp', 'ntm', 'connard', 'connasse', 'pute', 'salope', 'batard', 'bâtard', 'merde', 'enculé', 'encule', 'nique'}
        for mot in message.content.split():
            if mot.lower() in word_blacklist:
                await message.delete()
                await message.channel.send('Attention! je vais te bannir')
                break        


async def setup(client):
    await client.add_cog(Moderation(client))