---
name: raven-md
description: "Utwórz, uaktualnij lub oceń AGENTS.md (albo inny plik instrukcji AI) na podstawie rzeczywistych plików, poleceń i konwencji projektu. Review daje kartę wyników bez przepisywania zasad. Nie inicjalizuje folderów kontekstu ani stacku."
---

# Raven MD

Dwa tryby: **tworzenie/aktualizacja** (domyślny) i **review** — gdy użytkownik prosi o ocenę pliku instrukcji. W trybie review stosuj [procedurę przeglądu](references/review.md): pięć kontroli (długość, fragmenty kodu/config, precyzja, nadmiarowa wiedza, kolejność), karta wyników z `path:line` i Top 3 actions w czacie, bez edycji pliku poza zatwierdzoną zmianą kolejności. Prywatnych globalnych instrukcji nie kopiuj do repo.

Twórz zwięzły przewodnik dla agenta pracującego w projekcie. Wynikiem jest jeden plik `AGENTS.md`, z konkretnymi zasadami, działającymi odnośnikami i poleceniami opartymi na źródłach. Zachowaj język istniejącego dokumentu, a dla nowego użyj języka użytkownika. Tytuł nowego dokumentu: `# Repository Guidelines`.

## Cel i zakres

- Bez argumentów wybierz główny katalog bieżącego repozytorium (`git rev-parse --show-toplevel`); poza Git użyj katalogu projektu wskazanego przez użytkownika albo cwd.
- Jawny katalog jako argument oznacza `<katalog>/AGENTS.md`. Jawna ścieżka pliku Markdown oznacza dokładnie ten plik. Rozwiąż ścieżkę przed zapisem; symlink nie może niejawnie skierować zapisu do innego projektu.
- Czytaj obowiązujące instrukcje nadrzędne i istniejący plik docelowy. Zagnieżdżone `AGENTS.md` dotyczą swoich poddrzew: nie przenoś ich lokalnych zakazów do całego repo bez uzasadnienia.
- Główny dokument opisuje pracę w repozytorium. Dokument w podkatalogu opisuje lokalne wzorce i różnice względem instrukcji nadrzędnych.
- Samo wywołanie skilla autoryzuje utworzenie lub celową aktualizację dokumentu. Nie dodawaj rutynowej bramki akceptacji szkicu; pytaj przy istotnej sprzeczności, której źródła nie rozstrzygają.

## Zbierz dowody

Użyj `rg --files` do rozpoznania struktury, pomijając zależności, wyniki buildów i `.git`. Czytaj tylko źródła potrzebne do stworzenia przewodnika:

1. README, istniejące instrukcje agentów, indeks dokumentacji oraz dokumenty architektury.
2. Manifesty, skrypty, deklarowany package manager, lockfile i konfigurację workspace. Nie zakładaj stacku Raven tylko na podstawie nazwy skilla.
3. Konfigurację formatowania, lintowania, typów, testów i istotne workflow CI.
4. Reprezentatywne pliki źródłowe i testy potwierdzające strukturę, nazewnictwo i granice modułów.
5. Krótką historię Git, jeśli istnieje i potrzebne są konwencje commitów. Zaobserwowany zwyczaj nie jest automatycznie obowiązkową regułą.

Niezależne odczyty można wykonywać równolegle narzędziami. Nie uruchamiaj instalacji, migracji, serwera ani całej baterii testów tylko po to, żeby udokumentować dostępne polecenia. Rozróżniaj polecenie znalezione w konfiguracji od faktycznie uruchomionego i zaliczonego. Nie czytaj wartości sekretów; do opisania konfiguracji wystarczą nazwy zmiennych z bezpiecznych szablonów i odnośniki do instrukcji.

Dla podkatalogu skup się na sąsiednich plikach, lokalnych konfiguracjach i jednym dobrym przykładzie nowej jednostki. Nie powtarzaj globalnej mapy monorepo, historii commitów ani wszystkich poleceń CI. Wskaż nadrzędny przewodnik rzeczywistą ścieżką względną.

## Kontekst Raven

Jeśli projekt używa Raven, przeczytaj istotne dokumenty w `context/foundation/` (PRD, architektura, tech-stack, test-stack, lessons). Zapisz tylko reguły potrzebne przyszłemu agentowi i linki do kanonicznych źródeł; nie kopiuj instrukcji skilli.

Nie twórz zależności od osobistych ścieżek `~/.codex/skills`. Nie narzucaj modeli agentów, procesu, zakazów edycji testów ani struktury archiwów projektowi, który ich nie przyjął. Nie inicjalizuj `context/` przy okazji edycji instrukcji; potrzebne katalogi tworzy właściwy etap Raven.

## Utwórz albo zaktualizuj

**Nowy plik:** opisz krótko projekt, następnie najważniejsze ograniczenia i polecenia. Pozostałe sekcje dobierz do dowodów:

- mapa kodu i granic modułów;
- polecenia dev/build/lint/typecheck/test z katalogiem uruchomienia i istotnymi warunkami;
- lokalne konwencje, których nie widać z samych domyślnych zachowań frameworka;
- wymagane kontrole CI i zasady testowania, jeśli istnieją;
- zasady commitów i PR tylko jeśli są ustalone;
- linki do architektury, konfiguracji i dokumentów kontekstowych.

**Istniejący plik:** przeczytaj go w całości oraz sprawdź niezacommitowane zmiany. Zachowaj poprawną treść, styl i ręczne ustalenia. Zweryfikuj wymienione ścieżki i polecenia względem aktualnego drzewa, także plików nieśledzonych. Historia ostatniej edycji i diff od tego commitu mogą pomóc znaleźć zmiany, ale nie zastępują sprawdzenia aktualnej konfiguracji.

Wprowadź celowane poprawki: zachowaj aktualne informacje, popraw nieaktualne, uzupełnij istotne braki. Usuwaj twierdzenia dopiero po potwierdzeniu, że są nieaktualne. Sam brak egzekwowania zasady w kodzie nie dowodzi, że użytkownik ją wycofał. Sprzeczność z ręcznymi ustaleniami ujawnij zamiast po cichu je zastępować. Przepisuj dokument od zera tylko na wyraźne zlecenie lub gdy jest pusty; nie traktuj krótkiego pliku jako pustego szablonu.

Jeśli repo jest puste, wykorzystaj dostępny opis użytkownika i dokumenty produktu. Zapisz tylko znane fakty, bez wymyślonych komend i folderów. Gdy brak nawet celu projektu, zapytaj o krótki opis przed tworzeniem treści.

## Kontrola przed i po zapisie

- Każde twierdzenie wynika ze sprawdzonego źródła albo jawnej decyzji użytkownika. Nie dopisuj ogólnych porad o jakości kodu.
- Celuj w 200–400 słów dla głównego pliku i 120–250 dla lokalnego. Nie dodawaj tekstu dla dolnego limitu ani nie usuwaj istotnych zasad dla górnego.
- Najważniejsze ograniczenia i częste polecenia są blisko początku. Pomijaj puste sekcje, poradniki frameworków i obszerne bloki kodu.
- Używaj względnych linków Markdown do istniejących plików zamiast kopiować dokumentację. Sprawdź linki względem katalogu docelowego. Nie twórz odnośnika z pliku do niego samego.
- Polecenia używają rzeczywistego package managera i istniejących skryptów; w monorepo podaj właściwy katalog lub filtr. Nie deklaruj zaliczenia niewykonanych kontroli.
- Przed zapisem upewnij się, że dokument nie zmienił się od odczytu; przy zmianie wczytaj go ponownie i zachowaj nowe ustalenia. Po zapisie sprawdź treść, odnośniki oraz diff, jeśli Git jest dostępny.

Edytuj tylko wskazany dokument. Nie modyfikuj kodu, konfiguracji, zagnieżdżonych instrukcji ani dokumentów Raven przy okazji. Zakończ ścieżką, liczbą słów oraz krótką informacją, co utworzono lub zmieniono i jakie dane pozostają niepotwierdzone. Skuteczność instrukcji można ocenić później na rzeczywistym zadaniu; walidacja dokumentu nie zastępuje takiej obserwacji.
