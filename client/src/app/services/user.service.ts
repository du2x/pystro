import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import { User } from '../models';
import { DevConfig } from '../config'
import 'rxjs/add/operator/toPromise';

@Injectable()
export class UserService {
  private BASE_URL: string = DevConfig.BASE_URL;
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  constructor(private http: Http) {}
  login(user): Promise<any> {
    let url: string = `${this.BASE_URL}/auth`;
    return this.http.post(url, user.loginData(), {headers: this.headers}).toPromise();
  }
  register(user): Promise<any> {
    let url: string = `${this.BASE_URL}/users`;
    return this.http.post(url, user, {headers: this.headers}).toPromise();
  }  
  completeRegistration(user): Promise<any> {
    let url: string = `${this.BASE_URL}/users`;
    return this.http.put(url, user, {headers: this.headers}).toPromise();
  }    
  requestResetPassword(user): Promise<any> {
    let url: string = `${this.BASE_URL}/resetpassword`;
    return this.http.put(url, {'email': user.email}, {headers: this.headers}).toPromise();
  }      
  resetPassword(user): Promise<any> {
    let url: string = `${this.BASE_URL}/resetpassword`;
    return this.http.post(url, user.resetPasswordData(), {headers: this.headers}).toPromise();
  }        
}