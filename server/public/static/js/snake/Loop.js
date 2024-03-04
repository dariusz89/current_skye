export default class Loop {
    #context;
    
    #frameCounter;
    #startTime;

    #animationFrame;
    #fps;
    #then;
    #interval;
    
    #now;
    #delta;

    constructor(context) {
        this.#context = context;
        this.#frameCounter = 0;
    }

    initLoop() {
        this.#fps = 1;
        this.#then = performance.now();
        this.#startTime = this.#then;
        this.#interval = 1000/this.#fps;
        this.#animationFrame = requestAnimationFrame(() => this.#startRender());
    }

    breakLoop() {
        this.#stopRender();
    }

    #startRender() {
        if (!this.#context.end) this.#animationFrame = requestAnimationFrame(() => this.#startRender());
        this.#now = performance.now();
        this.#delta = this.#now - this.#then;

        if (this.#delta > this.#interval) {
            this.#then = this.#now - (this.#delta % this.#interval);
            this.#frameCounter += 1;
            
            this.#context.renderStats = {
                "animationFrame" : this.#animationFrame, 
                "count": this.#frameCounter,
                "now": this.#now,
                "then": this.#then,
                "delta": this.#delta,
                "interval": this.#interval,
                "current fps": Math.round(1000 / ((this.#now - this.#startTime) / this.#frameCounter) * 100) / 100,
                "target fps": this.#fps
            }

            if (this.#context.snake == undefined || this.#context.end) {
                this.#stopRender();
                return;
            }

            this.#context.frame();
        }
        
    }

    #stopRender() {
        if (this.#animationFrame) {
            cancelAnimationFrame(this.#animationFrame);
            this.#animationFrame = undefined;
        }
    }
}