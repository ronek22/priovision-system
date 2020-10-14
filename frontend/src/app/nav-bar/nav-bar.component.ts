import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { AuthenticationService } from '../services/authentication.service';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit {

  pageLinks = [];
  loggedInPageLinks = [{ route: 'home', text:'Home'}]
  loggedOutPageLinks = [{ route: 'home', text: 'Home'}]
  accountLinks = [];
  loggedInAccountLinks = [{route: 'logout', text: 'Logout', class: 'btn btn-icon btn-warning', icon: 'logout'}]
  loggedOutAccountLinks = [{route: 'login', text: 'Login', class: 'btn btn-icon btn-primary', icon: 'login'}]
  activePageLink = this.pageLinks[0];

  private componentDestroyed: Subject<void> = new Subject();

  constructor(private authenticationService: AuthenticationService) { }

  ngOnInit(){
    this.authenticationService.isLoggedIn.pipe(takeUntil(this.componentDestroyed))
      .subscribe((result: boolean) => {
        this.accountLinks = result ? this.loggedInAccountLinks : this.loggedOutAccountLinks;
        this.pageLinks = result ? this.loggedInPageLinks : this.loggedOutPageLinks;
      })
  }

  ngOnDestroy() {
    this.componentDestroyed.next();
    this.componentDestroyed.unsubscribe();
  }

}
