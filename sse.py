from flask import Flask, render_template, request, Response
from flask_sse import sse
import logging
import redis
import json
import helper as h


r = redis.Redis()
app = Flask(__name__)
# suppressing flask log messages
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# TODO: cleanup function for empty rooms
# r.pubsub_channels()?
rooms = []

@app.route("/")
def home():
    return render_template("index.html", rooms=rooms)


@app.route("/chatroom/<chatroom_name>")
def chatroom(chatroom_name):
    if chatroom_name not in rooms:
        rooms.append(chatroom_name)
    return render_template("chatroom.html", room=chatroom_name)



@app.route("/chatroom/message", methods=["POST"])
def message():
    if request.method == "POST":
        message_json = request.get_json()

        h.log_message("Message From Client Received")
        r.publish(message_json["chatroom"], str(message_json))
        
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

 # message["data"].decode('utf8').replace("'", '"')
                    # message = message["data"].decode("utf-8").replace("'", '"').encode("utf-8")


@app.route("/stream/<chatroom_name>")
def stream(chatroom_name):
    p = r.pubsub()
    p.subscribe(chatroom_name)

    
    def get_data():
        while True:
            # has to yield in a certain format to work
            for message in p.listen():
                if message["type"] != "subscribe":
                    h.log_message("Message Heard: " + str(json.loads(message["data"].decode("utf-8"))["message"]))
                    
                    message = message["data"].decode("utf-8")
                    
                    h.log_message("Relaying Message...")
                    try:
                        # throws error
                        # can remove this line as it works fine w/o, but included to illustrate point
                      
                        yield f"data: {message["data"].decode("utf-8")} \n\n"
                    except TypeError as t:
                        h.log_message("Error sending message: " + str(t))
                        decoded_message = message["data"].decode("utf-8")
                        h.log_message("∟> Decoded Bytes Message to utf-8")
                        
                    
                        # doesnt throw error
                        # FIXED LINE
                        yield f"data: {decoded_message} \n\n"
                    h.log_message("Message Sent!")
                    print("\n")

    return Response(get_data(), mimetype="text/event-stream")





