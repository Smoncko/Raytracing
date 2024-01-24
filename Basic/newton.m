function [t, gradient,CLR] = newton(F, T0, P, t0, v)
%g(t) := F(T0+v*t)
%F.. funkcija
%t0 .. začetni približek

tol = 1e-5;
maxit = 500;

for k=1:maxit
    

    %izračunamo vrednost ter gradient funkcije v približku
    %vrednost je skalar, gradient pa 3x1 , vrstice so parcialni odvodi
    [vr, gradient,CLR] = F(T0+t0*v, P);
    vr_grad = v(1)*gradient(1) + v(2)*gradient(2)+v(3)*gradient(3);
    
    %... korak newtonove metode
    t = t0 - vr/vr_grad;

    if(norm(t-t0) < tol)
        break;
    end
    t0 = t;
end