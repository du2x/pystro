import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'; 
import { Restaurant, Section } from '../models';
import { config } from '../config';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class RestaurantService {  
  private restaurantsURL = config.BASE_URL+'/restaurants';  
  private access_token = localStorage.getItem('token');
  private headers: HttpHeaders = new HttpHeaders({'Authorization': 'JWT ' + this.access_token});
  constructor(private http: HttpClient) {}
  getRestaurants(): Observable<Restaurant[]> {
    return this.http.get<Restaurant[]>(this.restaurantsURL, {headers: this.headers});
  }
  getRestaurant(cname: string): Observable<Restaurant> {
    return this.http.get<Restaurant>(config.BASE_URL+'/restaurant/'+cname, {headers: this.headers});
  }
  getMenu(cname: string): Observable<Section[]> {
    return this.http.get<Section[]>(config.BASE_URL+'/'+cname+'/menu', {headers: this.headers});
  }
  
}
