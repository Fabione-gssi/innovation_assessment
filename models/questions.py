"""
Registry centralizzato delle domande di assessment.
Ogni domanda ha: id, modulo, tipo, testo, opzioni, peso, tip di compilazione.
Aggiungere una domanda = aggiungere un dict alla lista del modulo.

Allineamento normativo:
- Moduli 1-6, 10: clausole §4-§10 UNI EN ISO 56001:2024
- Moduli 7-8: assessment digitale/tecnologico (§7 risorse, §8 processi)
- Modulo 9: assessment gestionale (§5 leadership, §7 supporto, UNI 11814 T1-T8)
"""
from __future__ import annotations

# ── Struttura domanda ───────────────────────────────────────────────────────
# {
#   "id":       str   — identificativo unico (formato: m01_q01)
#   "module":   str   — id del modulo
#   "type":     str   — scale | single_choice | multi_choice | text | yes_no
#   "text":     str   — testo della domanda
#   "options":  list  — opzioni (per single/multi_choice)
#   "weight":   float — peso nel calcolo del punteggio (default 1.0)
#   "tip":      str   — suggerimento di compilazione
#   "required": bool  — obbligatoria per il calcolo
#   "iso_ref":  str   — riferimento normativo specifico
# }

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 1 — CONTESTO DELL'ORGANIZZAZIONE (§4 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M01_QUESTIONS = [
    {
        "id": "m01_q01", "module": "m01_contesto", "type": "scale",
        "text": "L'organizzazione ha identificato e documentato i fattori esterni rilevanti (politici, economici, sociali, tecnologici, legali, ambientali)?",
        "weight": 1.0, "required": True, "iso_ref": "§4.1",
        "tip": "Considerare analisi PESTEL, trend di settore, quadro normativo. Valutare se esiste documentazione formale aggiornata.",
    },
    {
        "id": "m01_q02", "module": "m01_contesto", "type": "scale",
        "text": "L'organizzazione ha identificato e documentato i fattori interni rilevanti (vision, mission, cultura, risorse, capacità, governance)?",
        "weight": 1.0, "required": True, "iso_ref": "§4.1",
        "tip": "Valutare se esistono documenti strategici aggiornati (piano industriale, organigramma, analisi SWOT interna).",
    },
    {
        "id": "m01_q03", "module": "m01_contesto", "type": "scale",
        "text": "Sono state identificate le parti interessate (stakeholder) rilevanti e le loro esigenze e aspettative?",
        "weight": 1.0, "required": True, "iso_ref": "§4.2",
        "tip": "Stakeholder: clienti, fornitori, dipendenti, investitori, enti regolatori, community. Mappatura e analisi delle aspettative.",
    },
    {
        "id": "m01_q04", "module": "m01_contesto", "type": "scale",
        "text": "L'organizzazione ha definito un intento di innovazione documentato?",
        "weight": 1.2, "required": True, "iso_ref": "§4.3.1",
        "tip": "L'intento di innovazione esprime come le attività innovative contribuiscono allo scopo strategico. Deve essere documentato formalmente.",
    },
    {
        "id": "m01_q05", "module": "m01_contesto", "type": "scale",
        "text": "È stato determinato il campo di applicazione del sistema di gestione per l'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§4.3.2",
        "tip": "Il campo di applicazione indica confini, processi, funzioni e strutture coperte dal sistema di gestione dell'innovazione.",
    },
    {
        "id": "m01_q06", "module": "m01_contesto", "type": "text",
        "text": "Descrivere i principali fattori competitivi del settore e il posizionamento dell'organizzazione.",
        "weight": 0, "required": False, "iso_ref": "§4.1",
        "tip": "Indicare concorrenti principali, barriere all'ingresso, trend di mercato, vantaggi competitivi dell'organizzazione.",
    },
    {
        "id": "m01_q07", "module": "m01_contesto", "type": "multi_choice",
        "text": "Quali aree di opportunità per l'innovazione sono state identificate?",
        "options": ["Prodotto/servizio", "Processo", "Modello di business", "Organizzazione", "Marketing/commerciale", "Supply chain", "Sostenibilità", "Digitale/tecnologico"],
        "weight": 0.8, "required": False, "iso_ref": "§4.1",
        "tip": "Selezionare tutte le aree in cui l'organizzazione ha identificato potenziale di innovazione.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 2 — LEADERSHIP E STRATEGIA (§5 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M02_QUESTIONS = [
    {
        "id": "m02_q01", "module": "m02_leadership", "type": "scale",
        "text": "L'alta direzione dimostra leadership e impegno per il sistema di gestione dell'innovazione?",
        "weight": 1.2, "required": True, "iso_ref": "§5.1.1",
        "tip": "Valutare: assunzione di responsabilità, compatibilità con strategia, integrazione nei processi di business, risorse dedicate.",
    },
    {
        "id": "m02_q02", "module": "m02_leadership", "type": "scale",
        "text": "Esiste un focus documentato sulla realizzazione di valore (finanziario e non) attraverso l'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§5.1.2",
        "tip": "Il valore può essere finanziario (ricavi, margini) e non finanziario (brand, competenze, sostenibilità, impatto sociale).",
    },
    {
        "id": "m02_q03", "module": "m02_leadership", "type": "scale",
        "text": "L'alta direzione gestisce attivamente il cambiamento necessario per l'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§5.1.3",
        "tip": "Valutare: comunicazione dell'importanza del cambiamento, coinvolgimento attivo delle persone, preparazione al cambiamento.",
    },
    {
        "id": "m02_q04", "module": "m02_leadership", "type": "scale",
        "text": "È stata stabilita e comunicata una politica per l'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§5.2",
        "tip": "La politica deve essere appropriata, includere impegno al miglioramento continuo, essere comunicata e disponibile.",
    },
    {
        "id": "m02_q05", "module": "m02_leadership", "type": "scale",
        "text": "Esiste una strategia per l'innovazione documentata, comunicata e allineata alla strategia aziendale?",
        "weight": 1.2, "required": True, "iso_ref": "§5.3",
        "tip": "La strategia deve considerare: intento di innovazione, aree di opportunità, portafoglio, risorse, indicatori di successo.",
    },
    {
        "id": "m02_q06", "module": "m02_leadership", "type": "scale",
        "text": "Quanto è sviluppata la cultura dell'innovazione nell'organizzazione?",
        "weight": 1.0, "required": True, "iso_ref": "§5.4",
        "tip": "Valutare: tolleranza al rischio, apertura a nuove idee, collaborazione cross-funzionale, apprendimento dai fallimenti.",
    },
    {
        "id": "m02_q07", "module": "m02_leadership", "type": "scale",
        "text": "Sono stati definiti ruoli, responsabilità e autorità per la gestione dell'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§5.5",
        "tip": "Verificare: organigramma dell'innovazione, job description, delega di autorità, risorse assegnate ai ruoli.",
    },
    {
        "id": "m02_q08", "module": "m02_leadership", "type": "text",
        "text": "Descrivere la visione dell'alta direzione riguardo all'innovazione e le principali aspettative.",
        "weight": 0, "required": False, "iso_ref": "§5.1",
        "tip": "Raccogliere la visione del top management: dove vuole portare l'azienda, priorità, aspettative di risultato.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 3 — PIANIFICAZIONE (§6 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M03_QUESTIONS = [
    {
        "id": "m03_q01", "module": "m03_pianificazione", "type": "scale",
        "text": "L'organizzazione ha identificato rischi e opportunità da affrontare per il sistema di gestione dell'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§6.1",
        "tip": "Considerare: gestione incertezze, livello e tipo di rischi accettati, azioni per migliorare effetti desiderati.",
    },
    {
        "id": "m03_q02", "module": "m03_pianificazione", "type": "scale",
        "text": "Sono stati stabiliti obiettivi per l'innovazione misurabili e coerenti con la strategia?",
        "weight": 1.2, "required": True, "iso_ref": "§6.2",
        "tip": "Gli obiettivi devono: essere coerenti con la politica, misurabili, monitorati, comunicati, aggiornati, documentati.",
    },
    {
        "id": "m03_q03", "module": "m03_pianificazione", "type": "scale",
        "text": "Esiste una pianificazione strutturata per raggiungere gli obiettivi (chi, cosa, quando, come)?",
        "weight": 1.0, "required": True, "iso_ref": "§6.2.2",
        "tip": "Verificare: piano d'azione con risorse, responsabili, tempistiche, criteri di valutazione, modalità di realizzazione del valore.",
    },
    {
        "id": "m03_q04", "module": "m03_pianificazione", "type": "scale",
        "text": "È gestito un portafoglio per l'innovazione con criteri di selezione e bilanciamento?",
        "weight": 1.0, "required": True, "iso_ref": "§6.4",
        "tip": "Il portafoglio bilancia rischio/rendimento, breve/lungo termine, innovazione incrementale/radicale.",
    },
    {
        "id": "m03_q05", "module": "m03_pianificazione", "type": "scale",
        "text": "Le strutture organizzative sono adeguate per supportare le attività di innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§6.5",
        "tip": "Valutare: team dedicati, cross-funzionalità, autonomia decisionale, risorse allocate.",
    },
    {
        "id": "m03_q06", "module": "m03_pianificazione", "type": "scale",
        "text": "Esistono meccanismi di collaborazione interna ed esterna per l'innovazione?",
        "weight": 0.8, "required": True, "iso_ref": "§6.6",
        "tip": "Collaborazione: con università, centri di ricerca, startup, fornitori, clienti, ecosistemi di innovazione.",
    },
    {
        "id": "m03_q07", "module": "m03_pianificazione", "type": "text",
        "text": "Quali sono i principali rischi identificati che ostacolano l'innovazione?",
        "weight": 0, "required": False, "iso_ref": "§6.1",
        "tip": "Elencare rischi: mancanza risorse, resistenza al cambiamento, vincoli normativi, obsolescenza tecnologica, etc.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 4 — SUPPORTO E RISORSE (§7 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M04_QUESTIONS = [
    {
        "id": "m04_q01", "module": "m04_supporto", "type": "scale",
        "text": "L'organizzazione fornisce risorse adeguate (finanziarie, umane, tempo) per l'innovazione?",
        "weight": 1.2, "required": True, "iso_ref": "§7.1",
        "tip": "Valutare: budget dedicato, persone allocate, tempo protetto per l'innovazione, infrastruttura disponibile.",
    },
    {
        "id": "m04_q02", "module": "m04_supporto", "type": "scale",
        "text": "Le competenze necessarie per la gestione dell'innovazione sono disponibili e sviluppate?",
        "weight": 1.0, "required": True, "iso_ref": "§7.2",
        "tip": "Verificare: assessment delle competenze, piani di formazione, gap analysis sulle skill, coaching/mentoring.",
    },
    {
        "id": "m04_q03", "module": "m04_supporto", "type": "scale",
        "text": "Esiste consapevolezza diffusa sulla politica e gli obiettivi di innovazione?",
        "weight": 0.8, "required": True, "iso_ref": "§7.3",
        "tip": "Le persone devono conoscere: politica, obiettivi, proprio contributo, conseguenze del mancato rispetto.",
    },
    {
        "id": "m04_q04", "module": "m04_supporto", "type": "scale",
        "text": "La comunicazione interna ed esterna sull'innovazione è pianificata e efficace?",
        "weight": 0.8, "required": True, "iso_ref": "§7.4",
        "tip": "Determinare: cosa comunicare, quando, a chi, come. Canali interni (intranet, meeting) ed esterni (stakeholder).",
    },
    {
        "id": "m04_q05", "module": "m04_supporto", "type": "scale",
        "text": "La gestione della proprietà intellettuale è strutturata e integrata nei processi di innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.7",
        "tip": "Valutare: policy IP, brevetti, marchi, segreti industriali, accordi di riservatezza, gestione know-how.",
    },
    {
        "id": "m04_q06", "module": "m04_supporto", "type": "scale",
        "text": "Gli strumenti e metodi a supporto dell'innovazione sono adeguati e utilizzati?",
        "weight": 0.8, "required": True, "iso_ref": "§7.1.8",
        "tip": "Strumenti: design thinking, lean startup, business model canvas, prototipazione rapida, software collaborativi.",
    },
    {
        "id": "m04_q07", "module": "m04_supporto", "type": "scale",
        "text": "Le informazioni documentate sono create, aggiornate e controllate adeguatamente?",
        "weight": 0.8, "required": True, "iso_ref": "§7.5",
        "tip": "Verificare: procedure di creazione documenti, versioning, accesso controllato, conservazione.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 5 — PROCESSI DI INNOVAZIONE (§8 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M05_QUESTIONS = [
    {
        "id": "m05_q01", "module": "m05_processi", "type": "scale",
        "text": "Esistono processi strutturati per l'identificazione delle opportunità di innovazione?",
        "weight": 1.2, "required": True, "iso_ref": "§8.3.2",
        "tip": "Considerare: analisi mercato, trend tecnologici, feedback clienti, scouting, brainstorming strutturato.",
    },
    {
        "id": "m05_q02", "module": "m05_processi", "type": "scale",
        "text": "Esiste un processo di creazione e selezione dei concept (ideazione)?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.3",
        "tip": "Valutare: generazione idee, criteri di selezione, analisi fattibilità, sviluppo concept strutturato.",
    },
    {
        "id": "m05_q03", "module": "m05_processi", "type": "scale",
        "text": "I concept vengono validati prima dello sviluppo completo (prototipazione, test, MVP)?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.4",
        "tip": "Verificare: prototipi, POC (proof of concept), test con utenti, validazione tecnica ed economica.",
    },
    {
        "id": "m05_q04", "module": "m05_processi", "type": "scale",
        "text": "Lo sviluppo delle soluzioni è strutturato con milestone e punti decisionali?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.5",
        "tip": "Valutare: stage-gate, agile, milestone chiare, criteri go/no-go, allocazione risorse per fase.",
    },
    {
        "id": "m05_q05", "module": "m05_processi", "type": "scale",
        "text": "L'implementazione delle soluzioni è pianificata con gestione del cambiamento?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.6",
        "tip": "Implementazione: piano di rollout, formazione, gestione resistenze, monitoraggio adozione, feedback loop.",
    },
    {
        "id": "m05_q06", "module": "m05_processi", "type": "scale",
        "text": "I processi di innovazione sono flessibili, iterativi e regolarmente rivisti?",
        "weight": 0.8, "required": True, "iso_ref": "§8.3.1",
        "tip": "I processi devono poter essere ripetuti, adattati, interrotti. Prevedere libertà e sperimentazione.",
    },
    {
        "id": "m05_q07", "module": "m05_processi", "type": "text",
        "text": "Descrivere il processo di innovazione attuale dell'organizzazione (se esistente).",
        "weight": 0, "required": False, "iso_ref": "§8.3",
        "tip": "Descrivere fasi, attori, strumenti, tempistiche, esempi recenti di innovazioni introdotte.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 6 — VALUTAZIONE DELLE PRESTAZIONI (§9 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M06_QUESTIONS = [
    {
        "id": "m06_q01", "module": "m06_valutazione", "type": "scale",
        "text": "Sono definiti indicatori di prestazione (KPI) per monitorare l'innovazione?",
        "weight": 1.2, "required": True, "iso_ref": "§9.1",
        "tip": "KPI: input (risorse, idee), throughput (concept, prototipi), output (soluzioni), outcome (ROI, adozione, impatto).",
    },
    {
        "id": "m06_q02", "module": "m06_valutazione", "type": "scale",
        "text": "I metodi di monitoraggio e misurazione sono validi e applicati sistematicamente?",
        "weight": 1.0, "required": True, "iso_ref": "§9.1.1",
        "tip": "Valutare: frequenza di misurazione, responsabili, strumenti di raccolta dati, analisi periodica.",
    },
    {
        "id": "m06_q03", "module": "m06_valutazione", "type": "scale",
        "text": "Vengono condotti audit interni del sistema di gestione dell'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§9.2",
        "tip": "Audit: frequenza, criteri, obiettività degli auditor, reporting dei risultati, azioni conseguenti.",
    },
    {
        "id": "m06_q04", "module": "m06_valutazione", "type": "scale",
        "text": "La direzione conduce riesami periodici del sistema di gestione dell'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§9.3",
        "tip": "Il riesame deve considerare: stato azioni precedenti, cambiamenti nel contesto, prestazioni, risorse, miglioramenti.",
    },
    {
        "id": "m06_q05", "module": "m06_valutazione", "type": "multi_choice",
        "text": "Quali KPI di innovazione sono attualmente monitorati?",
        "options": ["N. idee/anno", "N. progetti innovazione", "Budget innovazione", "Time-to-market", "ROI innovazione", "Brevetti depositati", "Tasso adozione nuove soluzioni", "Customer satisfaction", "Revenue da nuovi prodotti", "Nessuno"],
        "weight": 0.8, "required": False, "iso_ref": "§9.1",
        "tip": "Selezionare tutti gli indicatori effettivamente monitorati con cadenza regolare.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 7 — ASSESSMENT DIGITALE E TECNOLOGICO
# ═══════════════════════════════════════════════════════════════════════════
M07_QUESTIONS = [
    {
        "id": "m07_q01", "module": "m07_digitale", "type": "scale",
        "text": "Qual è il livello di maturità digitale complessivo dell'organizzazione?",
        "weight": 1.2, "required": True, "iso_ref": "§7.1.5",
        "tip": "1=Analogico, 2=Digitalizzazione base, 3=Integrazione sistemi, 4=Data-driven, 5=Digitally native.",
    },
    {
        "id": "m07_q02", "module": "m07_digitale", "type": "scale",
        "text": "L'infrastruttura IT è adeguata, scalabile e sicura?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Valutare: server/cloud, rete, backup, disaster recovery, scalabilità, aggiornamento tecnologico.",
    },
    {
        "id": "m07_q03", "module": "m07_digitale", "type": "scale",
        "text": "I sistemi informativi sono integrati e supportano i processi core?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Considerare: ERP, CRM, MES, PLM, integrazione tra sistemi, API, flussi dati automatizzati.",
    },
    {
        "id": "m07_q04", "module": "m07_digitale", "type": "scale",
        "text": "La cybersecurity è gestita con policy, strumenti e formazione adeguati?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Valutare: policy sicurezza, firewall, backup, formazione personale, incident response, compliance GDPR.",
    },
    {
        "id": "m07_q05", "module": "m07_digitale", "type": "scale",
        "text": "L'organizzazione utilizza piattaforme cloud e strumenti collaborativi in modo efficace?",
        "weight": 0.8, "required": True, "iso_ref": "§7.1.5",
        "tip": "Cloud: IaaS, PaaS, SaaS. Collaborazione: Microsoft 365, Google Workspace, Slack, tool di project management.",
    },
    {
        "id": "m07_q06", "module": "m07_digitale", "type": "multi_choice",
        "text": "Quali tecnologie digitali sono attualmente adottate?",
        "options": ["Cloud computing", "IoT/sensori", "Big data/analytics", "RPA (automazione)", "Blockchain", "Digital twin", "AR/VR", "E-commerce", "Mobile apps", "Low-code/no-code"],
        "weight": 0.6, "required": False, "iso_ref": "§7.1.5",
        "tip": "Selezionare le tecnologie effettivamente in uso (non in valutazione o pianificate).",
    },
    {
        "id": "m07_q07", "module": "m07_digitale", "type": "text",
        "text": "Descrivere i principali sistemi informativi e le integrazioni esistenti.",
        "weight": 0, "required": False, "iso_ref": "§7.1.5",
        "tip": "Elencare: ERP, CRM, MES, PLM, BI, e-commerce, e le integrazioni/flussi dati tra di essi.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 8 — AI E DATA READINESS
# ═══════════════════════════════════════════════════════════════════════════
M08_QUESTIONS = [
    {
        "id": "m08_q01", "module": "m08_ai_readiness", "type": "scale",
        "text": "Qual è la qualità, completezza e accessibilità dei dati aziendali?",
        "weight": 1.2, "required": True, "iso_ref": "§7.1.6",
        "tip": "Valutare: data quality, completezza, consistenza, accessibilità, data catalog, data governance policy.",
    },
    {
        "id": "m08_q02", "module": "m08_ai_readiness", "type": "scale",
        "text": "Esistono competenze interne in data science, machine learning o intelligenza artificiale?",
        "weight": 1.0, "required": True, "iso_ref": "§7.2",
        "tip": "Valutare: data scientist, ML engineer, data engineer interni. Oppure collaborazioni con partner esterni.",
    },
    {
        "id": "m08_q03", "module": "m08_ai_readiness", "type": "scale",
        "text": "L'organizzazione ha già implementato soluzioni di machine learning o analytics avanzati?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3",
        "tip": "Esempi: modelli predittivi, clustering clienti, raccomandazioni, anomaly detection, NLP, computer vision.",
    },
    {
        "id": "m08_q04", "module": "m08_ai_readiness", "type": "scale",
        "text": "L'infrastruttura dati supporta carichi di lavoro AI/ML (storage, compute, pipeline)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Valutare: data warehouse/lake, pipeline ETL, GPU/TPU, MLOps, ambienti di sviluppo e deployment.",
    },
    {
        "id": "m08_q05", "module": "m08_ai_readiness", "type": "scale",
        "text": "Esiste una governance per l'AI che copra etica, bias, trasparenza e conformità normativa?",
        "weight": 1.0, "required": True, "iso_ref": "§8.2",
        "tip": "Considerare: policy AI, gestione bias, explainability, conformità EU AI Act, responsabilità, audit modelli.",
    },
    {
        "id": "m08_q06", "module": "m08_ai_readiness", "type": "multi_choice",
        "text": "Quali tecnologie AI/ML sono già in uso o in fase di valutazione?",
        "options": ["Machine learning classico", "Deep learning / reti neurali", "NLP / text mining", "Computer vision", "RAG (Retrieval-Augmented Generation)", "LLM / chatbot AI", "Agenti autonomi / reti agentiche", "Automazione intelligente (RPA+AI)", "Gemelli digitali con AI", "Nessuna"],
        "weight": 0.8, "required": False, "iso_ref": "§8.3",
        "tip": "Selezionare le tecnologie in uso operativo O in fase avanzata di valutazione/pilota.",
    },
    {
        "id": "m08_q07", "module": "m08_ai_readiness", "type": "single_choice",
        "text": "Qual è il livello di adozione dell'AI nell'organizzazione?",
        "options": ["Nessuna adozione", "Esplorazione/awareness", "Pilota/POC in corso", "Produzione su casi d'uso limitati", "Adozione estesa e integrata"],
        "weight": 1.0, "required": True, "iso_ref": "§8.3",
        "tip": "Indicare il livello più alto raggiunto su almeno un caso d'uso concreto.",
    },
    {
        "id": "m08_q08", "module": "m08_ai_readiness", "type": "text",
        "text": "Descrivere i casi d'uso AI/ML già implementati o in fase di valutazione.",
        "weight": 0, "required": False, "iso_ref": "§8.3",
        "tip": "Per ogni caso d'uso indicare: area di applicazione, tecnologia, stato (POC/produzione), risultati ottenuti.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 9 — ASSESSMENT GESTIONALE E MANAGERIALE
# ═══════════════════════════════════════════════════════════════════════════
M09_QUESTIONS = [
    {
        "id": "m09_q01", "module": "m09_gestionale", "type": "scale",
        "text": "Il modello organizzativo è chiaro, documentato e adeguato alla complessità aziendale?",
        "weight": 1.0, "required": True, "iso_ref": "§5.5",
        "tip": "Valutare: organigramma, ruoli e responsabilità, flessibilità organizzativa, span of control.",
    },
    {
        "id": "m09_q02", "module": "m09_gestionale", "type": "scale",
        "text": "I processi decisionali sono strutturati, trasparenti e basati su dati?",
        "weight": 1.2, "required": True, "iso_ref": "§5.1",
        "tip": "Valutare: governance, comitati, criteri decisionali, uso di dati e KPI, velocità decisionale.",
    },
    {
        "id": "m09_q03", "module": "m09_gestionale", "type": "scale",
        "text": "La gestione del cambiamento è pianificata e supportata da metodologie strutturate?",
        "weight": 1.0, "required": True, "iso_ref": "§5.1.3",
        "tip": "Change management: comunicazione, formazione, gestione resistenze, coinvolgimento stakeholder, monitoraggio.",
    },
    {
        "id": "m09_q04", "module": "m09_gestionale", "type": "scale",
        "text": "I processi aziendali core sono mappati, standardizzati e ottimizzati?",
        "weight": 1.0, "required": True, "iso_ref": "§8.1",
        "tip": "Valutare: mappatura processi (BPMN), standard operativi, efficienza, eliminazione sprechi, lean management.",
    },
    {
        "id": "m09_q05", "module": "m09_gestionale", "type": "scale",
        "text": "La gestione delle risorse umane supporta l'innovazione (formazione, incentivi, sviluppo)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.2",
        "tip": "Valutare: piani formazione, percorsi di carriera, incentivi per l'innovazione, gestione talenti, welfare.",
    },
    {
        "id": "m09_q06", "module": "m09_gestionale", "type": "scale",
        "text": "L'organizzazione è resiliente e capace di adattarsi a shock e cambiamenti imprevisti?",
        "weight": 0.8, "required": True, "iso_ref": "§5.1.3",
        "tip": "Resilienza: business continuity, diversificazione, flessibilità operativa, capacità di pivot.",
    },
    {
        "id": "m09_q07", "module": "m09_gestionale", "type": "text",
        "text": "Descrivere i principali punti di forza e debolezza del modello gestionale attuale.",
        "weight": 0, "required": False, "iso_ref": "§5-§7",
        "tip": "Analisi SWOT del modello gestionale: cosa funziona bene, cosa è critico, cosa manca.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# MODULO 10 — MIGLIORAMENTO CONTINUO (§10 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M10_QUESTIONS = [
    {
        "id": "m10_q01", "module": "m10_miglioramento", "type": "scale",
        "text": "L'organizzazione identifica e gestisce le non conformità del sistema di innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§10.2",
        "tip": "Non conformità: mancato raggiungimento obiettivi, scostamenti dai processi, feedback negativi, audit finding.",
    },
    {
        "id": "m10_q02", "module": "m10_miglioramento", "type": "scale",
        "text": "Vengono intraprese azioni correttive per eliminare le cause delle non conformità?",
        "weight": 1.0, "required": True, "iso_ref": "§10.2",
        "tip": "Azioni correttive: analisi root cause, definizione azioni, implementazione, verifica efficacia.",
    },
    {
        "id": "m10_q03", "module": "m10_miglioramento", "type": "scale",
        "text": "Esiste un processo sistematico di miglioramento continuo del sistema di innovazione?",
        "weight": 1.2, "required": True, "iso_ref": "§10.1",
        "tip": "Miglioramento continuo: ciclo PDCA, lessons learned, benchmarking, best practices, knowledge management.",
    },
    {
        "id": "m10_q04", "module": "m10_miglioramento", "type": "scale",
        "text": "Le conoscenze ottenute (successi e insuccessi) vengono acquisite e riutilizzate?",
        "weight": 1.0, "required": True, "iso_ref": "§8.2k",
        "tip": "Knowledge management: post-mortem dei progetti, database lessons learned, condivisione best practices.",
    },
    {
        "id": "m10_q05", "module": "m10_miglioramento", "type": "yes_no",
        "text": "L'organizzazione ha un sistema di gestione della conoscenza (knowledge management)?",
        "weight": 0.8, "required": True, "iso_ref": "§7.1.6",
        "tip": "Valutare: wiki interne, database conoscenze, community of practice, programmi di mentoring.",
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# REGISTRY COMPLETO
# ═══════════════════════════════════════════════════════════════════════════
ALL_QUESTIONS = (
    M01_QUESTIONS + M02_QUESTIONS + M03_QUESTIONS + M04_QUESTIONS +
    M05_QUESTIONS + M06_QUESTIONS + M07_QUESTIONS + M08_QUESTIONS +
    M09_QUESTIONS + M10_QUESTIONS
)

QUESTIONS_BY_MODULE: dict[str, list[dict]] = {}
for q in ALL_QUESTIONS:
    mod = q["module"]
    if mod not in QUESTIONS_BY_MODULE:
        QUESTIONS_BY_MODULE[mod] = []
    QUESTIONS_BY_MODULE[mod].append(q)

QUESTIONS_BY_ID: dict[str, dict] = {q["id"]: q for q in ALL_QUESTIONS}


def get_questions_for_module(module_id: str, custom_questions: list | None = None) -> list[dict]:
    """Ritorna domande standard + custom per un modulo."""
    qs = list(QUESTIONS_BY_MODULE.get(module_id, []))
    if custom_questions:
        qs.extend([q for q in custom_questions if q.get("module") == module_id])
    return qs


def get_scorable_questions(module_id: str, custom_questions: list | None = None) -> list[dict]:
    """Ritorna solo domande con peso > 0 (contribuiscono al punteggio)."""
    return [q for q in get_questions_for_module(module_id, custom_questions)
            if q.get("weight", 0) > 0 and q.get("type") in ("scale", "yes_no")]
