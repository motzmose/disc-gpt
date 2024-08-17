import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from chatgpt import send_to_chatGPT

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
guild_ids = [int(os.getenv("GUILD_ID"))]
channel_id = int(os.getenv("CHANNEL_ID"))
history_limit = int(os.getenv("HISTORY_MAX_LEN"))

intents = discord.Intents.default()
intents.message_content = True


bot = discord.Bot(intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Event handler for when a message is sent on the server
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    # Check if the message is in a thread and in the specified channel
    if isinstance(ctx.channel,discord.channel.Thread) and ctx.channel.parent_id == channel_id:
        messages = await ctx.channel.history(history_limit).flatten()
        messages.reverse().pop(0)
        messages = [{'role': gpt_author(message.author), 'content': message.content} for message in messages]
        response = send_to_chatGPT(messages)
        await ctx.channel.send(response)

# Command to send a single message to the Chatbot
@bot.slash_command(description="Send a single message to the Chatbot", guild_ids=guild_ids)
async def one_shot(ctx, message: str):
    messages = [{'role': 'user', 'content': message}]
    response = send_to_chatGPT(messages)
    await ctx.respond(response)

# Command to start a conversation with the Chatbot
@bot.slash_command(description="Start a conversation with the Chatbot", guild_ids=guild_ids)
async def start_conversation(ctx, topic: str):
    await ctx.respond("Starting a conversation")
    message = await ctx.send(topic)
    await message.create_thread(name=f"Started a conversation about {topic}")

# Command to end a conversation with the Chatbot
@bot.slash_command(description="End a conversation with the Chatbot", guild_ids=guild_ids)
async def end_conversation(ctx):
    thread = ctx.channel
    await ctx.respond("Ending the conversation")
    await thread.archive()

def gpt_author(author):
    if author == bot.user:
        return 'assistant'
    else:
        return 'user'

# Run bot
bot.run(discord_token)