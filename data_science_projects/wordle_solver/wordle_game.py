class wordle_game:

    def __init__(self, size:int, answer: str):

        if not answer.isalpha():
            raise Exception("Answer must only contain letters in alphabet")
        self.size = size
        # convert answer into list of characters
        self.answer_list = [*answer.lower()]
        self.game_history=[]


    def guess_word(self,guess :str):

        if not guess.isalpha():
            raise Exception("Guess must only contain letters in alphabet")

        if len(guess)== self.size:
            word= [*guess.lower()]
            output = [None]*(self.size+1)
            score =0
            for idx,char in enumerate(word):
                if char == self.answer_list[idx]:
                    output[idx+1] =2
                    score+=2
                elif char in self.answer_list:
                    output[idx+1] = 1
                    score+=1
                else:
                    output[idx+1]=0
               
                    
            
            if score == self.size*2:
                output[0]= 'c'
                
            elif score ==0:
                output[0] = 'f'
                
            else:
                output[0] ='p'
                
            
            return output
        else:
            raise Exception(f"Word is not {self.size} characters long!")


