from nltk.corpus import words
from datetime import date, timedelta
import random
import requests
import urllib
import queue
import asyncio

class dictionary:

    def __init__(self, word_length:int) -> None:
        self.word_list=[word.lower() for word in list(set(words.words())) if len(word) == word_length and word.isalpha()== True] 
        self.words_with_freq =[]
        self.start_year = date.today().year -5
        self.end_year = date.today().year

        
        # self.count =0

        # for word in self.word_list:
        #     self.word_q.put(word)

    def pick_random_word(self):
        return random.choice(self.word_list)
    

    async def send_request(self,queue,word:str) -> int:
        
        word = urllib.parse.quote(word)
        url =f'https://books.google.com/ngrams/json?content={word}&year_start={str(self.start_year)}&year_end={str(self.end_year)}&corpus=26&smoothing=0'
        
        # await asyncio.sleep(2)
        response = requests.get(url)

        if response.status_code == 200:

            output = response.json()
            if len(output[0]['timeseries']) ==0:
                self.words_with_freq.append([word,0])
                
            else:
                self.words_with_freq.append([word,output[0]['timeseries'][-1]])

            # self.count+=1
            # print(f"processed {self.count} records!")
            # print(self.words_with_freq)
            # print(f"Processed {word}")
        
        elif response.status_code == 429:
            await queue.put(word)
            # print("429 Error")

    
    async def process_async_queue(self,queue)-> None:
        
        while True:
            item = await queue.get()
            if item is None:
                break
            
            await self.send_request(queue, item)
        print("Dictionary is ready")
       
    

    async def query_google_ngrams(self)-> None:
        queue = asyncio.Queue()    

        for word in self.word_list:
            await queue.put(word)

        await asyncio.gather(self.process_async_queue(queue))
    

    def build_dictionary_with_frequencies(self)-> None:
        # print(f"{self.word_q.qsize()} left in the list!")
        asyncio.run(self.query_google_ngrams())

        for record in self.words_with_freq:
            with open('temp','w') as f:
                f.write(f"{record[0]} {record[1]}")






if __name__ == "__main__":

    dic= dictionary(4)
    dic.build_dictionary_with_frequencies()
    print(dic.words_with_freq)