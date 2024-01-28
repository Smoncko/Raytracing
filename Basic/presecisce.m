function [X, gradF,CLR] = presecisce(T0, v, h, F, P)
    %funkcija na vhodu prejme argumente 
    %T0 .. izhodišče žarka
    %v ... vektor med izhodiščem in pikslom ( [a,b,c] ), parameterizirana premica
    %h ... korak
    %F ... funckija 
    %in na izhodu vrne
    %X ... vektor 3x1, točka presečišča premice vzdolž v ter funkcije F
    %gradF ... 3x1, gradient F v točki X oz. v presečišču
    
    
    %Če se v ter F ne sekata, sta X ter gradX NaN
    X = NaN;
    gradF = NaN;
    CLR = NaN;
    maxit = 1000;

    zacSign = sign(F(T0,P));
    
    
    for i=1:maxit
        %izračunamo točko v trenutnem koraku
        T = T0+i*h*v;
    
        %Če je vrednost F v točki T spremenila predznak, pomeni, da smo jo
        %sekali oz. smo na drugi "strani" ploskve
        if(sign(F(T,P)) == -zacSign)
    
            %Newtonova metoda za natančen izračun točke sekanja
            [t,gradF,CLR] = newton(F, T0, P, i*h - h/2, v);
            X = T0 + t*v;
           break;
        end
    end
end