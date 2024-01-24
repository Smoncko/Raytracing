function raytracing(T0, res, luc, funkcije, parametri)
    %Vrednost res, ki bo določala ločljivost našega zaslona, torej res*res
    %matrika, ki je postavljena na ravnino y=0
    
    %Kvadraten zaslon
    zaslon = zeros(res, res, 3);
    shadows = zeros(res,res);
    %kamera = [0; -1; 0];
    
    %Izberemo nekaj ploskev, ki so podane kot rešitev enačbe oblike f(x,y,z)=0
    %funkcije = {@krogla, @krogla};
    %parametri = {[0,0,255,0,3,0,1.5], [255,0,0,-5,0,4,sqrt(2)]};
    for i = 1:res
        for j = 1:res
            %Položaj trenutnega piksla na kvadratnem zaslonu, ki ima središče
            %v izhodišču koordinatnega sistema, ter oglišča
            %([-1,0,1],[1,0,1],[1,0,-1],[-1,0,-1])
    
            pix = [-1 + (2/res) * j; 0; 1 - (2/res) * i];
            
            %Žarek skozi piksel predstavimo kot parametrično podano premico, ki
            %izhaja iz kamere (T0) in gre skozi piksel na zaslonu: 
            % v = r(pix) - r(kamera) (vektorji)
            % premica = T0 + v*t
            v = pix - T0;
        
            [~, ~, CLR, ~,senca] = rek(v, funkcije, parametri, 0, 0, T0, luc);
            if(~isnan(senca))
                shadows(i,j) = 1;
            end
            %TODO!!!
            %Če žarek ni trčil v noben objekt, bo črna...  
            if(isnan(CLR))
               zaslon(i,j,1) = uint8(0);
               zaslon(i,j,2) = uint8(0);
               zaslon(i,j,3) = uint8(0);
            else
                %Ima neko barvo..
    
                zaslon(i,j,1) = CLR(1);
                zaslon(i,j,2) = CLR(2);
                zaslon(i,j,3) = CLR(3);
            end
        end
    end
   

    %{
for i =1:res
        for j = 1:res
            if(shadows(i,j) == 1)
                sumR = 0;
                sumG = 0;
                sumB = 0;
                sosedCount = 0;
                for x = -2:2
                    for y = -2:2
                        sosed_x = i+x;
                        sosed_y = j+y;
                        if(sosed_x > 0 && sosed_x <=res && sosed_y > 0 && sosed_y <= res)
                            sumR = sumR + zaslon(sosed_x,sosed_y,1);
                            sumG = sumG + zaslon(sosed_x,sosed_y,2);
                            sumB = sumB + zaslon(sosed_x,sosed_y,3);
                            sosedCount = sosedCount +1;
                        end
                    end
                end
               
                zaslon(i,j,1) = sumR / sosedCount;
                zaslon(i,j,2) = sumG/ sosedCount;
                zaslon(i,j,3) = sumB / sosedCount;
            end
        end
        
end
%}
    
    
    %izris slike
    zaslon = zaslon ./ 256;
    imshow(zaslon);
    
end