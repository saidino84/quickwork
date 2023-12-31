from plyer import notification
from json import load,dump
import os

# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file='.env', env_file_encoding='utf-8'
#     )
     
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int
def send_notiication(title,message):

        notification.notify(
            title=title,
            message=message,
            app_name="Price Tag",
            timeout=10
        )

class Utils:
    @staticmethod
    def get_providers():
        if(os.path.exists(os.path.join('settings','settings.json'))):
            print('Arquivo JA existe')
        else:
            try:
                Utils.create_if_not_exist()
            except OSError as e:
                print('[-] Erro na criacoa de pasta')
        try:
            with open(os.path.join('settings','settings.json'), 'r') as settings:
                data=load(settings)
                providers=data['providers']
                print(providers)
                return providers
        except IOError as e:
            Utils.create_if_not_exist()
    @staticmethod
    def create_if_not_exist():
        providers=[
        "VIP ARM. MUXARA",
        "JACARANDA MONAPO LDA",
        "AELIZ COMERCIAL",
        "TERRA MAR",
        "VIP MONTEPUEZ",
        "GOLDEN POWER REPRESENTACOES",
        "J.J.E COMERCIO",
        "HANDLING",
        "Titos Chichava",
        "INSELTEC SOLUTIONS",
        "BUCHANI",
        "Builders Warehouse",
        "Cha de Mangoma",
        " ADRIANO ARLINDO ",
        "AGRO-SULAHA FARMS LDA",
        "MOZBIFE",
        "RCL-RAHI COMERCIAL",
        "Casa Das Loiças",
        "Momade Bica Comercial",
        "DESSE CAMARA",
        "SOCOAL",
        "VIP WAREHOUSE CHAMANCULO",
        "OASIS MOÇAMBIQUE, LDA",
        "GENNY SALGADOS",
        "SALLU TRADING",
        "LOGOS Industrias Lda",
        "DESSE CAMARA",
        "PASTELARIA FLOR",
        "VIP NACALA",
        "VIP NAMPULA",
        "Niri Nkayi (Menteigas de amendoim)",
        "Marin Trading",
        "UNIBASMA",
        "IOCOMAS FARM",
        "FAZENDA OPHENTANA",
        "Vip Maputo Armazem",
        "Higest Moçambique , Lda",
        "Jephta Kasusu Wayella",
        "NECIFA LDA",
        "CANAS",
        "NOVO HORIZONTES",
        "TROPIGALIA",
        "Dona Julia",
        "VIP FASHION",
        "Kratos Empire , Lda"
    ]
        dados={"providers":providers}
        if(not os.path.isdir('settings')):
            os.makedirs('settings')
        with open(os.path.join('settings','settings.json'),'w+') as settigs:
            dump(dados,settigs)
            print('provider created')
        send_notiication('SETTINGS',"Provides Has been loaded sucessfully")

    
   
        
            