const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");


async function sendMessage(){

    const message = input.value.trim();


    if(message === "")
        return;


    // Show user message
    addUserMessage(message);


    input.value = "";


    try {

        // Show NAYAN thinking
        showTyping();


        // Call backend
        const answer = await askNayan(message);


        // Remove thinking
        removeTyping();


        // Show AI answer
        addAIMessage(answer);


    }
    catch(error){

        console.error(error);


        removeTyping();


        addAIMessage(
            "Sorry, I could not connect to NAYAN backend."
        );

    }

}



sendBtn.addEventListener(
    "click",
    sendMessage
);



input.addEventListener(
    "keypress",
    function(e){

        if(e.key === "Enter")
            sendMessage();

    }
);