# Final_Project_SDA
Auction web
# Final_Project_SDA
Auction web

superuser: admin/admin

ZÁKLADNÍ SEZNAM ÚKOLŮ: 

1. MOCKUP (NÁSTŘEL)
- Hlavní funkce:
  - Hlavní stránka [x]
  - Aukce [x]
  - Aukce a nákupy [ ]
  - Uživatelský účet [ ]
  - Kategorie [x]
  - Vyhledávání aukcí [x]
  - Sledování aukcí [ ]
  - Hodnocení transakcí [ ]
- Důležité zprovoznit hlavní stránku a aukce s nákupy + uživatelský účet (základ). Poté se začít věnovat vyhledávání aukcí, sledování aukcí a hodnocení transakcí.

2. ZÁKLAD
- Základ by měla být správná funkčnost aplikace. V našem případě by tedy mělo jít se registrovat/přihlásit, vytvořit aukci, zúčastnit se aukce.

3. PLNÁ VERZE
- Funkční základ, dále fungující vyhledávání aukcí, sledování aukcí, kategorie a hodnocení transakcí

Základní entity (návrh)

Kategorie:
- název [x]
- popis názvu [Nevím co přesně znamená.]
- logo / náhled (volitelné) [Nechci.]

Uživatelský účet
- přihlašovací údaje (email užívaný pro komunikaci a notifikace) [x] 
- heslo [x]
- uživatelské jméno (viditelné na profilovém účtu) [x]
- město [x]
- adresa (ulice, číslo domu, PSČ) [x]
- datum vytvoření účtu [x]
- status účtu (AKTIVNÍ / NEAKTIVNÍ / BLOKOVANÝ) [x]
- logotyp / náhled / avatar [Nechci.]
- typ (BĚŽNÝ/PREMIUM) [Nechci.]

Detaily aukce 
- název
-  popis
  fotky (volitelné)
  kategorie
  minimální příhoz
  částka Kup teď (údaj zmizí v případě, že začne aukce)
  propagace (lze předpokládat, že s prémiovým účtem je možné propagovat např. 10 aukcí měsíčně)
  lokalita (souhlasí s lokalitou uživatelského účtu)
  datum začátku aukce
  datum ukončení aukce
  počet zobrazení (zobrazení stránky)
