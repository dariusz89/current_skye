import { io } from "../../libs/socket.io/dist/socket.io.esm.min.js";
export default class SocketIOEvents {
    #context;
    #socket;

    constructor(context) {
        this.#context = context;
        this.#init('/snake');
        this.#callbacks();
    }

    #init(namespace) {
        this.#socket = io(namespace, {
            auth : {
                token : "browser" // we must make use of it
            },
            transports: ["websocket"]
        });
    }

    #callbacks() {
        this.#socket.on("connect", () => this.#onConnect());
        this.#socket.on("connect_error", (error) => this.#onConnectError(error));
        this.#socket.on("disconnect", (reason) => this.#onDisconnect(reason));
        this.#socket.on("start_training_game", (data) => this.#onStartTrainingGame(data));
        this.#socket.on("on_request_for_observation", (data) => this.#onRequestForObservation(data));
        this.#socket.on("on_request_for_info", (data) => this.#onRequestForInfo(data));
    }

    #onConnect() {
        console.log("sid:", this.#socket.id);
        this.welcome();
    }

    #onConnectError(error) {
        console.info(error.message);
        this.#socket.close();
    }

    #onDisconnect(reason) {
        console.log("sid:", this.#socket.id);
        console.log("disconnect reason:", reason);
        if (reason === "io server disconnect") {
            this.#socket.connect();
        }
    }

    #onStartTrainingGame(data) {
        this.#context.events.add('startTrainingGame', {
            'info' : data
        });
        this.events.dispatch('startTrainingGame');
    }

    #onRequestForObservation(data) {
        this.#context.events.add('requestForObservation', {
            'info' : data
        });
        this.events.dispatch('requestForObservation');
    }

    #onRequestForInfo(data) {
        this.#context.events.add('requestForInfo', {
            'info' : data
        });
        this.events.dispatch('requestForInfo');
    }
    
    welcome() {
        this.#socket.emit("welcome", {
            "message" : "Jasiu Stasiu"
        });
    }

    async downloadGameOptions() {
        return await new Promise((resolve) => {
            this.#socket.emit("game_options", (data) => {
                resolve(data);
            })
        }).then((result) => result);
    }

    sendEnvironmentData(data) {
        this.#socket.emit("environment_data", data);
    }

    sendEnvironmentInfo(data) {
        this.#socket.emit("environment_info", data);
    }

    startTrain() {
        this.#socket.emit("start_training");
    }

    testEnvironment() {
        this.#socket.emit("test_environment");
    }

}