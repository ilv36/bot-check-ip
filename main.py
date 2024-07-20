import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ui import Button, View, Modal, TextInput
import aiohttp
import datetime

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all(), case_insensitive=True)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged {bot.user} is ready!")
    await bot.change_presence(activity=nextcord.Streaming(name='ilv', url='https://www.twitch.tv/Discord'))

# ระบบเช็ค IP
async def fetch_ip_info(ip: str) -> dict:
    url = f"https://ipapi.co/{ip}/json/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# ฟังก์ชันเพื่อจัดรูปแบบข้อมูล IP
def format_ip_info(data: dict) -> str:
    return (
        f"IP: {data.get('ip', 'N/A')}\n"
        f"Network: {data.get('network', 'N/A')}\n"
        f"Version: {data.get('version', 'N/A')}\n"
        f"City: {data.get('city', 'N/A')}\n"
        f"Region: {data.get('region', 'N/A')}\n"
        f"Region Code: {data.get('region_code', 'N/A')}\n"
        f"Country: {data.get('country', 'N/A')}\n"
        f"Country Name: {data.get('country_name', 'N/A')}\n"
        f"Country Code: {data.get('country_code', 'N/A')}\n"
        f"Country Code ISO3: {data.get('country_code_iso3', 'N/A')}\n"
        f"Country Capital: {data.get('country_capital', 'N/A')}\n"
        f"Country TLD: {data.get('country_tld', 'N/A')}\n"
        f"Continent Code: {data.get('continent_code', 'N/A')}\n"
        f"In EU: {data.get('in_eu', 'N/A')}\n"
        f"Postal: {data.get('postal', 'N/A')}\n"
        f"Latitude: {data.get('latitude', 'N/A')}\n"
        f"Longitude: {data.get('longitude', 'N/A')}\n"
        f"Timezone: {data.get('timezone', 'N/A')}\n"
        f"UTC Offset: {data.get('utc_offset', 'N/A')}\n"
        f"Country Calling Code: {data.get('country_calling_code', 'N/A')}\n"
        f"Currency: {data.get('currency', 'N/A')}\n"
        f"Currency Name: {data.get('currency_name', 'N/A')}\n"
        f"Languages: {data.get('languages', 'N/A')}\n"
        f"Country Area: {data.get('country_area', 'N/A')}\n"
        f"Country Population: {data.get('country_population', 'N/A')}\n"
        f"ASN: {data.get('asn', 'N/A')}\n"
        f"ORG: {data.get('org', 'N/A')}\n"
    )

class IPCheckModal(Modal):
    def __init__(self):
        super().__init__(title="Check IP")
        self.ip_input = TextInput(
            label="IP Address",
            placeholder="Enter the IP address",
            required=True,
        )
        self.add_item(self.ip_input)

    async def callback(self, interaction: Interaction):
        ip = self.ip_input.value
        data = await fetch_ip_info(ip)
        formatted_info = format_ip_info(data)
        await interaction.response.send_message(formatted_info, ephemeral=True)

async def ip_check_button(interaction: Interaction):
    await interaction.response.send_modal(IPCheckModal())

class MultiSystemView(View):
    @nextcord.ui.button(label="เช็ค IP", style=nextcord.ButtonStyle.primary, emoji="🌐", custom_id="check_ip")
    async def check_ip_button(self, button: Button, interaction: Interaction):
        await ip_check_button(interaction)

@bot.slash_command(name="setup", description="Setup Check IP")
async def setup(interaction: Interaction):
    view = MultiSystemView()

    embed = nextcord.Embed(
        title="ระบบเช็ค IP",
        description="```ระบบเช็ค IP ฟรี```",
        color=0x00ff00 
    )
    embed.set_image(url="https://c.tenor.com/J2qI_909o3wAAAAC/tenor.gif")
    embed.set_footer(text=f"Requested at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    await interaction.response.send_message(embed=embed, view=view)

bot.run("")