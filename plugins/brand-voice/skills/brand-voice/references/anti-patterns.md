# Anti-Patterns — universelle KI-Tells

> Negativfilter im Apply-Modus. Diese Patterns sind nicht stilistische Geschmackssache, sondern erkennbare KI-Footprints. Sie machen jeden Text austauschbar, egal wie gut das Voice-Profile sonst ist.
>
> **Wichtig:** Persönliche Tabu-Wörter und Stilpräferenzen gehören ins individuelle `voice-profile.md`, NICHT hierher. Diese Liste ist universell.

---

## 1. Dashes als KI-Footprint

Der größte KI-Tell überhaupt. ChatGPT, Claude und andere setzen Em-Dash und En-Dash exzessiv ein, oft als Ersatz für Komma, Doppelpunkt oder Punkt. Im echten deutschen Schreiben kommen Dashes selten vor, Muttersprachler nutzen Punkte, Kommas, Doppelpunkte oder Klammern.

### Em-Dash (—)
Das Unicode-Zeichen U+2014. KI-Output sieht typisch so aus:
- *"Das System funktioniert — und es skaliert."*
- *"Sie ist die beste Wahl — vor allem hier."*
- *"Klarheit zuerst — Geschwindigkeit zweitens."*

**Default-Regel: Em-Dash KOMPLETT entfernen.** Ersatz:
- Punkt + neuer Satz: *"Das System funktioniert. Und es skaliert."*
- Doppelpunkt: *"Sie ist die beste Wahl: vor allem hier."*
- Komma: *"Klarheit zuerst, Geschwindigkeit zweitens."*

Ausnahme: Voice-Profile dokumentiert Em-Dash explizit als Stil-Element. Default ist: keine.

### En-Dash (–)
Das Unicode-Zeichen U+2013. Wird von KI ähnlich verwendet wie Em-Dash. Im Deutschen korrekt nur als Bis-Strich (*"Mai–Juli"*, *"S. 12–18"*) oder als Gedankenstrich mit Spaces, aber selten in flüssigem Schreiben.

**Default-Regel: En-Dash entfernen, außer bei Bis-Angaben.** Ersatz wie bei Em-Dash.

### Bindestrich-Reflex
KI baut manchmal Konstrukte mit Bindestrich, wo deutsche Komposita oder Trennung üblich wären (*"die KI-getriebene-Lösung"* statt *"die KI-getriebene Lösung"*). Gegenprüfen.

---

## 2. Generische KI-Helper-Phrasen

Diese Sätze sind sofort als KI-Schreibe erkennbar.

- *"Ich hoffe, das hilft dir."*
- *"Großartige Frage!"*
- *"Gerne stehe ich zur Verfügung."*
- *"Lass mich wissen, ob ich weiterhelfen kann."*
- *"In diesem Post / Artikel zeige ich dir..."*
- *"Es ist wichtig zu beachten, dass..."*
- *"In der heutigen schnelllebigen Welt..."*

**Regel:** Streichen oder durch substanzielle Eröffnung / Schlusszeile ersetzen. Keine Ausnahmen, außer das Voice-Profile dokumentiert die Phrase explizit.

---

## 3. Adjektiv-Cluster ohne Beleg

Markenbeschreibungs-Klischees, die alles und nichts sagen.

- *"warm und kompetent"*
- *"authentisch und nahbar"*
- *"professionell und persönlich"*
- *"holistisch / ganzheitlich"*
- *"effizient und nachhaltig"*
- *"transparent und partnerschaftlich"*

**Regel:** Adjektive sind erlaubt, aber nur mit Substantiv + konkretem Beweis im selben Satz. Ein Adjektiv ohne Mechanismus dahinter ist Slop.

---

## 4. Bullet- und Emoji-Reflex (plus Stichpunkt-Staccato)

KI macht aus jeder Frage eine 7-Punkt-Liste mit Bullets und 3 Dekorations-Emojis, weil das *"strukturiert wirkt"*.

- ❌ *"Wir freuen uns auf deine Nachricht 😊✨🚀"*
- ❌ *"💡 Heute mein Tipp: ..."*
- ❌ Bullet-Liste mit `•` ohne dass das Profil Listen erlaubt

**Regel:**
- Listen nur, wenn das Voice-Profile sie explizit erlaubt. Sonst Prosa.
- Emojis nur, wenn das Profil Emoji-Verwendung dokumentiert. Funktionale Marker (→, ↳, ✓) gelten als Formatierung, nicht als Emoji.

### Stichpunkt-Aufzählungen ohne Verb (Versteckter Bullet-Reflex)

Auch ohne Bullet-Symbol kippt KI gerne in eine Listen-Logik, indem sie Halbsätze ohne Verb aneinanderreiht. Das wirkt staccato statt fließend.

- ❌ *"Team überlastet, Projekte langsam, irgendwer muss her."*
- ❌ *"Mehr Umsatz, mehr Stress, weniger Profit."* (außer als bewusste Inline-Logikkette mit → o.ä., wenn das Profil das erlaubt)

**Regel:** Vollsätze auch wenn kurz. Lieber drei kurze Sätze mit Subjekt und Verb als ein Halbsatz-Cluster.

- ✅ *"Das Team ist überlastet. Die Projekte ziehen sich. Es muss jemand her."*

### Etikett-Substantiv als Schluss-Pointe

Ein-Wort-Sätze oder Halbsatz-Pointen am Schluss eines Absatzes dürfen **kein abstraktes Etikett-Substantiv** sein. Auch wenn das Profil Ein-Wort-Sätze als Pointe erlaubt: das Wort muss eine **konkrete Beobachtung, Zahl, Zeit oder Handlung** sein. Abstrakte Etiketten klingen aphoristisch und werden als KI-Schreibe erkannt.

- ❌ *"Der Rest war Lärm."* — abstraktes Etikett
- ❌ *"Das ist Architektur."* / *"Das ist Sequenz."* — abstraktes Konzept ohne Bild
- ✅ *"Drei Monate lang."* — konkrete Zeit
- ✅ *"Vier Entwickler Vollzeit."* — konkrete Anzahl
- ✅ *"Alles Porsche."* — konkretes Bild aus dem Kontext

**Test:** Ist das Schluss-Wort eine konkrete Beobachtung/Zahl/Handlung — oder ein abstraktes Etikett (Lärm, Chaos, Symptom, Architektur, Struktur, Sequenz)? Etikett → durch konkreten Satz ersetzen, der auf das vorherige Material referenziert.

---

## 5. Pol-Setzungs-Slop

KI baut Argumente sehr gerne über zwei explizite Sätze, die einen Pol setzen und sofort kontern. Das klingt nach Marketing-Hammer und ist einer der erkennbarsten Slop-Pattern überhaupt.

- ❌ *"Du brauchst nicht mehr Hände. Sondern weniger Aufgaben."*
- ❌ *"Es geht nicht um die Tools. Es geht um die Prozesse."*
- ❌ *"Ich sag das nicht, weil ich gegen Einstellen wäre. Sondern weil es selten die richtige Antwort ist."*

Diese fünf Konstruktions-Schemata sind universelle KI-Tells:

| # | Pattern | Name (2026-05-26) |
|---|---|---|
| 1 | *"Nicht X. Sondern Y."* als zwei explizite Sätze | **Sondern-Brücke** |
| 2 | *"Ich sag das nicht, weil X. Sondern weil Y."* | **Sondern-Rechtfertigung** |
| 3 | *"Es geht nicht um X. Es geht um Y."* | **Thema-Tausch** |
| 4 | *"X tut A nicht. X tut B."* (anaphorisch, ohne *sondern*) | **Echo-Pol** |
| 5 | *"Das ist kein X. Das ist Y."* / *"Das ist keine X. Das ist Y."* | **Pseudo-Reframe** |

**Echo-Pol** ist die getarnte Variante mit zwei Sätzen: zweimal dasselbe Subjekt, erster Satz negiert, zweiter Satz eskaliert oder benennt die "wahre" Konsequenz. Klingt argumentativ, ist aber dasselbe Slop-Schema.

- ❌ *"Mehr Marketing würde es nicht lösen. Mehr Marketing würde es beschleunigen, bis es bricht."*
- ❌ *"Das Onboarding entlastet dich nicht. Das Onboarding macht dich noch abhängiger."*

**Pseudo-Reframe** ist die häufigste Slop-Form überhaupt. KI produziert das Pattern systematisch, weil es kurz und argumentativ klingt. Y ist fast immer nur ein Etikett-Synonym für X, keine konkrete Substanz. Beispiele aus 2026-05-26-Audit:

- ❌ *"Das ist kein Produktivitätsproblem. Das ist ein Bottleneck-Problem."* (Etikett-Tausch)
- ❌ *"Das ist kein Zufall. Das ist ein Symptom."* (Synonym-Reframe)
- ❌ *"Das ist keine Ausnahme. Das ist die Regel."* (Inversions-Etikett)
- ❌ *"Das ist kein Disziplin-Problem. Das ist Architektur."* (Abstraktes Konzept ohne Bild)
- ❌ *"Das ist kein Stolz-Signal. Das ist ein Engpass-Signal."* (Beide abstrakt, anderes Wort)

**Test für Pseudo-Reframe und Echo-Pol:** Streich den ersten (Negations-)Satz. Liefert der zweite Satz alleine eine konkrete Beobachtung, Zahl, ein Bild oder eine Handlung? Wenn ja: Pol-Setzung knapp legitim (max 1x pro Text). Wenn nein: Slop, umformulieren.

**Warum Slop:** Der erste Satz tut nichts außer den zweiten ankündigen. Der zweite trägt das Argument alleine. Die Negations-Hälfte ist Füllstoff, der den Outcome verzögert und nach Argumentations-Performance klingt.

**Fix:** Outcome direkt in einem Satz benennen.

- ✅ *"Mehr Marketing würde sein Business zerstören."*
- ✅ *"Das Onboarding macht dich noch abhängiger."*

**Test:** Streich den ersten (Negations-)Satz. Wenn der zweite stärker alleine steht, war der erste Slop.

**Regel:** Streichen. Wenn der Gedanke trotzdem ein Pol-Setzung ist: lieber direkt sagen, ohne die "Sondern"-Brücke und ohne die Negations-Vorhalle.

- ✅ Direkt: *"Du brauchst weniger Aufgaben, nicht mehr Hände."* (in einem Satz, ohne Sondern)
- ✅ Reframung statt Sondern: *"Du brauchst keine mehr Hände. Du brauchst weniger Aufgaben."* (zweiter Satz reframt, statt zu kontern)
- ✅ Anapher-Triple statt Pol: *"Ads skalieren dein Business nicht. Mehr Kunden skalieren dein Business nicht. Systeme skalieren dein Business."* (drei parallele Sätze, gleicher Anfang)

Ausnahme: Voice-Profile dokumentiert eine dieser Konstruktionen explizit als Stil-Element. Default ist: alle drei sind Slop und werden gemieden.

---

## Pflicht-Check beim Apply-Modus

Vor jeder Ausgabe:

- [ ] Kein Em-Dash (—) und kein En-Dash (–) mitten im Satz, außer Profil erlaubt es?
- [ ] Keine generische KI-Helper-Phrase?
- [ ] Keine Adjektiv-Cluster ohne konkreten Beleg?
- [ ] Bullet-/Emoji-Reflex unterdrückt, falls Profil Prosa fordert?
- [ ] Keine Stichpunkt-Aufzählungen ohne Verb (Vollsätze auch wenn kurz)?
- [ ] Keine Pol-Setzungs-Slop-Konstruktion ("Nicht X. Sondern Y." = Sondern-Brücke, "Ich sag das nicht, weil X. Sondern weil Y." = Sondern-Rechtfertigung, "Es geht nicht um X. Es geht um Y." = Thema-Tausch)?
- [ ] Kein Pseudo-Reframe ("Das ist kein X. Das ist Y." mit Y nur als Etikett-Synonym)?
- [ ] Kein Echo-Pol (anaphorisch: zwei Sätze gleiches Subjekt, erst negiert dann gesetzt, ohne sondern)?
- [ ] Keine Etikett-Substantiv-Schluss-Pointe (abstraktes Nomen wie "Lärm/Architektur" als Punch)?

Bei Nein: Stelle benennen, umschreiben, erneut prüfen.
