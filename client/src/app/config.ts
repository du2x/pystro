import { environment } from '../environments/environment';

interface Config {
    BASE_URL: string;
}

export let config: Config;

if (environment.production) {
    config = {
        BASE_URL: 'http://pystro.herokuapp.com'
    }
} else {
    config = {
        BASE_URL: 'http://localhost:5000'
    }    
}
