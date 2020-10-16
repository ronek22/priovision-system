import { Component, OnInit } from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { Client } from '../models/client';
import { ClientService } from '../services/client.service';

@Component({
  selector: 'client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.css']
})
export class ClientComponent implements OnInit {

  private componentDestroyed: Subject<void> = new Subject();

  constructor(private clientService: ClientService) { 
  }

  columns = ["Client Id", "Number", "Type", "Core", "Premium", "Total", "Created On"];
  index = ["id", "number", "type", "core", "premium", "total", "created_on"];

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

  onEdit(client) {
    console.log(`Edit: ${client.id}`);
  }

  onDelete(client) {
    console.log(`Delete ${client.id}`);
  }

  openDialog(): void {
    // this.dialog.open(ClientDialog, {});
  }

  ngOnDestroy() {
    this.componentDestroyed.next();
    this.componentDestroyed.unsubscribe();
  }

}
