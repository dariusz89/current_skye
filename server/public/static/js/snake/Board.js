export default class Board {
    #dimensions;

    constructor(dimensions) {
        this.#dimensions = dimensions;

        this.#create();
    }
    
    #create() {
        let board = document.getElementById("board");
        for (let k = 0; k < this.#dimensions.y; k++) {
            let elementLine = [];
            let line = document.createElement("div");
            line.classList.add("line");
            line.classList.add("line-node-" + k);
            for (let i = 0; i < this.#dimensions.x; i++) {
                let block = document.createElement("div");
                block.classList.add("block");
                block.classList.add("block-node-" + i);
                line.appendChild(block);
                elementLine.push(0);
            }
            board.appendChild(line);
        }
    }

    drawSnake(newBody) {
        newBody.forEach(element => {
            let block = document.getElementsByClassName("block-node-" + element.x)[element.y];
            if (typeof block == 'undefined') return;
            block.classList.add("snake");
        });

        let headBlock = document.getElementsByClassName("block-node-" + newBody[0].x)[newBody[0].y];
        if (typeof headBlock == 'undefined') return;
        headBlock.classList.add("snake-head");
    }

    undrawSnake(oldBody) {
        oldBody.forEach(element => {
            let block = document.getElementsByClassName("block-node-" + element.x)[element.y];
            if (typeof block == 'undefined') return;
            block.classList.remove("snake");
        });
        
        let headBlock = document.getElementsByClassName("block-node-" + oldBody[0].x)[oldBody[0].y];
        if (typeof headBlock == 'undefined') return;
        headBlock.classList.remove("snake-head");
    }

    drawFood(newFood) {
        let block = document.getElementsByClassName("block-node-" + newFood.x)[newFood.y];
        if (typeof block == 'undefined') return;
        block.classList.add("food");
    }

    undrawFood(oldFood) {
        let block = document.getElementsByClassName("block-node-" + oldFood.x)[oldFood.y];
        if (typeof block == 'undefined') return;
        block.classList.remove("food");
    }

    reDrawSnake(newBody, oldBody) {
        if (typeof oldBody != 'undefined') this.undrawSnake(oldBody);
        this.drawSnake(newBody);        
    }

    reDrawFood(newFood, oldFood) {
        if (typeof oldFood != 'undefined') this.undrawFood(oldFood);
        this.drawFood(newFood);        
    }

}