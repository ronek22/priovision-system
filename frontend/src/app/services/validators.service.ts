import { Injectable } from '@angular/core';
import { FormControl } from '@angular/forms';

function check_if_is_integer(value) {
  return ((parseFloat(value) == parseInt(value)) && !isNaN(value));
}

@Injectable({
  providedIn: 'root'
})
export class ValidatorsService {
  public isInteger = (control:FormControl) => {
    return check_if_is_integer(control.value) ? null : { notNumeric: true}
  }

  constructor() { }
}
