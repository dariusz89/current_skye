export default class Snake {
    #currentBody;
    #previousBody;
    #possibleMovements;
    #currentDirection;
    #previousDirection;

    debug_info() {
        return `\r\n\tcurrentBody: ${this.#debug_currentBody()}` +
        `\r\n\tpreviousBody: ${this.#debug_previousBody()}` +
        `\r\n\tpossibleMovements: ${this.#debug_possibleMovements()}` +
        `\r\n\tcurrentDirection: ${this.#debug_currentDirection()}` +
        `\r\n\tpreviousDirection: ${this.#debug_previousDirection()}`
    }

    #debug_currentBody() {
        let info = '';
        for(let i = 0; i < this.#currentBody.length; i++) {
            info += `\r\n\t\t{x:${this.#currentBody[i].x},y:${this.#currentBody[i].y}}`;
        }
        return info;
    }
    #debug_previousBody() {
        if (typeof this.#previousBody == 'undefined') return;
        let info = '';
        for(let i = 0; i < this.#previousBody.length; i++) {
            info += `\r\n\t\t{x:${this.#previousBody[i].x},y:${this.#previousBody[i].y}}`;
        }
        return info;
    }
    #debug_possibleMovements() {
        return `\r\n\t\ttop:${this.#possibleMovements.top}` + 
        `\r\n\t\tbottom:${this.#possibleMovements.bottom}` + 
        `\r\n\t\tleft:${this.#possibleMovements.left}` +
        `\r\n\t\tright:${this.#possibleMovements.right}`;
    }
    #debug_currentDirection() {
        return `\r\n\t\ttop:${this.#currentDirection.top}` + 
        `\r\n\t\tbottom:${this.#currentDirection.bottom}` + 
        `\r\n\t\tleft:${this.#currentDirection.left}` +
        `\r\n\t\tright:${this.#currentDirection.right}`;
    }
    #debug_previousDirection() {
        return `\r\n\t\ttop:${this.#previousDirection.top}` + 
        `\r\n\t\tbottom:${this.#previousDirection.bottom}` + 
        `\r\n\t\tleft:${this.#previousDirection.left}` +
        `\r\n\t\tright:${this.#previousDirection.right}`;
    }

    constructor(newBody, movements, direction) {
        this.init(newBody, movements, direction);
    }
    
    get head() {
        return this.#currentBody[0];
    }

    get bodyParts() {
        let body = JSON.parse(JSON.stringify(this.#currentBody));
        body.shift();
        return body;
    }

    get currentBody() {
        return this.#currentBody;
    }

    get previousBody() {
        return this.#previousBody;
    }

    get possibleMovements() {
        return this.#possibleMovements;
    }

    get currentDirection() {
        return this.#currentDirection;
    }

    get previousDirection() {
        return this.#previousDirection;
    }

    set currentBody(currentBody) {
        this.#currentBody = currentBody;
    }

    set previousBody(previousBody) {
        this.#previousBody = previousBody;
    }

    set possibleMovements(possibleMovements) {
        this.#possibleMovements = possibleMovements;
    }

    set currentDirection(currentDirection) {
        this.#currentDirection = currentDirection;
    }

    set previousDirection(previousDirection) {
        this.#previousDirection = previousDirection;
    }

    init(newBody, movements, direction) {
        this.#currentBody = JSON.parse(JSON.stringify(newBody));
        this.#previousBody = undefined;
        this.#possibleMovements = JSON.parse(JSON.stringify(movements));
        this.#currentDirection = JSON.parse(JSON.stringify(direction));
        this.#previousDirection = {
            'top': false,
            'bottom': false,
            'left': false,
            'right': false
        }
    }

    #storeCurrentBodyIntoPreviousBody() {
        if (this.#previousBody == undefined) {
            this.#previousBody = [];
        }
        this.#previousBody.splice(0, this.#previousBody.length);
        this.#currentBody.forEach(element => {
            this.#previousBody.push(element);
        });
    }

    moveUp() {
        if (!this.possibleMovements.top) { console.log("nope"); return; }
        this.#storeCurrentBodyIntoPreviousBody();
        this.#previousDirection = JSON.parse(JSON.stringify(this.#currentDirection));
        this.#currentBody.pop();
        this.#currentBody.unshift({
            x: this.#currentBody[0].x, 
            y: this.#currentBody[0].y - 1
        });
        this.#possibleMovements.top = true;
        this.#possibleMovements.bottom = false;
        this.#possibleMovements.left = true;
        this.#possibleMovements.right = true;
        this.#currentDirection.top = true;
        this.#currentDirection.bottom = false;
        this.#currentDirection.left = false;
        this.#currentDirection.right = false;

    }
    
    moveDown() {
        if (!this.possibleMovements.bottom) { console.log("nope"); return; }
        this.#storeCurrentBodyIntoPreviousBody();
        this.#previousDirection = JSON.parse(JSON.stringify(this.#currentDirection));
        this.#currentBody.pop();
        this.#currentBody.unshift({
            x: this.#currentBody[0].x, 
            y: this.#currentBody[0].y + 1
        });
        this.#possibleMovements.top = false;
        this.#possibleMovements.bottom = true;
        this.#possibleMovements.left = true;
        this.#possibleMovements.right = true;
        this.#currentDirection.top = false;
        this.#currentDirection.bottom = true;
        this.#currentDirection.left = false;
        this.#currentDirection.right = false;
    }
    
    moveLeft() {
        if (!this.possibleMovements.left) { console.log("nope"); return; }
        this.#storeCurrentBodyIntoPreviousBody();
        this.#previousDirection = JSON.parse(JSON.stringify(this.#currentDirection));
        this.#currentBody.pop();
        this.#currentBody.unshift({
            x: this.#currentBody[0].x - 1, 
            y: this.#currentBody[0].y
        });
        this.#possibleMovements.top = true;
        this.#possibleMovements.bottom = true;
        this.#possibleMovements.left = true;
        this.#possibleMovements.right = false;
        this.#currentDirection.top = false;
        this.#currentDirection.bottom = false;
        this.#currentDirection.left = true;
        this.#currentDirection.right = false;
    }
    
    moveRight() {
        if (!this.possibleMovements.right) { console.log("nope"); return; }
        this.#storeCurrentBodyIntoPreviousBody();
        this.#previousDirection = JSON.parse(JSON.stringify(this.#currentDirection));
        this.#currentBody.pop();
        this.#currentBody.unshift({
            x: this.#currentBody[0].x + 1, 
            y: this.#currentBody[0].y
        });
        this.#possibleMovements.top = true;
        this.#possibleMovements.bottom = true;
        this.#possibleMovements.left = false;
        this.#possibleMovements.right = true;
        this.#currentDirection.top = false;
        this.#currentDirection.bottom = false;
        this.#currentDirection.left = false;
        this.#currentDirection.right = true;
    }

    grow() {
        this.#currentBody.push({
            x: this.#previousBody[JSON.parse(JSON.stringify(this.#currentBody)).length-1].x, 
            y: this.#previousBody[JSON.parse(JSON.stringify(this.#currentBody)).length-1].y
        });
    }
}