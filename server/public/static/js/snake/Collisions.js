export default class Collisions {
    #dimensions;
    #farsight;

    constructor(dimensions, farsight) {
        this.#dimensions = dimensions;
        this.#farsight = farsight;
    }
    
    selfHit(head, body) {
        let hits = body.filter(body => JSON.stringify(body) === JSON.stringify(head));
        return hits.length > 0;
    }

    wallHit(snakeHead) {
        return (
            snakeHead.x < 0 ||
            snakeHead.y < 0 ||
            snakeHead.x >= this.#dimensions.x ||
            snakeHead.y >= this.#dimensions.y
        );
    }

    foundFood(food, head) {
        return JSON.stringify(food) === JSON.stringify(head);
    }

    areAnyEmptyBlocksOnBoard(snakeLength) {
        return (snakeLength) < ((this.#dimensions.x) * (this.#dimensions.y) - Math.min(this.#dimensions.x, this.#dimensions.y));
    }

    foodIsCoverBySnake(body, foodLocation) {
        let hits = body.filter(bodyPart => JSON.stringify(bodyPart) === JSON.stringify(foodLocation));
        return hits.length > 0;
    }

    generateCoords() {
        return {
            x: Math.floor(Math.random() * (this.#dimensions.x - 0)) + 0, 
            y: Math.floor(Math.random() * (this.#dimensions.y - 0)) + 0
        };
    }

    generateFoodLocation(currentSnakeBody) {
        let foodLocation = this.generateCoords();
        if (this.foodIsCoverBySnake(currentSnakeBody, foodLocation)) { 
            return this.generateFoodLocation(currentSnakeBody);
        }
        return foodLocation;
    }

    foodDirection(head, foodLocation) {
        return {
            "left" : foodLocation.x < head.x,
            "right" : foodLocation.x > head.x,
            "top" : foodLocation.y < head.y,
            "bottom" : foodLocation.y > head.y
        }
    }

    directDanger(head, body, direction) {
        let dangerOnLeft = false;
        let dangerOnRight = false;
        let dangerOnTop = false;
        let dangerOnBottom = false;

        if (direction.top) {
            dangerOnTop = this.#checkDangerOnTop(head, body);
            dangerOnLeft = this.#checkDangerOnLeft(head, body);
            dangerOnRight = this.#checkDangerOnRight(head, body);
        }
        if (direction.bottom) {
            dangerOnBottom = this.#checkDangerOnBottom(head, body);
            dangerOnLeft = this.#checkDangerOnLeft(head, body);
            dangerOnRight = this.#checkDangerOnRight(head, body);
        }
        if (direction.left) {
            dangerOnTop = this.#checkDangerOnTop(head, body);
            dangerOnBottom = this.#checkDangerOnBottom(head, body);
            dangerOnLeft = this.#checkDangerOnLeft(head, body);
        }
        if (direction.right) {
            dangerOnTop = this.#checkDangerOnTop(head, body);
            dangerOnBottom = this.#checkDangerOnBottom(head, body);
            dangerOnRight = this.#checkDangerOnRight(head, body);
        }

        return {
            "left" : dangerOnLeft,
            "right" : dangerOnRight,
            "top" : dangerOnTop,
            "bottom" : dangerOnBottom
        }
    }

    #checkDangerOnTop(head, body) {
        for (let farness = 1; farness <= this.#farsight; farness++) {
            head = JSON.parse(JSON.stringify(head));
            head.y = head.y - farness
            if (this.#checkDanger(head, body)) return true;
        }
        return false;
    }

    #checkDangerOnBottom(head, body) {
        for (let farness = 1; farness <= this.#farsight; farness++) {
            head = JSON.parse(JSON.stringify(head));
            head.y = head.y + farness
            if (this.#checkDanger(head, body)) return true;
        }
        return false;
    }

    #checkDangerOnLeft(head, body) {
        for (let farness = 1; farness <= this.#farsight; farness++) {
            head = JSON.parse(JSON.stringify(head));
            head.x = head.x - farness
            if (this.#checkDanger(head, body)) return true;
        }
        return false;
    }

    #checkDangerOnRight(head, body){
        for (let farness = 1; farness <= this.#farsight; farness++) {
            head = JSON.parse(JSON.stringify(head));
            head.x = head.x + farness
            if (this.#checkDanger(head, body)) return true;
        }
        return false;
    }

    #checkDanger(head, body) {
        let wallHit = this.wallHit(head)
        let bodyHit = this.selfHit(head, body)

        return wallHit || bodyHit;
    }

}