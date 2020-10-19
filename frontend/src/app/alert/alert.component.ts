import { Component, Input, OnInit } from '@angular/core';
import { NavigationStart, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { Alert, AlertType } from '../models/alert';
import { AlertService } from '../services/alert.service';

@Component({
  selector: 'alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.css']
})
export class AlertComponent implements OnInit {

  @Input() id = 'default-alert';
  @Input() fade = true;

  alerts: Alert[] = [];
  alertSubscription: Subscription;
  routeSubscription: Subscription;
  
  constructor(private router: Router, private alertService: AlertService) { }

  ngOnInit(): void {
    this.alertSubscription = this.alertService.onAlert(this.id)
      .subscribe(alert => {
        // clear alerts when an empty alert is received
        if (!alert.message) {
          // filter out alerts without keepAfterRouteChange flag
          this.alerts = this.alerts.filter(x => x.keepAfterRouteChange);

          // remove keepAfterRouteChange flag on the rest
          this.alerts.forEach(x => delete x.keepAfterRouteChange);
          return;
        }

        // add alert to array
        this.alerts.push(alert);

        // auto close alert if required
        if (alert.autoClose) {
          setTimeout(() => this.removeAlert(alert), 3000);
        }
      });

      // clear alerts on location change
      this.routeSubscription = this.router.events.subscribe(event => {
        if (event instanceof NavigationStart) {
          this.alertService.clear(this.id);
        }
      });
  }

  ngOnDestroy() {
    this.alertSubscription.unsubscribe();
    this.routeSubscription.unsubscribe();
  }

  removeAlert(alert: Alert) {
    if (!this.alerts.includes(alert)) return;

    if (this.fade) {
      this.alerts.find(x => x === alert).fade = true;

      setTimeout(() => {
        this.alerts = this.alerts.filter(x => x !== alert);
      }, 250);
    } else {
      this.alerts = this.alerts.filter(x => x !== alert);
    }
  }

  cssClass(alert: Alert) {
    if (!alert) return;

    // const classes = ['alert', 'alert-dismissable'];
    const classes = []

    const alertTypeClass = {
      [AlertType.Success]: 'success',
      [AlertType.Error]: 'danger',
      [AlertType.Info]: 'info',
      [AlertType.Warning]: 'warning'
    }

    classes.push(alertTypeClass[alert.type]);

        if (alert.fade) {
            classes.push('fade');
        }

        return classes.join(' ');
  }

}
