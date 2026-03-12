# Koda za diplomsko nalogo sledenje žarkom

## Uporaba programa
Program poganjamo preko ukazne vrstice v obliki:
```
python main.py konfig.json
```
kjer je *konfig.json* konfiguracijska datoteka v sledečem formatu:x

    "objekti": niz                                    - ime datoteke v formatu .obj
    "loc": [x, y]                                     - ločljivost slike
    "luc": [x, y]                                     - položaj luči
    "luc_moc": i                                      - moč luči
    "T0": [x, y, z]                                   - položaj opazovalca
    "viewport": i                                     - velikost platna
    "BG": [r, g, b]                                   - barva ozadja
    "barve": [[r_1, g_1, b_1], [r_2, g_2, b_2], ...]  - barve objektov
    "glad": bool                                      - glajenje ozadja
    "bvh": bool                                       - prva implementacija BVH
    "bvh2": bool                                      - druga implementacija BVH
    "bvh3": bool                                      - tretja implementacija BVH
    "sence": bool                                     - učinek senc
    "max_odbojev": i                                  - največje dovoljeno število odbojev

Dve take konfiguracijski datoteki s pripadajočimi objektnimi datotekami sta za lažjo uporabo že dodani.
Ob izvozu objektne datoteke iz modelirnega programa (kot je npr. Blender) je priporočeno, da se nastavita glavni osi na Y (naprej) in Z (gor) ter da datoteko izvozimo brez UV koordinat in z normalami. Nujno je tudi, da je prizor zgrajen iz trikotnikov in ne štirikotnikov.