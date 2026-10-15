---
name: raven-pilot-init
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Przygotuj ustalony stack Raven dla pilota przez raven-init-stack albo zweryfikuj istniejący szkielet. Bez wyboru stacku, konfiguracji testów i implementowania produktu."
---

# Raven Pilot Init

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

Ten skill stanowi wejście do istniejącego `$raven-init-stack`, nie kopię jego generatora.

1. Sprawdź instrukcje repozytorium, manifesty i istniejący kod. Jeśli aplikacja już istnieje, nie uruchamiaj generatora; sprawdź stan integracji i zanotuj potrzebne działania w `context/pilot/setup.md`.
2. Dla nowego projektu znajdź i przeczytaj zainstalowany `raven-init-stack/SKILL.md`. Postępuj według jego instrukcji, zachowując `context/`, `archive/`, `.git/`, instrukcje i pliki użytkownika. Jeśli skilla brakuje, zgłoś konkretną brakującą zależność, bez zastępowania stacku własnym starterem.
3. Użyj podanej nazwy produktu; pytaj tylko jeśli jest potrzebna i nie wynika ze źródeł. Stack domyślny Raven: TypeScript, Next.js, Hono, tRPC, Better Auth, PostgreSQL, Drizzle, Bun, Turborepo. Istniejący projekt i jawne wybory użytkownika mają pierwszeństwo.
4. Sprawdź kontrolę typów, kompilację i dostępność konfiguracji integracji stosownie do etapu. Brak połączenia z bazą lub działającego auth zapisuj jako brak, nie sukces.
5. Nie twórz testów, konfiguracji testowych ani E2E. Szkielet nie jest zaakceptowanym flow produktu. Nie wdrażaj aplikacji ani nie modyfikuj zdalnej bazy na podstawie samego init.

Zapisz w setup stan, polecenia uruchomienia, wyniki kontroli oraz brakujące dostępy bez sekretów. Techniczne przygotowanie jest zadaniem wspierającym pierwszy chunk, a nie osobną wartością biznesową w roadmapie.
