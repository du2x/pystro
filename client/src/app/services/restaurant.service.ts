import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'; 
import { Restaurant } from '../models';
import { config } from '../config';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class RestaurantService {  
  private restaurantURL = config.BASE_URL+'/restaurants';
  constructor(private http: HttpClient) {}
  getRestaurants(): Observable<Restaurant[]> {
    return this.http.get<Restaurant[]>(this.restaurantURL);
  }

}
