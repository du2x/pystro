import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import { User } from '../models';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class UserService {
  private BASE_URL: string = 'http://localhost:5000';
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  constructor(private http: Http) {}
  login(user): Promise<any> {
    let url: string = `${this.BASE_URL}/auth`;
    user.username = user.email;
    user.email = undefined;
    return this.http.post(url, user, {headers: this.headers}).toPromise();
  }
  register(user): Promise<any> {
    let url: string = `${this.BASE_URL}/users`;
    return this.http.post(url, user, {headers: this.headers}).toPromise();
  }  
  completeRegistration(user): Promise<any> {
    let url: string = `${this.BASE_URL}/users`;
    return this.http.put(url, user, {headers: this.headers}).toPromise();
  }    
}