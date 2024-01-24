function [vr,gradF,CLR] = ploskev(V0,P)
  %za ravnino s funkcijo z = zodmik
 
  CLR = uint8([P(1),P(2),P(3)]);
  z = V0(3);
  
  zodmik = P(4);
  vr = z-zodmik;
  
  gradF = [0;
        0;
        1];
end
