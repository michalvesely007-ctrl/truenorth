# -*- coding: utf-8 -*-
"""Texty všech zelených polí – zdroj pravdy podle zadání.

Odkazy na pole se zapisují jako {N:7} (číslo hlavní trasy, kde leží událost 7)
nebo {R:B} (rozsah políček větve, např. B1–B4). Tučně: **text**.
"""

# Pořadí hlavní trasy: id událostí a počet hnědých polí ZA nimi.
# 'X' = doplněné nebiografické hráčské pole (68 + 1 = 69).
TRUNK = [
    ("1", 1), ("2", 1),
    ("3", None),                                  # rozcestí -> větve L/E/V -> 7
    ("7", 3),
    ("22", 2),                                    # Nový Zéland se slepou cestou (pole 10)
    ("8", 0), ("9", 2),                           # zápisky a dívka – dvě zelená za sebou
    ("27", 2), ("28", 2),                         # přijímací pohovor do Nadace Partnerství
    ("29", 2),
    ("10", 1), ("23", 1), ("24", 1),              # syn + Madagaskar
    ("11", 2), ("12", 2),
    ("13", 2), ("14", 2), ("15", 2), ("16", 2), ("17", None),  # -> CZ/EU -> 20
    ("20", 2), ("21", 2),
    ("30", 2), ("31", 2), ("32", 2),
    ("33", 2), ("34", 2), ("35", 2), ("36", 2), ("37", 2), ("38", 2),
    ("39", 2), ("40", 2), ("41", 2), ("42", 2), ("43", 2), ("44", 2),
    ("45", 1), ("46", 2), ("47", 2), ("48", 2), ("49", 2), ("50", 2),
    ("51", 2), ("52", 2), ("53", 2),
    ("26", 2),                                    # Annapurna před třemi lety
    ("54", 2),
    ("25", 2),                                    # Kanada a Aljaška – sabatikl
    ("55", 5),
    ("LA", 2),                                    # Ladakh letos s oběma dětmi (pole 143)
    ("56", 0),                                    # Podnikání s přesahem (pole 146)
    ("57", 1),                                    # OwnerCompass (pole 147)
    ("58", None),                                 # -> P/O -> 60
    ("60", 0),
]

# Větve: kód, rozcestí, cíl (spojení nebo návrat), strana, seznam políček
# (None = hnědé pole, jinak id události)
BRANCHES = [
    dict(code="L", name="lesní cesta", fork="3", join="7", side="R",
         tiles=[None, None, "4L", None]),
    dict(code="E", name="cesta ESF", fork="3", join="7", side="S",
         tiles=[None, "5E", None, "6E", None]),
    dict(code="V", name="environmentalistika", fork="3", join="7", side="L",
         tiles=[None, "4V", None, "5V", None]),
    dict(code="CZ", name="české stromy", fork="17", join="20", side="L",
         tiles=[None, "18", None]),
    dict(code="EU", name="Evropa", fork="17", join="20", side="R",
         tiles=[None, "19", None]),
    dict(code="B", name="Brusel – slepá", fork="21", back="21", side="L",
         tiles=[None, None, None, "21B"]),
    dict(code="N", name="Nový Zéland – slepá", fork="22", back="22", side="L",
         tiles=[None, None, None, "22B"]),
    dict(code="F", name="další firma – slepá", fork="33", back="33", side="L",
         tiles=[None, None, None, "33B"]),
    dict(code="S", name="sociální podnik – slepá", fork="37", back="37", side="L",
         tiles=[None, None, None, "37B"]),
    dict(code="Z", name="zahraničí – slepá", fork="54", back="54", side="L",
         tiles=[None, None, None, "54B"]),
    dict(code="P", name="Podnikání s přesahem", fork="58", join="60", side="L",
         tiles=["59P"] + [None] * 8),
    dict(code="O", name="OwnerCompass", fork="58", join="60", side="R",
         tiles=["59O"] + [None] * 10),
]

FORKS = {"3", "17", "21", "22", "33", "37", "54", "58"}

# id -> (titulek, popisek úkolu, text úkolu)
EV = {
"1": ("Babička mě poprvé bere do Vysokých Tater.", "Úkol",
      "Udělám tři kroky do kopce."),
"2": ("Chci být lesníkem.", "Úkol", "Zatvářím se jako přísný lesník."),
"3": ("Rozcestí: les, ekonomie, nebo environmentalistika?", "Úkol a účinek",
      "Hoď kostkou: **1–2 lesník** – doprava; **3–4 ESF** – rovně; "
      "**5–6 environmentalistika** – doleva. Jdi na odpovídající cestu. "
      "Všechny tři se spojí na poli {N:7}."),
"4L": ("V lese znám každý strom. Skoro.", "Úkol a účinek",
       "Pojmenuju jeden strom. Kdo řekne jiný, **posune se o 1**. "
       "Pak pokračuju na pole {N:7}."),
"5E": ("Myslím si, že ekonomie odpoví na všechny otázky světa.", "Úkol a účinek",
       "Odpovím: „Vyřeší ekonomie všechno?“ "
       "ANO: **posunu se o 2** políčka dopředu. NE: **vrátím se o 1** políčko. "
       "Potom pokračuju po cestě ESF na E4 a dál na pole {N:7}."),
"6E": ("Kupuju si Samuelsonovu Ekonomii a nastupuju na ESF.", "Úkol a účinek",
       "Předstírám, že listuju obří učebnicí. **Posunu se o 2.** Pak na pole {N:7}."),
"4V": ("Na Silvestra potkávám dívku, která mi vypráví o environmentalistice.",
       "Úkol a účinek",
       "Řeknu nejlepší silvestrovskou radu. Pak na V4."),
"5V": ("Nastupuju na environmentalistiku. Ekonomie najednou neřeší úplně všechno.",
       "Úkol a účinek",
       "Udělám obličej člověka, kterému došel grant. Pak na pole {N:7}."),
"7": ("Studium environmentalistiky nestíhám.", "Úkol a účinek",
      "Tři sekundy panikařím. **Vrátím se o 2** (po cestě, kterou jsem přišel/a). "
      "Při dalším tahu pokračuju znovu dopředu."),
"8": ("Vyměňuju zápisky z přednášek za čokoládu.", "Úkol",
      "Řeknu, kterou čokoládu bych přijal/a."),
"9": ("Dívka si myslí, že ji balím. Vezme si mě.", "Úkol a účinek",
      "Ostatní hádají: „Byl to plán?“ ANO/NE. "
      "Správná odpověď: **posunu se o 2** a kdo uhodl, **posune se o 1**. "
      "Špatná odpověď: **posunu se o 2**, ostatní se neposouvají."),
"10": ("Narodí se nám syn.", "Úkol", "Zamávám jako hrdý rodič."),
"11": ("O tři roky později se nám narodí dcera.", "Úkol",
       "Řeknu jednu věc, která se vejde do přebalovací tašky."),
"12": ("Kupujeme dům.", "Úkol a účinek",
       "Předvedu zvuk vrtačky. **Zůstávám tu jedno kolo**: něco se musí opravit."),
"13": ("Dělám veřejnou sbírku pro stromy.", "Úkol a účinek",
       "Zvednu ruce jako strom. **Posunu se o 1.**"),
"14": ("Sázím strom.", "Úkol a účinek",
       "Zasadím imaginární sazenici. **Posunu se o 2.**"),
"15": ("Potkávám Antonína Bučka.", "Úkol", "Řeknu jméno jednoho stromu."),
"16": ("Zakládám celostátní Strom roku.", "Úkol a účinek",
       "Vyhlásím „strom roku“ v místnosti. **Posunu se o 2.**"),
"17": ("Rozcestí: zůstanu u českých stromů, nebo zamířím do Evropy?",
       "Úkol a účinek",
       "Hoď kostkou: **lichá – doleva**, zůstávám v české stromové větvi {R:CZ} "
       "(pole 18); **sudá – doprava**, evropská cesta {R:EU} (pole 19). "
       "Obě se spojí na poli {N:20}."),
"18": ("V Česku je pořád co sázet.", "Úkol a účinek",
       "Jmenuju jednu věc, kterou potřebuje strom. Pak se připojím na pole {N:20}."),
"19": ("Potkávám Laca Mika a zakládám Evropský strom roku.", "Úkol a účinek",
       "Řeknu „good luck“ jako moderátor. **Posunu se o 2.**"),
"20": ("Organizuju akce v Evropském parlamentu.", "Úkol a účinek",
       "Předvedu desetisekundový projev. Pak na pole {N:21}."),
"21": ("Přemýšlím, jestli nezůstanu pracovat v Bruselu.", "Úkol a účinek",
       "Odpovím: „Dal bych si eurový oběd?“ "
       "ANO: **doleva** na slepou cestu {R:B} (konec B4, návrat na pole {N:21}). "
       "NE: **doprava**, pokračuju na pole {N:30}."),
"21B": ("V Bruselu hledám kariéru i levný oběd.", "Úkol a účinek",
        "Zjistím, že obojí je složité. **Slepá cesta: vrať se na pole {N:21}.**"),
"22": ("Jedu na Nový Zéland. Přemýšlím, že tam zůstanu.", "Úkol a účinek",
       "Hoď kostkou: **lichá – doleva**, zkusím zůstat, slepá cesta {R:N} "
       "(návrat na pole {N:22}); **sudá – doprava**, vracím se domů, pokračuju na pole {N:8}."),
"22B": ("Na Novém Zélandu se mi líbí až podezřele moc.", "Úkol a účinek",
        "Řeknu, co bych si vzal/a na ostrov. **Slepá cesta: vrať se na pole {N:22}.**"),
"23": ("Na Madagaskaru zjišťuju, že expedice může být větší než můj batoh.",
       "Úkol a účinek", "Předvedu lemura. **Posunu se o 2.**"),
"24": ("Na expedici hledám dobrodružství, ne signál.", "Úkol a účinek",
       "Řeknu, co bych dělal/a bez internetu."),
"25": ("Vyrážím na další cesty: Andy, Pamír, Aljaška i další kouty světa.",
       "Úkol a účinek", "Ukážu na mapě směr, kterým bych vyrazil/a."),
"26": ("Beru Vítka na trek k Annapurně.", "Úkol a účinek",
       "Udělám tři kroky do kopce. **Posunu se o 1.**"),
"LA": ("Letos beru obě děti do Ladakhu a společně vystoupáme na šestitisícovku. Signál zůstal dole.",
       "Úkol a účinek",
       "Předvedu, jak se dýchá v 6 000 metrech. Hodím kostkou: padne-li **6**, "
       "**posunu se o 6 a házím znovu**. Při 1–5 zůstávám a pokračuju příštím tahem."),
"27": ("Jdu na pohovor do Nadace Partnerství. Rozumím asi dvěma třetinám otázek.",
       "Úkol", "Řeknu jednu odpověď s vážnou tváří."),
"28": ("Pohovor vyhrávám.", "Úkol a účinek",
       "Ostatní zatleskají. **Posunu se o 3.**"),
"29": ("V Nadaci Partnerství se potkávají les, ekonomie i environmentalistika.",
       "Úkol", "Řeknu, která moje cesta se tu nejvíc hodí."),
"30": ("Chci zlepšit města. Hádej jak?", "Úkol a účinek",
       "Ostatní hádají, každý jednou. Správná odpověď (trefa): **posunu se o 1**. "
       "Špatná odpověď: pokračuju bez posunu."),
"31": ("Chci rozjet car-pooling.", "Úkol a účinek",
       "Předvedu, jak zvu spolujezdce. Pak na pole {N:32}."),
"32": ("Car-pooling nevyjde.", "Úkol a účinek",
       "Vydám zvuk prázdného auta. **Vrátím se o 3.**"),
"33": ("Mohl jsem rozjet firmu. Nebo taky ne.", "Úkol a účinek",
       "Hoď kostkou: **lichá – doleva**, zkusím podnikat znovu, slepá cesta {R:F} "
       "(návrat na pole {N:33}); **sudá – doprava**, pokračuju na pole {N:34}."),
"33B": ("Zakládám firmu na sdílení všeho. Zatím sdílím hlavně starosti.",
        "Úkol a účinek", "**Slepá cesta: vrať se na pole {N:33}.**"),
"34": ("Investuju do James Cook Caravan Ltd. a stávám se menšinovým vlastníkem.",
       "Úkol a účinek", "Řeknu, kam bych jel/a karavanem. **Posunu se o 2.**"),
"35": ("Z karavanové firmy se nestává karavanový gigant. Prodávám svůj podíl.",
       "Úkol a účinek", "Zamávám odjíždějícímu karavanu. **Vrátím se o 2.**"),
"36": ("Jedu na IVLP do USA studovat sociální podnikání.", "Úkol",
       "Řeknu jednu věc, kterou bych si přivezl/a z USA."),
"37": ("Po IVLP přemýšlím, kam dál: sociální podnikání, nebo JIC?",
       "Úkol a účinek",
       "Hoď kostkou: **lichá – doleva**, zkusím sociální podnikání, slepá cesta "
       "{R:S} (návrat na pole {N:37}); **sudá – doprava**, nastupuju na cestu JIC, "
       "jdi na pole {N:38}."),
"37B": ("Zakládám sociální podnik. Zatím podnikám hlavně v přemýšlení.",
        "Úkol a účinek", "**Slepá cesta: vrať se na pole {N:37}.**"),
"38": ("V JIC se snažím zjistit, co všechno může podnikavost rozhýbat.",
       "Úkol a účinek",
       "Odpovím: „Mám nový nápad?“ ANO: **posunu se o 1**. "
       "NE: **vrátím se o 1**. Potom pokračuju k poli {N:39}."),
"39": ("V Yosemitech mě napadá oživit mezinárodní síť nadací.", "Úkol a účinek",
       "Udělám gesto „mám nápad!“. **Posunu se o 2.**"),
"40": ("Píšu projekt LIFE pro síť EPA.", "Úkol",
       "Řeknu název projektu, který zní důležitě."),
"41": ("Vyhrávám LIFE a stávám se ředitelem EPA v sedmi zemích.", "Úkol a účinek",
       "Pozdravím jako ředitel. **Posunu se o 3.**"),
"42": ("Po třech letech pro EPA další financování nezískáváme.", "Úkol a účinek",
       "Udělám zvuk prázdné pokladny. **Stojím jedno kolo.**"),
"43": ("Zkouším získat LIFE na adaptaci měst ve střední Evropě.", "Úkol",
       "Řeknu, co by město potřebovalo při vedru."),
"44": ("Díky lobby evropských šlechticů vyhráváme LIFE.", "Úkol a účinek",
       "Předvedu šlechtickou poklonu. **Posunu se o 2.**"),
"45": ("Eva Vacíková mi domlouvá mentora: Jiřího Tomíčka z Honeywellu.", "Úkol",
       "Řeknu jednu otázku pro mentora."),
"46": ("Jdu podpořit Petra Chládka v nové roli na JIC.", "Úkol",
       "Předvedu, jak vypadá podpůrný potlesk."),
"47": ("Vedu marketing JIC. K jádru dění se snažím dostat přes vedení.",
       "Úkol a účinek",
       "Odpovím: „Jsem u jádra?“ ANO: **posunu se o 2**. "
       "NE: **vrátím se o 1**. Potom pokračuju k poli {N:48}."),
"48": ("Covid: všichni čekáme, co bude dál.", "Úkol a účinek",
       "**Stojím dvě kola.** Můžeš během čekání dělat obličej na videohovoru."),
"49": ("Zakládáme Změnu k lepšímu.", "Úkol a účinek",
       "Řeknu jednu věc, kterou bych změnil/a k lepšímu. **Posunu se o 1.**"),
"50": ("Přesvědčují mě, abych vedl správní radu a organizaci posouval dál.",
       "Úkol a účinek",
       "Zatvářím se, že právě přebírám odpovědnost. **Posunu se o 2.**"),
"51": ("Stávám se členem správní rady Nadace Partnerství.", "Úkol",
       "Jmenuju jednu věc, kterou chrání strom."),
"52": ("Hlásím se do vedení JINAG. Neuspěju.", "Úkol a účinek",
       "Zatvářím se jako člověk po nepříjemném e-mailu. **Vrátím se o 2.**"),
"53": ("Odcházím z vedení marketingu JIC a přecházím do Scaleup týmu.",
       "Úkol a účinek",
       "Udělám krok stranou a pak dopředu. **Posunu se o 2.**"),
"54": ("Dávám si sabatikl a přemýšlím o životě v zahraničí.", "Úkol a účinek",
       "Hoď kostkou: **lichá – doleva**, zkusím zahraničí, slepá cesta {R:Z} "
       "(návrat na pole {N:54}); **sudá – doprava**, zůstávám na české cestě, "
       "pokračuju na pole {N:55}."),
"54B": ("Hledám nový život v zahraničí. Zapomněl jsem, jak se tam říká „kde je kafe?“",
        "Úkol a účinek", "**Slepá cesta: vrať se na pole {N:54}.**"),
"55": ("Nacházím si kouče a jdu studovat koučink.", "Úkol a účinek",
       "Ostatní se zeptají: „A co teď?“ Odpovím jednou větou. "
       "Potom pokračuju bez posunu."),
"56": ("Hlásím se do vedení Podnikání s přesahem.", "Úkol",
       "Řeknu jednu věc, která má přesah."),
"57": ("Zakládám OwnerCompass.", "Úkol",
       "Ukážu směr, kterým mě teď táhne kompas."),
"58": ("Rozcestí: Podnikání s přesahem, nebo OwnerCompass?", "Úkol a účinek",
       "Hoď kostkou: **lichá – doleva** na {R:P} (Podnikání s přesahem, P1); "
       "**sudá – doprava** na {R:O} (OwnerCompass, O1). Obě cesty vedou do cíle na pole {N:60}."),
"59P": ("Vydávám se cestou Podnikání s přesahem.", "Úkol",
        "Řeknu svůj první krok a vydám se po této závěrečné trase."),
"59O": ("Vydávám se cestou OwnerCompass.", "Úkol",
        "Řeknu svůj první krok a vydám se po této závěrečné trase."),
"60": ("Šťastný život?", "Úkol a účinek",
       "K cíli musíš hodit **přesný počet**. Když přehodíš, čekáš na další tah. "
       "**Která cesta sem skutečně vede, se ukáže až časem.**"),
}
