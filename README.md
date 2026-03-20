# 🔬 Innovation Assessment Tool

**Conforme UNI 11814:2021 · UNI EN ISO 56001:2024**

Tool professionale per Innovation Manager certificati per condurre assessment strutturati delle organizzazioni clienti, analizzare la maturità innovativa e definire roadmap di intervento.

---

## Installazione

```bash
pip install -r requirements.txt
```

## Avvio

```bash
cd innovation_assessment
streamlit run app.py
```

Il tool sarà disponibile su `http://localhost:8501`.

---

## Struttura del progetto

```
innovation_assessment/
├── app.py                      # Entry point Streamlit
├── config.py                   # Costanti, tema, metadati
├── requirements.txt
├── models/
│   ├── schema.py               # Dataclass assessment (modello dati canonico)
│   └── questions.py            # Registry domande (65+ domande standard)
├── modules/                    # (estendibile per logica modulo-specifica)
├── engine/
│   ├── scoring.py              # Calcolo punteggi maturity (1-5)
│   └── analysis.py             # Gap analysis, raccomandazioni, roadmap
├── io_handlers/
│   ├── json_handler.py         # Persistenza JSON (formato canonico)
│   └── excel_handler.py        # Import/export Excel (5 sheet strutturati)
├── ui/
│   ├── components.py           # Widget riusabili (domande, badge, progress)
│   └── dashboard.py            # Dashboard (radar, gap, KPI, roadmap)
└── data/                       # (per file dati default opzionali)
```

---

## Allineamento normativo

### UNI EN ISO 56001:2024 — Sistema di gestione per l'innovazione

I 10 moduli di assessment mappano la struttura della norma:

| Modulo | Clausola ISO | Area |
|--------|-------------|------|
| 1. Contesto dell'organizzazione | §4 | Fattori interni/esterni, stakeholder, intento |
| 2. Leadership e strategia | §5 | Impegno, politica, strategia, cultura, ruoli |
| 3. Pianificazione | §6 | Rischi, obiettivi, portafoglio, collaborazione |
| 4. Supporto e risorse | §7 | Risorse, competenze, IP, strumenti, documenti |
| 5. Processi di innovazione | §8 | Opportunità → concept → validazione → implementazione |
| 6. Valutazione prestazioni | §9 | KPI, audit, riesame di direzione |
| 7. Assessment digitale | §7-§8 | Maturità digitale, infrastruttura, cybersecurity |
| 8. AI e data readiness | §7-§8 | Dati, ML, DL, RAG, agenti, governance AI |
| 9. Assessment gestionale | §5-§7 | Organizzazione, processi, change management |
| 10. Miglioramento continuo | §10 | Non conformità, azioni correttive, PDCA |

### UNI 11814:2021 — Figure professionali gestione innovazione

Il tool supporta i compiti dell'Innovation Manager (livello 7 EQF/QNQ):
- **T2** — Raccolta, strutturazione, interpretazione dati e informazioni
- **T4** — Percorso di innovazione basato su IMS
- **T5** — Integrazione IMS con modello gestionale
- **T7** — Supporto decisione strategica per adozione IMS

---

## Funzionalità

- **65+ domande standard** organizzate in 10 moduli con punteggi 1-5
- **Domande custom** aggiungibili a qualsiasi modulo con integrazione completa
- **Tip di compilazione** su ogni domanda per guidare l'utente
- **Scoring automatico** con maturity level 1-5 per modulo
- **Gap analysis** AS-IS vs TO-BE con prioritizzazione
- **Raccomandazioni** contestualizzate per modulo e livello
- **Radar chart** interattivo (Plotly)
- **Roadmap** automatica e manuale con priorità/effort/impatto
- **Import/Export** JSON e Excel bidirezionale (5 sheet strutturati)
- **Target personalizzabili** per modulo
- **UI professionale** con tema custom e navigazione intuitiva

---

## Persistenza dati

### JSON (formato canonico)
Struttura completa e versionabile, ideale per backup e versioning.

### Excel (formato di interscambio)
5 sheet: Metadati, Risposte, Risultati, Roadmap, Domande Custom.
Utile per condivisione con il cliente e analisi in spreadsheet.

---

## Licenza

Uso interno — Innovation Management Professional Tool.
