from dotenv import load_dotenv
load_dotenv()

from discord import app_commands
import random
import discord
import os
import json 

# On active les intents pour pouvoir détecter les nouveaux membres
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree_commands = app_commands.CommandTree(client)

# --- DONNÉES DU JEU ---

WEAPONS_LIST = [
    {"nom": "AK-47", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/AK-47_type_II_Part_DM-ST-89-01131.jpg/1200px-AK-47_type_II_Part_DM-ST-89-01131.jpg"},
    {"nom": "M4A1", "image": "https://upload.wikimedia.org/wikipedia/commons/4/44/M4A1_ACOG.jpg"},
    {"nom": "Desert Eagle", "image": "https://upload.wikimedia.org/wikipedia/commons/5/54/Desert_Eagle_.50_AE.jpg"},
    {"nom": "Katana Laser", "image": "https://i.pinimg.com/originals/4d/75/90/4d75909c95085631567307116075b175.jpg"},
    {"nom": "Marteau de Guerre", "image": "https://cdna.artstation.com/p/assets/images/images/014/334/844/large/timothy-ferreira-warhammer-render01.jpg"},
    {"nom": "Ray Gun Alien", "image": "https://static.wikia.nocookie.net/callofduty/images/1/19/Ray_Gun_BO4.png"},
    {"nom": "Sabre Laser", "image": "https://lumiere-a.akamaihd.net/v1/images/skywalker-lightsaber-main_7b669382.jpeg"},
]

RARITIES = {
    "Commun": 1,
    "Rare": 2,
    "Epique": 3,
    "Légendaire": 4
}

PRIX_GENERATE = 100  # Coût pour générer une arme

# --- SYSTÈME DE SAUVEGARDE (JSON) ---

FILE_NAME = "collections.json"

def save_data():
    """Sauvegarde les données."""
    with open(FILE_NAME, "w") as f:
        json.dump(user_collections, f, indent=4)

def load_data():
    """Charge les données."""
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

user_collections = load_data()

# --- FONCTION UTILITAIRE ---

def check_user_exists(user_id):
    """Vérifie si le joueur existe, sinon le crée avec 0 coins."""
    if user_id not in user_collections:
        user_collections[user_id] = {"coins": 0, "inventory": []}
        return

    if isinstance(user_collections[user_id], list):
        ancien_inventaire = user_collections[user_id]
        user_collections[user_id] = {"coins": 0, "inventory": ancien_inventaire}
        save_data()

# --- COMMANDES ÉCONOMIE ---

@tree_commands.command(name="daily", description="Récupère 200 pièces chaque minute")
@app_commands.checks.cooldown(1, 60)
async def daily_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    check_user_exists(user_id)

    gain = 200
    user_collections[user_id]["coins"] += gain
    save_data()

    embed = discord.Embed(title="💰 Salaire Rapide", description=f"Tu as reçu **{gain} coins** !\nNouveau solde : **{user_collections[user_id]['coins']}** 🪙", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@tree_commands.command(name="work", description="Travaille pour gagner un peu d'argent")
@app_commands.checks.cooldown(1, 3600)
async def work_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    check_user_exists(user_id)

    salaire = random.randint(20, 100)
    user_collections[user_id]["coins"] += salaire
    save_data()

    jobs = ["Tu as tondu la pelouse", "Tu as réparé un robot", "Tu as nettoyé le vaisseau spatial", "Tu as aidé une grand-mère"]
    job_text = random.choice(jobs)

    await interaction.response.send_message(f"🔨 {job_text} et tu as gagné **{salaire} coins** !")

@tree_commands.command(name="wallet", description="Affiche ton argent")
async def wallet_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    check_user_exists(user_id)
    
    argent = user_collections[user_id]["coins"]
    await interaction.response.send_message(f"👛 Tu as actuellement **{argent} coins**.")

@tree_commands.command(name="sell_last", description="Vend la DERNIÈRE arme que tu as obtenue")
async def sell_last_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    check_user_exists(user_id)

    inventaire = user_collections[user_id]["inventory"]

    if len(inventaire) == 0:
        await interaction.response.send_message("❌ Tu n'as rien à vendre !")
        return

    objet_vendu = inventaire.pop()
    prix_vente = objet_vendu["value"] * 50
    
    user_collections[user_id]["coins"] += prix_vente
    save_data()

    await interaction.response.send_message(f"🤝 Tu as vendu **{objet_vendu['name']}** pour **{prix_vente} coins** !")


# --- AUTRES COMMANDES ---

@tree_commands.command(name="help_weapon", description="Affiche la liste de toutes les commandes")
async def help_weapon_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📚 Aide", color=discord.Color.teal())
    embed.add_field(name="💰 /daily", value="Gagne 200 coins (toutes les minutes)", inline=False)
    embed.add_field(name="🔨 /work", value="Travaille pour gagner des coins (toutes les 1h)", inline=False)
    embed.add_field(name="👛 /wallet", value="Voir ton argent", inline=False)
    embed.add_field(name="🔫 /generate", value=f"Achète une arme aléatoire (Coût: {PRIX_GENERATE} coins)", inline=False)
    embed.add_field(name="🤝 /sell_last", value="Vend ta dernière arme pour récupérer de l'argent", inline=False)
    embed.add_field(name="🎒 /show_collection", value="Affiche ton inventaire", inline=False)
    await interaction.response.send_message(embed=embed)

@tree_commands.command(name="generate", description=f"Achète une arme aléatoire ({PRIX_GENERATE} coins)")
async def generate_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id) 
    check_user_exists(user_id)

    solde_joueur = user_collections[user_id]["coins"]
    if solde_joueur < PRIX_GENERATE:
        await interaction.response.send_message(f"❌ Tu es pauvre ! Il te faut **{PRIX_GENERATE} coins**. Utilise `/daily` ou `/work`.", ephemeral=True)
        return

    user_collections[user_id]["coins"] -= PRIX_GENERATE
    
    arme_choisie = random.choice(WEAPONS_LIST)
    arme_nom = arme_choisie["nom"]
    arme_image_url = arme_choisie["image"]

    choix_rarete = random.choices(list(RARITIES.keys()), weights=[50, 30, 15, 5], k=1)[0]
    valeur_tri = RARITIES[choix_rarete]

    nouvel_objet = {
        "name": arme_nom,
        "image": arme_image_url,
        "rarity": choix_rarete,
        "value": valeur_tri
    }

    user_collections[user_id]["inventory"].append(nouvel_objet)
    save_data() 

    couleur = discord.Color.blue()
    if choix_rarete == "Légendaire": couleur = discord.Color.gold()
    elif choix_rarete == "Epique": couleur = discord.Color.purple()
    elif choix_rarete == "Rare": couleur = discord.Color.green()

    embed = discord.Embed(title="🎁 Drop obtenu !", description=f"Coût : {PRIX_GENERATE} coins", color=couleur)
    embed.add_field(name="Arme", value=arme_nom, inline=True)
    embed.add_field(name="Rareté", value=choix_rarete, inline=True)
    embed.set_image(url=arme_image_url)
    embed.set_footer(text=f"Solde restant : {user_collections[user_id]['coins']} coins")

    await interaction.response.send_message(embed=embed)


@tree_commands.command(name="show_collection", description="Affiche ta collection triée par rareté")
async def show_collection_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    check_user_exists(user_id)

    items = user_collections[user_id]["inventory"]
    solde = user_collections[user_id]["coins"]

    if len(items) == 0:
        await interaction.response.send_message(f"Tu n'as pas d'armes, mais tu as **{solde} coins** ! Utilise `/generate`.")
        return

    items_tries = sorted(items, key=lambda x: x['value'], reverse=True)

    description = f"💰 **Porte-monnaie : {solde} coins**\n\n"
    for item in items_tries:
        icone = "⚪"
        if item['rarity'] == "Rare": icone = "🟢"
        elif item['rarity'] == "Epique": icone = "🟣"
        elif item['rarity'] == "Légendaire": icone = "🟡"
        
        description += f"{icone} **{item['name']}** ({item['rarity']})\n"

    embed = discord.Embed(title=f"Collection de {interaction.user.name}", description=description, color=discord.Color.orange())
    
    if items_tries:
        meilleure_arme = items_tries[0]
        embed.set_image(url=meilleure_arme["image"])
        
    await interaction.response.send_message(embed=embed)

# --- GESTION DES ERREURS ---
@tree_commands.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        temps_restant = int(error.retry_after)
        if temps_restant > 3600:
            msg = f"⏳ Doucement ! Reviens dans {temps_restant // 3600} heures."
        elif temps_restant > 60:
            msg = f"⏳ Doucement ! Reviens dans {temps_restant // 60} minutes."
        else:
            msg = f"⏳ Doucement ! Reviens dans {temps_restant} secondes."
        await interaction.response.send_message(msg, ephemeral=True)
    else:
        print(f"Erreur : {error}")

# --- EVENTS (BIENVENUE) ---

# >>> PARTIE AJOUTÉE POUR LE MESSAGE DE BIENVENUE <<<
@client.event
async def on_member_join(member: discord.Member):
    print(f"Nouveau membre détecté : {member.name}")
    
    # 1. ENVOI EN MESSAGE PRIVÉ (DM)
    try:
        await member.send(f"Bienvenue sur le serveur {member.guild.name} ! 🎮\nSi tu as besoin d'aide ou si tu veux commencer à jouer, tape la commande **/help_weapon**.")
    except:
        print(f"Impossible d'envoyer un DM à {member.name} (bloqué)")

    # 2. ENVOI SUR UN SALON SPÉCIFIQUE (OPTIONNEL MAIS CONSEILLÉ)
    # Remplace les 00000 ci-dessous par l'ID de ton salon "Général" ou "Bienvenue"
    ID_SALON_BIENVENUE = 1445360670395596922
    
    try:
        channel = client.get_channel(ID_SALON_BIENVENUE)
        if channel:
            await channel.send(f"Bienvenue {member.mention} ! 👋\nN'hésite pas à taper **/help_weapon** pour découvrir le jeu !")
    except:
        print("Erreur: ID de salon invalide ou bot sans permission.")


@client.event
async def on_ready():
    await tree_commands.sync()
    print(f'lancement du bot {client.user}')
    print("Système économique et Bienvenue chargés !")

client.run(os.getenv('DISCORD_TOKEN'))