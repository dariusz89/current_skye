console.log("home template")

const namespace = "/home";

const socket = io(namespace, {
    auth : {
        token : "browser"
    },
    transports: ["websocket"]
});

socket.on("connect", () => {
    console.log("sid:", socket.id);
    socket.emit("welcome", {
        "message" : "Jasiu Stasiu"
    });
    console.log("Environment data was sent.");
});

socket.on("connect_error", (error) => {
    console.info(error.message);
    socket.close();
});

socket.on("disconnect", (reason) => {
    console.log("sid:", socket.id);
    console.log("disconnect reason:", reason);
    if (reason === "io server disconnect") {
        socket.connect();
    }
});

socket.on("welcome", (data) => {
    console.log("data:", data);
});

let options = document.getElementById("options");

let startBtn = document.createElement("button");
startBtn.id = "startBtn";
startBtn.type = "button";
startBtn.textContent = "Start";
let startEvent = function () {
    socket.emit("start_agent")
}
startBtn.addEventListener("click", startEvent);
options.appendChild(startBtn);

socket.on("hello_from_agent", (data) => {
    console.log("data:", data);
    helloResponse(3000, data["by"])
});

async function helloResponse(time, to) {
    await sleep(time)
    socket.emit("hello_from_browser", {"to" : to, "message" : "Browser send his regards", "by" : socket.id})
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
