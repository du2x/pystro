import { Component, OnInit } from '@angular/core';
import { Restaurant } from '../../models';
import { RestaurantService } from '../../services/restaurant.service';



@Component({
  selector: 'app-restaurants',
  templateUrl: './restaurants.component.html',
  styleUrls: ['./restaurants.component.css']
})
export class RestaurantsComponent implements OnInit {
  
  restaurants: Restaurant[];
  error: string;
  
  constructor(private restaurantService: RestaurantService) { }

  ngOnInit() {
    this.getRestaurants();
  }

  getRestaurants(): void {
    this.restaurantService.getRestaurants()
      .subscribe(restaurants => this.restaurants = restaurants);
  }  

}
