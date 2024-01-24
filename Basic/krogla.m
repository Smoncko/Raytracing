function [f, gf, rgb] = krogla(V, P)
    % Vhodi:
    % V ... V ∈ R^3
    % r ... r ∈ R
    % V0 ... V0 ∈ R^3, vektor odmikov od središča (x_0, y_0, z_0)
    % rgb ... rgb ∈ [0,255]^3, barva telesa
    % Izhodi:
    % f ... f, funkcija f(x,y,z) = 0, ki predstavlja telo
    % gf ... g, gradient funkcije f
    % rgb ... barva telesa
    

    rgb = uint8(P(1:3));

    Vx = P(4);
    Vy = P(5);
    Vz = P(6);

    r = P(7);

    x = V(1);
    y = V(2);
    z = V(3);
    
    
    f =  (x - Vx).^2 + (y - Vy).^2 + (z - Vz).^2 - r.^2;
    gf =  [(2.*x - 2.*Vx); (2.*y - 2.*Vy); (z - 2.*Vz)];
end



