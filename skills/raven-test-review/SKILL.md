---
name: raven-test-review
description: "Niezależnie oceń konkretne testy lub ochronę before-change. Użyj przy osobnym zleceniu albo ryzyku; zwykłe review change obejmuje już testy."
---

# Raven Test Review

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [kontrakt źródeł i oceny testów](../raven-test/references/test-review.md). Świeży reviewer Astra/high dostaje wymagania, zakres, publiczne decyzje i dowody, bez transkryptu autora. Nie edytuje kodu ani testów.

Sprawdź zachowanie chronione testem, niezależne Expected, zdolność wykrycia regresji, izolację/cleanup i adekwatność mocków. Zapisz `test-review.md` z fingerprintem, ocenianym drzewem, poleceniami, finding IDs i ograniczeniami. Raport nie jest testem ani zgodą na merge. W zleconym cyklu napraw potwierdzone defekty wracają do autora bez nowej rutynowej zgody, z limitem dwóch nieskutecznych prób. Nowy zakres wymaga decyzji.

Zakończenie zwykłego raven-test nie uruchamia tego skilla automatycznie. Wykorzystaj aktualne review implementacji i QA zgodnie z wpływem zmian; osobna ocena wymaga zlecenia albo nazwanego nierozstrzygniętego ryzyka. Nie wymuszaj zmian w wystarczających testach dla wykazania aktywności.

Instrukcja ręczna jest wyłącznie w końcowej wiadomości czatu implementatora. Nie wymagaj acceptance.md ani nie twórz/aktualizuj go; nie kopiuj kroków odbioru do artefaktów. Historyczne pliki i pola zachowaj. Oceniaj rzeczywiste dowody i feedback, bez domniemanego odbioru.
