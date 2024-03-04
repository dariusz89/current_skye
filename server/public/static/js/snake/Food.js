export default class Food {
    #currentLocation;
    #previousLocation;

    constructor(location) {
        this.#currentLocation = {'x': location.x, 'y': location.y};
        this.#previousLocation = this.#currentLocation;
    }

    debug_info() {
        return `\r\n\tcurrentLocation: ${this.#debug_currentLocation()}` +
        `\r\n\tpreviousLocation: ${this.#debug_previousLocation()}`;
    }
    #debug_currentLocation() {
        return `\r\n\t\t{x:${this.currentLocation.x},y:${this.#currentLocation.y}}`;
    }
    #debug_previousLocation() {
        return `\r\n\t\t{x:${this.previousLocation.x},y:${this.#previousLocation.y}}`;
    }

    updateFoodLocation(newLocation) {
        this.previousLocation = JSON.parse(JSON.stringify(this.#currentLocation));
        this.currentLocation = newLocation;
    }

    get currentLocation() {
        return this.#currentLocation;
    }

    get previousLocation() {
        return this.#previousLocation;
    }

    set currentLocation(coords) {
        return this.#currentLocation = coords;
    }

    set previousLocation(coords) {
        return this.#previousLocation = coords;
    }   

}