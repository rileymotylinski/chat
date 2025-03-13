import json
import redis


# Setup
CHANNEL="channel"
MESSAGE={
    "name": "Jason",
    "message": "Hello World",
}

r = redis.Redis()
p = r.pubsub()

# Subscribe to the channel.
p.subscribe(CHANNEL)

# Publish message onto channel. Take the dict and serialize as JSON
r.publish(CHANNEL, json.dumps(MESSAGE))

# Get message from channel
p.get_message() # Honestly, I don't know why I have to call get_message twice. 
subbed_msg=p.get_message()

# Print the raw string from Redis
print(subbed_msg)

# Deserialize the data field to a dict
print(json.loads(subbed_msg['data']))