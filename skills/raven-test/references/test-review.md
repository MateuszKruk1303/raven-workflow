# Wspólne źródła i niezależne review testów

Obowiązuje autorów testów oraz reviewerów w raven-test, raven-test-review i raven-auto-test. Przed pisaniem testów utrwal w checkpointcie GH `test_sources`: URL i wersję/fingerprint wymagań oraz zaakceptowanego planu z taskami, URL/wersję strategii (lub jawny brak), źródłowe decyzje użytkownika i raporty review/odbioru, bazowy SHA produktu oraz wersje instrukcji repo, lessons, test-stack, konfiguracji i wzorców testowych. Dla treści edytowalnych zachowaj snapshot z hashem; sam link do zmiennego issue nie zamraża źródła. Wykorzystuj istniejące snapshoty zamiast je dublować. Nie publikuj sekretów ani prywatnych ścieżek.

Reviewer otrzymuje ten sam zestaw źródeł i ich wersje, pełny diff etapu oraz finalny SHA. Czyta wymagania rodzica i tasków bezpośrednio, nie wyłącznie mapę pokrycia autora. Podsumowania i raporty wykonania są twierdzeniami do weryfikacji. Nie otrzymuje transkryptu autora, jego prywatnych rozważań ani sugerowanego werdyktu. Brak źródła nazwij; istotna luka lub nieodtwarzalna wersja blokuje ocenę zgodności zamiast zachęcać do zgadywania.

Przed oceną porównaj źródła z aktualnym GH. Późniejsze decyzje lub zmiany wymagań pokaż jako różnicę; ustal aktualny zakres i uzupełnij testy na jego podstawie, nie oceniaj po cichu według innych wymagań niż te przekazane autorowi. Nie używaj nieaktualnego snapshotu, aby zignorować nowe zlecenie użytkownika. Zmiany samych dowodów i postępu nie zmieniają wymagań.

## Pragmatyczna ocena

Reviewer sprawdza, czy testy chronią uzgodnione zachowania i istotne ryzyka: niezależne źródło oczekiwań, asercje skutków, reprezentatywne błędy i granice, właściwą warstwę, granice mocków, izolację/cleanup i powtarzalność. Czyta też helpery, konfigurację i zmiany produktu w diffie. Istniejące dobre testy liczą się jako ochrona; nie żądaj ich kopii.

Nie wymagaj wszystkich warstw dla każdego kryterium, arbitralnego coverage, dodatkowych frameworków ani czysto stylistycznych poprawek. Każda uwaga musi wskazywać wymaganie/ryzyko, konkretny dowód, praktyczny skutek i najmniejszą skuteczną poprawkę. Ulepszenia poza zakresem oznacz jako opcjonalne, bez blokowania PASS. Nie wymuszaj liczby uwag. Odmienna preferencja autora nie jest defektem.

Weryfikuj dowody i uruchamiaj kontrole, które rozstrzygają konkretne wątpliwości. Nie powtarzaj całego kosztownego zestawu bez powodu. Kontrolowane zepsucie wykonuj wyłącznie w izolowanej kopii, przywracanej po próbie; reviewer nie nanosi trwałych poprawek. Nie traktuj samego zielonego uruchomienia, liczby testów lub deklaracji autora jako dowodu ochrony regresji. Wewnętrzny REVIEW raven-test nie zastępuje niezależnego agenta.

## Agent i raport

Przy nowym review uruchom świeżego agenta bez historii (`fork_turns="none"` lub odpowiednik). Nie może być autorem testów ani implementatorem produktu. Osobne wywołanie skilla w tej samej sesji samo w sobie nie zapewnia niezależności. Główny agent przekazuje surowe źródła i publikuje wynik w GH; reviewer nie zmienia kodu, wymagań ani statusów. Gdy świeży kontekst jest niedostępny, zgłoś blokadę, nie udawaj niezależności.

Raport `raven:test-review` zawiera identyfikację test_sources, base/head SHA, oceniony zakres, dowody faktycznie wykonanych kontroli, stabilne T1/T2, ważność uwag, praktyczny skutek, minimalną poprawkę i PASS/REVISE/BLOCKED. Odróżnij wadę testu, błąd produktu, lukę wymagań i opcjonalną sugestię. Werdykt dotyczy ustalonej wersji, nie całego projektu. Zachowaj historię raportów i decyzji.
