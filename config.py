import os
from decouple import config
from pathlib import Path

os.environ['CHATBOT_API_KEY']='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'
os.environ['API_PASSWORD']='ROOT'
API_KEY=config('api_key')
kpass=config('user_key')
def get_password(password):
    print(kpass)
    _env_k=os.getenv('API_PASSWORD')
    if password ==_env_k:
        print('Sucess')
        return True
    print('failed')
    return False
def set_env_data(key,value):
    _home=str(Path().absolute())
    with open(_home+'.env','a+') as env:
        print('write done !!!')
        env.write(f'{key}={value}')


dark_tm="#081d33"