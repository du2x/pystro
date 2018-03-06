import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { UserService } from '../../services/user.service';
import { User } from '../../models';


@Component({
  selector: 'app-resetpassword',
  templateUrl: './resetpassword.component.html',
  styleUrls: ['./resetpassword.component.css']
})
export class ResetpasswordComponent implements OnInit{
  user: User = new User();
  constructor(private userService: UserService, private route: ActivatedRoute, private router: Router) {}
  ngOnInit(): void {    
    this.user.reset_pw_token = this.route.snapshot.queryParams["token"];
    this.user.email = this.route.snapshot.queryParams["email"];
  }  
  onRequestResetPassword(): void {
    this.userService.requestResetPassword(this.user)
    .then((user) => {
      this.router.navigate(['']);
    })
    .catch((err) => {
      console.log(err);
    });      
  }
  onResetPassword(): void {
    this.userService.resetPassword(this.user)
    .then((user) => {
      this.router.navigate(['']);
    })
    .catch((err) => {
      console.log(err);
    });      
  }

}
