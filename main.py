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

bot = commands.Bot(command_prefix='!', intents=intents)

latest_bot_message = ""
message_embed = ""
chosen_eight = []

active_channels = {}
users_reacted_on_message = {}


async def operation_lets_play(embed, message):

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

    channel = message.channel
    message_edit = await channel.fetch_message(message.id)
    embed = message_edit.embeds[0]
    embed.title = content_name
    embed.set_thumbnail(url = content_picture)
    embed.set_image(url = "https://cdn.discordapp.com/attachments/1310334851043295302/1323741150464573440/sexo.gif?ex=6791f5c4&is=6790a444&hm=18daec64a4b1dedcbc4ff04919cae49cc5c076894b9e6ea4744d3c12b6afbd37&")

    desc = ""
    users_to_ping = ""
    for i in range(len(users_reacted_on_message[message.id])):
        if i == 0 or i == 1:
            desc += "🛡️"
        elif i == 2 or i == 3:
            desc += "👨‍⚕️"
        else:
            desc += "⚔️"
        desc += f' {roster[i]} {chosen_eight[i].display_name}\n'
        users_to_ping += f"<@{chosen_eight[i].id}> "
    embed.description = desc
    del users_reacted_on_message[message.id]
    print(f"AFTER GAME: {users_reacted_on_message}")
    await channel.send(content=f'{users_to_ping}', embed=embed)
    

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
    global chosen_eight
    global active_channels
    global users_reacted_on_message
    print("react added")
    
    if reaction.emoji == "🫃" and user.id != bot.application_id and reaction.message.id == active_channels[reaction.message.channel.id]:

        users_reacted_on_message[reaction.message.id].add(user)
        print(f"AFTER ADD: {users_reacted_on_message}")

        channel = reaction.message.channel
        message = await channel.fetch_message(reaction.message.id)
        embed = message.embeds[0]
        embed_description(users_reacted_on_message[reaction.message.id], embed)
        await message.edit(embed=embed)
        
        if len(users_reacted_on_message[reaction.message.id]) == 1:
            print("ENTRY")
            chosen_eight = list(users_reacted_on_message[reaction.message.id])
            del active_channels[channel.id]
            #print(active_channels)
            await operation_lets_play(embed, reaction.message)

@bot.event
async def on_reaction_remove(reaction, user):
    global users_reacted_on_message

    if reaction.message.channel.id in active_channels:
        print("skibidi")
        if reaction.emoji == "🫃" and  user.id != bot.application_id and reaction.message.id == active_channels[reaction.message.channel.id]:
            users_reacted_on_message[reaction.message.id].remove(user)
            print(f"AFTER DEL: {users_reacted_on_message}")
            
            channel = reaction.message.channel
            message = await channel.fetch_message(reaction.message.id)
            embed = message.embeds[0]
            embed_description(users_reacted_on_message[reaction.message.id], embed)
            await message.edit(embed=embed)
    else:
        print("brick")

@bot.command()
async def play(ctx):
    embed = discord.Embed(
        title = "FFXIV CONTENT ROULETTE",
        description = "Randomly picks an encounter and randomly picks role/job!",
        colour = discord.Colour.blue(),
    )
    embed.set_image(url = "https://cdn.discordapp.com/attachments/1331559141998596146/1331671884282200064/image.png?ex=67927796&is=67912616&hm=01b74a6f34fada548ac1e1a666d45b39a176b043842fcb1a41b3266433a1fd8d&")
    message = await ctx.send(embed = embed)
    global message_embed
    message_embed = embed

    global active_channels
    global users_reacted_on_message
    if ctx.channel.id in active_channels:
        previous_active_message = await ctx.channel.fetch_message(active_channels[ctx.channel.id])
        await previous_active_message.delete()
    active_channels[ctx.channel.id] = message.id
    users_reacted_on_message[message.id] = set()
    print(f"ON DECLARA: {users_reacted_on_message}")

    #print(f'CHANNEL: {ctx.channel.id} : MESSAGE: {message.id}')
    #print(active_channels)


    await message.add_reaction("🫃")
    #print(f'CHANNEL NAME: {ctx.channel}')
    #print(f'MESSAGE ID: {message.id}')
    #print(f'MESSAGE CHANNEL: {message.channel}')
    #print(f'MESSAGE CHANNEL ID: {message.channel.id}')
    #print(f'SERVER NAME:{message.guild}')
    #print(f'SERVER ID:{message.guild.id}')
    #print(f'SERVER CHANNELS: {message.guild.channels}')
    
bot.run(bot_token)