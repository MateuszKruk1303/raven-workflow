---
name: raven-roadmap
description: Twórz roadmapę greenfield z ustalonego PRD i publikuj changes, kolejność oraz zależności bezpośrednio w prywatnym GitHub Project Ravena. Użyj także do aktualizacji tej roadmapy i odczytu jej statusu; nie do bieżącego prowadzenia pojedynczej zmiany brownfield, szczegółowego planowania tasków ani implementacji.
---

# Raven Roadmap

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

Domyślnie działaj jako skill greenfield: zamień ustalone wymagania produktu w kolejkę changes dostarczających odbieralne rezultaty i od razu opublikuj ją w GitHubie. Nie dodawaj osobnej bramki akceptacji dekompozycji wiernie wynikającej z PRD. GitHub Issues i Project są źródłem prawdy o kolejce, statusach i zależnościach; dokumenty produktu pozostają w `context/foundation/`, a plany changes i taski w GitHubie zgodnie z kontraktem GH. Nie twórz lokalnego `roadmap.md` ani innej trwałej kopii kolejki.

## Granice i uprawnienia

- Przygotowanie zakresu produktu pozostaje wspólne z użytkownikiem niezależnie od późniejszego trybu realizacji. Ustalone PRD i decyzje z rozmowy są podstawą do samodzielnego podziału i sekwencjonowania. Wywołanie skilla lub prośba o utworzenie/aktualizację roadmapy upoważnia do jej publikacji w skonfigurowanym GitHubie bez osobnego pytania „czy publikować?”.
- Pytaj o rzeczywiste braki lub sprzeczności wpływające na produkt, nie o każdą decyzję dekompozycji. Nie rozszerzaj zakresu ani nie odkładaj koniecznych wymagań bez uzgodnienia. Brak odpowiedzi nie rozstrzyga otwartej decyzji; możesz opublikować niezależną, jednoznaczną część zakresu, a zależną pozostawić nieopublikowaną lub oznaczoną Blocked z konkretną przeszkodą, jeśli jej rezultat jest już określony.
- Prośba wyłącznie o propozycję, dyskusję, status lub następny krok nie upoważnia do mutacji. Respektuj jawne „jeszcze nie publikuj”.
- Nie implementuj, nie commituj, nie pushuj, nie wysyłaj komentarzy ani wiadomości i nie uruchamiaj automatycznie kolejnego skilla. Autoryzowana publikacja obejmuje treść issues, etykiety, pola Project i uzgodnione relacje.
- Nie wymuszaj logowania do produktu, wielu użytkowników, wdrożenia ani testów E2E. Wynikają z wymagań konkretnego projektu. Weryfikowalny przepływ od początku do końca nie oznacza automatycznego testu E2E.
- Nie zapisuj nowych preferencji użytkownika bez jego zgody. Nie wprowadzaj osobnych katalogów pilota. Używaj neutralnego języka, bez marek kursów, społeczności i autorów źródłowego workflow.

## 1. Rozpoznaj intencję, źródła i istniejący stan

Rozróżnij: pierwsza roadmapa greenfield, aktualizacja jej ustalonego zakresu, status/następny krok, jawnie zlecona migracja istniejącej roadmapy. Bieżące zadanie brownfield skieruj do przygotowania konkretnego change; nie generuj z jego powodu roadmapy całego produktu. Samo ponowne wywołanie przy istniejącej kolejce zaczyna się od statusu i propozycji następnego kroku, nie pełnej regeneracji.

Przeczytaj instrukcje projektu, `context/foundation/github.json` i całe wskazane PRD (domyślnie `context/foundation/prd.md`). Uzupełnij je istotnymi shape-notes, decyzjami, stackiem, researchami oraz aktywnymi i zarchiwizowanymi changes. Nie wymagaj bootstrapu ani wyboru stacku do planowania produktu. Brak PRD: wykorzystaj jawnie wskazane materiały lub poproś o opis celu; nie wymyślaj wymagań. `raven-prd` jest dostępną ścieżką przygotowania PRD.

Sprawdź we frontmatter PRD pola `roadmap` i `roadmap_project_url`. `roadmap: created` wskazuje opublikowaną roadmapę: zacznij od odczytu jej stanu w GitHubie. Brak tych pól lub lokalnego `roadmap.md` nie oznacza braku roadmapy — sprawdź Project z `github.json`. Znacznik jest odsyłaczem, nie kopią statusów ani dowodem aktualnego stanu kolejki.

Status `draft` PRD nie jest blokadą. Oceń treść: problem i odbiorca, wymagane zachowania, scenariusze oraz reguły domenowe. Pokaż konkretne luki i ich wpływ. Nierozstrzygnięte pytanie blokuje tylko zależny zakres; nie uznawaj całego produktu za niemożliwy do zaplanowania.

Przy dostępnym GitHubie przeczytaj [kontrakt publikacji](references/github-publication.md). Zweryfikuj wskazane repo i Project, ich prywatność oraz pola. Pobierz pełny istniejący stan, w tym zamknięte issues i zależności; nie ograniczaj wykrywania duplikatów do otwartej kolejki.

Brak poprawnego powiązania: można opracować propozycję w czacie, lecz publikacja wymaga `raven-github-setup`. Nazwij konkretny brak. Nie uruchamiaj setupu bez upoważnienia ani nie wybieraj innego konta/repo po cichu. Nie zmieniaj widoczności publicznego celu.

## 2. Zbadaj, co rzeczywiście istnieje

W greenfield sprawdź szkielet i istniejące funkcje. W brownfield sprawdź kod, konfigurację, dokumentację oraz historię changes; wskaż rozbieżności zamiast traktować stare dokumenty jako dowód działania.

Badaj tylko obszary istotne dla zakresu. Dla każdego odróżnij: działa, częściowe, brak, niezweryfikowane; poprzyj ustalenie wskazaniem pliku lub innym dowodem. Deklaracja stacku nie dowodzi implementacji. Nie pytaj użytkownika o fakty możliwe do odczytania z repo.

Nie planuj ponownie istniejących funkcji. Zidentyfikuj brakujący rezultat lub konieczną adaptację. Jeśli dokumentacja się rozmija, zaproponuj ograniczoną korektę i uwzględnij ją w uzgodnieniu; nie przepisuj PRD ani archiwów przy okazji roadmapy.

Przy migracji odczytaj starą roadmapę jako źródło. Pokaż mapowanie istniejących identyfikatorów i statusów na GitHub; zachowaj historię. Migracja wymaga jawnego uzgodnienia, nie jest skutkiem samego istnienia pliku. Nie usuwaj starego dokumentu ani nie utrzymuj dwóch aktywnych kolejek; uzgodnij oznaczenie starego źródła jako historycznego.

## 3. Uzgodnij cel i zaproponuj podział

Wyprowadź rekomendację z PRD i kodu: najważniejszy rezultat, pierwszy używalny przepływ, główna niewiadoma i kolejność. Zadaj zwykle 1–3 krótkie pytania wyłącznie o rzeczywiste decyzje. Nie pytaj ponownie o ustalone priorytety. Dalsze pytania są uzasadnione, jeśli bez odpowiedzi zakres pozostaje niejasny; nie zastępuj ich automatyczną decyzją po arbitralnym limicie.

Każdy change:

- Dostarcza jeden spójny rezultat widoczny dla odbiorcy i ma obserwowalne kryteria odbioru.
- Obejmuje wszystkie potrzebne warstwy. Nie dziel roadmapy na „cały backend”, „całą bazę” i „cały frontend”.
- Wskazuje wymagania źródłowe (np. FR/US/NFR) albo konkretną zaakceptowaną decyzję użytkownika.
- Ma zakres, wyłączenia, zależności oraz nierozstrzygnięte pytania.
- Jest wystarczająco spójny do przygotowania jednego planu. Rozdziel niezależne działania i ryzyka; nie dziel według warstw technicznych.

Osobny change techniczny ma sens tylko jako minimalne odblokowanie nazwanej funkcji lub konkretnego ryzyka. Jeśli tę pracę można wykonać w pierwszym korzystającym z niej change, umieść ją tam. Nie dodawaj infrastruktury „na przyszłość”.

Nie wybieraj bibliotek, schematów danych ani szczegółów implementacji. Nazwy istniejących integracji lub produktów mogą pozostać, gdy określają wymaganie. Nie dodawaj estymacji, punktów ani terminów bez potrzeby użytkownika.

Zbuduj acykliczny graf zależności. Relacja rodzic–dziecko nie jest zależnością wykonania. Kolejność dobieraj zgodnie z zależnościami, wartością i przyjętymi priorytetami; pokaż niezależne gałęzie bez obiecywania, że nie wystąpią konflikty w kodzie.

Domyślnie przedstaw całość uzgodnionego zakresu PRD na poziomie changes, z jasno oznaczoną częścią „teraz” i odłożoną. Każde wymaganie konieczne musi być pokryte, już dostarczone albo jawnie odłożone z uzasadnieniem zatwierdzonym przez użytkownika. Poza zakresem nie staje się automatycznie backlogiem.

Nie twórz obowiązkowej warstwy milestones ani nie wymuszaj jednego otwartego milestone. Jeśli projekt już ich używa lub użytkownik ich chce, zachowaj grupowanie po rezultatach w natywnych GitHub milestones. Nie zamykaj milestone na podstawie samego merge lub zamknięcia issues; potrzebne są dowody odbioru zakresu.

## 4. Przygotuj treść publikacji i pokaż ją w czacie

Pokaż zwięzłą tabelę: `Raven ID | Rezultat | Zależności | Źródła | Proponowany status`. Dla każdego change podaj zakres, wyłączenia i kryteria odbioru na tyle dokładnie, żeby zakres publikowanych issues był czytelny, nie ograniczał się do samych tytułów. Dodaj kolejność, pokrycie wymagań, odłożony zakres i otwarte decyzje.

Przy aktualizacji pokaż diff: dodane, zmienione, proponowane wycofanie oraz wpływ na rozpoczęte changes i istniejące taski. Nie podmieniaj zakresu zakończonej pracy. Nowy zakres po ukończeniu to nowy change, z relacją do wcześniejszej pracy.

Nowy change zwykle ma **Backlog**. **Preparing** oznacza trwające przygotowanie; **Ready** wymaga dopracowanego planu/tasków i spełnionych zależności. Sam opis roadmapowy ani brak zależności nie wystarcza do Ready. **Blocked** wymaga konkretnej przeszkody i wskazania potrzebnej decyzji/akcji; zwykłe czekanie w kolejce nie musi zmieniać Backlog na Blocked.

Szczegółowe taski powstają później podczas przygotowania change, po planowaniu i ewentualnym potrzebnym researchu. Nie publikuj spekulacyjnych sub-issues dla całego PRD. Zachowaj istniejące taski i wskaż potrzebę ich aktualizacji, jeśli zmienia się zakres. Nie przedstawiaj dotkniętego change jako gotowego do implementacji, dopóki taski i zależności nie są spójne; proponowaną zmianę statusu uwzględnij w diffie.

Jeśli treść wynika z ustalonego zakresu, przejdź bez zatrzymania do publikacji. Prezentacja w czacie jest informacją, nie obowiązkowym pytaniem o zgodę. Pytaj tylko o decyzje zmieniające produkt lub nierozstrzygnięty zakres. Użyj dostępnego narzędzia pytań albo zwykłego czatu.

## 5. Sprawdź i opublikuj roadmapę

Przed pierwszą mutacją sprawdź: pokrycie wymagań, brak wymyślonego zakresu, poprawne kryteria, unikalne trwałe ID, brak cykli i nieistniejących zależności, zgodność z kodem, zachowanie istniejącego postępu i prywatność celu.

Napraw własne błędy przed publikacją. Jeśli poprawka zmienia zakres produktu, uzgodnij ją z użytkownikiem. Techniczne poprawki dekompozycji i kolejności wynikające z zależności wykonaj samodzielnie. Nie publikuj sprzecznej części; nazwij brakującą decyzję.

Wykonaj [procedurę publikacji](references/github-publication.md): utwórz lub uaktualnij issues, dodaj do Project, ustaw pola oraz natywne zależności, po czym odczytaj wynik. Działaj wyłącznie w uzgodnionym zakresie. Przy zmianie współbieżnej ponownie porównaj stan, nie nadpisuj cudzych edycji.

Nie odtwarzaj istniejących issues i nie resetuj statusów przy ponownym uruchomieniu. Nie zamykaj, nie usuwaj ani nie wycofuj pracy dlatego, że nowa propozycja jej nie zawiera. Takie zmiany wymagają jawnego zlecenia użytkownika; sama regeneracja roadmapy ich nie upoważnia.

## 6. Handoff i kolejne wywołania

Po pomyślnej publikacji i odczycie potwierdzającym wynik uzupełnij frontmatter źródłowego PRD:

```yaml
roadmap: created
roadmap_project_url: https://github.com/users/OWNER/projects/NUMBER
```

Wstaw rzeczywisty, zweryfikowany URL Project (dla organizacji zachowaj właściwy adres). Zapis tych metadanych jest częścią tworzenia/aktualizacji roadmapy i nie wymaga osobnego potwierdzenia. Zachowaj treść PRD oraz pozostałe pola frontmatter; aktualizuj istniejące klucze zamiast je duplikować. Przy autoryzowanej aktualizacji istniejącej roadmapy uzupełnij też brakujący znacznik po weryfikacji GitHuba. Nie oznaczaj `created` po samej propozycji ani niepełnej lub nieudanej pierwszej publikacji. Prośba wyłącznie o status pozostaje tylko do odczytu. Jeśli nie ma źródłowego pliku PRD, nie twórz go wyłącznie dla znacznika; zgłoś brak miejsca zapisu. Jeśli zapis metadanych się nie powiedzie, zgłoś to osobno, bez ponownej publikacji issues.

W czacie podaj link do Project, linki utworzonych/zmienionych issues, faktycznie zweryfikowany wynik oraz ewentualne niedokończone operacje. Nie odsyłaj do osobnego pliku z instrukcjami.

Zarekomenduj jeden następny change do **przygotowania**, uzasadniając wartością i zależnościami. Jeśli nie ma dostępnego kroku, wskaż konkretną decyzję odblokowującą pracę. Nie myl gotowości do przygotowania z Ready do realizacji i nie odsyłaj do nieistniejących skilli.

Przy prośbie o status odczytaj GitHub i istotny kontekst lokalny, opisz postęp oraz rozbieżności. Nie awansuj automatycznie do Done na podstawie zamknięcia issue, merge lub ukończenia samych sub-issues — zakres change i wymagany odbiór muszą być spełnione. Po zakończeniu zakresu zaproponuj rozmowę o następnym, bez automatycznego otwierania kolejnej porcji pracy.
