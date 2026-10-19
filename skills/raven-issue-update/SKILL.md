---
name: raven-issue-update
description: Wpleć dodatkowe lub doprecyzowane wymaganie do treści wskazanego istniejącego GitHub issue. Opcjonalny helper do aktualizacji zakresu i kryteriów odbioru, bez reorganizacji roadmapy ani realizacji change.
---

# Raven Issue Update

Stosuj [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Zlecenie „zaktualizuj issue o…” obejmuje zapis **body jednego wskazanego istniejącego issue**. Nie wymagaj dodatkowej rutynowej zgody na ten zapis. Samo pytanie, pomysł bez polecenia zapisu lub prośba o propozycję pozostaje read-only. Nie twórz nowych issues, komentarzy ani lokalnego backlogu; nie zmieniaj tytułu, zależności, kolejności, statusu, assignee, planu, kodu, PRD ani Jira. Nie podejmuj taska jako In progress: zapis wymagania nie rozpoczyna planowania lub implementacji. To opcjonalny helper, bez obowiązkowego review każdej aktualizacji.

## Ustal źródło i intencję

Rozwiąż dokładny URL/numer issue albo change ID na podstawie instrukcji repo i istniejących powiązań (`.raven/config.json`, historyczne `context/foundation/github.json`, wskazany plan). Sam numer wymaga jednoznacznego repo, a change ID jednoznacznego mapowania. Nie wybieraj najnowszego/podobnego issue i nie skanuj całej kolejki. Przy brakującym celu zapytaj tylko o identyfikację.

Odczytaj aktualny pełny body, stan issue i powiązanie z PR/change. Przeczytaj potrzebne do redakcji źródła i decyzje, w tym wskazane wątki oraz kontrakt aktywnego planu, jeśli istnieje. Nie kopiuj całej historii ani ticketów Jira. Rozróżnij nowe wymaganie użytkownika od dotychczasowej decyzji i od propozycji technicznej.

Jeśli issue jest zamknięty lub jego change został zmergowany, przed edycją wyjaśnij, czy chodzi o korektę opisu dostarczonego zachowania, czy nowy zakres. Nie dopisuj niespełnionego zakresu do ukończonej pracy, nie otwieraj issue ponownie i nie twórz następnego przy okazji.

Istotna sprzeczność z wcześniejszym wymaganiem, wyłączeniem lub decyzją wymaga rozstrzygnięcia użytkownika przed zależnym zapisem. Pokaż konkretną sprzeczność i zapytaj o intencję; nie osłabiaj dodatku ani nie rozszerzaj go samodzielnie, aby pasował do starego tekstu. Jednoznaczne polecenie zastąpienia wcześniejszego wymagania jest już decyzją. Drobne redakcyjne szczegóły rozwiąż sam. Gdy dodatek wymaga zmiany innych issues lub podziału pracy, nazwij potrzebę osobnego [raven-roadmap](../raven-roadmap/SKILL.md), bez reorganizacji w tym wywołaniu.

## Wpleć wymaganie

Przygotuj najmniejszą semantyczną zmianę istniejącego opisu: uzupełnij odpowiedni zakres i obserwowalne kryteria odbioru, ewentualnie bezpośrednio dotknięte wyłączenie lub opis wyniku. Zachowaj strukturę issue. Nie kończ na luźnym „do zapamiętania”, komentarzu czy dopisku pod gotową treścią. AC opisują wynik wymagany przez użytkownika, bez wymyślania parametrów, gwarancji lub decyzji implementacyjnych.

Zachowaj pozostałą treść, identyfikatory AC, linki, decyzje, markery/zarządzane fragmenty i postęp. Nie rozszerzaj znaczenia zaznaczonego `[x]` o niesprawdzony warunek: zachowaj zaliczony punkt, a nowy obowiązek zapisz jako osobne niezaznaczone AC. Nie resetuj istniejących checkboxów ani nie oznaczaj nowych jako wykonanych. Jeśli wymaganie już wynika z zakresu i AC, zakończ no-op z odwołaniem do istniejącego zapisu; sama inna fraza nie uzasadnia duplikatu.

Nowy mechanizm jest wymaganiem, nie planem wykonawczym. Przy aktywnym change wolno zapisać wymaganie w issue bez uruchamiania całego cyklu. Nie edytuj historycznych decyzji ani PASS. W wyniku wskaż rozbieżność z aktualnym kontraktem: przed zależną implementacją potrzebne są aktualizacja planu i review dotkniętego zakresu w ramach zleconej dalszej pracy, bez formalnej akceptacji planu. Wcześniejsze dowody pozostają obserwacją swojej wersji; nie potwierdzają nowego zakresu. Sam zapis issue nie wykonuje tych następnych etapów.

## Zapisz i potwierdź

Użyj dostępnego connectora/API lub `gh` według jego aktualnej pomocy; nie wymagaj konkretnej integracji. Przed zapisem sprawdź różnicę: tylko uzgodniony dodatek i jego konieczne powiązania w body. Dla CLI przekaż dokładne wielowierszowe body przez plik tymczasowy i `--body-file`, bez interpolacji treści do polecenia shell.

Bezpośrednio przed zapisem ponownie odczytaj body i stan. Jeśli zmieniły się od redakcji, opracuj deltę na najnowszej treści, zachowując cudze zmiany; konflikt znaczenia wyjaśnij przed zapisem. Jeśli API obsługuje warunkowy zapis wersji, użyj go. Zwykły read → write nie jest blokadą: przy oznakach równoległej edycji, których nie da się bezpiecznie rozstrzygnąć, zatrzymaj zapis zamiast nadpisywać cudzą pracę. Nie wysyłaj pól spoza body ani starego payloadu po konflikcie wersji.

Po zapisie odczytaj issue i sprawdź wymaganie, AC oraz zachowanie wcześniejszej treści/postępu. Po timeout najpierw odczytaj stan: jeśli zmiana już istnieje, nie ponawiaj; jeśli jej brak, przygotuj ewentualne ponowienie na aktualnej treści. Brak odczytu nie oznacza nieudanego zapisu. Po dwóch nieskutecznych próbach tego samego zapisu zakończ z jawnym niepotwierdzonym wynikiem i gotową propozycją w rozmowie; nie wracaj automatycznie do starego body.

Brak dostępu do GH lub prawa zapisu nie tworzy lokalnego backlogu: oddaj w rozmowie gotowy fragment do wplecenia albo pełny proponowany body, jeśli odczytano oryginał, oraz nazwij niewykonaną operację. Bez oryginału nie deklaruj kompletnego scalenia. Przy wznowieniu odczytaj rzeczywisty stan i uwzględnij wcześniejsze próby zamiast zakładać, że ostatnia mutacja zawiodła.

Oddaj link do issue, krótko co wpleciono i wynik readback albo no-op/niewykonany zapis. Dla aktywnego planu dodaj tylko potrzebny następny krok. Nie deklaruj gotowej implementacji ani aktualizacji innych artefaktów.
