import discord
import aiohttp 
import json
from discord.ext import commands

TOKEN = '' #เอา Token Bot มาใส่
PREFIX = '!' #คำนำหน้า

bot = commands.Bot(command_prefix=PREFIX)

@bot.event 
async def on_ready() :
	print(f"Bot {bot.user.name} has started!")

@bot.event
async def on_message(message) :
	await bot.process_commands(message)

async def get_data_url(url) :
	async with aiohttp.ClientSession() as session :
		html = await fetch(session, url)

		return html

async def fetch(session, url) :
	async with session.get(url) as respones :
		return await respones.text()

@bot.command()
async def covid19(ctx) :
    thai = await get_data_url('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
    thai = json.loads(thai)
    e = discord.Embed(title="ข้อมูลโควิด 19", description=f"อัพเดตล่าลุดเมื่อ {thai[0]['update_date']} ", color=0x17c1ff)
    e.add_field(name=':thermometer_face: ผู้ป่วยสะสม',value=f"{thai[0]['total_case']} คน")
    e.add_field(name=':mask: ผู้ป่วยรายใหม่',value=f"{thai[0]['new_case']} คน")
    e.add_field(name=':homes:  ผู้ป่วยรักษาหายแล้ว',value=f"{thai[0]['new_recovered']} คน")
    e.add_field(name=':skull_crossbones: ผู้ป่วยเสียชีวิต',value=f"{thai[0]['new_death']} คน")
    await ctx.channel.send(embed=e)

bot.run(TOKEN)