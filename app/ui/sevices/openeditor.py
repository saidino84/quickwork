
import asyncio,os
from ttkui import main
async def open_editor_app( e):
    curdir=os.getcwd()
    data=os.listdir(curdir)
    db=None
    for file in data:
        if file.endswith('db.db'):
            db=file
            print(f"File Found {db}")
    await asyncio.gather(main(path=db))

async def start_app( x=None):
    print('runnig app... started')
    await open_editor_app(x)