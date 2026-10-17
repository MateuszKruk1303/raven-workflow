---
name: raven-auto-implement
description: "Zrealizuj zatwierdzony lokalny change wraz z testami, przeprowadź jedno niezależne review wymagań, kodu i testów oraz ograniczoną pętlę napraw w uzgodnionym zakresie."
---

# Raven Auto Implement

Przed zależną implementacją sprawdź również aktualne niezależne `plan-review.md` dla bieżącego fingerprintu i rozstrzygnięcie blokujących findings. Sama akceptacja planu nie zastępuje zachowanego etapu review; brak lub nieaktualne review kieruje do raven-plan-review/auto-plan. Nie wymagaj nowego review dla samych checkboxów lub checkpointu.

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Koordynuj świeżego implementatora Sol/low oraz świeżego reviewera Astra/high. Używaj [procedury implementacji](../raven-implement/references/procedures/implement/procedure.md) i [review](../raven-implement-review/references/procedures/impl-review/procedure.md). Agent roli nie uruchamia ponownie koordynatora.

1. Odtwórz lokalny plan/checkpoint, akceptację fingerprintu, branch/base/HEAD oraz istotne wcześniejsze dowody. Zachowaj cudze zmiany. Nie czytaj pełnej historii issues. Brak planu lub zmieniony niezaakceptowany kontrakt wraca do planowania/akceptacji.
2. Implementator wykonuje pozostały zlecony zakres i odpowiednie trwałe testy, aktualizuje Progress oraz checkpoint. Nie zatrzymuj go na rutynowych fazach. Publikacja draftu/aktualizacja PR odbywa się wcześnie i w toku pracy, tylko według rzeczywistej polityki publikacji.
3. Po zatrzymaniu edycji przypnij oceniane drzewo/base/head. Uruchom **jedno** świeże niezależne review obejmujące wymagania, kod i testy. Reviewer dostaje pełny kontrakt, źródła, diff i dowody; nie transkrypt autora. Dodatkowy tester/QA/audyt wymaga nazwanego ryzyka lub zlecenia. Gdy potrzebny jest tester UI, zastosuj [browser-review](references/browser-review.md).
4. Potwierdzone błędy w zaakceptowanym zakresie wracają automatycznie do implementatora. Po poprawkach uruchom potrzebne kontrole i odśwież dotknięte review. Dwie nieskuteczne próby tego samego problemu kończą zależną pętlę; liczniki przechodzą między sesjami. Nie naprawiaj przez zmianę wymagań, wyłączanie testów ani pomijanie bramek.
5. Oddaj wynik użytkownikowi do odbioru: działanie, sposób sprawdzenia, kontrole, review, luki i stan PR/CI. Nie wymagaj kolejnego etapu pisania testów, jeśli zostały już wykonane z implementacją. Odbiór/merge mogą być jedną jawną decyzją użytkownika, lecz nie wynikają z planu ani PASS.

Wznowienie wykorzystuje checkpoint i istniejące dowody: nie powtarzaj gotowej implementacji ani review na niezmienionym drzewie. Błąd publikacji wymaga ponowienia tylko właściwego zapisu po readback, nie ponownej implementacji. Feedback o defekcie w zleconym zakresie podlega tej samej pętli; nowe wymagania zmieniają kontrakt i wymagają decyzji.
