import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'; 
import { Restaurant } from '../models';
import { config } from '../config';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class RestaurantService {  
  private restaurantsURL = config.BASE_URL+'/restaurants';  
  constructor(private http: HttpClient) {}
  getRestaurants(): Observable<Restaurant[]> {
    return this.http.get<Restaurant[]>(this.restaurantsURL);
  }
  getRestaurant(id: number): Observable<Restaurant> {
    return this.http.get<Restaurant>(config.BASE_URL+'/restaurant/'+id);
  }
}
