import asyncio
import redis
import json
from websockets.asyncio.server import serve,broadcast

r = redis.Redis()
p = r.pubsub()

# webpages
subscribers = []
# individual connectees
clients = []
async def receive_message(websocket):
    
    clients.append(websocket)
    # needs error handling for when the client connection drops
    
    async for message in websocket:
        deserialized = json.loads(message)
    

        if deserialized["type"] == "MESSAGE":
            
            chatroom = deserialized["MESSAGE"]["chatroom"]
            
            for subscriber in subscribers:
                print(p.channels)
            

            broadcast(clients,str(deserialized))
        if deserialized["type"] == "SUBSCRIBER":
            subscribers.append(p.subscribe(deserialized["chatroom"]))
            p = redis.Redis().pubsub()
            
        
      
    

async def main():
    async with serve(receive_message, "localhost", 8766):
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())