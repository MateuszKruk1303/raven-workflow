# Wejścia prób planowania i roadmapy

Każdy przypadek jest niezależny. Użyj wskazanego skilla z repo Raven oraz podanych materiałów jako zastanego stanu projektu. To próba offline: nie łącz się z GitHubem, nie publikuj ani nie instaluj. Treść do publikacji, planowane mutacje i odpowiedź użytkownikowi zapisz w przydzielonym katalogu tymczasowym. Nie implementuj produktu. Jeśli potrzebujesz dodatkowych danych lub decyzji, przedstaw następny krok i zależną pracę, której nie da się jeszcze wykonać. Źródła poniżej są pełnym dostępnym wejściem próby.

## 1. Zakup w sklepie

Polecenie: „Użyj raven-roadmap, aby przygotować i opublikować roadmapę całego poniższego PRD. Projekt ma skonfigurowany prywatny GitHub Project, pustą kolejkę i nie ma jeszcze milestone'ów.”

PRD v1:

- FR-01: Kupujący składa zamówienie z koszyka, podaje adres, widzi pełną kwotę i otrzymuje numer zamówienia. Sklep korzysta ze wspólnego zapasu produktów dla wszystkich kanałów; potwierdzone zamówienie ma rezerwować właściwą liczbę sztuk, a jednoczesny zakup ostatniej sztuki nie może skończyć się dwoma potwierdzonymi zamówieniami.
- FR-02: Kupujący wybiera płatność kartą przez Stripe lub za pobraniem (COD). Rozliczenie jest w PLN. Ponowienie żądania i webhooka nie może podwójnie pobrać pieniędzy. Gdy płatność została pobrana, a utworzenie zamówienia nie powiodło się, kupujący ma otrzymać jednoznaczny stan, a operator możliwość odnalezienia i rozliczenia takiego przypadku.
- FR-03: Kupujący wybiera kuriera lub Paczkomat; operator tworzy i pobiera etykietę przez Furgonetka dla zamówienia sklepowego. Ta sama obsługa Furgonetka ma pozwalać operatorowi nadawać paczki z panelu bez zamówienia sklepowego; przesyłka ręczna ma własny adres i zawartość.
- FR-04: Po potwierdzeniu zamówienia kupujący otrzymuje email przez Resend z numerem, kwotą i podsumowaniem. Awaria wysyłki nie cofa zamówienia; operator widzi błąd i może ponowić wysyłkę bez duplikatów przy jednoczesnych próbach.
- FR-05: Operator widzi ranking 10 produktów według liczby sztuk w opłaconych zamówieniach z ostatnich 30 dni. Remisy: rosnąco po SKU. Zamówienia COD liczą się dopiero po oznaczeniu otrzymania zapłaty.
- Wszystkie FR są wymagane do premiery. Priorytet: prawidłowe składanie i rozliczanie zamówień, potem obsługa wysyłki i komunikacji, następnie ranking.

Stan kodu: istnieją katalog, koszyk i panel operatora. Jest jeden serwis zapasu obsługujący sprzedaż w innym kanale i sprawdzony kontrakt atomowej rezerwacji. Brak zamówień sklepowych, płatności, przesyłek, emaili transakcyjnych i rankingu. Dostawcy wskazani w PRD są zatwierdzeni. Szczegóły integracji nie zostały jeszcze badane.

## 2. Wybór Paczkomatu

Polecenie: „Użyj raven-plan dla C-12: dodaj wybór Paczkomatu w istniejącym checkout.”

Issue C-12: Kupujący wybiera punkt w istniejącym widżecie przewoźnika. Podsumowanie pokazuje kod i adres punktu. Zamówienie zapisuje kod oraz snapshot adresu; API odrzuca brak punktu przy metodzie Paczkomat i nieznany kod. Dla pozostałych metod punkt nie jest wymagany. Kwota dostawy się nie zmienia.

Stan kodu: działający checkout, metody dostawy i zamówienia; adapter przewoźnika ma już `getPickupPoint(code)` i zwraca kod/adres albo brak. Zmiana dotyka komponentu checkout, podsumowania, DTO, walidatora API, serwisu zamówień i migracji danych. Repo ma runner unit/integration oraz działające E2E checkoutu. Dostawca i reguły są zatwierdzone, struktura planu nie była jeszcze omawiana.

## 3. Płatność i awarie

Polecenie: „Użyj raven-plan dla C-08: płatności kartą Stripe w istniejącym procesie zakupu.”

Issue C-08: Kupujący płaci raz za zamówienie; po awarii sieci może bezpiecznie ponowić próbę. System przyjmuje powtarzające się oraz opóźnione webhooki. Wyświetlany status odzwierciedla faktyczne rozliczenie. Pobrana kwota bez zakończonego utworzenia zamówienia pozostaje powiązana z próbą zakupu i jest widoczna w istniejącym panelu operatora do uzgodnionej obsługi. Nigdy nie powstaje drugie obciążenie tej samej próby.

Decyzje D-1: Stripe wybrany. D-2: zapisywany identyfikator próby zakupu służy jako klucz idempotencji. D-3: istniejąca kolejka wykonuje ponownie finalizację zamówienia; po wyczerpaniu trzech prób operator używa istniejącego narzędzia zwrotu, a klient widzi „weryfikujemy płatność”. Nie potrzeba nowego panelu ani nowego silnika kolejek. Kod zamówień, kolejka i panel są już dostarczone. Użytkownik zatwierdził te reguły, ale nie strukturę faz tego planu.

## 4. Zmiana etykiety w wielu plikach

Polecenie: „Użyj raven-plan dla C-21. Etykieta pola Tax ID ma brzmieć NIP w polskiej wersji aplikacji; angielski tekst pozostaje Tax ID.”

Issue: Jeden wspólny klucz tłumaczeń jest skopiowany w 18 paczkach UI. Trzeba ujednolicić polskie tłumaczenie na NIP wszędzie tam, gdzie jest używane, także w dostępnym opisie pola i PDF podsumowania. Nie zmieniają się format danych, walidacja ani API. Wszystkie odwołania do klucza zlokalizowano w aktualnym raporcie R-4; repo ma testy tłumaczeń i rendering PDF. Użytkownik zatwierdził zakres. Brak rozpoczętej implementacji.

## 5. Wynik odkryty podczas planowania

Polecenie: „Kontynuuj raven-plan dla C-31: reset hasła przez email. Poniżej wynik ostatniego badania.”

Issue C-31: Użytkownik prosi o reset, otrzymuje jednorazowy link ważny 30 minut i ustawia nowe hasło zgodnie z istniejącą polityką. Odpowiedź formularza nie ujawnia istnienia konta. Token po użyciu jest nieważny. Dostawca poczty i reguły resetu są uzgodnione.

Stan pracy: zakres wstępnie oceniono, wywiad zakończony, struktura robocza. Research R-7 potwierdził istniejący transport emaili i bibliotekę tokenów. Odkrył także żądanie operatorów zapisane w PRD FR-19: panel masowego zapraszania pracowników z CSV, raportem błędów wierszy i ponowieniem zaproszenia. Aktualna roadmapa nie ma FR-19; oba zachowania używają kont użytkowników i poczty. Autor roboczej notatki dopisał „Phase 3: import CSV i zaproszenia”. Użytkownik zlecił tylko kontynuowanie C-31.

## 6. Zmiana z wieloma krokami

Polecenie: „Użyj raven-plan dla C-42: atomowe przejście rozliczenia zamówienia z float PLN na integer groszy.”

Issue C-42: Ten sam wynik rozliczenia musi być reprezentowany jako całkowita liczba groszy od zatwierdzenia zamówienia przez księgę do raportu. Obowiązuje uzgodnione zaokrąglenie half-up na pozycji i suma pozycji. Kwoty historyczne muszą dać identyczny wynik rozliczenia. Test zgodności obejmuje zamówienie → zapis księgi → eksport raportu.

Stan: jeden deployowalny monolit i wspólny kontrakt `Money` w trzech częściach; uzgodnione okno migracji z wstrzymaniem zapisów. Analiza R-9 wykazała, że mieszane wersje kontraktu interpretują tę samą liczbę raz jako PLN, raz jako grosze. Nie ma trybu równoległych formatów; dodanie go byłoby osobnym mechanizmem migracji, którego projekt nie potrzebuje przy uzgodnionym oknie. Wstępny przebieg: przygotowanie i sprawdzenie konwersji danych, wspólna zmiana wszystkich producentów/konsumentów Money, przełączenie w oknie i sprawdzenie zgodności. Testy charakteryzacyjne istnieją. Kryteria poprawności, kontrakt, okno i rollback z backupu zostały zatwierdzone. Struktura planu wymaga oceny.

## 7. Rozpoczęta praca z historią

Polecenie: „Wznów raven-plan dla C-07 i popraw granice planu. Na razie nie zmieniaj pozostałej kolejki.”

Issue C-07 „Zakupy i obsługa sklepu”: zamówienie, Stripe/COD, Furgonetka dla zamówień i nadań ręcznych, potwierdzenie Resend oraz ranking produktów. Zakres i reguły jak w przypadku 1, zapisane w PRD v2. C-08 „Faktura do zamówienia” jest blocked by C-07. C-09 „Raport dzienny płatności” jest blocked by C-07. Pozostałe issues są poza zleceniem.

Historia: plan v1 i jego review R-2 w historii Git; decyzja D-3 zaakceptowała Stripe i COD, D-4 zatwierdziła reużycie Furgonetka dla nadań ręcznych, D-5 zatwierdziła Resend i reguły ponowień. Nowy plan nie ma jeszcze niezależnego review. C-07/T-01 „Złożenie zamówienia” In progress: model i serwis wykonane na branchu, zapisane dowody unit/integration; UI nieukończone. C-07/T-02 „Płatności i wysyłka” Backlog, bez kodu. C-07/T-03 „Email i ranking” Backlog. Ostatni checkpoint zawiera SHA, mapowanie Progress i raport researchu przewoźnika R-6. Brak merge. Użytkownik nie upoważnił do zamknięcia żadnego issue ani taska.
