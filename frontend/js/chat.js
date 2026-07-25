const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const chatMessages = document.getElementById("chatMessages");


function addMessage(message, sender){

    const wrapper = document.createElement("div");

    wrapper.className =
        sender === "user"
        ? "user-message"
        : "ai-message";


    wrapper.innerHTML = `

        <div class="message-avatar">
            ${sender === "user" ? "👤" : "🤖"}
        </div>


        <div class="message-content">
            ${message}
        </div>

    `;


    chatMessages.appendChild(wrapper);


    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}



async function sendMessage(){

    const message = input.value.trim();


    if(message === "")
        return;


    addMessage(message,"user");


    input.value="";


    // Temporary AI response
    setTimeout(()=>{


        addMessage(
        `
        I understand your question 😊

        This is a demo response from NAYAN.

        Soon I will answer using NCERT knowledge,
        RAG and AI models.
        `,
        "ai"
        );


    },800);



}



sendBtn.addEventListener(
    "click",
    sendMessage
);



input.addEventListener(
    "keypress",
    function(e){

        if(e.key==="Enter")
            sendMessage();

    }
);