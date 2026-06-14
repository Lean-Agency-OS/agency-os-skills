# Modus 3: Qualifizieren

Schneller Check, ob eine reale Person ins ICP fällt. Input kann sein: LinkedIn-Profil-URL, Name + Firma, Screenshot, Copy-Paste aus einem Profil, oder eine kurze Beschreibung.

Grundlage: die Tabelle **"Wer (harte Kriterien)"** und die **weichen Signale** aus `{context}/brands/{brand}/icp.md`.

---

## Bewertungs-Reihenfolge

### 1. Harte Kriterien (KO)

Prüfe Branche, Rolle, Größe, Region gegen die Profil-Tabelle. **Ein einziges nicht erfülltes hartes Kriterium reicht für "Passt nicht".**

### 2. Weiche Signale (Scoring)

Positive und negative Signale aus dem Profil durchgehen. Zusätzlich generisch prüfbar:

- **Positiv:** Rolle mit Entscheidungsmacht im Titel; beschreibt, was die Firma FÜR KUNDEN tut; Aktivität zu Themen, die das Kernproblem berühren
- **Negativ:** Angestellten-Titel ohne Entscheidungsmacht; Solo ohne Team-Signale, wo das Profil ein Team verlangt; Größenordnung klar außerhalb; mehrere simultane Positionen

### 3. Anti-Persona-Check

Auch wenn alles passt: gleicht die Person der dokumentierten Anti-Persona? Dann Grenzfall mit Begründung.

---

## Output-Format

```
**[Name / Firma]: [PASST / PASST NICHT / GRENZFALL]**

- Harte Kriterien: [je Kriterium ✓/✗ in einer Zeile]
- Weiche Signale: [die 2-3 ausschlaggebenden]
- [Bei Grenzfall: was fehlt zur Klärung — konkrete nächste Info]
```

Bei "Passt": einen Satz dazu, welcher Aufhänger (Kernproblem/Spannung aus dem Profil) für die Ansprache am vielversprechendsten ist.

## Regeln

- Nur verifizierbare Information nutzen. Aus einem Titel nicht die Teamgröße erfinden — als offen markieren.
- Bei Screenshot/Copy-Paste: nichts dazuinterpretieren, was nicht dasteht.
- Grenzfälle sind ein legitimes Ergebnis — besser als falsche Sicherheit.
