function [X, gradF, CLR, oddaljenost,senca] = rek(v, funkcije, parametri, tr_funkcija, p, T0, luc)
    %p je število odbojev, katerim bomo sledili, "globina rekurzije"
    
    %velikost koraka
    h = 0.08;
    

    X = NaN;
    gradF = NaN;
    CLR = NaN;
    najblizji = NaN;
    oddaljenost = NaN;
    senca = NaN;

    if (p==2)
        return
    end
    
    for i = 1:length(funkcije)
        
        F = funkcije{i};
        P = parametri{i};

        %ne iščemo presečišča funkcije same s sabo
        if (i == tr_funkcija)
            continue;
        else
            [tr_X, tr_gradF, tr_CLR] = presecisce(T0, v, h, F, P);
    
            if (~isnan(tr_X))
                oddaljenost = norm(tr_X-T0);
                
                if (isnan(najblizji) || oddaljenost < najblizji)
                    najblizji = oddaljenost;
                    X = tr_X;
                    gradF = tr_gradF;
                    CLR = tr_CLR;
                    senca = NaN;
                else
                    %če nismo bližje, poskusimo z drugimi ploskvami v prostoru
                    continue;
                end
                
                %Izračunamo odboj žarka glede na normalo ploskve - v našem
                %primeru, je odbojni kot glede na normalo enak vpadnemu kotu,
                %Normala je pa ravno gradient, le da jo še normaliziramo:
    
                n = gradF / norm(gradF);
                odboj = v - 2*dot(v,n)*n;
    
              
                %Vektor med lučjo in presečiščem:
                luc_pr = luc-X;
                
                %Preverimo, če luč kje prej seka kakšen drug objekt
                for k= 1:length(funkcije)
                     F2 = funkcije{k};
                     P2 = parametri{k};
                     if(k == i)  
                         continue;
                     else
                         [X2, ~, ~] = presecisce(luc, -luc_pr, h, F2, P2);
                         if(~isnan(X2))
                             if(norm(luc-X2) < norm(luc_pr))
                                 senca = 1;

                                 break;
                             end
                         end
                     end
                end


                if(isnan(senca))
                    %Barvo določimo na podlagi kosinusa kota med odbitim žarkom in %svetlobnim virom (2. način)
                    cos = dot(luc_pr,odboj)/(norm(luc_pr)*norm(odboj));
                    CLR = (CLR + uint8([255,255,255].*cos))./(norm(luc_pr)/2);
                else
                    CLR = (CLR - uint8([50,50,50]))./(norm(luc_pr)/2);
                end
                CLR = min(CLR, uint8([255, 255, 255]));
                CLR = max(CLR, uint8([0, 0, 0]));
                
                [~, ~, rekCLR, rekNorm] = rek(odboj,funkcije,parametri,i,p+1,X, luc);
                %rekNorm;

                %nastavi barvo na podlagi barv drugih odbojev D:
                %if(isnan(rekCLR))
                %   CLR = CLR + uint8([256,256,256].*abs(cos))
                %end

                if (~isnan(rekNorm))
                    utez1 = 1/oddaljenost^2;
                    utez2 = 1/(rekNorm+oddaljenost)^2;
                    sum = utez1 + utez2;
                    utez1 = utez1 / sum;
                    utez2 = utez2 / sum;
                    CLR = CLR.*utez1+rekCLR.*utez2;
                end
            end
        end
    end
end

