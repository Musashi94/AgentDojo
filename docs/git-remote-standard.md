# Git Remote Standard (verbindlich)

Für alle v0.x-Umsetzungen gilt verpflichtend:

- `origin` muss auf `Musashi94/AgentDojo` zeigen.
- Abschluss ist blockiert, wenn `origin` fehlt oder auf ein anderes Repo zeigt.

## Erlaubte URL-Formen

- `https://github.com/Musashi94/AgentDojo.git`
- `https://github.com/Musashi94/AgentDojo`
- `git@github.com:Musashi94/AgentDojo.git`

## Automatische Prüfung

- Lokal/CI über `scripts/check-git-remote.ps1`
- v0.x-Guard aktiv; bei Abweichung harter Fehler (No-Go).
