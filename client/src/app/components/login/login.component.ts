import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../../models';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent {
  user: User = new User();  
  constructor(private auth: UserService, private router: Router) {}  
  onLogin(): void {
    this.auth.login(this.user)
    .then((user) => {
      localStorage.setItem('token', user.json().access_token);
      this.router.navigate(['']);
    })
    .catch((err) => {
      console.log(err);
    });
  }
}