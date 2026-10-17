---
name: raven-domain-distillation
description: Porównaj język dokumentów z modelem istniejącego kodu przez niezależne analizy. Zapisz słownik i rozbieżności domenowe w repo; użyj przed modernizacją niejasnych granic domeny.
---

# Raven Domain Distillation

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

Analiza modernizacji istniejącego systemu: destylacja języka i rozjazdów model–kod, inspirowana DDD. Nie jest pełnym procesem DDD ani automatycznym projektowaniem agregatów, mikroserwisów lub migracji.

Przeczytaj [kontrakt raportów brownfield](../raven-repo-map/references/github-brownfield.md). Ustal obszar produktu, repo kodu, dokumenty źródłowe i docelowy raport: folder change dla lokalnego badania albo context/foundation/domain.md i glossary.md dla analizy projektu. Zapisz HEAD, wersje dokumentów i zakres. Mapę repo wykorzystaj do wyboru plików, nie jako dowód znaczenia biznesowego.

## Niezależne rozpoznanie

1. Przygotuj trzy świeże zadania bez odziedziczonej historii rozmowy. Agent dokumentów otrzymuje wymagania, dokumenty i wypowiedzi domenowe; wyodrębnia pojęcia, reguły, procesy i konteksty z referencjami. Dwaj agenci kodu otrzymują zakres repo, HEAD i instrukcje techniczne, ale nie słownik ani wyniki dokumentów. Jeden śledzi modele/persistencję, drugi zachowanie/przepływy; obaj samodzielnie opisują język i reguły widoczne w kodzie.
2. Każdy agent zwraca odczytowy raport z dowodami i niepewnościami. Nie przekazuj wyników między agentami przed zakończeniem niezależnych analiz. Przy braku trzech slotów uruchom świeże zadania kolejno; przy braku delegacji zgłoś brak niezależności i przedstaw jedynie analizę wstępną.
3. Dopiero potem zestaw dokumenty i oba raporty kodu. Zweryfikuj wskazania w źródłach: synonimy, jeden termin o różnych znaczeniach, brakujące pojęcia, ukryte reguły i rozjazdy cyklu życia. Dokument też może być nieaktualny; kod nie jest automatycznie prawdą biznesową. Bez dokumentów nie deklaruj zgodności modelu z wymaganiami.
4. Nadaj rozbieżnościom stabilne ID D1, D2…; przy kolejnej rundzie zachowaj tożsamość problemów. Dla każdej podaj źródła obu stron, skutek, pewność i pytanie lub możliwy następny krok. Granice kontekstów i inwarianty oznacz jako zaobserwowane albo hipotezy do potwierdzenia przez człowieka. Wiedza modelu o branży nie zastępuje eksperta projektu.
5. Zapisz raport domain.md oraz krótki słownik glossary.md w tej samej rundzie, z wzajemnymi linkami. Słownik: termin, znaczenie w kontekście, aliasy w kodzie/dokumentach, status potwierdzenia i referencje. Raport: zakres/źródła, metoda niezależności, procesy i granice, tabela D, niewiadome i priorytety według wpływu. Przy odświeżeniu pokaż zmiany i rozstrzygnięcia, zachowaj poprzednią wersję.

Tylko koordynator utrwala syntezę; publikacja zewnętrzna wynika z polityki. Nie zmieniaj kodu, nazw, AGENTS.md ani wymagań. Możesz wskazać słownik do późniejszego podlinkowania z instrukcji. Wydzielanie agregatów, ACL czy strangler fig wymaga osobnego planu i nie jest obowiązkowym wynikiem analizy. Zakończ linkami i pytaniami potrzebnymi do dalszych decyzji.
