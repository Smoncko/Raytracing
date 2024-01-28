function raytracing(T0, loc, luc, tipi, parametri, BG, GPU, glad)
    %Vektor res, ki določala ločljivost zaslona, torej res(0)*res(1)
    %matrika, ki je postavljena na ravnino y=0
    
    r0 = loc(1);
    r1 = loc(2);

    zaslon = zeros(r0, r1, 3);
    shadows = zeros(r0, r1);
    
    if GPU == false
        for i = 1:r0
            for j = 1:r1
                %Položaj trenutnega piksla na kvadratnem zaslonu, ki ima
                %središče v izhodišču koordinatnega sistema
                %in oglišča ([-1,0,1],[1,0,1],[1,0,-1],[-1,0,-1])
        
                pix = [-1 + (2/r1) * j; 0; 1 - (2/r0) * i];
                
                %Žarek skozi piksel predstavimo kot parametrično podano premico, ki
                %izhaja iz kamere (T0) in gre skozi piksel na zaslonu: 
                % v = r(pix) - r(kamera) (vektorji)
                % premica = T0 + v*t
                v = pix - T0;
            
                [~, ~, CLR, ~, senca] = rek(v, tipi, parametri, 0, 0, T0, luc);
    
                if (~isnan(senca))
                    shadows(i, j) = 1;
                end
    
                %Če žarek ni trčil v noben objekt, bo barva ozadja
                if (isnan(CLR))
                   zaslon(i, j, :) = BG;
                else
                    %Ob trku dobi barvo objekta
                    zaslon(i, j, :) = CLR;
                end
            end
        end
    end

    if GPU == true
        parfor i = 1:r0
            for j = 1:r1
                pix = [-1 + (2/r1) * j; 0; 1 - (2/r0) * i];

                v = pix - T0;
            
                [~, ~, CLR, ~, senca] = rek(v, tipi, parametri, 0, 0, T0, luc);
    
                if (~isnan(senca))
                    shadows(i, j) = 1;
                end

                if (isnan(CLR))
                   zaslon(i, j, :) = BG;
                else
                    zaslon(i, j, :) = CLR;
                end
            end
        end
    end
   

    if glad == true
        for i =1:r0
            for j = 1:r1
                if(shadows(i,j) == 1)
                    sumR = 0;
                    sumG = 0;
                    sumB = 0;
                    sosedCount = 0;
                    for x = -2:2
                        for y = -2:2
                            sosed_x = i+x;
                            sosed_y = j+y;
                            if(sosed_x > 0 && sosed_x <= loc && sosed_y > 0 && sosed_y <= loc)
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
    end
    
    %Izris slike
    zaslon = zaslon ./ 256;
    imshow(zaslon);
    
end