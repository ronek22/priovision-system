import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { empty, Observable } from 'rxjs'
import { catchError, map } from 'rxjs/operators'
import { AuthenticationService } from './authentication.service'

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

    constructor(private authenticationService: AuthenticationService) {}

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(catchError(err => {
            if (err.status === 403) {
                return this.handleUnauthorized(request, next);
            }
            
        }))
    }

    handleUnauthorized(req: HttpRequest<any>, next: HttpHandler): Observable<any> {
        localStorage.removeItem('currentUser');
        return this.authenticationService.refreshToken().pipe(map(user => {
            if (user && user.access_token) {
                localStorage.setItem('currentUser', JSON.stringify(user));
              }
            return next.handle(req);
        }))
    }


}