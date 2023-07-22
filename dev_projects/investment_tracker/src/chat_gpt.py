import openai
import pandas as pd
import config

class gpt_model:

    def __init__(self) -> None:
        self.key=config.gpt_key

    
    def prompt(self,df,mkt):

        openai.api_key = self.key

        prompt = f"""Give me a summary of my portfolio performance and the individual stocks within the portfolio.
                
                  Here is my stocks, i want you to interpret the performance of each stock and the performance of the portfolio since its inital purchase :\n\n{df}\n\n 
                  also compare the performance of the portfolio since purchase to the market return since purchase which is this table: \n\n{mkt}\n\n
                complete this prompt in 500 tokens
            """

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None
        )

        output = response.choices[0].text.strip()


        return output


