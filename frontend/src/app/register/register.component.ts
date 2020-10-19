import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ValidatorFn, FormControl, AbstractControl, ValidationErrors, NgForm } from '@angular/forms';
import { Subject } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../services/authentication.service';
import { UsernameValidator } from './username-validator';
import { switchMap } from 'rxjs/operators';

function passwordMatchValidator(password: string): ValidatorFn {
  return (control: FormControl) => {
    console.log(control)
    if (!control || !control.parent) {
      return null;
    }
    return control.parent.get(password).value === control.value ? null : { mismatch: true };
  };
}

function emailOrEmpty(control: AbstractControl): ValidationErrors | null {
  return control.value === '' ? null : Validators.email(control);
}




@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;
  username: string = '';
  password: string = '';
  passwordConfirmation: string = '';
  email: string = '';
  returnUrl: string = '';

  private componentDestroyed: Subject<void> = new Subject();

  get isRequesting() {
    return this.authenticationService.isRequesting;
  }

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authenticationService: AuthenticationService,
    private usernameValidator: UsernameValidator
  ) { }



  ngOnInit(): void {
    this.registerForm = this.fb.group({
      'username': [null, [Validators.required], this.usernameValidator.checkUsername.bind(this.usernameValidator)],
      'password': [null, [Validators.required, Validators.minLength(8)]],
      'passwordConfirmation': [null, [Validators.required, passwordMatchValidator('password')]],
      'email': [null, [emailOrEmpty]]
    })
  }

  submit(form: NgForm) {
    this.authenticationService.changeStatus().pipe(switchMap(() => this.authenticationService.register(form)))
    .subscribe(() => {
      this.authenticationService.isRequesting = false;
      this.router.navigate(['/login']);
      console.log("Success registartion");
    })
  }

  ngOnDestroy() {
    this.componentDestroyed.next();
    this.componentDestroyed.unsubscribe();
  }

}
