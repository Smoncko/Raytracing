function [vr,gradF,CLR] = zadaj(V0,P)
  %za ravnino s funkcijo y = yodmik
  
  CLR = uint8([P(1),P(2),P(3)]);
  vr = V0(2)-P(4);
  
  
  gradF = [0;
        1;
        0];
end
