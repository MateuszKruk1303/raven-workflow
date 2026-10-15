# Realizacja i wznowienie

## Role i zakres pracy

Agent główny jest koordynatorem i jedynym autorem state, planu chunka, roadmapy oraz handoff. Implementator robi całość A–Z: wykorzystuje istniejący plan, pisze kod, integruje zadania i uruchamia niezbędne proste kontrole. Niezależny reviewer sprawdza wymaganie na działającym rezultacie. Nie rozbijaj każdego zadania na osobne delegacje, plany i rundy review. Zachowaj ID zadań i ich zależności; grupuj realizację w jednym wątku implementatora, odbiór w jednym wątku reviewera.

Przy delegacji użyj modeli z kontraktu, fork none i krótkiego pakietu: wymaganie, istotne decyzje, ścieżki planu/kodu, dozwolone zapisy, oczekiwany rezultat. Nie kopiuj całego PRD, rozmowy ani raportów. Nie zlecaj pracownikom czytania instrukcji koordynatora. Dodatkowy planista i automatyczna diagnoza kolejnym modelem nie są częścią tego trybu.

## Wybór i wznowienie

Jawne ID ma pierwszeństwo. Bez ID kontynuuj jednoznaczny aktywny chunk z rozmowy/stanu, a przy jego braku pierwszy ready ze spełnionymi zależnościami. Draft kieruj do prepare; awaiting_review do review; accepted/testing/ready_to_archive do właściwego etapu. Nie zmieniaj archiwów i nie cofaj stanu bez zlecenia zmian.

Odczytaj state, next_step, blockers i pending journal. Sprawdź właściciela zapisu oraz lokalne zmiany. Czytaj tylko aktualne raporty i sekcje planu potrzebne dalej. Nie odtwarzaj ukończonych zadań, researchu ani baseline. Przy blokadzie wykonaj jedno celowane sprawdzenie, czy ustała; jeśli nie, zapisz potrzebne działanie i zakończ. Kontynuacja nie wymaga ponownego prepare. Zachowaj liczniki poprawek i wyniki, również między sesjami.

## Implementator → reviewer → użytkownik

1. Implementator wykonuje wymaganie A–Z. Zapisuje jeden krótki wynik implementacji dla całego chunka lub pakietu: pliki, proste kontrole, adres i dane do sprawdzenia, znane braki. Nie tworzy planu technicznego ani raportu dla każdego pliku, jeżeli istniejący plan wystarcza.
2. Reviewer sprawdza główne wymaganie na jednym reprezentatywnym przepływie, od wejścia do oczekiwanego wyniku. W UI używa przeglądarki zgodnie z właściwym skillem; w backendzie wystarczy celowane wywołanie API lub istniejący test. Do sprawdzenia wybiera minimalne dane dev/sandbox. Kod czyta celowo, gdy wynik jest niejasny lub dotyczy uprawnień, pieniędzy albo trwałości danych; nie przeprowadza szerokiego audytu.
3. Działa → `PASS` i natychmiastowe przekazanie użytkownikowi. Nie dodawaj sprawdzeń „dla pewności”, nie szukaj kolejnych zadań po PASS. Koordynator nie powtarza przebiegu reviewera.
4. Nie działa → `CHANGES_REQUIRED` z konkretnym objawem, odtworzeniem i oczekiwanym wynikiem. Implementator naprawia wskazane błędy. Reviewer ponawia tylko niesprawny fragment oraz bezpośrednio dotkniętą część głównego przepływu. Nie otwiera przy okazji nowej listy opcjonalnych ulepszeń.

## Mały zakres weryfikacji

Domyślnie do trzech prostych poleceń kontroli na cały chunk (np. typecheck, potrzebny build, istniejący celowany test) oraz jeden reprezentatywny przepływ reviewera. Wybierz tylko potrzebne polecenia; trzy nie są celem do wypełnienia. Po poprawce ponów wyłącznie dotkniętą kontrolę. Jawne obowiązkowe bramki repozytorium wykonaj, ale nie dodawaj do nich własnego pełnego zestawu.

Nie twórz ani nie edytuj testów automatycznych, konfiguracji runnera, fixtures i infrastruktury testowej w implement. Nie uruchamiaj szerokiej regresji, pełnej macierzy ról/metod/operatorów, testów awarii, powtórnych sesji wizualnych ani zebrania dowodów dla wszystkich AC. Pozostałe warianty, wygląd i przypadki brzegowe sprawdza użytkownik; automatyzacja należy do osobnego raven-pilot-test. Istniejące scenariusze można wykorzystać, jeśli są najtańszym sposobem sprawdzenia głównego wymagania. Nie naprawiaj historycznego zestawu testów w ramach tej fazy.

Nie powtarzaj kosztownej operacji zewnętrznej tylko dla nowego raportu. Sprawdź utrwalony stan przed ewentualnym ponowieniem płatności/nadania/wysyłki. Zachowaj uprawnienia, izolację sklepów, ochronę danych i istniejące granice autoryzacji. Zaobserwowany wyciek, nieprawidłowe obciążenie lub utrata danych wymagają poprawki; hipotetyczne ryzyko bez konkretnego objawu nie uzasadnia rozbudowy testowania.

## Warunek zakończenia i nieudane poprawki

Domyślnie najwyżej dwie rundy poprawek po pierwszym sprawdzeniu całego chunka. To zabezpieczenie przed pętlą, nie wymagane dwie rundy. Nie resetuj licznika nowym zadaniem, agentem, sesją ani nową nazwą tego samego błędu. Nie eskaluj automatycznie do dodatkowej diagnozy/modelu.

Jeżeli główne wymaganie działa, pozostałe niekrytyczne niedoskonałości zapisz i przekaż do odbioru. Nie wymagaj ich usunięcia przed `awaiting_review`. Brak sprawdzenia wariantu nie oznacza błędu; nie oznaczaj go jednak jako PASS.

Jeżeli po dwóch rundach nadal nie działa główny przepływ lub pozostaje znany krytyczny błąd, zatrzymaj pętlę, zapisz `blocked`, `resume_status=implementing`, konkretny problem i potrzebną decyzję użytkownika o dalszej diagnozie lub zakresie. Ten limit jest jawną regułą kosztową workflow, nie dowodem braku dostępu. Nie oznaczaj takiego wyniku jako gotowego ani nie zmniejszaj samodzielnie zakresu. Przy wcześniejszym rzeczywistym blockerze wymagającym dostępu/decyzji zatrzymaj od razu. Kontynuacja diagnozy po limicie wymaga jawnego zlecenia użytkownika, które zapisz wraz z nową granicą pracy.

## Artefakty i checkpointy

Jeden krótki implementation.md i numerowany, niezmieniany review-NN.md mogą obejmować cały chunk i wskazywać wszystkie właściwe T-ID. Osobne verification.md, coverage.json, screenshoty, trace i raporty sesji nie są wymagane; użyj ich tylko gdy już istnieją i pomagają wznowić pracę. Nie produkuj ich wyłącznie dla kompletności dokumentacji.

W state rozróżniaj zaimplementowane, sprawdzone i pozostawione użytkownikowi. Zadanie implementacyjne może być done przy AC wymagającym odbioru użytkownika; niesprawdzonego AC nie zmieniaj na zweryfikowane. Handoff zapisuje zakres kontroli, wynik krytycznego przepływu, braki i następny krok. Zachowaj manifest istotnych plików na końcowym checkpointcie, bez nowych manifestów po każdym sprawdzeniu. Bramka awaiting_review oznacza zaimplementowany zakres i sprawdzony główny przepływ, nie dowiedzenie wszystkich AC.

Checkpointy łącz: start/wznowienie, istotna decyzja lub blocker, końcowe przekazanie. Wynik review i poprawki utrwal w raporcie oraz przy najbliższym checkpointcie, bez osobnej rewizji roadmapy dla każdego komunikatu. Stosuj protokół synchronizacji, blokadę roadmapy i atomowy zapis state. Nie odpytywaj pracowników cyklicznie o status; korzystaj z powiadomień. Nie uruchamiaj test stage, commita, pusha ani deploya bez zlecenia.
