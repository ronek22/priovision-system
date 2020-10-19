import { HttpClient } from '@angular/common/http';
import { templateJitUrl } from '@angular/compiler';
import { Injectable } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Observable, ReplaySubject, Subject } from 'rxjs';
import { Client } from '../models/client';
import { ConfigurationService } from './configuration.service';

@Injectable({
  providedIn: 'root'
})
export class ClientService {

  // communication between create and list client component
  reload = new ReplaySubject<boolean>(1); 

  controlerUrl = '/upc'
  baseLink = `${this.configurationService.apiUrl}${this.controlerUrl}`;
  
  constructor(private http: HttpClient, private configurationService: ConfigurationService) { }

  getClients() {
    return this.http.get<Client[]>(`${this.baseLink}/list`)
  }

  addClient(form: NgForm) {
    return this.http.post<any>(`${this.baseLink}/create`, form);
  }

  editClient(id, form) {
    return this.http.put<any>(`${this.baseLink}/client/${id}/`, form);
  }

  deleteClient(id) {
    return this.http.delete<any>(`${this.baseLink}/client/${id}/`);
  }


  getProfit() {
    return this.http.get<any>(`${this.baseLink}/profit`);
  }


  sendRequestToReload() {
    this.reload.next(true);
  }



}
