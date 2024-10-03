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
  - Aukce a nákupy [x]
  - Uživatelský účet [x]
  - Kategorie [x]
  - Vyhledávání aukcí [x]
  - Sledování aukcí [x]
  - Hodnocení transakcí [x]
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
- název [x]
- popis [x]
- fotky (volitelné) [x]
- kategorie [x]
- minimální příhoz [x]
- částka Kup teď (údaj zmizí v případě, že začne aukce) [x]
- propagace (lze předpokládat, že s prémiovým účtem je možné propagovat např. 10 aukcí měsíčně) [Nechci.]
- lokalita (souhlasí s lokalitou uživatelského účtu) [x]
- datum začátku aukce [x]
- datum ukončení aukce [x]
- počet zobrazení (zobrazení stránky) [x]

Přihazování
- aukce [x]
- uživatel [x]
- částka k zaplacení [x]

Nákup (nejvyšší příhoz nebo Kup teď)
- aukce [x]
- uživatel [x]
- částka k zaplacení [x]

Sledování aukce
- aukce [x]
- uživatel [x]

Hodnocení transakce (nákupu)
- nákup [x]
- hodnocení prodejce [x]
- komentář prodejce [x]
- hodnocení kupujícího [x]
- komentář kupujícího [x]