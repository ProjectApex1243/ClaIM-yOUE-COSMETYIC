import discord
from discord.ext import commands
import requests
import os

PLAYFAB_TITLE_ID = os.getenv('1E0677')
PLAYFAB_SECRET_KEY = os.getenv('Y75W36PFBN31KOPUJD79PMIFECGD6XIM3A4D3KMJ8A1IHCPMFO')
BOT_TOKEN = os.getenv('MTQ2ODc2ODg4MTQwMDIxNzcyNA.GAs8x1.9CnxHJ3F3accJ7Bqi1a-vywUKVqszX8rs0xw8s')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')
    print(f'📡 Connected to {len(bot.guilds)} server(s)')
    print('🎮 Ready to redeem codes!')

@bot.command()
async def redeem(ctx, code: str = None, playfab_id: str = None):
    if not code or not playfab_id:
        await ctx.reply('❌ Usage: `!redeem <CODE> <PLAYFAB_ID>`\nExample: `!redeem X7K2M9P1 ABC123DEF456`')
        return
    
    print(f'🔍 Redeeming code: {code} for player: {playfab_id}')
    
    url = f'https://{PLAYFAB_TITLE_ID}.playfabapi.com/Server/ExecuteCloudScript'
    
    headers = {
        'X-SecretKey': PLAYFAB_SECRET_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'PlayFabId': playfab_id,
        'FunctionName': 'RedeemDiscordCode',
        'FunctionParameter': {
            'code': code.upper(),
            'playfabId': playfab_id
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'data' in data and 'FunctionResult' in data['data']:
            result = data['data']['FunctionResult']
            
            if result.get('success'):
                embed = discord.Embed(
                    title='✅ Code Redeemed Successfully!',
                    description=f"**Cosmetic Unlocked:** {result.get('itemGranted')}",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name='📦 What\'s Next?',
                    value='Your wardrobe will automatically refresh in-game within 5 seconds!',
                    inline=False
                )
                embed.set_footer(text='Enjoy your new cosmetic!')
                await ctx.reply(embed=embed)
                print(f'✅ Code {code} redeemed successfully!')
            else:
                error_msg = result.get('error', 'Unknown error')
                await ctx.reply(f"❌ **Redemption Failed:** {error_msg}")
                print(f'❌ Redemption failed: {error_msg}')
        else:
            await ctx.reply('❌ **Error:** Invalid response from game servers.')
            print(f'❌ Invalid response: {data}')
            
    except Exception as e:
        print(f'❌ Error: {e}')
        await ctx.reply('❌ **Error:** Unable to connect to game servers. Please try again later.')

@bot.command()
async def linkaccount(ctx):
    embed = discord.Embed(
        title='🔗 How to Link Your Account',
        description='To redeem codes, you need your PlayFab ID from the game',
        color=discord.Color.blue()
    )
    embed.add_field(
        name='📋 Step 1',
        value='In-game, find your **Player ID** in the Settings menu',
        inline=False
    )
    embed.add_field(
        name='💬 Step 2',
        value='Use the redeem command with your code and Player ID',
        inline=False
    )
    embed.add_field(
        name='✏️ Example',
        value='`!redeem X7K2M9P1 ABC123DEF456`',
        inline=False
    )
    embed.set_footer(text='Need help? Contact a moderator!')
    await ctx.reply(embed=embed)

@bot.command()
async def codehelp(ctx):
    embed = discord.Embed(
        title='📖 Code Redemption Commands',
        description='Here are all available commands:',
        color=discord.Color.purple()
    )
    embed.add_field(
        name='!redeem <CODE> <PLAYFAB_ID>',
        value='Redeem a code from the game',
        inline=False
    )
    embed.add_field(
        name='!linkaccount',
        value='Show instructions to get your PlayFab ID',
        inline=False
    )
    embed.add_field(
        name='!codehelp',
        value='Show this help message',
        inline=False
    )
    await ctx.reply(embed=embed)

if __name__ == '__main__':
    if not BOT_TOKEN:
        print('❌ ERROR: BOT_TOKEN environment variable not set!')
    elif not PLAYFAB_TITLE_ID:
        print('❌ ERROR: PLAYFAB_TITLE_ID environment variable not set!')
    elif not PLAYFAB_SECRET_KEY:
        print('❌ ERROR: PLAYFAB_SECRET_KEY environment variable not set!')
    else:
        print('🚀 Starting bot...')
        bot.run(BOT_TOKEN)
