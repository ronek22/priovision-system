import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, NgForm, Validators } from '@angular/forms';
import { ClrLoadingState } from '@clr/angular';
import { Client } from 'src/app/models/client';
import { ClientService } from 'src/app/services/client.service';
import { ValidatorsService } from 'src/app/services/validators.service';

@Component({
  selector: 'client-create',
  templateUrl: './client-create.component.html',
  styleUrls: ['./client-create.component.css']
})
export class ClientCreateComponent implements OnInit {
  
  @Input() edited: Client;

  clientForm: FormGroup;
  type: string;
  number: number;
  core: number;
  premium: number;
  total: number;
  

  submitBtnState: ClrLoadingState = ClrLoadingState.DEFAULT;

  constructor(
    private clientService: ClientService,
    private fb: FormBuilder,
    private validatorsService: ValidatorsService
    ) { }

  sendAfterSuccess() {
    this.clientService.sendRequestToReload();
  }

  ngOnInit(): void {
    this.clientForm = this.fb.group({
      'type': [null],
      'number': [null, [Validators.required, this.validatorsService.isInteger]],
      'core': [null, [Validators.required]],
      'premium': [null, [Validators.required]],
      'total': [null, [Validators.required]],
    })
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('value changed', this.edited);
    this.clientForm.setValue({
      type: this.edited.type,
      number: this.edited.number,
      core: this.edited.core,
      premium: this.edited.premium,
      total: this.edited.total
    })
  }

  onSubmit(form: NgForm) {
    if (this.edited) {
      this.onEdit(this.edited.id, form);
    } else {
      this.onCreate(form);
    }
  } 

  onCreate(form: NgForm) {
    this.submitBtnState = ClrLoadingState.LOADING;
    this.clientService.addClient(form).subscribe(() => {
      this.submitBtnState = ClrLoadingState.SUCCESS;
      this.sendAfterSuccess();
      this.clientForm.reset();
    }, 
    (error) => { 
      console.info(error);
      this.submitBtnState = ClrLoadingState.ERROR;
    }
    )
  }

  onEdit(id: any, form: NgForm){
    this.submitBtnState = ClrLoadingState.LOADING;
    this.clientService.editClient(id, form).subscribe(() => {
      this.submitBtnState = ClrLoadingState.SUCCESS;
      this.sendAfterSuccess();
      this.edited = null;
      this.clientForm.reset();
    }, 
    (error) => { 
      console.info(error);
      this.submitBtnState = ClrLoadingState.ERROR;
    }
    )
  }

  cancelEdit() {
    this.edited = null;
    this.clientForm.reset();
  }



}
