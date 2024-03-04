import SocketIOEvents from './SocketIOEvents.js';
export default class Events {
    /**
     * Lista zdarzeń:
     * - otrzymaj opcje
     * - gra gotowa
     * - zacznij grę
     * - zakończ grę
     * - zacznij trening
     * - zakończ trening
     * - stan gry
     * - akcja
     * 
     */
    /**
     * Czego potrzebuje przy starcie gry?
     * opcje gry:
     * 1. Rozmiar planszy
     * 2. Początkowe położenie jedzenia
     * 3. Początkowe położenie węża
     * 4. Początkowy kierunek ruchu węża
     */
    #available_listners = {
        'keydown' : this.#keydownListner(),
        'startGameButton' : this.#startGameButtonListner(),
        'startTrainingButton' : this.#startTrainingButtonListner(),
        'testEnvironmentButton' : this.#testEnvironmentButtonListner(),
        'stopGameButton' : this.#stopGameButtonListner(),
        'initGame' : this.#downloadGameOptionsListner(),
        'startTrainingGame' : this.#startTrainingGameListner(),
        'sendEnvironmentData' : this.#sendEnvironmentDataListner(),
        'sendEnvironmentInfo' : this.#sendEnvironmentInfoListner(),
    };
    
    #context;
    #events;
    #references;
    #socketIOEvents;
    

    constructor(context) {
        this.#context = context;
        this.#events = [];
        this.#references = [];
        this.#socketIOEvents = new SocketIOEvents(this);
        this.#uiListeners();
    }

    #uiListeners() {
        this.addListener('keydown');
        this.addListener('startGameButton');
        this.addListener('stopGameButton');
        this.addListener('startTrainButton');
        this.addListener('startTrainingButton');
    }

    add(name, data=null) {
        this.#events.push({
            'name' : name,
            '_event' : new CustomEvent(name, {"detail": data})
        });
        console.log(`Event ${name} has been registered`);
        this.addListener(name);
    }

    dispatch(name) {
        if (!this.#events.some(event => event.name === name)) {
            console.log(`Event ${name} not exists, fire has been canceled`);
            return;
        }
        
        let event = this.#getEventCallback(name)._event;
        document.dispatchEvent(event);
        this.#events = this.#events.filter(event => event.name !== name);
        console.log(`Event ${name} has been dispatched and removed`);
        this.removeListener(name);
    }

    addListener(name) {
        this.#register(name);
        document.addEventListener(name, this.#getListenerCallBack(name)._func);
    }

    removeListener(name) {
        document.removeEventListener(name, this.#getListenerCallBack(name)._func);
        this.#unRegister(name);
    }

    #register(name) {
        this.#references.push({
            'name': name, 
            '_func': this.#available_listners[name]
        });
        console.log(`Event Listner ${name} has been registered`);
    }

    #unRegister(name) {
        this.#references = this.#references.filter(reference => reference.name !== name);
        console.log(`Event Listner ${name} has been unregistered`);
    }

    #getEventCallback(name) {
        for (let i in this.#events) {
            if (this.#events[i].name === name) return this.#events[i];
        }
    }

    #getListenerCallBack(name) {
        for (let i in this.#references) {
            if (this.#references[i].name === name) return this.#references[i];
        }
    }

    #downloadGameOptionsListner() {
        let that = this;
        let downloadGameOptions = (ev) => {
            that.#socketIOEvents.downloadGameOptions().then(result => {
                that.#context.init(result);
            });
        }
        
        return downloadGameOptions;
    }

    #sendEnvironmentDataListner() {
        let that = this;
        let sendEnvironmentData = (ev) => {
            that.#socketIOEvents.sendEnvironmentData(ev.detail);
        }

        return sendEnvironmentData;
    }

    #sendEnvironmentInfoListner() {
        let that = this;
        let sendEnvironmentInfo = (ev) => {
            that.#socketIOEvents.sendEnvironmentInfo(ev.detail);
        }

        return sendEnvironmentInfo;
    }

    #startTrainingGameListner() {
        let that = this;
        let startTrainingGame = (ev) => {
            that.#context.start();
        }

        return startTrainingGame;
    }

    #keydownListner() {
        let that = this;
        let keydown = function (ev) {
            if (!that.#context.state.isRunning) return;
            switch (ev.key) {
                case 'ArrowUp':
                    if (that.#context.snake.possibleMovements.top) {
                        that.#context.snake.currentDirection.top = true;
                        that.#context.snake.currentDirection.bottom = false;
                        that.#context.snake.currentDirection.left = false;
                        that.#context.snake.currentDirection.right = false;
                    }
                    break;
                case 'ArrowDown':
                    if (that.#context.snake.possibleMovements.bottom) {
                        that.#context.snake.currentDirection.top = false;
                        that.#context.snake.currentDirection.bottom = true;
                        that.#context.snake.currentDirection.left = false;
                        that.#context.snake.currentDirection.right = false;
                    }
                    break;
                case 'ArrowLeft':
                    if (that.#context.snake.possibleMovements.left) {
                        that.#context.snake.currentDirection.top = false;
                        that.#context.snake.currentDirection.bottom = false;
                        that.#context.snake.currentDirection.left = true;
                        that.#context.snake.currentDirection.right = false;
                    }
                    break;
                case 'ArrowRight':
                    if (that.#context.snake.possibleMovements.right) {
                        that.#context.snake.currentDirection.top = false;
                        that.#context.snake.currentDirection.bottom = false;
                        that.#context.snake.currentDirection.left = false;
                        that.#context.snake.currentDirection.right = true;
                    }
                    break;
            }

        }
        return keydown;
    }

    #startGameButtonListner() {
        let options = document.getElementById("options");
        let startBtn = document.createElement("button");
        startBtn.id = "startBtn";
        startBtn.type = "button";
        startBtn.textContent = "Start";
        
        let that = this;
        let startGame = function () {
            console.log("Start button was pressed");
            if (!that.#context.state.isRunning) {
                that.#context.mode = "game"
                that.#context.start();
            }
        }

        startBtn.addEventListener("click", startGame);
        options.appendChild(startBtn);
        
        return startGame;
    }

    #stopGameButtonListner() {
        let options = document.getElementById("options");
        let stopBtn = document.createElement("button");
        stopBtn.id = "stopBtn";
        stopBtn.type = "button";
        stopBtn.textContent = "Stop";

        let that = this;
        let stopGame = function () {
            console.log("Stop button was pressed");
            if (that.#context.state.isRunning) {
                that.#context.stop();
            }
        }
        
        stopBtn.addEventListener("click", stopGame);
        options.appendChild(stopBtn);
        
        return stopGame;
    }

    #startTrainingButtonListner() {
        let options = document.getElementById("options");
        let startTrainBtn = document.createElement("button");
        startTrainBtn.id = "startTrainBtn";
        startTrainBtn.type = "button";
        startTrainBtn.textContent = "Train";
        
        let that = this;
        let startTrain = function () {
            console.log("Train button was pressed");
            if (!that.#context.state.isRunning) {
                that.#socketIOEvents.startTrain();
            }
        }

        startTrainBtn.addEventListener("click", startTrain);
        options.appendChild(startTrainBtn);
        
        return startTrain;
    }

    #testEnvironmentButtonListner() {
        let options = document.getElementById("options");
        let testEnvBtn = document.createElement("button");
        testEnvBtn.id = "testEnvBtn";
        testEnvBtn.type = "button";
        testEnvBtn.textContent = "Test";
        
        let that = this;
        let startTrain = function () {
            console.log("Test button was pressed");
            if (!that.#context.state.isRunning) {
                that.#socketIOEvents.testEnvironment();
            }
        }

        testEnvBtn.addEventListener("click", startTrain);
        options.appendChild(testEnvBtn);
        
        return startTrain;
    }

}