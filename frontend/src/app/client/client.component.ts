import { Component, OnInit } from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { Client } from '../models/client';
import { AlertService } from '../services/alert.service';
import { ClientService } from '../services/client.service';

@Component({
  selector: 'client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.css']
})
export class ClientComponent implements OnInit {

  private componentDestroyed: Subject<void> = new Subject();
  isDeleteMode: boolean = false;
  currentClient: Client;

  constructor(private clientService: ClientService, private alertService: AlertService) { 
  }

  columns = ["Number", "Type", "Core", "Premium", "Total", "Created On"];
  index = ["number", "type", "core", "premium", "total", "created_on"];


  clients: Client[] = [];
  profit;

  ngOnInit(): void {
    this.clientService.reload.next(true);

    this.clientService.reload.pipe(takeUntil(this.componentDestroyed))
      .subscribe((result: boolean) => {
        if (result) {
          this.clientService.getClients().subscribe((response) => {
            this.clients = response;
          })

          this.clientService.getProfit().subscribe((response) => {
            this.profit = response;
          })
        }
      })
    
  }

  setContextDelete(client) {
    this.isDeleteMode = true;
    this.currentClient = client;
  }

  unsetContextDelete() {
    this.isDeleteMode = false;
    this.currentClient = null;
  }

  onDelete() {
    console.log(`Deleted current user ${this.currentClient.id}`);
    this.clientService.deleteClient(this.currentClient.id).subscribe(() => {
      this.clientService.sendRequestToReload();
    }, 
    (error) => { 
      this.alertService.error(`Cannot delete client! Error: ${error.message}`)

    })
    this.isDeleteMode = false;

  }

  onEdit(client) {
    console.log(`Edit: ${client.id}`);
    this.currentClient = client;
  }

  openDialog(): void {
    // this.dialog.open(ClientDialog, {});
  }

  ngOnDestroy() {
    this.componentDestroyed.next();
    this.componentDestroyed.unsubscribe();
  }

}
