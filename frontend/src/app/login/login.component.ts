import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, NgForm } from '@angular/forms';
import { Subject } from 'rxjs';
import { AuthenticationService } from '../services/authentication.service';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntil, switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  Username: string = '';
  Password: string = '';
  returnUrl: string;
  hide = true;

  private componentDestroyed: Subject<void> = new Subject();

  get isRequesting() {
    return this.authenticationService.isRequesting;
  }

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
  ) { }

  ngOnInit(): void {
    // to initialize FormGroup
    this.loginForm = this.fb.group({
      'Username': [null, Validators.compose([Validators.required, Validators.max(15)])],
      'Password': [null, Validators.compose([Validators.required])]
    });

    // get return url from route parameters or default to '/'
    this.route.queryParams.pipe(takeUntil(this.componentDestroyed)).subscribe(params => {
      if (!params.returnUrl || params.returnUrl === '/logout') {
        this.returnUrl = '/';
      }
      else {
        this.returnUrl = params.returnUrl;
      }
    });
  }

  // Exectued when Form is Submitted
  onFormSubmit(form: NgForm) {
    this.authenticationService.changeStatus().pipe(switchMap(() => this.authenticationService.login(form['Username'], form['Password'])))
      .subscribe((user: any) => {
        this.authenticationService.isRequesting = false;
        console.log("TRYING TO LOGIN")
        this.router.navigate([this.returnUrl]);
      });
  }

  ngOnDestroy() {
    this.componentDestroyed.next();
    this.componentDestroyed.unsubscribe();
  }

}
