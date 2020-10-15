import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ValidatorFn, FormControl } from '@angular/forms';
import { Subject } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../services/authentication.service';

function passwordMatchValidator(password: string): ValidatorFn {
  return (control: FormControl) => {
    console.log(control)
    if (!control || !control.parent) {
      return null;
    }
    return control.parent.get(password).value === control.value ? null : { mismatch: true };
  };
}


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;
  Username: string = '';
  Password: string = '';
  PasswordConfirmation: string = '';
  Email: string = '';
  returnUrl: string = '';
  hide = true;

  private componentDestroyed: Subject<void> = new Subject();

  get isRequesting() {
    return this.authenticationService.isRequesting;
  }

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService
  ) { }



  ngOnInit(): void {
    this.registerForm = this.fb.group({
      'Username': [null, [Validators.required]],
      'Password': [null, [Validators.required, Validators.minLength(8)]],
      'PasswordConfirmation': [null, [Validators.required, passwordMatchValidator('Password')]],
      'Email': [null, [Validators.email]]
    })
  }

  submit() {
    if(this.registerForm.valid) {
      console.log(this.registerForm.value);
    }
  }

}
