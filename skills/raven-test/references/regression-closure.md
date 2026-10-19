# Audyt i domknięcie regresji

Wejściem są rzeczywiste wymagania i ich wersja, aktualny diff, checkpoint implementacji/kontroli, review, ewentualne raporty/scenariusze QA, rzeczywisty feedback ręczny ze źródłem; historyczna instrukcja odbioru nie jest wymaganym wejściem. Odtwórz istniejącą ochronę zamiast uruchamiać proces testowania od początku.

Dla każdego AC i istotnego ryzyka zapisz zwięźle: ścieżka testu i konkretna asercja, warstwa, polecenie, wynik i sprawdzona wersja/config/środowisko, pokrywający scenariusz QA, finding/feedback oraz nazwana luka. Linkuj raporty, nie kopiuj ich do planu ani issue. Test implementacji i QA mogą wystarczyć jako dowód działania; jednorazowy QA nie jest automatycznie trwałą ochroną regresji.

Oceń lukę przed edycją: brak asercji istotnego skutku, niechroniona granica, nieizolowane dane, niesprawdzona ścieżka awarii lub regresja ujawniona ręcznie. Każdy dodany/zmieniony test musi zamykać nazwaną lukę; nie przepisuj poprawnego testu ani nie dodawaj kopii E2E do istniejącego skutecznego integration bez uzasadnienia. Nie utrwalaj całego tymczasowego QA. Wybierz stabilne scenariusze o realnej wartości regresyjnej i przenieś je do konwencji runnera/fixtures projektu z izolacją i cleanup.

Reuse dotyczy dowodu, nie wywołania skilla: porównaj jego zależności kod/config/deps/env z deltą. Zapisz podstawę zachowania niedotkniętych wyników i ponów tylko dotknięte lub niepewne kontrole. Zaginiony sandbox QA nie kasuje historycznej obserwacji, lecz nie jest środowiskiem do powtórki; odtwórz potrzebne dane ze źródeł projektu lub rzeczywistego feedbacku. Jeżeli obecnej wiarygodności nie da się ustalić, oznacz dowód do ponowienia.

Wynik ma rozróżniać `completed` (audyt i potrzebna praca zakończone), `sufficient` (ochrona wystarcza dla zakresu), `gaps` (pozostałe braki), `evidence` (rzeczywiste kontrole i reuse). Samo zakończenie z jawnymi brakami nie daje PASS. Brak zmian testów uzasadnij konkretną mapą wymagań i istniejącej ochrony, a nie ogólnym „już są testy”. Nie trzeba odpalać pustego etapu ani tworzyć nowego raportu, jeżeli wcześniejsze dowody już obejmują te czynności: zapisz rzetelne mapowanie i źródła.

Nowe testy nie wymagają z automatu drugiego pełnego review czy osobnej sesji QA. Potrzebę aktualizacji review/QA wyprowadź ze zmiany produktu lub konkretnego ryzyka testów. Zachowaj jawne odrębne zlecenia QA i bramki projektu/kontraktu; historyczne qa_required lub tryb auto same nie przywracają obowiązku QA. Nie oznaczaj rzeczywiście wymaganej kontroli jako spełnionej samym audytem.
