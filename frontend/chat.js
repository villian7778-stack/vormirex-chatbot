// async function send() {
//   const input = document.getElementById("input");
//   const msg = input.value;

//   const res = await fetch("http://localhost:8000/chat", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ message: msg })
//   });

//   const data = await res.json();
//   document.getElementById("messages").innerHTML +=
//     `<p><b>You:</b> ${msg}</p><p><b>vormi:</b> ${data.reply}</p>`;

//   input.value = "";
// }

// Get or create a persistent user session ID
// function getUserId() {
//     let userId = localStorage.getItem("vormirex_user_id");
//     if (!userId) {
//         userId = "user_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
//         localStorage.setItem("vormirex_user_id", userId);
//     }
//     return userId;
// }

// async function sendMessage() {
//     const input = document.getElementById("user-input");
//     const chatBox = document.getElementById("chat-box");

//     const message = input.value.trim();
//     if (!message) return;

//     // Display user message
//     const userMsgDiv = document.createElement("div");
//     userMsgDiv.className = "user";
//     userMsgDiv.textContent = "You: " + message;
//     chatBox.appendChild(userMsgDiv);
    
//     input.value = "";

//     try {
//         const response = await fetch("/chat", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({
//                 message: message,
//                 user_id: getUserId()
//             })
//         });

//         if (!response.ok) {
//             throw new Error(`HTTP ${response.status}: ${response.statusText}`);
//         }

//         const data = await response.json();
//         console.log("Response received:", data); // DEBUG
        
//         // Display bot reply
//         const botMsgDiv = document.createElement("div");
//         botMsgDiv.className = "bot";
//         botMsgDiv.textContent = "vormi: " + data.reply;
//         chatBox.appendChild(botMsgDiv);
        
//         // Render buttons if present
//         if (data.buttons && Array.isArray(data.buttons) && data.buttons.length > 0) {
//             console.log("Rendering buttons:", data.buttons); // DEBUG
            
//             const buttonContainer = document.createElement("div");
//             buttonContainer.className = "button-container";
            
//             data.buttons.forEach(btn => {
//                 const button = document.createElement("button");
//                 button.className = "course-button";
//                 button.textContent = btn.label || btn.title || "Button";
//                 button.onclick = () => {
//                     console.log("Button clicked:", btn.id); // DEBUG
//                     input.value = btn.id || btn.value;
//                     sendMessage();
//                 };
//                 buttonContainer.appendChild(button);
//             });
            
//             chatBox.appendChild(buttonContainer);
//             console.log("Buttons rendered successfully"); // DEBUG
//         } else {
//             console.log("No buttons to render"); // DEBUG
//         }
        
//         chatBox.scrollTop = chatBox.scrollHeight;

//     } catch (error) {
//         const errorDiv = document.createElement("div");
//         errorDiv.className = "bot error";
//         errorDiv.textContent = "vormi: Server error - " + error.message;
//         chatBox.appendChild(errorDiv);
//         console.error("Error:", error);
//     }
// }



// function getUserId() {
//     let userId = localStorage.getItem("vormirex_user_id");
//     if (!userId) {
//         userId = "user_" + Date.now();
//         localStorage.setItem("vormirex_user_id", userId);
//     }
//     return userId;
// }

// async function sendMessage() {
//     const input = document.getElementById("user-input");
//     const chatBox = document.getElementById("chat-box");

//     const message = input.value.trim();
//     if (!message) return;

//     chatBox.innerHTML += `<div class="user">You: ${message}</div>`;
//     input.value = "";

//     const response = await fetch("/chat", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({message, user_id: getUserId()})
//     });

//     const data = await response.json();

//     chatBox.innerHTML += `<div class="bot">vormi: ${data.reply}</div>`;

//     // DOWNLOAD PDF
//     if (data.download_url) {
//         const a = document.createElement("a");
//         a.href = data.download_url;
//         a.download = "";
//         a.click();
//     }

//     // BUTTONS
//     if (data.buttons) {
//         const div = document.createElement("div");
//         data.buttons.forEach(btn => {
//             const b = document.createElement("button");
//             b.textContent = btn.label;
//             b.onclick = () => {
//                 input.value = btn.id;
//                 sendMessage();
//             };
//             div.appendChild(b);
//         });
//         chatBox.appendChild(div);
//     }

//     chatBox.scrollTop = chatBox.scrollHeight;
// }

// function getUserId() {
//     let userId = localStorage.getItem("vormirex_user_id");
//     if (!userId) {
//         userId = "user_" + Date.now();
//         localStorage.setItem("vormirex_user_id", userId);
//     }
//     return userId;
// }

// async function sendMessage() {
//     const input = document.getElementById("user-input");
//     const chatBox = document.getElementById("chat-box");

//     const message = input.value.trim();
//     if (!message) return;

//     // USER BUBBLE
//     chatBox.innerHTML += `
//         <div class="msg user-msg">
//             <div class="bubble">${message}</div>
//         </div>
//     `;
//     input.value = "";
//     chatBox.scrollTop = chatBox.scrollHeight;

//     const response = await fetch("/chat", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({
//             message,
//             user_id: getUserId()
//         })
//     });

//     const data = await response.json();

//     // BOT BUBBLE
//     chatBox.innerHTML += `
//         <div class="msg bot-msg">
//             <div class="bubble">${data.reply}</div>
//         </div>
//     `;

//     // BUTTONS
//     if (data.buttons) {
//         const btnDiv = document.createElement("div");
//         btnDiv.className = "button-group";

//         data.buttons.forEach(btn => {
//             const b = document.createElement("button");
//             b.textContent = btn.label;
//             b.onclick = () => {
//                 input.value = btn.id;
//                 sendMessage();
//             };
//             btnDiv.appendChild(b);
//         });

//         chatBox.appendChild(btnDiv);
//     }

//     // DOWNLOAD
//     if (data.download_url) {
//         const a = document.createElement("a");
//         a.href = data.download_url;
//         a.download = "";
//         a.click();
//     }

//     chatBox.scrollTop = chatBox.scrollHeight;
// }


// function getUserId() {
//     let userId = localStorage.getItem("vormirex_user_id");
//     if (!userId) {
//         userId = "user_" + Date.now();
//         localStorage.setItem("vormirex_user_id", userId);
//     }
//     return userId;
// }

// function addBotMessage(text) {
//     const chatBox = document.getElementById("chat-box");
//     chatBox.innerHTML += `
//         <div class="msg bot-msg">
//             <div class="bubble">${text}</div>
//         </div>
//     `;
//     chatBox.scrollTop = chatBox.scrollHeight;
// }

// function addUserMessage(text) {
//     const chatBox = document.getElementById("chat-box");
//     chatBox.innerHTML += `
//         <div class="msg user-msg">
//             <div class="bubble">${text}</div>
//         </div>
//     `;
//     chatBox.scrollTop = chatBox.scrollHeight;
// }

// function renderButtons(buttons) {
//     const chatBox = document.getElementById("chat-box");
//     const div = document.createElement("div");
//     div.className = "button-group";

//     buttons.forEach(btn => {
//         const b = document.createElement("button");
//         b.textContent = btn.label;
//         b.onclick = () => {
//             document.getElementById("user-input").value = btn.id;
//             sendMessage();
//         };
//         div.appendChild(b);
//     });

//     chatBox.appendChild(div);
//     chatBox.scrollTop = chatBox.scrollHeight;
// }

// async function sendMessage() {
//     const input = document.getElementById("user-input");
//     const message = input.value.trim();
//     if (!message) return;

//     addUserMessage(message);
//     input.value = "";

//     const response = await fetch("/chat", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({
//             message: message,
//             user_id: getUserId()
//         })
//     });

//     const data = await response.json();

//     addBotMessage(data.reply);

//     if (data.buttons) {
//         renderButtons(data.buttons);
//     }

//     if (data.download_url) {
//         const a = document.createElement("a");
//         a.href = data.download_url;
//         a.download = "";
//         a.click();
//     }
// }

// /* 🔥 AUTO GREETING (THIS FIXES YOUR ISSUE) */
// window.onload = async () => {
//     const response = await fetch("/chat", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({
//             message: "hi",
//             user_id: getUserId()
//         })
//     });

//     const data = await response.json();
//     addBotMessage(data.reply);

//     if (data.buttons) {
//         renderButtons(data.buttons);
//     }
// };


// ==============================
// DOM ELEMENTS (SAFE LOAD)
// ==============================
let chatBox;
let userInput;

window.addEventListener("DOMContentLoaded", () => {
    chatBox = document.getElementById("chat-box");
    userInput = document.getElementById("user-input");

    if (!chatBox || !userInput) {
        console.error("❌ chat-box or user-input not found in DOM");
        return;
    }

    // Initial bot greeting
    addBotMessage("🤖 Hello! I'm <b>Vormi</b>.<br>Please tell me your <b>name</b> to get started 😊");
});

// ==============================
// USER ID
// ==============================
function getUserId() {
    let userId = localStorage.getItem("vormirex_user_id");
    if (!userId) {
        userId = "user_" + Date.now();
        localStorage.setItem("vormirex_user_id", userId);
    }
    return userId;
}

// ==============================
// MESSAGE HELPERS
// ==============================
function appendMessage(className, html) {
    if (!chatBox) return;

    const div = document.createElement("div");
    div.className = className;
    div.innerHTML = html;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addUserMessage(text) {
    appendMessage("user", text);
}

function addBotMessage(text) {
    appendMessage("bot", text);
}

// ==============================
// SEND MESSAGE
// ==============================
async function sendMessage(text = null) {
    if (!userInput || !chatBox) return;

    const message = text || userInput.value.trim();
    if (!message) return;

    addUserMessage(message);
    userInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message,
                user_id: getUserId()
            })
        });

        const data = await response.json();

        // Bot reply
        if (data.reply) {
            addBotMessage(data.reply);
        }

        // Buttons
        if (data.buttons && Array.isArray(data.buttons)) {
            const btnWrap = document.createElement("div");
            btnWrap.className = "button-container";

            data.buttons.forEach(btn => {
                const b = document.createElement("button");
                b.className = "course-button";
                b.textContent = btn.label;
                b.onclick = () => sendMessage(btn.id);
                btnWrap.appendChild(b);
            });

            chatBox.appendChild(btnWrap);
        }

        // Download
        if (data.download_url) {
            const a = document.createElement("a");
            a.href = data.download_url;
            a.download = "";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            addBotMessage("📥 Download started! You can continue chatting with me 😊");
        }

    } catch (err) {
        console.error(err);
        addBotMessage("❌ Something went wrong. Please try again.");
    }
}
