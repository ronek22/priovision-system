import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, NgForm, Validators } from '@angular/forms';
import { ClrLoadingState } from '@clr/angular';
import { ClientService } from 'src/app/services/client.service';
import { ValidatorsService } from 'src/app/services/validators.service';

@Component({
  selector: 'client-create',
  templateUrl: './client-create.component.html',
  styleUrls: ['./client-create.component.css']
})
export class ClientCreateComponent implements OnInit {
  
  isEdited: boolean = false;
  isDeleted: boolean = false;

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

  onEdit(form: NgForm){

  }

  onDelete(id: number){
    
  }

}
