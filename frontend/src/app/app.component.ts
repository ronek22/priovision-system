import { Component } from '@angular/core';
import { NavigationCancel, NavigationEnd, NavigationError, NavigationStart, Router, RouterEvent } from '@angular/router';
import { AlertService } from './services/alert.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';

  options = {
    autoClose: true,
    keepAfterRouteChange: false
  }

  loading: boolean = true;

  constructor(private router: Router, public alertService: AlertService) {
    this.router.events.subscribe((e: RouterEvent) => {
      this.navigationInterceptor(e);
    })
  }

  navigationInterceptor(event: RouterEvent) {
    if (event instanceof NavigationStart) {
      this.loading = true; 
    }
    if (event instanceof NavigationEnd) {
      this.loading = false;
    }

    if (event instanceof NavigationCancel) {
      this.loading = false;
    }

    if (event instanceof NavigationError) {
      this.loading = false;
    }
  }
}
