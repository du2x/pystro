export class User {
    email: string;
    name: boolean;
    phone: string;
    password: string;
    username: string;
    activation_token: string;
    constructor(email?: string, name?: string, 
                phone?: string, password?: string,
            activation_token?: string) {}
}