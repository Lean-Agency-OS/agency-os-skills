---
name: brand-voice
version: 2.0.0
description: >
  Schreibt und prüft Texte in der dokumentierten Brand-Voice der Agentur.
  Die Voice-Daten leben im Agency OS unter 01-context/brand/voice-profile.md, der Skill
  liefert die Anwendungs-Methodik. Triggert bei jeder Anfrage nach Text in der
  eigenen Stimme: E-Mails, LinkedIn-Posts, Newsletter, Sales-Copy, WhatsApp-Antworten.
  Auch triggern bei: "schreib in meiner Voice", "klingt das nach mir",
  "schreib mir eine E-Mail in meiner Stimme", "beantworte das in meinem Stil",
  "mach daraus einen Post in meiner Voice", "prüf das auf meine Voice", "/brand-voice".

  Wenn das Voice-Profil noch nicht existiert: Skill verweist auf das Onboarding
  (agency-os-onboarding), das die Voice einrichtet. Dieser Skill macht kein eigenes Setup.
---

# Brand Voice Skill

Dieser Skill schreibt Texte in der dokumentierten Brand-Voice der Agentur. Die **Daten** leben im Agency OS (`01-context/brand/voice-profile.md`), der **Skill** liefert die Methodik.

**Datenquelle:** `01-context/brand/voice-profile.md`

Das Profil enthält Kernessenz/Säulen, Satzbau, Vokabular (Lieblings-Wörter, Tabu-Wörter, Anti-Phrasen), Formatierung, eine `## Anti-Patterns`-Sektion (universelle KI-Tells plus die dokumentierten Ausnahmen dieser Voice) und eine Qualitätsprüfungs-Checkliste.

---

## Schritt 1 — Voice-Profil-Check (IMMER ZUERST)

Vor jeder Antwort:

1. Lies `01-context/brand/voice-profile.md`.
2. **Existiert nicht** oder enthält noch unbearbeitete `{{Platzhalter}}` (Profil unvollständig):
   - Dem User kurz sagen: *"Deine Brand-Voice ist noch nicht (vollständig) eingerichtet. Das macht das Onboarding: sag 'einrichten' oder lass uns die Voice jetzt aufsetzen."* Das Voice-Setup läuft über **agency-os-onboarding** (`references/voice-setup.md`), nicht hier.
   - Solange kein Profil da ist: die ursprüngliche Frage in **neutraler Voice** beantworten und vermerken, dass ohne Profil nicht in der Brand-Voice geschrieben werden kann.
3. **Existiert vollständig:** weiter zu Schritt 2.

---

## Schritt 2 — Profil laden

Lies das Profil komplett. Halte besonders die `## Anti-Patterns`-Sektion bereit, sie ist der Negativfilter für Schritt 4.

---

## Schritt 3 — Text generieren

Halte dich an:
- Kernessenz und Säulen
- Satzbau-Rhythmus (Längen, Bruchmuster, Auffälligkeiten)
- Vokabular: Lieblings-Wörter/-Phrasen nutzen, Tabu-Wörter meiden
- Formatierung-Regeln (Pfeile, Bullets, Weißraum, Emoji-Default, Dash-Default)

---

## Schritt 4 — Anti-Slop-Check

Prüfe vor Ausgabe gegen die `## Anti-Patterns`-Sektion des Profils. Jedes dort gelistete Pattern strippen, **außer** es ist in der Stance-Spalte ausdrücklich als Ausnahme dieser Voice dokumentiert. Pflicht-Filter:

1. **Em-Dash und En-Dash entfernen** (— und –) mitten im Satz. Ersatz: Punkt, Doppelpunkt oder Komma.
2. **Pol-Setzungs-Slop entfernen** (Sondern-Brücke, Thema-Tausch, Echo-Pol, Pseudo-Reframe). Statt der Konstruktion: direkt sagen.
3. Keine generischen KI-Helper-Phrasen.
4. Keine Adjektiv-Cluster ohne Beleg.
5. Keine Stichpunkt-Aufzählungen ohne Verb. Vollsätze auch wenn kurz.
6. Bullet- und Emoji-Reflex unterdrücken, wenn das Profil Prosa fordert.

Wenn eine Stelle durchrutscht: streichen oder umschreiben.

---

## Schritt 5 — Qualitätsprüfung

Geh die Checkbox-Liste am Ende von `voice-profile.md` durch. Bei jedem Nein-Punkt: anpassen, erneut prüfen.

---

## Schritt 6 — Ausgabe

Liefere den finalen Text. Auf Wunsch eine 1-Satz-Begründung (welches Voice-Element wo) oder eine Alternativ-Variante.

---

## Profil nachschärfen

Kleine Korrekturen (neue Tabus, einzelne Mechaniken, Voice-Drift): direkt in `01-context/brand/voice-profile.md` eintragen, mit neuem Wartungsprotokoll-Eintrag. Das ist Mid-Course-Correction, kein Re-Setup.

Komplette Neu-Extraktion (neues Material, großer Re-Build): läuft über das Onboarding-Voice-Setup (`agency-os-onboarding/references/voice-setup.md`), das `01-context/brand/voice-profile.md` neu schreibt.

---

## Pflicht-Regeln

1. **Mechaniken vor Adjektiven.** Output folgt den dokumentierten Mechaniken, nicht generischer KI-Sprache.
2. **Kein Voice-Sound ohne Substanz.** Generische KI-Sauce raus.
3. **Format folgt Profil, nicht Standard-KI-Struktur.** Wenn das Profil "keine Bullet-Listen" sagt, dann auch wenn die Frage nach einer Aufzählung ruft.
4. **Kein eigenes Setup.** Bei fehlendem Profil auf das Onboarding verweisen, nicht selbst einrichten.
