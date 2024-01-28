function main(fname)
    %tipi objektov na voljo:
    %krogla ... P = [r, g, b, x, y, z, radij]
    %torus ... P = [r, g, b, x, y, z, radij, Radij], 
    %checkerboard ... P = [r1, g1, b1, r2, g2, b2, z]
    %horizontalna ploskev ... P = [r,g,b,z]

    S = readstruct(fname);
    o = S.objekti;
    
    nObj = size(o, 2);
    tipi = cell(1, nObj);
    parametri = cell(1, nObj);

    for i = 1:nObj
        tipi{i} = str2func(o(i).tip);
        parametri{i} = o(i).parametri;
    end
    
    loc = S.loc;
    luc = transpose(S.luc);
    T0 = transpose(S.T0);
    
    BG = S.BG;
    GPU = S.GPU;
    glad = S.glad;
    
    tStart = tic;
    raytracing(T0, loc, luc, tipi, parametri, BG, GPU, glad)
    toc(tStart)
end