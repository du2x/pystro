import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'; 
import { Restaurant } from '../models';
import { DevConfig } from '../config';
import { Observable } from 'rxjs/Observable';
import { catchError, map, tap } from 'rxjs/operators';
import { of } from 'rxjs/observable/of';

@Injectable()
export class RestaurantService {  
  private restaurantURL = DevConfig.BASE_URL+'/restaurants';
  constructor(private http: HttpClient) {}
  getRestaurants(): Observable<Restaurant[]> {
    return this.http.get<Restaurant[]>(this.restaurantURL);
  }

}
