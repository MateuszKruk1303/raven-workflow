---
name: raven-shape
description: "Dopracuj pomysł na nowy produkt lub znaczącą zmianę istniejącego systemu w uporządkowanej rozmowie o problemie, odbiorcach i zakresie produktu. Zapisuj i wznawiaj shape-notes.md dla skilli Raven przed PRD. Użyj przy kształtowaniu wizji, zakresu MVP, wymagań i reguł biznesowych; nie do implementacji pojedynczego błędu."
---

# Raven Shape

Przeprowadź użytkownika od pomysłu do notatek pozwalających napisać PRD. Wynik: `context/foundation/shape-notes.md`, zgodny z wejściem `$raven-prd`. Jawnie wskazane starsze notatki można wykorzystać jako źródło, bez automatycznego przenoszenia historii. Utrzymuj jeden kanoniczny dokument notatek.

## Start i wznowienie

1. Przeczytaj lokalne instrukcje oraz podany opis lub pliki. Zachowaj pierwotny opis i jego źródło. Sprawdź istniejące notatki, PRD i README; wcześniejsze dokumenty spoza tego etapu traktuj jako źródła do odczytu, bez automatycznej migracji ani modyfikowania.
2. Rozpoznaj greenfield albo brownfield z intencji i zawartości projektu. Sam manifest startera nie oznacza istniejącego produktu. Przy brownfield sprawdź tylko kod i dokumenty potrzebne do zrozumienia zmiany; rozróżnij zachowanie zaobserwowane od deklarowanego.
3. Jeśli brakuje `context/foundation/`, utwórz tylko potrzebny katalog.
4. Przeczytaj całe istniejące `shape-notes.md` i [format notatek](references/shape-notes.md). Wznów od checkpointu; jeśli wcześniejsze notatki nie mają checkpointu, ustal postęp z ich treści. Zachowaj sekcje, źródła i decyzje, których nie definiuje nowy format. Nie rozpoczynaj wywiadu ponownie bez powodu.
5. Krótko podsumuj znane ustalenia i przejdź do najważniejszej niewiadomej. Gdy nie podano pomysłu i nie ma go w źródłach, poproś o krótki opis odbiorcy, problemu i zamierzonej zmiany.

## Sposób rozmowy

- Prowadź rozmowę w języku użytkownika. Zadawaj zwykle jedno konkretne pytanie albo niewielki zestaw ściśle powiązanych pytań. Nie pytaj o liczbę rund ani informacje już dostępne.
- Kolejność tematów poniżej jest domyślna, nie obowiązkowym kwestionariuszem. Odpowiedź może zamknąć kilka tematów. Nie wymagaj osobnego zatwierdzenia każdego kroku.
- Formatuj wymagania na podstawie wypowiedzi i źródeł. Propozycje agenta oznaczaj jawnie; nie przedstawiaj ich jako decyzji użytkownika. Brak odpowiedzi to niewiadoma, nie zgoda.
- Po istotnej odpowiedzi utrwal checkpoint, decyzje i otwarte pytania. Zapisuj użyteczny draft także przy przerwaniu lub pominięciu tematu.

## Tematy odkrywania

### 1. Problem, wizja i odbiorcy

Ustal, kto ma problem, jak rozwiązuje go dziś, dlaczego obecne obejście nie wystarcza i jaka zmiana przyniesie wartość. Oddziel wizję docelową od pierwszego pilota. Dla brownfield opisz obecny system, oczekiwaną różnicę i zachowania, które muszą przetrwać.

### 2. Dostęp i role

Ustal sposób wejścia do produktu, role, właścicieli danych i granice widoczności. Nie zakładaj potrzeby kont ani wielu ról. W istniejącym systemie rozróżnij obecne uprawnienia od planowanych zmian. Pytaj o doświadczenie i uprawnienia, nie wybór biblioteki auth.

### 3. Najmniejszy kompletny przepływ i sukces

Przejdź od wejścia użytkownika do osiągnięcia wartości. Ustal, co stanowi najmniejszą użyteczną wersję, jakie ręczne operacje są akceptowane i jak dotrzeć do pierwszych użytkowników. Zapisz hipotezę wartości oraz obserwowalny sygnał sukcesu lub porażki; nie wymyślaj progów ani terminów.

Jeśli zakres rośnie, nazwij konkretne kosztowne elementy i zaproponuj ograniczenie lub odłożenie ich. Odnieś koszt do rzeczywistego czasu i budżetu użytkownika. Nie narzucaj limitu tygodni ani liczby kroków; świadomie większy zakres jest poprawną decyzją.

### 4. Wymagania i scenariusze

Z przepływu wyprowadź szkice FR z trwałymi ID `FR-001`, aktorem, możliwością, priorytetem `pilot` lub `later` i źródłem. Dla brownfield oznacz `new`, `modified` lub `preserved`. Nie numeruj ponownie istniejących wymagań przy edycji i nie wykorzystuj usuniętych ID.

Zapisz główny scenariusz i istotne wyjątki jako obserwowalne kryteria, np. Given/When/Then. Podważaj kosztowne lub nieoczywiste założenia: co przemawia za usunięciem wymagania, co się stanie przy błędzie, dlaczego jest potrzebne w pilocie? Nie wymuszaj osobnej rundy kontrargumentów dla każdego FR.

### 5. Reguły biznesowe, dane i jakość

Ustal rzeczywiste reguły decyzji, walidacji, obliczeń lub przejść stanów: wejście, wynik i wyjątki. Jeśli produkt to prosta ewidencja, sprawdź jej wartość wobec obecnego rozwiązania; nie wymyślaj dodatkowej logiki tylko po to, by wyjść poza CRUD.

Zapisz istotne dane i ograniczenia potrzebne do zrozumienia reguł, bez projektowania schematu bazy. Ustal adekwatne wymagania jakościowe: prywatność, dostępność, utratę danych, czas odpowiedzi lub obsługiwane urządzenia. Cele liczbowe wymagają źródła lub oznaczenia jako propozycja. Dla brownfield uwzględnij integracje, zgodność danych i ryzyko regresji; czysta zmiana infrastruktury nie musi mieć nowej reguły domenowej.

### 6. Granice i ograniczenia

Zapisz poza zakresem, przyszłe pomysły, typ produktu, początkową skalę oraz znane ograniczenia czasu i kosztu. Nie prowadź wyboru stacku. Zastaną technologię i dobrowolnie podane preferencje zachowaj jako kontekst do późniejszego przygotowania, nie nową zatwierdzoną architekturę.

## Kontrola i przekazanie

Sprawdź kompletność problemu i odbiorcy, przepływu, dostępu, wymagań, reguł, sygnału sukcesu oraz wyłączeń; dla brownfield także zachowania do zachowania. Przy każdej rzeczywistej luce zapisz nazwę, konsekwencję i otwarte pytanie. `Nie dotyczy` jest prawidłowym wynikiem z uzasadnieniem.

Gdy brakuje decyzji zmieniającej produkt, zapytaj konkretnie. Użytkownik może zakończyć z lukami: zapisz `warned`, nie fikcyjne uzgodnienie. Bez luk ustaw `complete`; przy trwającej rozmowie `in_progress`. W podsumowaniu podaj plik, najważniejsze niewiadome i następny krok `$raven-prd`. Samo shape nie uruchamia PRD, budowy, testów ani publikacji.

Nie edytuj istniejącego PRD, roadmapy, kodu ani archiwów. Jeśli nowe ustalenia zmieniają wcześniejsze PRD lub aktywne chunki, opisz rozbieżność w notatkach i wskaż konieczność aktualizacji w odpowiednim etapie Raven.
