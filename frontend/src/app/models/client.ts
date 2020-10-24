export class Client {
    id: string;
    number: number;
    type: string;
    core: number;
    premium: number;
    total: number;
    created_on: string;
    profit? : number;


    constructor(id, number, type, core, premium, total, created_on) {
        this.id = id;
        this.number = number;
        this.type = type;
        this.core = core;
        this.premium = premium;
        this.total = total;
        this.created_on = created_on;
    }
}