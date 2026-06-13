---
name: icp
version: 1.0.0
description: >
  Zentrale ICP-Referenz der Agentur. 3 Modi:
  (1) BEWERTEN — Content, Ads, Namen, Copy gegen das ICP prüfen inkl. simulierter ICP-Reaktion.
  (2) PERSONA — Konkrete fiktive ICP-Instanzen mit Psychogramm und Tagesablauf generieren.
  (3) QUALIFIZIEREN — Leads/Profile schnell gegen das ICP checken.
  Triggern bei: "passt das zu meinem ICP", "bewerte das", "ICP-Check", "würde mein ICP das kaufen",
  "wie reagiert mein ICP", "trifft das den Nerv", "generier mir eine Persona", "konkreter ICP",
  "passt dieser Lead", "ist das ein guter Lead", "check den Kontakt", "simuliere die Reaktion",
  "was denkt mein ICP dazu", "pitch dem ICP", "spricht das meine Zielgruppe an", "ICP einrichten".
  Andere Skills sollen diesen Skill als zentrale ICP-Referenz nutzen.
---

# ICP — Dein idealer Kunde als System

Dieser Skill ist die Single Source of Truth für das ICP deiner Agentur. Die Daten leben in **deinem** Agency OS, der Skill liefert die Methodik.

**Datenquelle:** `01-context/zielgruppe.md`

## Pre-flight Check

1. Lies `01-context/zielgruppe.md`.
2. **Existiert nicht oder enthält kein vollständiges Profil** (fehlende Abschnitte: Kernproblem, emotionale Spannungen, Sprache, Qualifizierungs-Kriterien): Setup anbieten — *"Dein ICP-Profil ist noch nicht vollständig. 10 Minuten Interview, dann steht es. Jetzt machen?"* → bei Ja dem ICP-Setup des Onboardings folgen (`agency-os-onboarding/references/icp-setup.md`), das `01-context/zielgruppe.md` schreibt. Dieser Skill macht kein eigenes Setup.
3. **Existiert vollständig:** direkt in den passenden Modus.

---

## 3 Modi

Der Modus ergibt sich automatisch aus der Anfrage.

### Modus 1: Bewerten

Analytische Bewertung auf 5 Dimensionen + simulierte ICP-Reaktion als innerer Monolog + konkreter Verbesserungsvorschlag. Funktioniert für Content-Ideen, Angebotstexte, Ads, Offer-Namen, Framework-Namen, Landing Pages, Lead Magnets, Hooks, CTAs, Newsletter-Themen.

**Triggert bei:** "bewerte das", "passt das", "wie reagiert mein ICP", "trifft das den Nerv", "kommt das an"

→ Lies `references/modus-bewerten.md`.

### Modus 2: Persona generieren

Erzeugt konkrete, fiktive ICP-Instanzen mit Name, Stadt, Firmen-Typ, Psychogramm, Tagesablauf, aktueller Krise und Trigger-Situation. Die Persona kann danach als Gesprächspartner genutzt werden (Pitch durchspielen, Angebot testen, Sales-Gespräch üben).

**Triggert bei:** "generier mir eine Persona", "konkreter ICP", "erstell mir einen Avatar", "gib mir ein Beispiel-Profil"

→ Lies `references/modus-persona.md`.

### Modus 3: Qualifizieren

Schneller Check ob eine reale Person ins ICP fällt. Input: LinkedIn-Profil, Name+Firma, Screenshot, oder kurze Beschreibung. Output: Passt / Passt nicht / Grenzfall mit Begründung.

**Triggert bei:** "passt dieser Lead", "fällt der in meinen ICP", "check den Kontakt", "ist das ein guter Lead"

→ Lies `references/modus-qualifizieren.md`.

---

## Nutzung durch andere Skills

Dieser Skill ist die zentrale ICP-Referenz. Andere Skills (z.B. weekly-goldmine, carousel, brand-voice-Anwendungen) verweisen auf `01-context/zielgruppe.md` statt eigene ICP-Daten zu pflegen. Modus 1 kann von jedem Skill genutzt werden, um Outputs zu prüfen.

## No-Gos

- Generische Business-Weisheiten ohne Bezug zum dokumentierten ICP
- Bewertungen aus dem Bauch, wenn das Profil etwas anderes sagt — das Profil ist die Quelle
- Profil-Lücken stillschweigend mit Annahmen füllen — Lücke benennen, nachfragen, Profil ergänzen
