import discord
import os, random
import cat
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from google import genai
from PIL import Image
from io import BytesIO

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

gemini = genai.Client()
print("gemini ready!")

GUILD_ID = discord.Object(id=os.environ.get("GUILD"))

@client.tree.command(name="heck", description="say hi to snek", guild=GUILD_ID)
async def heck(interaction: discord.Interaction):
    await interaction.response.send_message("no step on snek")

@client.tree.command(name="echo", description="repeats whatever you type in", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, input: str):
    await interaction.response.send_message(input)

@client.tree.command(name="embed", description="test command", guild=GUILD_ID)
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a Title", url="https://catsolutions1.github.io/kitkat/", description="I am the description", color=discord.Color.yellow())
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLOHuVo4Q4hJuETfLrXaUAm1na2c1TfT7zWQ&s")
    embed.add_field(name="Field 1 Title", value="no step on snek", inline=False)
    embed.set_footer(text="This is the footer!")
    embed.set_author(name=interaction.user.name, url="https://www.youtube.com/watch?v=KHQ2MaDbx5I&list=PL-7Dfw57ZZVQ-GCNQS4Kyz637Fffhb0Hs&index=4", icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="cat", description="sends a random cat pic using the cat api", guild=GUILD_ID)
async def random_cat(interaction: discord.Interaction):
    cat.getCat(filename="cat")
    await interaction.response.send_message(file=discord.File("cat.png"))

@client.tree.command(name="meme", description="sends a random meme from my computer", guild=GUILD_ID)
async def meme(interaction: discord.Interaction):
    try:
        filepath = random.choice(os.listdir("memes"))
        await interaction.response.send_message(file=discord.File("memes/" + filepath))
    except Exception as e:
            print(f'Error sending image: {e}')

@client.tree.command(name="imggen", description="creates an ai image using gemini", guild=GUILD_ID)
async def generate_image(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    response = gemini.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
        )
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save('gemini-native-image.png')
    await interaction.followup.send(file=discord.File("gemini-native-image.png"))

client.run(os.environ.get("TOKEN"))
