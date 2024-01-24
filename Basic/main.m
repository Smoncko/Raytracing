function main()
     %oz postavitev kamere
    res = 900;
    
    %luc = [-0.6 ;-0.5; 1];
    red = [255,0,0];
    blue = [0,0,255];
    white = [255,255,255];
    black = [0,0,0];
    %funkcije na voljo:
    %krogla ... P = [r, g, b, x, y, z, radij]
    %torus ... P = [r, g, b, x, y, z, radij, Radij], 
    %checkerboard ... P = [r1, g1, b1, r2, g2, b2, z]
    %ploskev horizontalna ... P = [r,g,b,z]
    %funkcije = {@torus};

    %odboj krogle v checkerboard
    funkcije = { @krogla, @checkerboard};
    parametri= {[255, 0, 0, 0,2,0.3,1.05],[black,white,-1]};
    luc = [-0.6 ;-0.5; 1];
    T0 = [0;-1;0];

    %senca
    %funkcije = { @krogla, @krogla,@ploskev};
    %parametri = {[136,46,149,-0.8,2.35,0.8,0.6],[255,11,255,1.2,3,-1.2,1.5],[200,200,200,-3],[red,0,2,-1,0.5]};
    %luc = [-4.2;1.6;4.2];
    %T0 = [0;-1;0];
    
    %senca2
    %funkcije = {@krogla,@krogla,@ploskev};
    %parametri = {[red,-0.4,2,0,1],[blue,0.5,1,-0.4,0.6],[220,220,220,-1]};
    %T0 = [0;-1;0];
    %luc = [-2;0;1.8];

    % torus - 
    % parametri = {[200,70,70,0,2.5,-2.3,0.5,1]};
    % parametri = {[200, 70, 70,-0.5, 1, 1, 0.5 ], [130, 90, 150, 1, 1, 0.5, 0.5]};
    % krogle1,2,zadaj: parametri = {[150, 30, 30, -0.9, 2.5, 0.9, 0.6 ], [30, 200, 80, 1.2, 3, -1.2, 1.5], [200,200,200,4]};
    

    raytracing(T0, res, luc, funkcije, parametri)
end