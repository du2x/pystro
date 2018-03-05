import { Component, OnInit } from '@angular/core';
import { User } from '../../models';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent {
  user: User = new User();  
  constructor(private auth: UserService) {}  
  onLogin(): void {
    this.auth.login(this.user)
    .then((user) => {
      console.log(user.json());
    })
    .catch((err) => {
      console.log(err);
    });
  }
}