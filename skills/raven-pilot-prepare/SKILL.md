---
name: raven-pilot-prepare
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Automatycznie wybierz następny chunk roadmapy Raven Pilot i dopracuj go z użytkownikiem i przygotuj kompletną paczkę autonomicznej realizacji. Uzgadniaj z użytkownikiem produkt i decyzje architektoniczne przed implementacją; samodzielnie rozstrzygaj szczegóły wykonawcze."
---

# Raven Pilot Prepare

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

## Wymagany model autora

Ten etap prowadzi **`gpt-6-astra` z effortem `high`** zgodnie z sekcją „Autorzy artefaktów produktowych” kontraktu. Jeśli bieżący model/effort nie są wiarygodnie potwierdzone jako zgodne, uruchom osobnego autora Astra high i przekazuj mu odpowiedzi użytkownika. To jawne zlecenie delegacji; nie wykonuj tego etapu na domyślnym modelu implementacyjnym. Autor już uruchomiony z właściwą konfiguracją realizuje skill bez ponownego delegowania tej samej roli.

Wejście: opcjonalne ID chunka lub opis rezultatu. Bez argumentu automatycznie wybierz następny chunk według kolejki w roadmapie i reguł synchronizacji kontraktu; nie pytaj użytkownika o ID, które da się ustalić z artefaktów. Wynik: `context/pilot/chunks/<id-slug>/plan.md` i `state.json`, zgodnie z kontraktem. To główna sesja pracy użytkownika z AI przed oddaniem paczki.

## Decyzje architektoniczne należą do użytkownika

Użytkownik pełni rolę solutions architect. Podczas dogadywania zakresu chunka ujawnij i uzgodnij decyzje wpływające na architekturę, nawet jeśli są odwracalne lub dotyczą pilota. Obejmuje to wybór usług/dostawców, miejsce przechowywania plików i danych, granice usług, komunikację realtime, kolejki i zadania w tle, integracje, hosting oraz istotne kompromisy kosztów, bezpieczeństwa i utrzymania. Nie odkładaj tych wyborów do planowania technicznego przez implementatora.

Dla rzeczywistego wyboru przedstaw krótką rekomendację, sensowne alternatywy i ich konsekwencje dla tego chunka. Przykład: przechowywanie plików w bazie zamiast object storage R2/S3 wymaga decyzji użytkownika; „prościej na MVP” nie jest zgodą. Nie wybieraj automatycznie dostawcy na podstawie tego przykładu.

Zapisuj w planie lub decisions.md: decyzję, uzasadnienie/kompromisy, status (proponowana/uzgodniona), źródło i datę odpowiedzi użytkownika oraz granice swobody implementatora. Wcześniej uzgodnione decyzje wykorzystuj bez ponownego pytania, jeśli nadal pasują; sam istniejący kod lub propozycja agenta nie dowodzi akceptacji. Nowa istotna decyzja bez odpowiedzi pozostawia paczkę w draft.

Nazwy funkcji, organizacja plików, użycie ustalonych bibliotek i inne szczegóły wykonawcze w uzgodnionej architekturze pozostają autonomiczne. Gdy w implementacji ujawni się potrzeba nowej lub zmienionej decyzji architektonicznej, implementator wraca do użytkownika z konkretnym wyborem zamiast stosować cichy zamiennik.

1. Przeczytaj PRD, roadmapę, zależności, instrukcje repozytorium i odpowiedni kod. Najpierw uzgodnij statusy roadmapy z artefaktami i dowodami, potem zastosuj deterministyczny wybór opisany w kontrakcie. Krótko ogłoś wybrane ID i powód, bez pytania o potwierdzenie. Jawne ID użytkownika ma pierwszeństwo, ale nie omija zależności ani ochrony archiwum. Istniejący plan wznawiaj, nie nadpisuj postępu.
2. Wyprowadź znane odpowiedzi ze źródeł. Przeanalizuj scenariusz główny, role, widoczność danych, błędy, puste stany i powrót do przerwanej czynności, tylko w zakresie tego flow.
3. Pytaj o materialne niedopowiedzenia lub sprzeczności. Nie pytaj o liczbę pytań, ponowny wybór uzgodnionego frameworka, oczywiste konwencje ani zatwierdzenie szczegółów wykonawczych. Nowe decyzje architektoniczne uzgodnij według zasad powyżej. Przedstaw konsekwencje rzeczywistych alternatyw. Grupuj powiązane decyzje w krótkie rundy. Dopóki odpowiedź jest istotnie potrzebna, zapisz draft zamiast zgadywać.
4. Zapisz szczegółowy plan chunka: uzgodnione zachowanie A–Z, kryteria `AC-01`, istotne przypadki negatywne, ograniczenia i wyłączenia, dane/uprawnienia, decyzje i założenia oraz zależny graf zadań `T-01`. Każde zadanie ma cel, wejście, zależności, obszar kodu, powiązane AC, wynik i sposób bezpośredniej weryfikacji. Nie dodawaj zadań pisania testów ani konfiguracji testowej.
5. Rozdziel plan kontraktowy od przyszłych planów technicznych `tasks/T-xx/plan.md`. Implementator lub opcjonalny planista może doprecyzować sposób realizacji, ale nie zmienia celu, AC, granic produktu ani uzgodnionej architektury.
6. Przygotuj runbook: start aplikacji, potrzebne usługi/zmienne (nazwy, bez wartości sekretów), sposób kontroli typów/builda, scenariusze weryfikacji oraz znane potrzeby uprawnień. Ustal granice działań zewnętrznych i modele; użyj domyślnych ustawień kontraktu bez osobnego pytania o każdą wartość. Nie wprowadzaj limitu czasu implementacji ani zastępczego budżetu tokenów. Zadania wymagające nieuzyskanej zgody zaznacz jako blokowane; rzeczywista blokada wykonania wymaga zatrzymania i konkretnego inputu użytkownika.
7. Sprawdź gotowość: brak materialnych nierozstrzygniętych decyzji produktowych i architektonicznych dla objętej paczki, osiągalne zależności, weryfikowalne AC, brak cykli, dostępne narzędzia i środowisko lub jawne zadania przygotowawcze możliwe bez udziału człowieka. Brak prawdziwych danych produkcyjnych nie blokuje pracy na bezpiecznych danych lokalnych, jeśli to wystarcza do AC.
8. Ustaw `ready` tylko gdy paczka spełnia te warunki; w przeciwnym razie `draft` z konkretnym brakiem. Przedstaw paczkę i komendę `$raven-pilot-implement <id>` bez kolejnej ceremonialnej akceptacji planu. Zlecenie implementacji jest autoryzacją pracy w zapisanym zakresie. Jeśli użytkownik już zlecił przygotowanie i realizację, kontynuuj automatycznie po spełnieniu gotowości.

Utworzenie draftu od razu odzwierciedl jako `preparing` / `draft`; ukończenie paczki jako `ready` / `ready`. Aktualizuj również wyliczoną kolejkę. Synchronizuj według protokołu z kontraktu; sam raport w czacie nie zastępuje zapisanych artefaktów.
