
var website_dir = document.querySelector("html").getAttribute("dir");
var leumi_API = 'https://leumi.netlify.app/';
// var leumi_API = 'http://localhost:3000/';

var screenWidth = screen.width;
var screenHeight = screen.height;

var chat_box_div_style = "border: hidden; height: 100%; width: 100%;  position: fixed; bottom: 110px; right: 30px;transition: 0.3s; transform-origin: bottom right;box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.1);border-radius: 15px; transform: scale(0);" + (screenWidth > 450 ? "max-width:380px;right: 30px;" : "max-width:calc(100% - 20px);right: 10px;") + (screenHeight > 700 ? "max-height: 550px;" : "max-height: calc(100% - 120px);")
var open_chat_div_style = "border: hidden; height: 70px; width: 70px; position: fixed;   width: 70px; height: 70px; background: rgb(197 231 253 / 30%); animation: pulse-animation 2s infinite; display: flex; justify-content: center; align-items: center; border-radius: 50%;" + (screenWidth > 450 ? "bottom: 30px; right: 30px;" : "bottom: 15px; right: 15px;")
var chat_button_style = "width: 50px; height: 50px; flex-shrink: 0; border: 0; border-radius: 50.27px; background: linear-gradient(0deg, #0084da 0%, #06bff5 100%); cursor: pointer;"
var chat_button_icon_style = "height: 20px; margin-left: auto; margin-top: 5px; width: 20px;"


// eslint-disable-next-line no-unused-vars
function handleToOpenChat() {
  const chatBoxElement = document.getElementById("leumi-chat-box");
  const chatButtonElement = document.getElementById("leumi-chat-button-img");
  if (chatBoxElement.style.transform === "scale(1)" || chatBoxElement.style.transform === "") {
    chatBoxElement.style.transform = "scale(0)";
    chatButtonElement.style.transform = "scaleY(1)";
  } else {
    chatBoxElement.style.transform = "scale(1)";
    chatButtonElement.style.transform = "scaleY(-1)";
  }
}

const OpenChatDiv = document.createElement("div");
OpenChatDiv.setAttribute("style", open_chat_div_style);
const ChatButton = document.createElement("button");
ChatButton.setAttribute("onclick", "handleToOpenChat()");
ChatButton.setAttribute("style", chat_button_style);
const ChatButtonIcon = document.createElement("img");
ChatButtonIcon.setAttribute("src", leumi_API + "arrow.svg");
ChatButtonIcon.setAttribute("id", "leumi-chat-button-img");
ChatButtonIcon.setAttribute("style", chat_button_icon_style + "transform: scaleY(1);");
OpenChatDiv.appendChild(ChatButton);
ChatButton.appendChild(ChatButtonIcon);
document.body.appendChild(OpenChatDiv);


const ChatBoxDiv = document.createElement("iframe");
ChatBoxDiv.src = leumi_API + 'chatbot?dir=' + website_dir;
ChatBoxDiv.setAttribute("id", "leumi-chat-box");
ChatBoxDiv.setAttribute("style", chat_box_div_style);
document.body.appendChild(ChatBoxDiv);
