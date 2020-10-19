import { Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';

@Injectable({providedIn: 'root'})
export class AuthGuard implements CanActivate {
    constructor(private router: Router) {}

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        if (localStorage.getItem('currentUser')) {
            // logged in user should not have access to login or register view
            if (state.url.indexOf("login") !== -1 || state.url.indexOf("register") !== -1) {
                return false;
            }
            return true;
        }

        // anonymous user should have access to login or register view
        if (state.url.indexOf("login") !== -1 || state.url.indexOf("register") !== -1)
            return true;

        // anonymous user should automatically be redirected to login view
        this.router.navigate(['/login'], {queryParams: {returnUrl: state.url}});
        return false;
    }
}