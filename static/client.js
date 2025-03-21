window.addEventListener("DOMContentLoaded", () => {
   
    chatroom = document.head.querySelector("meta[name='chatroom-name']").content;
    document.querySelector("#message-send").addEventListener("click", () => {
            console.log("sending message");
            message = $("#message").val();
            user = $("#username").val();
            console.log(message)
            // formatting outgoing message
            // rememeber to change this when you change port
            fetch("http://127.0.0.1:4999/chatroom/message", {
                method: "POST",
                body: JSON.stringify({
                    type: "MESSAGE",
                    chatroom: chatroom,
                    user: user,
                    message: message
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })
                
            
            
        }
        
    );

    // whenever a messages is published to the redis channel, a stream api endpoint in flask is updated.
    // The EventSource object handles that.
    const sse = new EventSource("/stream/" + chatroom)

    function handleStream(data){
        //console.log("Received message")
        const div = document.querySelector("#message-area");
        const paragraph = document.createElement("p");
        // incoming data is a string that needs to be parsed as dict. JSON needs double quotes instead of single quotes
        data = JSON.parse(data.replaceAll("\'","\""))

        //console.log(data.replaceAll("\'","\""))
        console.log(typeof(data))
        
        
        // TODO: single quotes don't work right now :(. Something with escape characters on server side maybe?
        // inserting into current page
        paragraph.innerText = data["user"] + ": " + data["message"];
        //paragraph.innerText = data["user"] + ": " + data;
        div.appendChild(paragraph);
    }

    // behavior on received message
    sse.onmessage = e => {handleStream(e.data)}



    // handles weird connection interrupted error on firefox
    window.addEventListener('beforeunload', () => {
        sse.close();
    });



   

   
    
});


