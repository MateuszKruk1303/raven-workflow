---
name: raven-test-review
description: Niezależnie oceń testy change Raven na podstawie tych samych wersji wymagań i źródeł co ich autor. Świeży reviewer publikuje pragmatyczny raport w GitHubie; użytkownik decyduje o poprawkach.
---

# Raven Test Review

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Procedury do odczytu przez wykonawcę właściwej roli (E2E tylko gdy wybrano tę warstwę): [e2e](../raven-test/references/procedures/e2e/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż ścieżki procedur jego roli oraz kontrakt GH; koordynator nie musi ładować instrukcji wykonawczych innych ról. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Przeczytaj [kontrakt GH](../raven-auto-plan/references/github-contract.md) i [kontrakt źródeł i review testów](../raven-test/references/test-review.md). Ten skill jawnie wymaga delegowania oceny świeżemu agentowi bez historii autora testów i implementatora produktu. Manual oznacza osobne wywołanie i decyzję użytkownika, nie ocenę własnego kodu przez tego samego agenta.

Przyjmij change/Raven ID lub URL raportu do triage. Odczytaj test_sources z checkpointu, raport raven:test-report, wymagania, plan/taski, strategię i decyzje oraz Git. Zweryfikuj kompletność i aktualność źródeł według kontraktu. Zapisz oceniany SHA i ustal bazę etapu testów z checkpointu, nie z daty planu. Nie oceniaj ruchomego worktree. Gdy źródła starszego wykonania nie zostały zapisane, odtwórz je z dowodów GH/Git; nie udawaj pewności co do brakujących wersji.

Przekaż reviewerowi pełny pakiet surowych źródeł i diff, ścieżki wymaganych instrukcji raven-implement oraz dla E2E raven-test i jego reguł jakości. Reviewer stosuje wspólny pragmatyczny kontrakt. Koordynator publikuje jego raport w GH i przedstawia w czacie istotne ustalenia oraz ograniczenia. Nie wymaga wcześniejszego PASS wszystkich testów, aby ocenić wskazany zakres; nie zalicza jednak nieudanych lub niewykonanych kontroli.

Zakończ na raporcie i decyzji użytkownika. Nie uruchamiaj automatycznych poprawek ani kolejnej rundy review. Zapisz decyzje dotyczące T1/T2 osobno, z wersją i uzasadnieniem użytkownika. Jawne zlecenie poprawki wystarcza do przekazania wybranego zakresu autorowi przez raven-test; reviewer sam nie poprawia testów. Poprawki produktu kieruj do implementacji, a rozbieżności wymagań do uzgodnienia. Po zmianach nowe review wymaga zlecenia; poprzedniego PASS nie przenoś na nowy kod.

Wznowienie triage istniejącego raportu nie wymaga nowego audytu ani spawnowania reviewera. Dla nowej oceny uruchom świeżego reviewera, podając wcześniejsze uwagi i decyzje jako publiczne artefakty. Zachowaj ID i nie otwieraj zaakceptowanych ryzyk bez nowego dowodu. Nie twórz PR ani nie ustawiaj Done. Po zamknięciu tego etapu raven-pr pozostaje na osobne zlecenie.

Dla testów przed refaktorem lub reprodukcji bugfixu stosuj [before-change](../raven-test/references/before-change.md): oceniaj bazowy kontrakt i jakość testów niezależnie od oczekiwanego RED produktu.
