# Safe Zone (9:16 vertikal)

TikTok und Instagram legen UI über das Video: oben der Account-/Sound-Bereich, unten Caption-Text + Username, rechts die Action-Buttons. Alles Wichtige - **eingebrannte Untertitel und der Text-Hook** - muss innerhalb der Safe Zone liegen, sonst verdeckt die Plattform-UI es.

## Maße (Referenz: 1080x1920)

| Rand | Anteil | px @1080x1920 |
|---|---|---|
| oben | 14 % | ~265 px |
| unten | 19 % | ~365 px |
| links / rechts | je 6.5 % | je ~70 px |

Daraus ergibt sich die Safe-Zone-Box: **x von ~70 bis ~1010, y von ~265 bis ~1555**. Immer prozentual rechnen, damit es bei jeder 9:16-Auflösung passt.

## Platzierung

- **Untertitel:** feste **obere Kante** (Anchor), die Captions wachsen nach **unten**. Die Captions dürfen **nie vertikal springen** - die obere Kante bleibt über alle Captions hinweg auf derselben Linie, egal ob ein- oder mehrzeilig. Den Anchor so hoch im unteren Safe-Zone-Bereich setzen, dass auch die längste (mehrzeilige) Caption noch **über** dem unteren 19-%-Band bleibt (nie tiefer als y ~1555 @1080x1920).
- **Text-Hook:** im oberen bis mittleren Bereich der Safe Zone, **unter** dem oberen 14-%-Band. Scroll-stopping, gut lesbar, bricht nie an den Seitenrändern um.
- **Seiten:** Text nie über die seitlichen 6.5-%-Ränder hinaus (rechts sitzen die Action-Buttons).
- **Caption-Maximalbreite:** Untertitel haben zusätzlich eine feste Maximalbreite über seitliche Ränder (`MarginL`/`MarginR` im force_style, ~12% je Seite ≈ 130px auf 1080-breit). Zu breite Cues **brechen um** statt randvoll zu laufen. Die Ränder liegen innerhalb der Safe Zone, sind aber enger als die 6.5-%-Hartgrenze, damit Captions angenehm lesbar bleiben.

## Andere Formate

16:9 und 1:1 haben keine vertikale Plattform-UI in dem Maß; dort reicht ein moderater Rand (~5 %) rundum. Die strenge Safe Zone gilt für 9:16.
