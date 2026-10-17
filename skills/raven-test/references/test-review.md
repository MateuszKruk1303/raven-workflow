# Źródła i ocena testów

Autor i niezależny reviewer otrzymują ten sam kontrakt/fingerprint, wersje źródeł wymagań, base/head/tree i publiczne decyzje. Zapisz to w raportach; nie twórz osobnego manifestu tylko dla metadanych. Reviewer nie dziedziczy transkryptu autora i nie poprawia ocenianych testów.

Expected pochodzi z wymagań lub świadomie chronionego zachowania before-change. Prześledź AC/ryzyko → test → asercję → wynik. Oceniaj realne negatywne ścieżki, granice, izolację danych, cleanup, kontrolę czasu i adekwatność mocków. Test porównujący implementację z jej kopią nie stanowi niezależnej ochrony. Sprawdź istotną regresję przez rzeczywisty błąd lub kontrolowaną perturbację, gdy to rozstrzyga niepewność; zawsze przywróć kod przed commitem.

Dowód istniejącego uruchomienia można wykorzystać przy zgodnym drzewie, konfiguracji, zależnościach i środowisku. Reviewer wykonuje kontrole rozstrzygające jego obawy; nie powtarza całej suite bez przyczyny. Niewykonanie to NOT VERIFIED/BLOCKED. EXPECTED_RED before-change nie jest zielonym wynikiem gotowego produktu.

Normalne review implementacji obejmuje ten wymiar razem z wymaganiami i kodem. Oddzielne test-review służy osobnym zleceniom/ryzyku; nie tworzy obowiązkowego drugiego review każdego change.
