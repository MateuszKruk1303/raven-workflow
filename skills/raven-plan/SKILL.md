---
name: raven-plan
description: Przygotuj lub popraw plan change w GitHubie interaktywnie i bez automatycznego plan-review. Manualny etap workflow Raven; dla połączonego planowania i review użyj raven-auto-plan.
---

# Raven Plan

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [plan](references/procedures/plan/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Wykonaj lokalną procedurę planowania z [manualnym adapterem GitHub](references/manual-github.md). Zachowaj analizę kodu, skalowanie i budżet pytań, wywiad, akceptację struktury, szablony, fazy, Intent + Contract, Progress oraz zapis/wznawianie planu. Nie zastępuj ich procedurą raven-auto-plan.

## Wejście i tożsamość

Przyjmij change z GH i przeczytaj wymagania, taski, komentarze, research, decyzje i lokalne lessons. Issue z roadmapy jest już tożsamością zmiany — nie wymagaj osobnego new ani lokalnego change.md. Przy jawnym zleceniu nowej zmiany zapewnij jej tożsamość w GH zgodnie z raven-roadmap, po sprawdzeniu duplikatów. Nie uruchamiaj całej roadmapy od nowa. Nie twórz kopii istniejącego ticketa.

Odtwórz adapter Raven i wykonaj procedurę. Zwykłe czytanie kodu pozostaje analizą planistyczną; osobny raven-research wymaga decyzji użytkownika. Tryb save zapisuje już uzgodniony plan, nie restartuje wywiadu.

## Publikacja i zakończenie

Opublikuj pełną część przekrojową i brief w rodzicu, fazy jako kontrakty sub-issues z Progress i zależnościami. Zachowaj ID oraz rozpoczętą pracę. Po spójnym odczycie publikuj kompletny snapshot vN z fingerprintem. Zachowaj rozróżnienie bramek implementacji, manualnego odbioru i późniejszych testów/checków przed merge.

Zakończ na planie: pokaż zwięzły zakres, decyzje, wersję, link i stan publikacji. Nie uruchamiaj raven-plan-review ani implementacji automatycznie. Plan pozostaje do osobnego review; nie ustawiaj Ready na podstawie samego zapisu. Zlecone poprawki planu publikują nową wersję bez automatycznego review. Historyczna akceptacja nie obejmuje nowej wersji.

## Osobny obowiązkowy etap trwałych testów

Po oddaniu implementacji i sprawdzeniu użytkownika, przed PR, workflow wymaga raven-test. Plan wydziela odpowiednie fazy unit/integration/E2E dla tego etapu. Implementacja wykonuje swoje bieżące bramki, lecz nie realizuje odroczonych faz trwałych testów i nie uruchamia raven-test automatycznie. W handoffie wskaż go jako wymagany następny etap przed publikacją PR.

Etap trwałych testów ma dwa warianty: raven-test → osobno raven-test-review (manual) albo raven-auto-test (pisanie, uruchomienie, niezależne review i poprawki wad testów w jednym cyklu). Oba używają tego samego change i źródeł; wybór należy do użytkownika. Samo ukończenie manualnego raven-test nie oznacza ukończenia review testów.
