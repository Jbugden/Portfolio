import discord_bot
import config 
import inv_data
import chat_gpt
import pandas as pd
import asyncio


def main():

    bot = discord_bot.discord_bot()

    

    data_obj = inv_data.get_investment_data()
    df = data_obj.get_data()
    mkt = data_obj.get_market_data()



    gpt = chat_gpt.gpt_model()

    gpt_answer = gpt.prompt(df,mkt)

    bot.send_investment_message(df,mkt,gpt_answer)
  


if __name__ == "__main__":
    main()