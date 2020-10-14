import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {
  isLoggedOut: boolean = false;


  constructor(private authenticationService: AuthenticationService) { }

  ngOnInit(): void {
    setTimeout(() => this.logout(), 1000);
  }

  logout(){
    let currentUser = JSON.parse(localStorage.getItem('currentUser'))
    // add here something like snackbar
    this.isLoggedOut = true;
    this.authenticationService.logout();
  }

}
