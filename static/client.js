window.addEventListener("DOMContentLoaded", () => {
   
    chatroom = document.head.querySelector("meta[name='chatroom-name']").content;
    document.querySelector("#message-send").addEventListener("click", () => {
            message = $("#message").val();
            user = $("#username").val();
            console.log(message)
            // formatting outgoing message
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
        const div = document.querySelector("#message-area");
        const paragraph = document.createElement("p");
    
        data = JSON.parse(data)

        console.log(data)
        
        
        // TODO: single quotes don't work right now :(. Something with escape characters on server side maybe?
        // inserting into current page
        paragraph.innerText = data["user"] + ": " + data["message"];
        div.appendChild(paragraph);
    }

    // behavior on received message
    sse.onmessage = e => {handleStream(e.data)}



    // handles weird connection interrupted error on firefox
    window.addEventListener('beforeunload', () => {
        sse.close();
    });



   

   
    
});


