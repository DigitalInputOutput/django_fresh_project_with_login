import { Dom } from "./vanilla/dom.js";
import { Menu } from "./ui/menu.js";

export class Main{
    constructor(){
        this.bindEvents();
        this.menu = new Menu();
    }
    bindEvents(){
        Dom.query('body').on('click', () => {
            console.log("This JS code works");
        });
    }
}