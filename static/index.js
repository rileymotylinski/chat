function redirect(chatroom) {
    window.location.href = "/chatroom/" + chatroom
}

window.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#submit").addEventListener("click", () => {
       
        var chatroom_name = document.querySelector("#chatroom-name").value;
        var chatroom_button = document.createElement("BUTTON");
        chatroom_button.textContent = chatroom_name;

        chatroom_button.addEventListener("click", function(){
            window.location.href = "/chatroom/" + chatroom_name;
        })


        document.querySelector("#buttons").appendChild(chatroom_button);
    })

    

    
    


});