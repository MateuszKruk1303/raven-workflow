---
name: raven-architecture
description: Interaktywnie ustal przekrojowe decyzje architektoniczne i utwórz lub uaktualnij context/foundation/architecture.md na podstawie PRD, dokumentacji, kodu i roadmapy. Prowadzi przez opcje, rekomendacje i kompromisy; nie zastępuje planu pojedynczego change.
---

# Raven Architecture

Zbuduj z użytkownikiem zrozumiały obraz architektury całego produktu: odpowiedzialności części systemu, przepływy, miejsca przechowywania danych, granice integracji i zasady operacyjne. Wynikiem jest `context/foundation/architecture.md`, a nie implementacja, lista bibliotek ani roadmapa. Czytaj najpierw [raven-workflow](../raven-workflow/SKILL.md).

## Zakres i uprawnienia

Wywołanie upoważnia do czytania źródeł i zapisu dokumentu wraz z krótkim odnośnikiem w odpowiednim istniejącym AGENTS.md. Nie zmieniaj przy okazji PRD, kodu, konfiguracji usług, issues, statusów Project, innych instrukcji agenta ani globalnych preferencji. Nie commituj, nie pushuj, nie wdrażaj i nie uruchamiaj kolejnego skilla bez osobnego zlecenia. Repo obce lub ograniczone instrukcjami traktuj zgodnie z dozwolonym miejscem zapisu; nie instaluj tam własnego workflow samowolnie.

Wymagania i jawne decyzje użytkownika są ograniczeniami, nie sugestiami do zastąpienia. Architektura opisuje fakty oraz uzgodniony kierunek, nie nadaje propozycjom statusu decyzji. Istniejący stack nie jest zaproszeniem do jego wymiany. Nie wprowadzaj usług, mikroserwisów, kolejek, cache, wielodostępności ani infrastruktury pod nieuzgodnione przyszłe potrzeby.

## 1. Odtwórz źródła i mapę decyzji

Rozróżnij pierwsze opracowanie, wznowienie rozmowy i aktualizację określonej części. Odczytaj istniejące architecture.md zanim coś zapiszesz. Zachowaj nieruszone decyzje, ich ID, uzasadnienia i źródła.

Przejrzyj inwentarz dokumentacji repo: instrukcje, README, pełne aktualne PRD/shape, dokumenty stacku/infrastruktury, ADR, bezpieczeństwa, testów, integracji oraz lessons. Czytaj wszystkie materiały istotne dla architektury; pokaż brakujące źródła i sprzeczności. Nie traktuj archiwum jako bieżącego wymagania. Nie odczytuj sekretów ani generowanych katalogów w celu uzupełnienia dokumentacji.

Odczytaj roadmapę w GitHub Issues, wyłącznie potrzebne changes/zależności i lokalne plany/research/decyzje. Nie czytaj całej historii GH i nie twórz drugiej kolejki. Brak dostępu do źródła nazwij, kontynuując niezależne ustalenia. Nie uruchamiaj setupu przy okazji. Brak PRD w brownfield nie blokuje pracy, jeżeli cel i zakres wynikają z innych wiarygodnych materiałów; rzeczywiście brakujące wymagania uzgodnij.

Sprawdź w kodzie i konfiguracji obszary istotne dla decyzji. Ładuj dostępne skille domenowe, gdy analizujesz ich technologię. Rozróżniaj „istnieje i sprawdzono”, „deklarowane w dokumentacji”, „docelowe, uzgodnione” i „propozycja”. Napisanie w dokumencie „S3” nie dowodzi wdrożenia S3.

Pokaż krótki punkt wyjścia i listę obszarów rozmowy wynikających z produktu. Oddziel już ustalone decyzje od pytań; nie pytaj użytkownika o fakty dostępne w repo ani ponownie o zaakceptowany wybór. Sprzeczność z kodem przedstaw jako różnicę obecne/docelowe, a nie powód do cichej zmiany decyzji.

## 2. Prowadź rozmowę od ogółu do szczegółu

Zacznij od granic systemu, głównych przepływów i odpowiedzialności. Następnie przejdź do danych, plików, komunikacji, integracji oraz utrzymania. Kolejność dostosuj do zależności decyzji i ryzyka. Użytkownik nie musi znać nazw technologii.

Zadawaj zwykle 1–3 powiązane pytania na rundę, przez dostępne narzędzie pytań lub czat. Każde pytanie powinno zawierać:
- potrzebę wynikającą z konkretnego wymagania lub przepływu;
- 2–3 rzeczywiście sensowne opcje, w tym zachowanie obecnego rozwiązania, jeśli spełnia potrzebę;
- rekomendację z uzasadnieniem dla tego projektu;
- korzyści, koszty/odpowiedzialność operacyjną, ograniczenia i istotne konsekwencje każdej opcji;
- informację, co decyzja odblokuje, a co można rozstrzygnąć później.

Nie twórz pozornych alternatyw wyłącznie dla liczby opcji. Przy jednej wykonalnej opcji wyjaśnij ograniczenie i uzgodnij kierunek. Nie ukrywaj kosztów dostawcy ani pracy utrzymaniowej. Ceny, limity, zgodność i możliwości usług weryfikuj w aktualnych oficjalnych źródłach przed rekomendacją. Weryfikuj też niepewne twierdzenia techniczne. Gdy nie ma dostępu do źródeł, oznacz je jako niezweryfikowane zamiast obiecywać działanie.

Czekaj na odpowiedzi przed rozstrzygnięciem zależnych wyborów. Brak odpowiedzi nie jest zgodą. Po rundzie krótko podsumuj decyzje, ich konsekwencje i pozostałe obszary. Jeśli nowa odpowiedź zmienia wcześniejszy wybór, pokaż wpływ i uzgodnij tylko sprzeczne elementy. Nie narzucaj liczby pytań ani nie kończ rozmowy po arbitralnym limicie.

Przykład typu pytania: „Gdzie mają trafiać obrazy użytkowników i produktów? Obecnie pliki są lokalne. Dla planowanego hostingu rekomenduję storage obiektowy, ponieważ pliki muszą przetrwać wymianę instancji. Alternatywą jest trwały dysk z własnym backupem. W obu wariantach trzeba określić, jakie referencje i metadane przechowuje baza oraz jak działa dostęp.” To przykład sposobu rozumowania, nie uniwersalny zakaz przechowywania binariów w bazie ani narzucony dostawca.

## 3. Buduj jeden dokument podczas rozmowy

Przeczytaj [format dokumentu](references/architecture-document.md). Zapisuj uzgodnione decyzje i pytania w tym samym architecture.md, oznaczając wersję roboczą. Zapis draftu nie wymaga dodatkowej akceptacji; nie oznacza jednak akceptacji propozycji. Nie twórz obok kolejnego rejestru rozmowy ani lokalnego statusu changes. Przy wznowieniu wróć do nierozstrzygniętych punktów, bez powtarzania całego wywiadu.

Każda decyzja ma stabilne ID, status, źródło, uzasadnienie i konsekwencje dla implementacji. Przy decyzji „później” zapisz świadome odroczenie, warunek powrotu i dotknięte changes. Odroczenie wyboru dostawcy może być poprawne, jeśli kontrakt przechowywania, dostępów i trwałości jest już określony. Nie odkładaj za użytkownika decyzji potrzebnej do zrozumienia architektury.

Zapisuj zasady na tyle konkretnie, by agent wiedział, gdzie umieścić odpowiedzialność, dane lub integrację. Nie projektuj każdej tabeli, endpointu, funkcji ani faz wykonania; to zakres planowania change. Jeśli potrzeba badań blokuje wybór, nazwij precyzyjne pytanie i zaproponuj `raven-research` dla właściwego change, nie uruchamiaj go automatycznie i nie wymyślaj wyniku.

## 4. Domknij pełny obraz i przekaż dalej

Sprawdź pokrycie wszystkich istotnych wymagań i changes: każdy przekrojowy obszar ma decyzję, jawne „nie dotyczy” z powodem albo uzgodnione odroczenie. Szczególnie sprawdź zgodność diagramu z tabelami, granice odpowiedzialności, dane w bazie vs pliki, różnice lokalnie/produkcja, dostęp i trwałość oraz skutki błędów integracji. Brak funkcji w produkcie nie wymaga rozdziału o jej architekturze.

Pokaż użytkownikowi pełny zwięzły obraz: komponenty i przepływy, kluczowe decyzje z powodami, różnice obecne/docelowe, koszty i otwarte punkty. Zapytaj o akceptację tego konkretnego dokumentu, chyba że aktualna wersja została już wyraźnie zaakceptowana. Status `accepted` nadaj dopiero dla zatwierdzonej wersji i uzgodnionych odroczeń. Przy nierozstrzygniętej fundamentalnej decyzji zachowaj `draft`, wskaż dokładny brak i kontynuuj rozmowę. Akceptacja nie jest pozwoleniem na implementację lub zakup usług.

Dodaj krótki odnośnik do architecture.md w istniejącym AGENTS.md, informując o czytaniu go przed planowaniem/implementacją i o respektowaniu statusów decyzji. Nie twórz całego AGENTS.md jako efektu ubocznego; gdy go brak, podaj odnośnik w handoffie. Zweryfikuj linki, formatowanie oraz spójność źródeł. Zakończ linkiem do dokumentu, stanem akceptacji, najważniejszymi decyzjami i konkretnym następnym krokiem. Nie oznaczaj żadnego change Ready lub Done.
