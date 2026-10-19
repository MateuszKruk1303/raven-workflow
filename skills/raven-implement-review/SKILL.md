---
name: raven-implement-review
description: "Niezależne review zmiany: zgodność z wymaganiami, poprawność kodu i skuteczność testów. Read-only; wynik w czacie."
---

# Raven Implement Review

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md).

Review wykonuje świeży agent bez transkryptu autora. Gdy wywołanie nastąpiło w sesji, w której powstała zmiana, uruchom review w świeżym subagencie hosta i przekaż mu tylko wejście poniżej; bez takiej możliwości wykonaj review sam i zgłoś w wyniku brak niezależności. Nie edytuje produktu ani testów. Respektuj `context/foundation/lessons.md`, jeśli istnieje.

## Wejście

Issue lub polecenie, plan (jeśli jest), branch lub PR. Ustal rzeczywisty zakres diffu: baza, head, niezacommitowane zmiany. Zakres może dotyczyć całego change albo tylko wskazanych testów.

## Ocena

1. **Wymagania.** Każde AC ma pokrycie w kodzie i dowód (test, sprawdzenie). Brak dowodu oznacz NOT VERIFIED.
2. **Poprawność.** Reguły, ścieżki błędów, przypadki brzegowe, wyścigi. Prześledź krytyczne ścieżki od wejścia do skutku.
3. **Architektura.** Zgodność z istniejącymi wzorcami i granicami modułów.
4. **Bezpieczeństwo i dane.** Uprawnienia, walidacja wejścia, utrata lub nadpisanie danych.
5. **Testy.** Czy wykryją regresję: niezależne Expected (nie przepisane z implementacji), sensowne asercje, izolacja i cleanup, adekwatne mocki. Testy autora są dowodem, nie wyrocznią.

Uruchom kontrolę, która rozstrzyga wątpliwość. Nie zgłaszaj stylistyki ani hipotetycznych problemów spoza zakresu jako blokady.

## Wynik

W czacie: zakres (baza..head), uruchomione kontrole z wynikiem, uwagi z ważnością (critical/warning/suggestion), miejscem `plik:linia`, scenariuszem i rekomendacją, oraz werdykt. Plik raportu tylko na prośbę użytkownika. Review nie jest odbiorem ani zgodą na merge.
