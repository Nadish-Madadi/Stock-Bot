import discord
import os
import requests
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


client = commands.Bot(command_prefix = "!")
@client.command(name="s")
async def stock_price(msg, *stock_prefix):
  
  channel = msg.channel
  user = msg.author.display_name
  timezone_ = pytz.timezone('America/New_York') 
  datetime_ = datetime.now(timezone_)
  x = datetime_.strftime("%H:%M:%S")

  nyse_hours_and_holidays = "https://www.nyse.com/markets/hours-calendars"
  stock_prefix = list(stock_prefix)

  if stock_prefix[0] == "close" and len(stock_prefix) == 1:
    embed=discord.Embed(title="Stock Market Closing Time", description="Stock Market closes at 4:00 pm EST excluding cryptocurrencies",url=nyse_hours_and_holidays, color=discord.Color.blurple())
    await channel.send(embed=embed)
    
  elif stock_prefix[0] == "open" and len(stock_prefix) == 1:
    embed=discord.Embed(title="Stock Market Opening Time", description="Stock Market opens at 9:30 am EST excluding cryptocurrencies",url=nyse_hours_and_holidays, color=discord.Color.gold())
    await channel.send(embed=embed)
  else:
    for i in range(len(stock_prefix)):
      try:
        print(f"{user} sent a request")
        url_ = "https://finance.yahoo.com/quote/"
        url_ += stock_prefix[i].upper()
        
        result = requests.get(url_)
        
        doc = BeautifulSoup(result.text, "html.parser")

        name = doc.findAll(class_ = "D(ib) Fz(18px)")[0].text
        price = doc.findAll(class_ ="Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
        price_after = doc.findAll(class_ ="C($primaryColor) Fz(24px) Fw(b)")[0].text
        market_cap = doc.findAll(class_ ="Ta(end) Fw(600) Lh(14px)")[8].text
        
        inc_dec = doc.findAll(class_ ="D(ib) Mend(20px)")[0].text
        inc_dec_after = doc.findAll(class_ ="Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)")[0].text

        low_high = doc.findAll(class_ ="Ta(end) Fw(600) Lh(14px)")[4].text.split(" - ")
        low = low_high[0]
        high = low_high[1]

        if "-" in inc_dec:
          embed=discord.Embed(title=name, description="Scraped from Yahoo Finance",url=url_, color=discord.Color.red())

        elif "+" in inc_dec:
          embed=discord.Embed(title=name, description="Scraped from Yahoo Finance",url=url_, color=discord.Color.green())

        embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
        embed.add_field(name="At Close", value=f"{price} {inc_dec[len(price):inc_dec.index('A')].strip()}", inline=True)
        embed.add_field(name="After Hours", value=f"{price_after} {inc_dec_after[len(price_after):inc_dec_after.index('A')].strip()}", inline=True)
        embed.add_field(name="Market Cap", value=market_cap, inline=False)
        embed.add_field(name="Daily Low", value=low, inline = True)
        embed.add_field(name="Daily High", value=high, inline = True)
        embed.set_footer(text= f"Requested by: {user} at {x}")

        await channel.send(embed=embed)
      except:
        await channel.send(url_)
        

keep_alive()

client.run(os.getenv('TOKEN'))

# reference for getting price at close and after hours

# print("At close:", price)
# print("After hours:", price_after)

# await channel.send(f"At close: {price} {inc_dec[len(price):inc_dec.index('A')].strip()}")
# await channel.send(f"After hours: {price_after} {inc_dec_after[len(price_after):inc_dec_after.index('A')].strip()}")