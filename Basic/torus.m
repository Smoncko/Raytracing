function [f, gf, rgb] = torus(V, P)
% Vhodi:
% V ... V ∈ R^3
% r ... r ∈ R, notranji radij
% R ... R ∈ R, zunanji radij
% V0 ... V0 ∈ R^3, vektor odmikov od središča (x_0, y_0, z_0)
% rgb ...rgb ∈ [0,255]^3, barva telesa
% Izhodi:
% f ... f , funkcija f(x,y,z) = 0, ki predstavlja telo
% gf ... g , gradient funkcije f
% rgb ... barva telesa

rgb = uint8(P(1:3));

Vx = P(4);
Vy = P(5);
Vz = P(6);

r = P(7);
R = P(8);

x = V(1);
y = V(2);
z = V(3);

f = (sqrt((x - Vx).^2 + (y - Vy).^2) - R).^2 + (z - Vz).^2 - r.^2;
gf = [2 .* (x - Vx) .* (sqrt((x - Vx) .^ 2 + (y - Vy) .^ 2) - R) / (sqrt((x - Vx) .^ 2 + (y - Vy) .^ 2));
      2 .* (y - Vy) .* (sqrt((x - Vx) .^ 2 + (y - Vy) .^ 2) - R) / (sqrt((x - Vx) .^ 2 + (y - Vy) .^ 2));
      2 .* (z - Vz)];