import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { UserService } from '../../services/user.service';
import { User } from '../../models';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit{
  user: User = new User();
  constructor(private userService: UserService, private route: ActivatedRoute) {}
  ngOnInit(): void {    
    this.user.activation_token = this.route.snapshot.queryParams["token"];
    this.user.email = this.route.snapshot.queryParams["email"];
  }  
  onRegister(): void {
    if(this.user.activation_token){
      this.userService.completeRegistration(this.user)
      .then((user) => {
        console.log(user.json());
      })
      .catch((err) => {
        console.log(err);
      });      
    }
    else {
      this.userService.register(this.user)
      .then((user) => {
        console.log(user.json());
      })
      .catch((err) => {
        console.log(err);
      });
    }  
  }
}