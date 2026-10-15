---
name: raven-pilot-prd
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Zapisz lub uaktualnij PRD pilota z wizji i notatek w workflow Raven Pilot. Zdefiniuj wymagania oraz kryteria pilot ready bez wyboru stacku i planowania implementacji."
---

# Raven Pilot Prd

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

## Wymagany model autora

Ten etap prowadzi **`gpt-6-astra` z effortem `high`** zgodnie z sekcją „Autorzy artefaktów produktowych” kontraktu. Jeśli bieżący model/effort nie są wiarygodnie potwierdzone jako zgodne, uruchom osobnego autora Astra high i przekazuj mu odpowiedzi użytkownika. To jawne zlecenie delegacji; nie wykonuj tego etapu na domyślnym modelu implementacyjnym. Autor już uruchomiony z właściwą konfiguracją realizuje skill bez ponownego delegowania tej samej roli.

Wynik: `context/pilot/prd.md`. Wejście: notatki shape, opis użytkownika lub istniejące PRD. Nie wymagaj osobnej sesji shape, jeśli wejście jest wystarczające.

Przeczytaj źródła i utwórz zwięzły, kompletny dokument:

1. Cel pilota, odbiorcy i problem.
2. Hipoteza wartości oraz sposób walidacji z rzeczywistymi użytkownikami: kanał dotarcia, obserwacja wyniku, ustalony próg lub jawna niewiadoma.
3. Zakres pilota i wyłączenia; odróżnij od przyszłej wizji.
4. Podróże użytkownika od wejścia do osiągnięcia wartości.
5. Wymagania funkcjonalne z trwałymi ID `FR-001`, priorytetem pilot/later, źródłem i obserwowalnymi kryteriami akceptacji. Nie zmieniaj ID przy edycjach.
6. Istotne reguły biznesowe, role/uprawnienia, dane i stany błędów.
7. Proporcjonalne wymagania pozafunkcjonalne: użyteczność, ochrona rzeczywistych danych, niezawodność kluczowego przepływu. Nie dodawaj skali tysięcy użytkowników bez potrzeby.
8. Akceptowane uproszczenia i operacje ręczne.
9. Kryteria `pilot ready`: dostępny produkt, działające krytyczne przepływy, sposób zebrania feedbacku oraz minimum operacyjne adekwatne do danych i sposobu wdrożenia. To kryteria, nie zgoda na publikację.
10. Decyzje, założenia, otwarte pytania i źródła.

Zastosuj politykę pytań. Nie wymyślaj zatwierdzenia produktu ani metryk. Przy niepełnym wejściu zapisz użyteczny draft z konkretnymi blokadami; nie oznaczaj go jako gotowy, jeśli brakuje celu lub krytycznych zasad.

Przy aktualizacji zachowaj uzgodnione wymagania, odnotuj wpływ na roadmapę i aktywne chunki. Nie edytuj archiwów. Zarekomenduj `$raven-pilot-roadmap`; inicjalizacja stacku jest niezależnym przygotowaniem, nie bramką PRD.
