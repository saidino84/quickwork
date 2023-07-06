import openai

from config import API_KEY
class IaService:
    
    def __init__(self) -> None:
        self.__api_key=API_KEY
        self.messages=[{'role':'system', 'content':'Voce é um assistente gente boa'}]
    
    def generate_response(self,message:str):
        response = openai.ChatCompletion(
            engine='gpt-3.5-turbo',
            messages=self.messages,
            max_tokens=1024,
            temperature=0.5
        )
        #return [response.choices[0].message.content, response.usage]
        return [response.choices[0].message.content, response.usage]

    def chat_bot(self):
        while True:
            question =input('Pergunte >>')
            if question =='sair' or question =='':
                print('saindo ...')
                break
            else:
                self.messages.append({'role':'user','content':str(question)})
                answer=self.generate_response(self.messages)
                print(' YOU :', question)
                print('BOT :',answer[0], 'CUSTO',answer[1])
        
