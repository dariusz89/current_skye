import Board from './Board.js';
import Collisions from './Collisions.js';
import Events from './Events.js';
import Food from './Food.js';
import Loop from './Loop.js';
import Snake from './Snake.js';

export default class Game {
    START_LINE      = "---------------  START   ---------------";
    START_LINE_END  = "-------------  START END  --------------";
    STOP_LINE       = "---------------  STOP    ---------------";
    STOP_LINE_END   = "-------------  STOP END  ---------------";
    UPDATE_LINE     = "---------------  UPDATE  ---------------";
    UPDATE_LINE_END = "-------------  UPDATE END --------------";
    END_LINE    = "========================================";
    LINE        = "----------------------------------------";
    
    #board;
    #collisions;
    #loop;
    #options;

    events;
    food;
    snake;

    gameMode;
    trainMode;

    renderStats;
    dangerDirection;
    foodDirection;
    alive;
    
    terminated; // true when episode end, or snake is dead 
    truncated; // true when user click end train button

    constructor() {
        this.events = new Events(this);
        
        this.events.add('initGame', "game initialized");
        this.events.dispatch('initGame');
    }

    init(opt) {
        this.#options = opt
        this.#board = new Board(this.#options.dimensions);
        this.#collisions = new Collisions(this.#options.dimensions, this.#options.snake.farsight);
        console.log(this.END_LINE);
    }

    frame() {
        console.log(this.UPDATE_LINE);
        
        this.#move();
        this.#foundFood();
        this.#lookArround();
        this.#isAlive();

        this.#sendEnvironmentData();
        this.#sendEnvironmentInfo();
        
        if (this.state.end) this.stop();

        console.log(this.UPDATE_LINE_END);
    }

    #move() {
        if (this.snake.currentDirection.top) {
            this.snake.moveUp();   
        } else if (this.snake.currentDirection.bottom) {
            this.snake.moveDown();
        } else if (this.snake.currentDirection.left) {
            this.snake.moveLeft();
        } else if (this.snake.currentDirection.right) {
            this.snake.moveRight();
        }
    }

    #lookArround() {
        this.dangerDirection = this.#collisions.directDanger(this.snake.head, this.snake.bodyParts, this.snake.currentDirection)
        this.foodDirection = this.#collisions.foodDirection(this.snake.head, this.food.currentLocation);
    }

    #foundFood() {
        if (this.#collisions.foundFood(this.food.currentLocation, this.snake.head)) {
            this.snake.grow();
            this.#updateFood();
        }
        this.#board.reDrawSnake(this.snake.currentBody, this.snake.previousBody)
    }

    #updateFood() {
        let canGenerateNewFoodLocation = this.#collisions.areAnyEmptyBlocksOnBoard(
            this.snake.currentBody.length
        );
        if (canGenerateNewFoodLocation) {
            let newFoodLocation = this.#collisions.generateFoodLocation(this.snake.currentBody);
            this.food.updateFoodLocation(newFoodLocation);
            this.#board.reDrawFood(this.food.currentLocation, this.food.previousLocation);
        }
    }

    #isAlive() {
        if (this.#collisions.wallHit(this.snake.head) || this.#collisions.selfHit(this.snake.head, this.snake.bodyParts)) {
            console.log("End of episode! => snake die!");
            if (!this.state.end) this.state.end = true;
        }

        if (!this.#collisions.areAnyEmptyBlocksOnBoard(this.snake.currentBody.length)) {
            console.log("End of episode! => snake win!");
            if (!this.state.end) this.state.end = true;
        }
    }

    #sendEnvironmentData() {
        this.events.add('sendEnvironmentData', {
            'obs' : {
                'direction' : this.snake.currentDirection,
                'danger' : this.dangerDirection,
                'food' : this.foodDirection,
                'body' : this.snake.currentBody,
                'alive' : this.alive
            }
        });
        this.events.dispatch('sendEnvironmentData');
    }

    #sendEnvironmentInfo() {
        this.events.add('sendEnvironmentInfo', {
            'info' : {
                'renderStats' : this.renderStats,
                'terminated' : this.terminated,
                'truncated' : this.truncated
            }
        });
        this.events.dispatch('sendEnvironmentInfo');
    }

    start() {
        console.log(this.START_LINE)
        console.log("START: Game has been started!");

        this.state.end = false;
        this.state.isRunning = true;

        this.alive = true;

        this.snake = new Snake(this.#options.snake.body, this.#options.snake.movement, this.#options.snake.direction);
        this.food = new Food(this.#options.food.location);

        this.#board.drawFood(this.food.currentLocation);
        this.#board.drawSnake(this.snake.currentBody);

        this.#loop = new Loop(this);
        this.#loop.initLoop();
        console.log(this.START_LINE_END);
    }

    stop() {
        console.log(this.STOP_LINE);
        console.log("STOP: Game has been stopped!");

        this.state.end = true;
        this.state.isRunning = false;

        this.alive = false;

        if (this.#loop) {
            this.#loop.breakLoop();
            this.#loop = false;
        }

        this.#board.undrawFood(this.food.currentLocation);
        this.#board.undrawSnake(this.snake.currentBody);

        if (this.food) this.food = false;
        if (this.snake) this.snake = false;
        console.log(this.STOP_LINE_END);
    }

    state = {
        selfInternal: null,
        endInternal: null,
        isRunningInternal : false,
        endListener: function(val) {
            console.log("Value of state.end changed to " + val);
        },
        set self(val) {
            this.selfInternal = val;
        },
        get self() {
            return this.selfInternal;
        },
        set end(val) {
            this.endInternal = val;
            this.endListener(val);
        },
        get end() {
            return this.endInternal;
        },
        set isRunning(val) {
            this.isRunningInternal = val;
        },
        get isRunning() {
            return this.isRunningInternal;
        }
    }
    
    /**
     * Observation state:
     *  - zagrożenie - done
     *  - aktualny kierunek węża - done
     *  - lokalizacja jedzenia z uwzględnieniem głowy węża - done
     */

}
