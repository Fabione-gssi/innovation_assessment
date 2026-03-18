# Streamlit Assessment Scaffold

Scaffold iniziale per un tool di assessment aziendale consulenziale, allineato ai principi discussi:
- core misto chiuso + aperto
- moduli opzionali
- scoring quantitativo + sintesi qualitativa
- persistenza JSON/Excel
- architettura modulare e manutenibile

## Avvio rapido

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app/main.py
```

## Stato del progetto

Questa v1 è uno scaffold funzionante con:
- setup assessment
- compilazione core assessment
- salvataggio in sessione
- scoring base
- sintesi qualitativa base
- export/import JSON
- export/import Excel
- template domande core configurabile

Sono lasciati volutamente semplici ma estendibili:
- motore finding
- prioritization engine
- roadmap engine
- moduli opzionali completi
- report builder avanzato
