# Dodatkowy tester wymagań

Uruchamiaj, gdy wskazane ryzyko albo zlecenie wymaga niezależnego przebiegu poza normalnym review change. Nie jest obowiązkowym poprzednikiem review kodu.

Świeży tester Astra/high otrzymuje pełne wymagania i wersje, kryteria, publiczne decyzje, URL/środowisko, zakres/base/head oraz dowody. Nie dostaje transkryptu implementatora. Dla UI stosuje [raven-browser](../../raven-browser/SKILL.md), własną sesję i dane testowe. Nie poprawia produktu ani testów.

Macierz obejmuje każde kryterium w zleconym zakresie: źródło, warunki, kroki, Expected, Actual, wynik i dowód. Sprawdź happy path, istotne błędy/granice oraz uprawnienia, gdy dotyczą funkcji. Kryteria poza UI badaj odpowiednią kontrolą; brak UI nie zwalnia z wymagań. Wersja wdrożenia wymaga potwierdzenia, lokalny HEAD jej nie dowodzi.

Zapisz `qa-report.md` obok planu, z base/head/buildem, fingerprintem, kontami/rolami bez sekretów, reprodukcjami B1/B2 i ograniczeniami. PASS oznacza wykonany oczekiwany wynik, nie samo pokrycie scenariuszy. BLOCKED/NOT VERIFIED nie są PASS. Nie zastępuj trwałych testów samym browser smoke.

W auto potwierdzone defekty w zakresie wracają do implementatora; tester ponawia zależne scenariusze po poprawce. Po dwóch nieskutecznych próbach tego samego problemu zatrzymaj pętlę. Zapisuj licznik w checkpointcie; kolejny agent nie zeruje historii. W samodzielnym QA bez zlecenia napraw oddaj raport.
