function [vr,gradF,CLR] = checkerboard(v0,P)
  
  %za ravnino z = P(1)

 

%checkerboard color
xt = mod(ceil(v0(1)),2);
yt = mod(ceil(v0(2)),2);


if (mod((xt+yt),2) == 1)
  CLR = uint8([P(1),P(2),P(3)]); 
else
  CLR = uint8([P(4),P(5),P(6)]);
end
  z = v0(3);
  
  zodmik = P(7);
  vr = z-zodmik;
  
  gradF = [0;
        0;
        1];
end
