import { TestBed, inject } from '@angular/core/testing';

import { RestaurantService } from './restaurant.service';

describe('RestaurantService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [RestaurantService]
    });
  });

  it('should be created', inject([RestaurantService], (service: RestaurantService) => {
    expect(service).toBeTruthy();
  }));
});
