import asyncio
import websockets

from aioredis import create_connection, Channel


async def publish_to_redis(msg, path):
    connection = await create_connection(('localhost', 6379))
    await connection.execute('publish', f'lightlevel_{path}', msg)


async def server(ws, path):
    try:
        while True:
            message = await ws.recv()

            await publish_to_redis(message, path)

            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosed:
        print('Connection is closed!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    ws_server = websockets.serve(server, "localhost", "8765")
    loop.run_until_complete(ws_server)
    loop.run_forever()
