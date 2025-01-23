import random
import discord
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix='?', intents=intents)

latest_bot_message = ""
message_embed = ""
users_reacted = []
chosen_eight = []
locked_in = False

async def operation_lets_play(embed):

    tank = ["WAR", "DRK", "GNB", "PLD"]
    regen = ["AST", "WHM"]
    shield = ["SCH", "SGE"]
    melee = ["MNK", "NIN", "DRG", "RPR", "SAM", "VPR"]
    prange = ["BRD", "DNC", "MCH"]
    caster = ["BLM", "PCT", "SMN", "RDM"]

    random.shuffle(tank)
    random.shuffle(regen)
    random.shuffle(shield)
    random.shuffle(melee)
    random.shuffle(prange)
    random.shuffle(caster)

    with open("content.json", "r") as file:
        content = json.load(file)
    keys = list(content.keys())
    random.shuffle(keys)
    shuffled_content = {key: content[key] for key in keys}

    roster = [tank[0], tank[1], regen[0], shield[0], melee[0], prange[0], caster[0]]

    temp_melee = melee.copy()
    temp_prange = prange.copy()
    temp_caster = caster.copy()
    temp_melee.pop(0)
    temp_prange.pop(0)
    temp_caster.pop(0)
    anydps = temp_melee + temp_prange + temp_caster
    random.shuffle(anydps)
    roster.append(anydps[0])

    global chosen_eight
    random.shuffle(chosen_eight)

    content_name = next(iter(shuffled_content))
    content_picture = shuffled_content[content_name]

    channel = latest_bot_message.channel
    message = await channel.fetch_message(latest_bot_message.id)
    embed = message.embeds[0]
    embed.title = content_name
    embed.set_thumbnail(url = content_picture)
    embed.set_image(url = "https://cdn.discordapp.com/attachments/1310334851043295302/1323741150464573440/sexo.gif?ex=6791f5c4&is=6790a444&hm=18daec64a4b1dedcbc4ff04919cae49cc5c076894b9e6ea4744d3c12b6afbd37&")

    desc = ""
    for i in range(len(users_reacted)):
        print(i)
        print(len(users_reacted))
        if i == 0 or i == 1:
            desc += "🛡️"
        elif i == 2 or i == 3:
            desc += "👨‍⚕️"
        else:
            desc += "⚔️"
        desc += f' {roster[i]} {chosen_eight[i].display_name}\n'
    print(f'{desc}')
    embed.description = desc
    await message.edit(embed=embed)

def embed_description(users_reacted, embed):
    user_count = len(users_reacted)
    embed.description = f"""
    Randomly picks an encounter and randomly picks a role!\n
    {user_count}/8 users in the game:
    """
    for users in users_reacted:
        embed.description += f"{users.display_name}\n"

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    global users_reacted
    global chosen_eight
    global locked_in
    
    if locked_in == False: 
        if reaction.emoji == "🫃" and reaction.message.id == latest_bot_message.id and user.id != bot.application_id:
            users_reacted.append(user)

            channel = reaction.message.channel
            message = await channel.fetch_message(reaction.message.id)
            embed = message.embeds[0]
            embed_description(users_reacted, embed)
            await message.edit(embed=embed)
            
            if len(users_reacted) == 8:
                print("ENTRY")
                locked_in = True
                chosen_eight = users_reacted
                await operation_lets_play(embed)

@bot.event
async def on_reaction_remove(reaction, user):
    global users_reacted

    if locked_in == False:
        if reaction.emoji == "🫃" and reaction.message.id == latest_bot_message.id and user.id != bot.application_id:
            
            if user in users_reacted:
                users_reacted.remove(user)
            
            channel = reaction.message.channel
            message = await channel.fetch_message(reaction.message.id)
            embed = message.embeds[0]
            embed_description(users_reacted, embed)
            await message.edit(embed=embed)

@bot.command()
async def play(ctx):
    global locked_in
    global users_reacted
    users_reacted = []
    locked_in = False
    embed = discord.Embed(
        title = "test FFXIV CONTENT ROULETTE",
        description = "Randomly picks an encounter and randomly picks role/job!",
        colour = discord.Colour.blue(),
    )
    embed.set_image(url = "https://cdn.discordapp.com/attachments/1331559141998596146/1331671884282200064/image.png?ex=67927796&is=67912616&hm=01b74a6f34fada548ac1e1a666d45b39a176b043842fcb1a41b3266433a1fd8d&")
    message = await ctx.send(embed = embed)
    global latest_bot_message
    global message_embed
    latest_bot_message = message
    message_embed = embed

    await message.add_reaction("🫃")

bot.run(bot_token)