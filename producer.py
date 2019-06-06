import asyncio
import websockets

from aioredis import create_connection, Channel


async def subscribe_to_redis(path):
    connection = await create_connection(('localhost', 6379))
    channel = Channel(f'lightlevel_{path}', is_pattern=False)
    await connection.execute_pubsub('subscribe', channel)
    return channel, connection


async def browser_server(ws, path):
    channel, connection = await subscribe_to_redis(path)
    try:
        while True:
            message = await channel.get()
            print(f"get and send message - {message}")
            await ws.send(message.decode('utf-8'))
    except websockets.exceptions.ConnectionClosed:
        await connection.execute_pubsub('unsubscribe', channel)
        connection.close()
        print('Conenction closed!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    ws_server = websockets.serve(browser_server, 'localhost', 8767)
    loop.run_until_complete(ws_server)
    loop.run_forever()
