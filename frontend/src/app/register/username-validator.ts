import { FormControl } from '@angular/forms';
import { AuthenticationService } from '../services/authentication.service';
import { Injectable } from '@angular/core';

@Injectable()
export class UsernameValidator {

    debouncer: any;

    constructor(public authenticationService: AuthenticationService){}

    checkUsername(control: FormControl): any {
        clearTimeout(this.debouncer);

        return new Promise(resolve => {
            this.debouncer = setTimeout(() => {
                this.authenticationService.validateUsername(control.value).subscribe((res) => {
                    if (res.available){
                      resolve(null);
                  }
                  else {
                      resolve({'usernameInUse': true});
                  }
                });
            }, 1000);
        });
    }

}