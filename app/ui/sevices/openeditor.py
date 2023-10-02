
import asyncio
from ttkui import main
async def open_editor_app( e):
    await asyncio.gather(main())

async def start_app( x=None):
    print('runnig app... started')
    await open_editor_app(x)