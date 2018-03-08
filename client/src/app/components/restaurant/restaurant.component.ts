import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { Restaurant } from '../../models';
import { RestaurantService } from '../../services/restaurant.service';


@Component({
  selector: 'app-restaurant',
  templateUrl: './restaurant.component.html',
  styleUrls: ['./restaurant.component.css']
})
export class RestaurantComponent implements OnInit {
  private restaurant: Restaurant;
  constructor(private restaurantService: RestaurantService, 
              private route: ActivatedRoute, 
              private router: Router) {}
  ngOnInit() {
    let id = this.route.snapshot.paramMap.get('id');
    this.restaurantService.getRestaurant(+id)
      .subscribe(restaurant => this.restaurant = restaurant);
  }

}
