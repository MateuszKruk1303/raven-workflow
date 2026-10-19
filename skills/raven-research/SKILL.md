---
name: raven-research
description: Zbadaj pytanie o kod lub wykonalność change i zapisz lokalny research.md z dowodami. Bez tworzenia task issues.
---

# Raven Research

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md). Odtwórz lokalny change i źródła; nowy raport może utworzyć folder bez issue/Project. Nie przygotowuj planu ani implementacji podczas samego researchu.

## 1. Ustal dowody i zakres

- Jeśli użytkownik wspomina konkretne pliki (tickety, dokumenty, JSON), przeczytaj je najpierw W CAŁOŚCI (bez limitu/offsetu)
- **KRYTYCZNE**: Przeczytaj te pliki samodzielnie w głównym kontekście przed uruchomieniem jakichkolwiek podzadań

Przeczytaj PRD, istotną dokumentację, `context/foundation/architecture.md` i `context/foundation/lessons.md`, jeśli istnieją, i traktuj wpisy lessons jako uprzednio znane wzorce podczas kształtowania obszarów badawczych — powtarzające się reguły już zaakceptowane przez zespół zawężają to, co warto ponownie badać.

Prowadź zwięzłą listę pytań wymagających odpowiedzi, istniejących dowodów, nierozwiązanych sprzeczności i kolejnych kontroli. Skoncentrowane pytanie może wymagać jednego lokalnego wyszukania; kompleksowy zakres domyślnie wymaga pokrycia każdego uzgodnionego obszaru, delegowanego równolegle (krok 2).

Doprecyzuj tylko niejednoznaczność, która istotnie zmieniłaby badanie. Gdy jest dostępna, użyj rzeczywistej możliwości zadawania pytań strukturyzowanych przez hosta, przestrzegając jej schematu, wielkości rundy i niestandardowych danych wejściowych. Używaj krótkich nagłówków (maksymalnie 12 znaków) oraz konkretnych opcji z opisami. W hoście bez tej możliwości zadaj użytkownikowi zwięzłe pytanie tekstowe w celu wymaganego doprecyzowania zakresu; nie symuluj wywołania narzędzia. Jednoznaczne żądanie badawcze nie wymaga wywiadu ani zmiany trybu. Preferencje użytkownika są decyzjami; zweryfikuj skorygowane twierdzenia faktyczne względem wskazanego źródła.

## 2. Wybierz i przeprowadź badanie

Pracuj lokalnie dla pojedynczego zlokalizowanego faktu lub rozumowania sekwencyjnego. Kompleksowe badanie lub badanie wielu obszarów jest domyślnie delegowane, a nie traktowane jako wyjątek. Przed pierwszym delegowaniem przeczytaj [references/task-orchestration.md](references/task-orchestration.md) i użyj opisanych tam ograniczonych przydziałów, kontroli dostępnych modeli/możliwości, procedury awaryjnej na wypadek niepowodzenia oraz wymagań dotyczących dowodów. Uruchom równolegle w jednej wiadomości pracowników tylko dla niezależnych luk, które można wykorzystać od razu (zwykle 1–2, najwyżej 4), każdego dla innego wymiaru badania i każdego z prośbą o kotwice `file:line` — na przykład jednego znajdującego każdy plik związany z X, jednego szukającego wskazanych wcześniejszych decyzji dotyczących Y w dokumentach i Git, jednego analizującego działanie podsystemu Z. Deleguj mniej tylko wtedy, gdy zakres rzeczywiście dotyczy jednego obszaru albo gdy luka zależy od warunku wstępnego, który nadal jest nierozstrzygnięty. Używaj natywnej możliwości sub-agentów lub zadań swojego AI coding assistant do lokalizowania kodu i analizy, wybierając odpowiedni dostępny typ agenta. Używaj śledzenia zadań, gdy pomaga ono koordynować kilka obszarów i host je udostępnia; w przeciwnym razie wystarczy lista robocza.

Główny agent odpowiada za pytanie i syntezę. Agenci podrzędni badają tylko do odczytu i zwracają kotwice, niepewność oraz rzeczywisty zakres pokrycia. Nie proś każdego pracownika o przeczytanie całego repozytorium ani tych samych dużych dokumentów. Kontynuuj niezależną pracę podczas ich działania; sprawdzaj istotne dowody w miarę napływania wyników. Przed syntezą poczekaj na pracowników, których wynik jest potrzebny do uzgodnionych pytań; nieukończony wymagany wynik jest jawną luką, a nie odpowiedzią. Zadania, które przestały być potrzebne, anuluj zamiast na nie czekać.

Przy kontynuacji lub korekcie zakresu zaktualizuj pytania i pracowników, których to dotyczy, zachowując niepowiązane ustalenia. Późna odpowiedź oparta na zastąpionym zakresie nie może nadpisać nowej decyzji. Zajmij się konkretną luką zamiast ponownie rozpoczynać szerokie odkrywanie.

## 3. Dokonaj syntezy i zamknij odkrywanie

Połącz dowody w odpowiedź na pierwotne pytanie. Rozróżniaj zaobserwowane zachowanie, wnioskowanie i nierozstrzygnięte fakty. Sprawdź decydujące/sprzeczne ścieżki kodu i wywołujących; sam brak wyników wyszukiwania nie dowodzi nieobecności. Przy negatywnym ustaleniu cytuj sprawdzony zakres. Poszerzaj zakres tylko wtedy, gdy może to rozstrzygnąć uzgodnione pytanie lub istotną sprzeczność, a nie po to, aby wypełnić opcjonalną sekcję dokumentu.

Gdy żądane są rekomendacje, zachowaj ustalone wymagania i odrzuć opcje osłabiające wymagane gwarancje. Rozróżniaj rozstrzygnięte decyzje, rzeczywiste wybory i brakujące dowody.

Zakończ, gdy uzgodnione pytania mają wystarczające dowody, a istotne konflikty są rozwiązane. Zamknij lub anuluj przestarzałe zadania. Nadal brakujące wymagane dowody oznaczają częściowe ustalenie z podaną luką i jej wpływem; nie deklaruj ukończenia ani nie uruchamiaj bez końca równoważnych wyszukiwań. Nie uruchamiaj buildów ani testów, chyba że ich wyniki odpowiadają na konkretne pytanie badawcze i host na to pozwala.

## 4. Zapisz i zweryfikuj artefakt badawczy

Zapisz raport w `context/changes/<id>/research.md`, według [formatu raportu](references/research-document.md). Historia Git przechowuje wcześniejsze wersje; kontynuacja aktualizuje ustalenia i wskazuje nowe dowody, nie publikuje snapshotów do komentarzy. Nie zmieniaj planu wykonawczego ani nie rozpoczynaj implementacji.

Przed zapisem raportu zastosuj kontrole ograniczonych twierdzeń oraz prozy/JSON z tego odwołania. Każde ilościowe lub uniwersalne twierdzenie w prozie wymaga jawnego warunku, kwantyfikatora (dokładnego zbioru, liczby lub „this inspected path”) oraz kotwicy źródłowej. Nie pisz „always”, „never”, „every”, „only” ani „on the first attempt”, chyba że nazwany warunek i sprawdzona ścieżka faktycznie mają taki zakres. Rozstrzygaj każde twierdzenie historyczne osobno: dokument nieaktualny pod względem liczebności może nadal być poprawny w innym polu; pozytywna lista nie jest zbiorem wyłącznym, chyba że źródło tak mówi.

Gdy zażądano ustrukturyzowanych faktów (JSON lub tabeli), przed publikacją którejkolwiek reprezentacji wykonaj osobne przejście proza-kontra-JSON: dla każdego liścia zapisz zdanie prozą, które ta wartość oznaczałaby, gdyby była prawdziwa, potwierdź, że to samo zdanie znajduje się w raporcie, i potwierdź, że wartość JSON odpowiada temu samemu źródłu. Zgodność JSON nie certyfikuje otaczającej prozy. Jeśli JSON został zamówiony, przygotuj tymczasowe pliki raportu i faktów poza repo tylko do kontroli; docelowo zachowaj zamówione wyniki w lokalnym raporcie. Uruchom dołączony kontroler Node jeden raz:

```sh
node <loaded-skill-dir>/scripts/prose-json-check.mjs <research.md> <facts.json>
```

Sprawdza on wyłącznie, czy każda liczba i wartość logiczna JSON występuje w prozie; nie dowodzi poprawności kwantyfikatorów. Brakujące liście lub dodatkowe uniwersalne sformułowania nadal wymagają ręcznej korekty. Jeśli Node jest niedostępny, wykonaj tę samą listę kontrolną ręcznie.

Zbierz metadane z rzeczywistego repozytorium i aktualnego zegara jeden raz; nie twórz fikcyjnej gałęzi, commitu, znacznika czasu ani tożsamości badacza. Metadane raportu opisują badane repo, rzeczywisty HEAD/branch, dirty state, czas i autora. Brak danych oznacz jako nieznane.

Przejrzyj końcowy artefakt raz, aby sprawdzić jego odpowiedź, cytowania, luki i metadane: odczytaj zapisane treści ponownie albo przejrzyj kompletny szkic podczas prezentowania go niezapisanego w rozmowie. W tym samym przejściu ponownie wykonaj listę kontrolną ograniczonych twierdzeń i prozy/JSON (nie pomijaj jej, ponieważ pierwszy szkic już istniał):

- Powiąż przykład liczbowy z jego nazwanymi danymi wejściowymi, jednostkami i warunkami przed wyprowadzeniem jego wyniku; rozróżniaj sumy od dodatkowych operacji. Nie wyciągaj znaczenia wartości wyłącznie z nazwy pola lub znanej liczby.
- Dla każdej istotnej wartości logicznej sformułuj twierdzenie, które oznaczałaby, gdyby była prawdziwa, a następnie sprawdź, czy sprawdzone źródło wspiera to twierdzenie przed przypisaniem wartości. Pole opisujące, czy twierdzenie historyczne jest poparte, odpowiada na pytanie o to poparcie, a nie na pytanie, czy dokument historyczny zawiera twierdzenie.
- Koryguj twierdzenia historyczne indywidualnie. Niektóre twierdzenia w nieaktualnym dokumencie mogą nadal być prawdziwe: dołącz bieżący werdykt do każdego istotnego twierdzenia historycznego zamiast oznaczać cały akapit jako nieaktualny. Prześledź istotnych konsumentów, zanim nazwiesz współdzieloną regułę wyłączną dla jednego komponentu. Preferuj dokładnie zaobserwowany zbiór lub predykat zamiast szerszych sformułowań, takich jak „all errors” lub „every status in a class”.

Ponownie użyj kotwic źródłowych i obliczeń już zweryfikowanych. Niezgodność uruchamia wyłącznie sprawdzenie i korektę dotkniętego źródła/wywołującego w każdym wyniku, a nie nowe przejście odkrywania. Jeśli pozostaje nierozstrzygnięta, zakwalifikuj twierdzenie i konsekwentnie wskaż lukę. Ta kontrola domyślnie nie wymaga dodatkowego artefaktu, pracownika ani uruchomienia testów.
Używaj zwięzłego wyjścia walidacji zamiast wielokrotnie je wypisywać. Uruchom wszystkie mające zastosowanie kontrole dokumentów repozytorium jeden raz. Dodaj permalinki commitów tylko wtedy, gdy cytowane bajty odpowiadają temu commitowi, a zdalne repozytorium na pewno go zawiera; lokalne niezatwierdzone dowody zachowują lokalne odwołania file:line. Nie twórz permalinku na podstawie nazwy gałęzi.

Jeśli host zabrania zapisów, przedstaw badanie i jawny status niezapisania w rozmowie. Nie twórz pliku zastępczego ani nie deleguj zapisu. Wznów zapisywanie w trybie z możliwością zapisu w tej samej rozmowie po sprawdzeniu bieżącego pliku docelowego i dostępnego kontekstu; nie rozpoczynaj ponownie rozstrzygniętego badania ani nie obiecuj odzyskania brakującej zawartości rozmowy.

## 5. Przedstaw ustalenia i obsłuż kontynuacje

Zacznij od odpowiedzi, lokalizacji artefaktu lub stanu niezapisania, decydujących referencji oraz istotnych ograniczeń. Badanie nie zleca planowania ani implementacji. Przy przekazaniu do planowania ujawnij rozstrzygnięte fakty, ich źródła, objęte kontrakty oraz nierozwiązane wybory produktowe, aby `raven-plan` budował na nich w tym samym change bez ponownego odkrywania. Raport wskazuje wejściowe wymagania i ich wersję/hash, SHA kodu i dirty state, zgodność z architecture.md, opcje z rekomendacją i kompromisami, ryzyka, luki oraz pytania wymagające decyzji użytkownika. Zalecenie badacza nie jest zaakceptowaną decyzją. Nie rozpisuj kroków implementacji ani kontraktów per plik; to wynik późniejszego planowania.

Zapisz ustalenia z kontynuacji jako aktualizację pliku wersjonowanego w Git, z bieżącymi metadanymi, linkiem do poprzedniej i wskazaniem wniosków zastąpionych przez nowe dowody. Ponownie użyj niezmienionych wyników; zbadaj wyłącznie nowe lub unieważnione pytania. Zachowaj zakres, uprawnienia hosta oraz wszelkie pośrednie edycje dokonane przez ludzi.
## Brownfield: Deep Focus

Gdy pytanie dotyczy istniejącej funkcji, odczytaj aktualną lokalną mapę raven-repo-map, jeśli jest dostępna. Sprawdź jej zakres/SHA i użyj punktów wejścia oraz stref ryzyka do zawężenia pracy; nie traktuj mapy jako dowodu aktualnego zachowania. Brak mapy nie blokuje badania i nie uruchamia automatycznie mapowania całego repo.

Prześledź konkretny przepływ od wejścia przez reguły, dane i skutki uboczne do wyniku. Sprawdź granice modułów, ścieżki błędów, istniejące testy i historię decyzji. Dla pytań strukturalnych użyj dostępnych narzędzi AST, gdy dają lepszy dowód niż tekstowe dopasowanie. Dokumentuj path:line, SHA, ograniczenia i rozbieżności z mapą.

Raport w istniejącym change rozdziela zachowanie potwierdzone, ryzyka, nieznane elementy oraz możliwe usprawnienia według wpływu. Wskaż, co warto zabezpieczyć przed refaktorem, bez implementowania testów lub zmian produkcyjnych. Aktualizacja mapy i plan pozostają osobnymi zleceniami. Nie wymuszaj pełnego DDD dla lokalnej poprawki.
