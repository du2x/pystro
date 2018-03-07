import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import { Restaurant } from '../models';
import { DevConfig } from '../config'
import 'rxjs/add/operator/toPromise';

@Injectable()
export class RestaurantService {
  private BASE_URL: string = DevConfig.BASE_URL;
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  constructor(private http: Http) {}
}
