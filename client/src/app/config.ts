interface Config {
    BASE_URL: string;
}

export let config: Config;

if (process.env.NODE_ENV==='heroku') {
    config = {
        BASE_URL = 'http://pystro.herokuapp.com'
    }
} else {
    config = {
        BASE_URL = 'http://localhost:5000'
    }    
}
