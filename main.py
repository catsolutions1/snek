import discord
import os, random
import cat
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=os.environ.get("GUILD"))
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

_ = load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=os.environ.get("GUILD"))

@client.tree.command(name="heck", description="Say hi to Snek", guild=GUILD_ID)
async def heck(interaction: discord.Interaction):
    await interaction.response.send_message("no step on snek")

@client.tree.command(name="printer", description="Returns input", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, input: str):
    await interaction.response.send_message(input)

@client.tree.command(name="embed", description="Embed demo", guild=GUILD_ID)
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a Title", url="https://catsolutions1.github.io/kitkat/", description="I am the description", color=discord.Color.yellow())
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLOHuVo4Q4hJuETfLrXaUAm1na2c1TfT7zWQ&s")
    embed.add_field(name="Field 1 Title", value="no step on snek", inline=False)
    embed.set_footer(text="This is the footer!")
    embed.set_author(name=interaction.user.name, url="https://www.youtube.com/watch?v=KHQ2MaDbx5I&list=PL-7Dfw57ZZVQ-GCNQS4Kyz637Fffhb0Hs&index=4", icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="cat", description="sends a random cat pic", guild=GUILD_ID)
async def random_cat(interaction: discord.Interaction):
    cat.getCat(filename="cat")
    await interaction.response.send_message(file=discord.File("cat.png"))

@client.tree.command(name="meme", description="sends a random meme", guild=GUILD_ID)
async def meme(interaction: discord.Interaction):
    try:
        filepath = random.choice(os.listdir("memes"))
        await interaction.response.send_message(file=discord.File("memes/" + filepath))
    except Exception as e:
            print(f'Error sending image: {e}')

client.run(os.environ.get("TOKEN"))
