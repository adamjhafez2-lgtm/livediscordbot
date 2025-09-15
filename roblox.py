import os
import random
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Lists
allowed_users = set()
denied_users = set()
owners = {OWNER_ID}

# ----------------- Helper Functions -----------------
def get_user_avatar(user: discord.User):
    return user.display_avatar.url if user.display_avatar else None

def check_owner(user_id):
    return user_id in owners

# ----------------- Commands -----------------
@bot.command()
async def ctx(ctx):
    """Shows list of all commands available to the user"""
    embed = discord.Embed(title="Commands List", color=0x00FFFF)
    embed.add_field(name="Moderation", value="!ban, !kick, !timeout, !spam", inline=False)
    embed.add_field(name="Fun", value="!gif, !msg, !dance, !roll, !sound", inline=False)
    embed.add_field(name="Owner", value="!Owner <user_id>", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, user: discord.User):
    if not check_owner(ctx.author.id):
        await ctx.send("You are not allowed to use this command.")
        return
    await ctx.send(f"Simulated banning {user.display_name} (testing)")

@bot.command()
async def kick(ctx, user: discord.User):
    if not check_owner(ctx.author.id):
        await ctx.send("You are not allowed to use this command.")
        return
    await ctx.send(f"Simulated kicking {user.display_name} (testing)")

@bot.command()
async def timeout(ctx, user: discord.User):
    if not check_owner(ctx.author.id):
        await ctx.send("You are not allowed to use this command.")
        return
    await ctx.send(f"Simulated timing out {user.display_name} (testing)")

@bot.command()
async def spam(ctx, user: discord.User):
    if not check_owner(ctx.author.id):
        await ctx.send("You are not allowed to use this command.")
        return
    await ctx.send(f"Simulated spamming {user.display_name} (testing)")

@bot.command()
async def gif(ctx, url: str):
    await ctx.send(url)

@bot.command()
async def msg(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def dance(ctx):
    dancing_frames = [
        "(>'-')>   ", "<('-'<)   ", "^('-')^   ", "v('-')v   "
    ]
    message = await ctx.send(dancing_frames[0])
    for frame in dancing_frames * 2:  # 3 seconds of animation
        await message.edit(content=frame)
        await discord.utils.sleep_until(ctx.message.created_at + discord.utils.timedelta(seconds=0.25))
    await message.edit(content="Dance finished! Press 'revive parrot' to dance again.")  

@bot.command()
async def roll(ctx, user: discord.User, *, options):
    options_list = [o.strip() for o in options.split(",")]
    chosen = random.choice(options_list)
    await ctx.send(f"{user.display_name} spun the wheel and got **{chosen}**!")

@bot.command()
async def sound(ctx, *, name: str):
    # Placeholder: Embed like Spotify preview
    embed = discord.Embed(title=f"Sound: {name}", description=f"Preview of {name}", color=0xFF00FF)
    embed.add_field(name="Listen", value=f"🔊 Click to play preview")
    await ctx.send(embed=embed)

@bot.command()
async def Owner(ctx, user_id: int):
    if ctx.author.id != OWNER_ID:
        await ctx.send("Only the main owner can add other owners.")
        return
    owners.add(user_id)
    await ctx.send(f"<@{user_id}> is now an owner.")

@bot.command()
async def list(ctx):
    embed = discord.Embed(title="User Lists", color=0x00FFFF)
    
    allowed_text = "\n".join([f"{bot.get_user(uid).display_name}" for uid in allowed_users])
    denied_text = "\n".join([f"{bot.get_user(uid).display_name}" for uid in denied_users])
    owner_text = "\n".join([f"{bot.get_user(uid).display_name}" for uid in owners])
    
    embed.add_field(name="Allowed", value=allowed_text or "None", inline=True)
    embed.add_field(name="Denied", value=denied_text or "None", inline=True)
    embed.add_field(name="Owners", value=owner_text or "None", inline=True)
    
    await ctx.send(embed=embed)

# ----------------- Run Bot -----------------
bot.run(TOKEN)
