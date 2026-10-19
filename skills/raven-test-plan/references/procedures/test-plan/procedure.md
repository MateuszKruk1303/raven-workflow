# Strategia testów i etapowe wdrożenie

Kanoniczny dokument: `context/foundation/test-plan.md`, historia: Git. Stosuj [kontrakt pracy](../../../../raven-workflow/references/change-contract.md) i [schemat §1–§8](references/test-plan-schema.md). Strategia nie implementuje testów ani CI i nie uruchamia całego cyklu automatycznie.

## 0. Zakres i wznowienie

Potwierdź repo lub greenfield PRD. Odczytaj istniejącą strategię, potrzebne plany/checkpointy i dokładne powiązane issues GH, gdy ustalasz stan tasków; nie skanuj całej kolejki. `--status` jest read-only; pokazuje realne dowody i luki, nie naprawia stanu. `--refresh` tworzy zmianę strategii z dotychczasowym źródłem/wersją. Brak pliku nie oznacza braku ochrony: sprawdź istniejące testy/konfigurację; historyczne artefakty wykorzystaj tylko gdy dotyczą wskazanej pracy.

Dla rollout rozróżniaj: brak change, rozpoznanie, plan, review, wykonanie, zweryfikowana ochrona i dostarczenie. Istnienie planu nie zleca implementacji, a komplet checkboxów nie dowodzi merge. Każdy konkretny change rollout lub odświeżenia strategii wymaga issue GH; jego podjęcie podczas zleconego planowania/implementacji potwierdź zgodnie ze wspólnym kontraktem. Stan taska, właściciel i zależności należą do GH; postęp wykonania i dowody do planu/checkpointu. Osobny change.md ani Project nie są wymagane. Sam dokument strategii nie otrzymuje osobnego issue będącego jego kopią. Research jest opcjonalny, gdy brakuje wiedzy; nie wymagaj osobnego skilla, jeśli dowody już istnieją.

## 1. Discovery

Czytaj PRD, architekturę, instrukcje, lessons, manifesty, dostępne runnery/komendy i reprezentatywne testy. Klasyfikuj profil `none / sparse / meaningful` na podstawie rzeczywistej ochrony, nie samej liczby plików. Zachowaj istniejące narzędzia. Dla młodego projektu użyj wymagań i obaw użytkownika zamiast nieistniejącej historii.

Ustal zakres hot-spotów przed kosztownym skanem. Historia/churn i współzmienność wskazują gdzie pytać, nie która linia powoduje błąd. Przy skanie np. ostatnich 30 dni zapisz zakres, wyklucz lockfile/vendor/generated/build i ograniczenia shallow clone. Obawy użytkownika oraz incydenty są pełnoprawnymi źródłami ryzyk. Nie twórz rankingu złego kodu z liczby commitów.

Zapisz dostępne możliwości CLI/browser/CI/platform tylko w zakresie ich przydatności dla przyszłych kontroli. Nie uznawaj istnienia konektora za zgodę zapisu ani nie konfiguruj MCP/sekretów. Test-stack dokumentuje rzeczywiste polecenia, runner, środowisko i konwencje.

## 2. Wywiad i challenger

Pytaj o nierozstrzygnięte obawy, najdroższe awarie, krytyczne przepływy, zakres danych i akceptowalny koszt sygnału. Wykorzystaj wcześniej udzielone odpowiedzi; nie wymagaj stałej liczby pytań. Pokaż rekomendację i kompromis.

Challenger sprawdza założenia mapy ryzyk, martwe pola i propozycje nadmiernego E2E. Przy niezależnym delegowaniu użyj świeżego kontekstu; nie traktuj samokontroli jako niezależnego dowodu. Dobór dodatkowej analizy wynika ze skali i ryzyka, nie sztywnej liczby agentów.

## 3. Brief i decyzja

Przedstaw priorytety, najtańszy skuteczny sygnał dla każdego ryzyka, świadomie niechronione obszary i plan etapów. Potwierdź istotne decyzje; zaakceptowane wcześniej ustalenia pozostają ważne. Nie obiecuj oszczędności procentowych bez pomiaru.

Trzy zasady: **koszt × sygnał** (najtańsza skuteczna kontrola), **obawy użytkownika są dowodem**, **sygnał ≠ wiedza**. Statystyka churn nie jest kotwicą implementacji. Nazwij potrzebną konkretną analizę, zanim przypiszesz przyczynę do kodu.

## 4. Dokument strategii

Zapisz §1–§8 według schematu: zasady i przyjęty zakres, rejestr ryzyk ze stabilnymi ID/źródłami, rollout opisujący kolejność ochrony ryzyk i powiązania z istniejącymi issues GH, bez lokalnej kolejki tasków ani tabeli ich statusów, Risk Response Guidance, dowody/metoda kontroli, cookbook oraz negative space/ograniczenia. Zachowaj semantykę schematu, nie wymuszaj sztucznych wierszy dla nieistniejącej warstwy.

Każde ryzyko opisuje obserwowalną awarię i skutek, dowód, źródło Expected, właściwą warstwę, granice do zbadania, przypadek brzegowy i antywzorzec do uniknięcia. Odwzorowanie implementacji, happy-path-only, nadmierne mocki i kruche porządki nie są dobrą ochroną. Nie nakładaj modelowego/visual review na deterministyczny sygnał bez niezależnego ryzyka.

## 5. Wybór rollout

Zaproponuj pierwszy ograniczony change ochrony według wartości/zależności. Konkretny change rollout jest odbieralnym rezultatem, nie automatycznie osobną warstwą testów. Jego task, zależności i stan śledź w issue GH; strategia opisuje uzasadnienie i sposób ochrony ryzyk. Nie twórz issues dla kroków planu ani nie reorganizuj kolejki na podstawie samej rekomendacji. Testy produktu normalnie powstają z implementacją; rollout służy rzeczywistym lukom lub inwestycji przekrojowej. Dokumentuj dostarczone wzorce w cookbook §6 wraz z plikami/komendami, nie samą deklaracją.

## 6. Handoff i refresh

Oddaj ścieżkę strategii, źródła/wersję, bieżący stan, dowody i jedno następne działanie. Odróżnij rekomendację od autoryzacji. Nie wymagaj czyszczenia rozmowy ani schowka; nowa sesja odczytuje repo i checkpoint.

Przy odświeżeniu badaj nowe/unieważnione ryzyka i zachowaj niezmienione ustalenia. Korekta wymagania lub istotnej strategii wraca do decyzji przed zależnym wykonaniem. Nie przepisuj §1/§2 na podstawie pojedynczego testu ani nie archiwizuj automatycznie starych changes. Aktualny plik i Git zastępują snapshoty komentarzy.

Cookbook powinien pomagać raven-test znaleźć istniejący test i asercję, powiązać je z AC/ryzykiem, ocenić aktualność dowodu i nazwać lukę przed dodaniem testu. Standardowe domknięcie regresji po ręcznej weryfikacji nie jest nowym rolloutem ani nowym issue. Wystarczająca ochrona może zakończyć audyt bez zmian testów; nie twórz recept duplikujących całą suite.
