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
        "text": "L'azienda ha una visione chiara di cosa succede nel mondo esterno che la riguarda (mercato, normative, economia, tecnologia, società)?",
        "weight": 1.0, "required": True, "iso_ref": "§4.1",
        "tip": "Chiedere se esiste un documento o un momento ricorrente in cui si analizzano trend di mercato, mosse dei concorrenti, nuove leggi o normative, evoluzioni tecnologiche. Può essere un piano strategico, un report periodico, o anche solo un confronto strutturato in CDA. Se non c'è nulla di scritto, il punteggio è basso.",
    },
    {
        "id": "m01_q02", "module": "m01_contesto", "type": "scale",
        "text": "L'azienda conosce bene se stessa: i propri punti di forza, le debolezze, le risorse disponibili e la propria cultura interna?",
        "weight": 1.0, "required": True, "iso_ref": "§4.1",
        "tip": "Verificare se esistono documenti come un piano industriale, un'analisi SWOT, un organigramma aggiornato, o se la direzione ha una visione chiara (anche non scritta) dei propri punti di forza e limiti. In aziende meno strutturate può essere sufficiente una consapevolezza condivisa nel team di direzione.",
    },
    {
        "id": "m01_q03", "module": "m01_contesto", "type": "scale",
        "text": "L'azienda sa chi sono le persone e le organizzazioni importanti per il suo successo, e cosa si aspettano da lei?",
        "weight": 1.0, "required": True, "iso_ref": "§4.2",
        "tip": "Pensare a: clienti chiave, fornitori strategici, dipendenti, soci/investitori, enti regolatori, comunità locale. Chiedere se l'azienda ha mai mappato questi soggetti e le loro aspettative, anche in modo informale. Esempio: 'Sapete cosa si aspettano da voi i vostri 3 clienti più importanti?'",
    },
    {
        "id": "m01_q04", "module": "m01_contesto", "type": "scale",
        "text": "L'azienda ha chiarito perché vuole innovare e cosa si aspetta dall'innovazione?",
        "weight": 1.2, "required": True, "iso_ref": "§4.3.1",
        "tip": "L'intento di innovazione è il 'perché' strategico: crescere in nuovi mercati? Ridurre costi? Migliorare i prodotti? Rispondere a una minaccia competitiva? Anche un'affermazione semplice conta, purché sia condivisa dalla direzione. Se nessuno sa rispondere alla domanda 'perché dovremmo innovare?', il punteggio è basso.",
    },
    {
        "id": "m01_q05", "module": "m01_contesto", "type": "scale",
        "text": "È chiaro dove l'innovazione si applica nell'azienda (quali aree, processi, prodotti) e dove no?",
        "weight": 1.0, "required": True, "iso_ref": "§4.3.2",
        "tip": "Chiedere: 'L'innovazione riguarda tutta l'azienda o solo alcune aree? Quali reparti, prodotti o processi sono coinvolti?' In aziende piccole può riguardare tutto; in aziende grandi è importante delimitare. Non serve un documento formale, ma ci deve essere chiarezza.",
    },
    {
        "id": "m01_q06", "module": "m01_contesto", "type": "text",
        "text": "Come si posiziona l'azienda nel suo settore? Chi sono i concorrenti principali e quali vantaggi o svantaggi ha rispetto a loro?",
        "weight": 0, "required": False, "iso_ref": "§4.1",
        "tip": "Far raccontare il panorama competitivo in modo semplice: chi sono i concorrenti diretti, cosa fa meglio l'azienda rispetto a loro, dove è più debole, quali trend di mercato la favoriscono o la minacciano. Utile anche per aziende di nicchia: 'Chi vi porta via clienti? Perché vi scelgono?'",
    },
    {
        "id": "m01_q07", "module": "m01_contesto", "type": "multi_choice",
        "text": "In quali ambiti l'azienda vede le maggiori opportunità di innovazione?",
        "options": ["Prodotto/servizio", "Processo", "Modello di business", "Organizzazione", "Marketing/commerciale", "Supply chain", "Sostenibilità", "Digitale/tecnologico"],
        "weight": 0.8, "required": False, "iso_ref": "§4.1",
        "tip": "Selezionare tutte le aree in cui l'azienda intravede margini di miglioramento o opportunità concrete. Non serve che ci siano già progetti in corso: basta che la direzione riconosca il potenziale.",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 2 — LEADERSHIP E STRATEGIA (§5 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M02_QUESTIONS = [
    {
        "id": "m02_q01", "module": "m02_leadership", "type": "scale",
        "text": "La direzione (titolare, AD, CDA) crede davvero nell'innovazione e ci mette la faccia, il tempo e le risorse?",
        "weight": 1.2, "required": True, "iso_ref": "§5.1.1",
        "tip": "Non basta dire 'l'innovazione è importante'. Chiedere: il vertice partecipa attivamente alle iniziative? Ha allocato budget? Ne parla nei meeting? L'ha inserita negli obiettivi aziendali? Se l'innovazione dipende solo dalla buona volontà di qualcuno, il punteggio è basso.",
    },
    {
        "id": "m02_q02", "module": "m02_leadership", "type": "scale",
        "text": "È chiaro quale valore concreto l'innovazione deve portare (più ricavi, meno costi, nuovi clienti, miglior reputazione, sostenibilità)?",
        "weight": 1.0, "required": True, "iso_ref": "§5.1.2",
        "tip": "Il valore può essere economico (aumentare il fatturato, ridurre sprechi) o non economico (migliorare il brand, attrarre talenti, ridurre l'impatto ambientale). L'importante è che la direzione sappia cosa vuole ottenere concretamente, non solo 'innovare per innovare'.",
    },
    {
        "id": "m02_q03", "module": "m02_leadership", "type": "scale",
        "text": "Quando serve cambiare qualcosa (un processo, un prodotto, un modo di lavorare), la direzione guida attivamente il cambiamento?",
        "weight": 1.0, "required": True, "iso_ref": "§5.1.3",
        "tip": "Innovare significa cambiare, e il cambiamento va gestito. Chiedere: 'Quando avete introdotto un cambiamento importante, come è stato comunicato? Le persone sono state coinvolte? C'è stata resistenza e come è stata gestita?' Se i cambiamenti vengono calati dall'alto senza spiegazione, il punteggio è medio-basso.",
    },
    {
        "id": "m02_q04", "module": "m02_leadership", "type": "scale",
        "text": "Esiste una dichiarazione chiara (anche semplice) su cosa l'azienda intende fare riguardo all'innovazione, conosciuta da tutti?",
        "weight": 1.0, "required": True, "iso_ref": "§5.2",
        "tip": "Non serve un documento formale di 20 pagine. Può essere un paragrafo nel piano strategico, un messaggio del CEO, o anche una slide condivisa in assemblea. L'importante è che esista, sia chiara e che le persone chiave la conoscano. Chiedere: 'Se chiedo a un responsabile di reparto qual è la linea dell'azienda sull'innovazione, saprebbe rispondere?'",
    },
    {
        "id": "m02_q05", "module": "m02_leadership", "type": "scale",
        "text": "C'è un piano o una strategia per l'innovazione che dice cosa fare, dove investire e con quali priorità?",
        "weight": 1.2, "required": True, "iso_ref": "§5.3",
        "tip": "Una strategia di innovazione risponde a: su cosa vogliamo innovare? Con quali risorse? In quanto tempo? Quali sono le priorità? Non deve essere per forza un documento separato: può essere parte del piano strategico aziendale. L'importante è che le scelte siano consapevoli e non casuali.",
    },
    {
        "id": "m02_q06", "module": "m02_leadership", "type": "scale",
        "text": "Nell'azienda è normale proporre idee nuove, sperimentare e anche sbagliare senza conseguenze negative?",
        "weight": 1.0, "required": True, "iso_ref": "§5.4",
        "tip": "La cultura dell'innovazione si vede nei comportamenti quotidiani: le persone propongono idee? Vengono ascoltate? Si può sperimentare senza paura? Si impara dagli errori o si cercano colpevoli? Reparti diversi collaborano o lavorano a silos? Chiedere esempi concreti recenti.",
    },
    {
        "id": "m02_q07", "module": "m02_leadership", "type": "scale",
        "text": "È chiaro chi si occupa di innovazione in azienda, con quale ruolo e con quale autonomia decisionale?",
        "weight": 1.0, "required": True, "iso_ref": "§5.5",
        "tip": "Chiedere: 'Chi è il responsabile dell'innovazione? Ha un mandato chiaro? Può prendere decisioni e allocare risorse?' In aziende piccole può essere il titolare stesso. L'importante è che non sia 'compito di nessuno' o 'compito di tutti' (che spesso significa di nessuno).",
    },
    {
        "id": "m02_q08", "module": "m02_leadership", "type": "text",
        "text": "Qual è la visione del vertice aziendale sull'innovazione? Dove vuole portare l'azienda nei prossimi 3-5 anni?",
        "weight": 0, "required": False, "iso_ref": "§5.1",
        "tip": "Raccogliere con parole loro cosa si aspetta la direzione: nuovi mercati, nuovi prodotti, trasformazione digitale, efficienza, sostenibilità. È la bussola per tutto il resto dell'assessment. Se la risposta è vaga ('vogliamo crescere'), approfondire con: 'crescere come? dove? con cosa?'",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 3 — PIANIFICAZIONE (§6 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M03_QUESTIONS = [
    {
        "id": "m03_q01", "module": "m03_pianificazione", "type": "scale",
        "text": "L'azienda ha ragionato su cosa potrebbe andare storto (rischi) e cosa potrebbe andare bene (opportunità) nel percorso di innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§6.1",
        "tip": "Chiedere: 'Avete mai fatto una lista dei rischi che potrebbero bloccare l'innovazione? E delle opportunità da cogliere?' Rischi tipici: mancanza di budget, persone non disponibili, tecnologie che non funzionano, clienti che non accettano il cambiamento. Anche una discussione informale in direzione conta.",
    },
    {
        "id": "m03_q02", "module": "m03_pianificazione", "type": "scale",
        "text": "Ci sono obiettivi concreti e misurabili per l'innovazione (non solo buone intenzioni)?",
        "weight": 1.2, "required": True, "iso_ref": "§6.2",
        "tip": "Esempio di obiettivo misurabile: 'Lanciare 2 nuovi prodotti entro dicembre', 'Ridurre i tempi di produzione del 15%', 'Ottenere 50 nuovi clienti dal canale digitale'. Se gli obiettivi sono vaghi ('migliorare l'innovazione') il punteggio è basso. Se sono scritti e monitorati, è alto.",
    },
    {
        "id": "m03_q03", "module": "m03_pianificazione", "type": "scale",
        "text": "Per gli obiettivi di innovazione, è stato definito un piano d'azione con responsabili, tempi e risorse?",
        "weight": 1.0, "required": True, "iso_ref": "§6.2.2",
        "tip": "Un piano d'azione risponde a: chi fa cosa, entro quando, con quali risorse, come misuriamo il successo. Può essere un foglio Excel, un Gantt, un board su Trello. Se gli obiettivi esistono ma nessuno sa come raggiungerli, il punteggio è medio-basso.",
    },
    {
        "id": "m03_q04", "module": "m03_pianificazione", "type": "scale",
        "text": "L'azienda gestisce i propri progetti e iniziative di innovazione come un portafoglio, bilanciando rischio e rendimento?",
        "weight": 1.0, "required": True, "iso_ref": "§6.4",
        "tip": "Un portafoglio di innovazione bilancia: progetti a basso rischio (miglioramenti incrementali) con progetti più ambiziosi (nuovi prodotti, nuovi mercati); progetti a breve termine con investimenti a lungo termine. Chiedere: 'Come scegliete su quali progetti investire? Avete criteri?'",
    },
    {
        "id": "m03_q05", "module": "m03_pianificazione", "type": "scale",
        "text": "La struttura organizzativa attuale (team, reparti, comitati) è adatta a supportare l'innovazione?",
        "weight": 1.0, "required": True, "iso_ref": "§6.5",
        "tip": "Chiedere: 'Ci sono team o persone dedicati all'innovazione? Possono lavorare in modo trasversale tra reparti? Hanno autonomia per prendere decisioni?' In molte aziende l'innovazione rimane bloccata perché i silos organizzativi impediscono la collaborazione.",
    },
    {
        "id": "m03_q06", "module": "m03_pianificazione", "type": "scale",
        "text": "L'azienda collabora con soggetti esterni (università, startup, fornitori, clienti) per innovare?",
        "weight": 0.8, "required": True, "iso_ref": "§6.6",
        "tip": "L'innovazione aperta (open innovation) non richiede grandi investimenti: può essere una collaborazione con un'università locale, un progetto con un fornitore tecnologico, il coinvolgimento dei clienti nel test di un nuovo prodotto. Anche partecipare a fiere e community di settore conta.",
    },
    {
        "id": "m03_q07", "module": "m03_pianificazione", "type": "text",
        "text": "Quali sono i principali ostacoli e rischi che oggi frenano l'innovazione in azienda?",
        "weight": 0, "required": False, "iso_ref": "§6.1",
        "tip": "Far parlare liberamente l'interlocutore. Rischi comuni: 'non abbiamo tempo', 'non abbiamo budget', 'le persone resistono al cambiamento', 'non sappiamo da dove partire', 'non abbiamo le competenze'. Questa risposta è preziosissima per il resto dell'assessment.",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 4 — SUPPORTO E RISORSE (§7 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M04_QUESTIONS = [
    {
        "id": "m04_q01", "module": "m04_supporto", "type": "scale",
        "text": "L'azienda dedica risorse concrete all'innovazione (budget, persone con tempo dedicato, spazi o strumenti)?",
        "weight": 1.2, "required": True, "iso_ref": "§7.1",
        "tip": "Chiedere: 'C'è un budget specifico per l'innovazione? Qualcuno ha tempo protetto per lavorare su nuovi progetti? Ci sono laboratori, strumenti di prototipazione, licenze software?' Se l'innovazione si fa 'nei ritagli di tempo', il punteggio è basso.",
    },
    {
        "id": "m04_q02", "module": "m04_supporto", "type": "scale",
        "text": "Le persone in azienda hanno le competenze necessarie per innovare (o c'è un piano per svilupparle)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.2",
        "tip": "Non servono solo competenze tecniche: servono anche capacità di problem solving, gestione progetti, creatività, analisi dati. Chiedere: 'Avete mai mappato le competenze presenti? Ci sono gap importanti? Fate formazione specifica? Usate consulenti o collaboratori esterni per colmare i gap?'",
    },
    {
        "id": "m04_q03", "module": "m04_supporto", "type": "scale",
        "text": "Le persone in azienda sanno cosa l'azienda vuole fare in termini di innovazione e qual è il loro ruolo?",
        "weight": 0.8, "required": True, "iso_ref": "§7.3",
        "tip": "Un test semplice: se chiedo a un capo reparto 'cosa vuole fare l'azienda per innovare?', saprebbe rispondere? Se le persone non conoscono la direzione, non possono contribuire. Anche nelle PMI piccole, condividere la visione è fondamentale.",
    },
    {
        "id": "m04_q04", "module": "m04_supporto", "type": "scale",
        "text": "L'azienda comunica in modo chiaro (internamente e verso l'esterno) cosa sta facendo in termini di innovazione?",
        "weight": 0.8, "required": True, "iso_ref": "§7.4",
        "tip": "Internamente: riunioni periodiche, newsletter interne, bacheca, canale Slack/Teams. Esternamente: sito web, social media, comunicati stampa, eventi. Anche la comunicazione informale conta. Se nessuno sa cosa sta succedendo, è un problema.",
    },
    {
        "id": "m04_q05", "module": "m04_supporto", "type": "scale",
        "text": "L'azienda protegge le proprie idee e il proprio know-how (brevetti, marchi, accordi di riservatezza, segreti industriali)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.7",
        "tip": "Non tutte le aziende hanno brevetti, ma tutte hanno know-how da proteggere. Chiedere: 'Usate NDA con fornitori e collaboratori? Avete brevetti o marchi registrati? Le informazioni sensibili sono accessibili solo a chi deve vederle?' Anche una semplice policy di riservatezza è un inizio.",
    },
    {
        "id": "m04_q06", "module": "m04_supporto", "type": "scale",
        "text": "L'azienda usa metodi o strumenti specifici per innovare (es. brainstorming strutturato, design thinking, prototipazione rapida, canvas)?",
        "weight": 0.8, "required": True, "iso_ref": "§7.1.8",
        "tip": "Non è necessario usare metodologie sofisticate. Anche un workshop periodico con il team, un canvas stampato su un foglio A3, o un semplice processo di raccolta idee sono strumenti validi. Chiedere: 'Quando dovete sviluppare qualcosa di nuovo, come procedete? Avete un metodo?'",
    },
    {
        "id": "m04_q07", "module": "m04_supporto", "type": "scale",
        "text": "I documenti importanti (procedure, progetti, decisioni) sono organizzati, facili da trovare e tenuti aggiornati?",
        "weight": 0.8, "required": True, "iso_ref": "§7.5",
        "tip": "Chiedere: 'Se domani un nuovo collega deve capire come funziona un processo, trova le informazioni? I documenti sono in una cartella condivisa, un gestionale, un wiki, o ognuno ha i suoi file?' Se le informazioni sono sparse o nella testa delle persone, il punteggio è basso.",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 5 — PROCESSI DI INNOVAZIONE (§8 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M05_QUESTIONS = [
    {
        "id": "m05_q01", "module": "m05_processi", "type": "scale",
        "text": "L'azienda ha un modo sistematico per cercare e individuare nuove opportunità (di mercato, tecnologiche, di miglioramento)?",
        "weight": 1.2, "required": True, "iso_ref": "§8.3.2",
        "tip": "Può essere: monitoraggio dei concorrenti, ascolto dei clienti, scouting tecnologico, partecipazione a fiere, sessioni di brainstorming, analisi dei reclami. L'importante è che non sia casuale. Chiedere: 'Come scoprite che c'è un'opportunità da cogliere?'",
    },
    {
        "id": "m05_q02", "module": "m05_processi", "type": "scale",
        "text": "Quando nasce un'idea, esiste un modo per svilupparla, valutarla e decidere se portarla avanti?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.3",
        "tip": "Il processo può essere semplice: raccolta idee → analisi di fattibilità → presentazione alla direzione → decisione. O più strutturato con criteri di selezione. Chiedere: 'Cosa succede quando qualcuno ha un'idea? Dove finisce? Chi decide se procedere?'",
    },
    {
        "id": "m05_q03", "module": "m05_processi", "type": "scale",
        "text": "Prima di investire pesantemente in una nuova idea, l'azienda la testa in modo rapido ed economico (prototipo, test, versione minima)?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.4",
        "tip": "Validare = verificare che l'idea funzioni prima di impegnare risorse importanti. Può essere: un prototipo fisico, un mockup, un test con un cliente, un pilota su scala ridotta, una landing page. Chiedere: 'Vi è mai capitato di lanciare qualcosa senza testarlo prima? Cosa è successo?'",
    },
    {
        "id": "m05_q04", "module": "m05_processi", "type": "scale",
        "text": "Quando un progetto di innovazione è approvato, lo sviluppo segue delle tappe chiare con momenti di verifica (e possibilità di fermarsi)?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.5",
        "tip": "L'importante è avere dei 'checkpoint': momenti in cui ci si chiede 'Siamo sulla buona strada? Ha ancora senso continuare? Dobbiamo cambiare qualcosa?' Può essere un approccio agile con sprint, o un classico stage-gate. Chiedere: 'Come gestite un progetto di sviluppo nuovo?'",
    },
    {
        "id": "m05_q05", "module": "m05_processi", "type": "scale",
        "text": "Quando si lancia una novità (prodotto, processo, servizio), c'è un piano per farla adottare con successo (formazione, comunicazione, supporto)?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3.6",
        "tip": "Un nuovo prodotto fallisce se i commerciali non sanno venderlo. Un nuovo processo fallisce se gli operatori non sono formati. Chiedere: 'Quando avete introdotto l'ultima novità, come avete gestito il lancio? Le persone erano pronte?' Il rollout è spesso il punto debole.",
    },
    {
        "id": "m05_q06", "module": "m05_processi", "type": "scale",
        "text": "Il modo in cui l'azienda innova è flessibile e si adatta: se qualcosa non funziona, si può cambiare rotta o fermarsi senza drammi?",
        "weight": 0.8, "required": True, "iso_ref": "§8.3.1",
        "tip": "L'innovazione richiede flessibilità: poter tornare indietro, cambiare approccio, abbandonare un progetto che non funziona senza che sia un 'fallimento'. Chiedere: 'Vi è capitato di interrompere un progetto? Come è stato vissuto?' Se fermarsi è tabù, il punteggio è basso.",
    },
    {
        "id": "m05_q07", "module": "m05_processi", "type": "text",
        "text": "Raccontare come funziona oggi il processo di innovazione in azienda, dalla nascita di un'idea fino alla sua realizzazione.",
        "weight": 0, "required": False, "iso_ref": "§8.3",
        "tip": "Chiedere di descrivere un esempio concreto recente: 'Prendiamo l'ultima innovazione che avete introdotto: come è nata l'idea? Chi l'ha portata avanti? Quanto tempo ci è voluto? Cosa ha funzionato e cosa no?' Se non c'è un esempio recente, è già un'informazione rilevante.",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 6 — VALUTAZIONE DELLE PRESTAZIONI (§9 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M06_QUESTIONS = [
    {
        "id": "m06_q01", "module": "m06_valutazione", "type": "scale",
        "text": "L'azienda misura in qualche modo i risultati delle attività di innovazione (indicatori, numeri, metriche)?",
        "weight": 1.2, "required": True, "iso_ref": "§9.1",
        "tip": "Non servono KPI sofisticati. Anche contare 'quante idee nuove abbiamo valutato quest'anno', 'quanti nuovi prodotti lanciati', 'quanto fatturato dai prodotti degli ultimi 3 anni' è già misurare. Chiedere: 'Come fate a sapere se l'innovazione sta funzionando?'",
    },
    {
        "id": "m06_q02", "module": "m06_valutazione", "type": "scale",
        "text": "Le misurazioni vengono fatte in modo regolare, con responsabili chiari e strumenti adeguati?",
        "weight": 1.0, "required": True, "iso_ref": "§9.1.1",
        "tip": "Chiedere: 'Chi raccoglie i dati? Con quale frequenza? I dati sono affidabili? Vengono analizzati e discussi?' Se si misurano le cose ma nessuno guarda i numeri, il valore è limitato. Anche un semplice cruscotto mensile condiviso in riunione è sufficiente.",
    },
    {
        "id": "m06_q03", "module": "m06_valutazione", "type": "scale",
        "text": "Ogni tanto l'azienda verifica se il modo in cui gestisce l'innovazione funziona davvero (una sorta di check-up interno)?",
        "weight": 1.0, "required": True, "iso_ref": "§9.2",
        "tip": "Non serve un audit formale ISO: può essere una riunione annuale in cui ci si chiede 'Il nostro processo di innovazione funziona? Cosa migliorare?' Se l'azienda ha un sistema qualità, potrebbe già includere questo tipo di verifica. Chiedere: 'Avete mai fatto una revisione critica del vostro modo di innovare?'",
    },
    {
        "id": "m06_q04", "module": "m06_valutazione", "type": "scale",
        "text": "La direzione periodicamente rivede la situazione dell'innovazione e prende decisioni su come migliorarla?",
        "weight": 1.0, "required": True, "iso_ref": "§9.3",
        "tip": "Il riesame di direzione è un momento in cui il vertice guarda i risultati, analizza cosa ha funzionato e cosa no, e decide le prossime mosse. Può essere un punto all'ordine del giorno del CDA o una riunione dedicata. Chiedere: 'Ogni quanto la direzione parla di innovazione in modo strutturato?'",
    },
    {
        "id": "m06_q05", "module": "m06_valutazione", "type": "multi_choice",
        "text": "Quali di questi indicatori l'azienda monitora effettivamente in modo regolare?",
        "options": ["N. idee/anno", "N. progetti innovazione", "Budget innovazione", "Time-to-market", "ROI innovazione", "Brevetti depositati", "Tasso adozione nuove soluzioni", "Customer satisfaction", "Revenue da nuovi prodotti", "Nessuno"],
        "weight": 0.8, "required": False, "iso_ref": "§9.1",
        "tip": "Selezionare SOLO gli indicatori che vengono realmente monitorati con una cadenza definita (mensile, trimestrale, annuale). 'Lo facciamo ogni tanto' o 'ci piacerebbe farlo' non conta. Se la risposta è 'Nessuno', è un'informazione importante.",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 7 — ASSESSMENT DIGITALE E TECNOLOGICO
# ═══════════════════════════════════════════════════════════════════════════
M07_QUESTIONS = [
    {
        "id": "m07_q01", "module": "m07_digitale", "type": "scale",
        "text": "Nel complesso, quanto l'azienda è digitalizzata? I processi chiave si appoggiano a strumenti digitali o si lavora ancora molto con carta, email e fogli Excel?",
        "weight": 1.2, "required": True, "iso_ref": "§7.1.5",
        "tip": "1 = Si lavora in gran parte con carta, telefonate, file non strutturati. 2 = Digitalizzazione di base (email, qualche software). 3 = Sistemi gestionali presenti e collegati tra loro. 4 = I dati guidano le decisioni, processi automatizzati. 5 = Nativa digitale, dati e tecnologia al centro di tutto.",
    },
    {
        "id": "m07_q02", "module": "m07_digitale", "type": "scale",
        "text": "L'infrastruttura tecnologica (server, rete, cloud, PC) è affidabile, aggiornata e in grado di crescere con l'azienda?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Chiedere: 'I sistemi si bloccano spesso? La rete è lenta? I PC hanno più di 5 anni? C'è un backup funzionante? Se domani raddoppiaste i dipendenti, l'IT reggerebbe?' Anche una piccola azienda ha bisogno di un'infrastruttura minima affidabile.",
    },
    {
        "id": "m07_q03", "module": "m07_digitale", "type": "scale",
        "text": "I software aziendali (gestionale, CRM, produzione, magazzino) si parlano tra loro o ci sono dati duplicati e isole separate?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Esempio: 'Il commerciale inserisce l'ordine nel CRM, poi qualcuno lo ricopia nel gestionale, poi l'amministrazione lo ricopia nella fatturazione' = bassa integrazione. Se i dati fluiscono automaticamente da un sistema all'altro, il punteggio è alto.",
    },
    {
        "id": "m07_q04", "module": "m07_digitale", "type": "scale",
        "text": "L'azienda gestisce la sicurezza informatica in modo consapevole (password, backup, formazione del personale, protezione dei dati)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Non serve un SOC dedicato. Chiedere: 'I dipendenti usano password robuste? I dati sono backuppati? C'è un antivirus aggiornato? Qualcuno ha fatto formazione sulla sicurezza? Siete conformi al GDPR?' Se la risposta è 'non ci abbiamo mai pensato', è un campanello d'allarme.",
    },
    {
        "id": "m07_q05", "module": "m07_digitale", "type": "scale",
        "text": "L'azienda usa strumenti per lavorare insieme a distanza o tra reparti (cloud, chat, videoconferenze, documenti condivisi, project management)?",
        "weight": 0.8, "required": True, "iso_ref": "§7.1.5",
        "tip": "Strumenti come Microsoft Teams, Google Workspace, Slack, Notion, Trello, Asana. Chiedere: 'Come condividete documenti? Come vi organizzate sui progetti? Come comunicate tra reparti o sedi diverse?' Se la risposta è 'ci mandiamo email con allegati', c'è margine di miglioramento.",
    },
    {
        "id": "m07_q06", "module": "m07_digitale", "type": "multi_choice",
        "text": "Quali di queste tecnologie l'azienda sta già utilizzando concretamente (non solo valutando)?",
        "options": ["Cloud computing", "IoT/sensori", "Big data/analytics", "RPA (automazione)", "Blockchain", "Digital twin", "AR/VR", "E-commerce", "Mobile apps", "Low-code/no-code"],
        "weight": 0.6, "required": False, "iso_ref": "§7.1.5",
        "tip": "Selezionare SOLO le tecnologie in uso effettivo oggi. 'Stiamo valutando' o 'ci piacerebbe' non conta. Va bene anche selezionare poche voci o nessuna: è un dato utile, non un giudizio.",
    },
    {
        "id": "m07_q07", "module": "m07_digitale", "type": "text",
        "text": "Fare una mappa dei principali software e sistemi usati in azienda: quali sono, a cosa servono, e come sono collegati tra loro.",
        "weight": 0, "required": False, "iso_ref": "§7.1.5",
        "tip": "Elencare i software principali (gestionale ERP, CRM, software di produzione, contabilità, BI, e-commerce) e indicare se si parlano tra loro o se i dati vengono riportati manualmente. Esempio: 'Usiamo SAP per la contabilità e Salesforce per i clienti, ma non sono collegati.'",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 8 — AI E DATA READINESS
# ═══════════════════════════════════════════════════════════════════════════
M08_QUESTIONS = [
    {
        "id": "m08_q01", "module": "m08_ai_readiness", "type": "scale",
        "text": "I dati aziendali (clienti, vendite, produzione, costi) sono affidabili, completi e facili da trovare e usare?",
        "weight": 1.2, "required": True, "iso_ref": "§7.1.6",
        "tip": "Chiedere: 'Se oggi voleste fare un'analisi sulle vendite degli ultimi 3 anni, quanto tempo ci mettereste? I dati sarebbero affidabili? Sarebbe facile incrociarli con i dati dei clienti?' Se la risposta è 'ci vorrebbe una settimana per mettere insieme i fogli Excel', la data readiness è bassa.",
    },
    {
        "id": "m08_q02", "module": "m08_ai_readiness", "type": "scale",
        "text": "In azienda o tra i consulenti abituali c'è qualcuno che sa lavorare con i dati in modo avanzato (analisi, modelli, algoritmi)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.2",
        "tip": "Non serve per forza un data scientist interno. Può essere un analista che sa usare bene Excel e Power BI, un consulente esterno, un partner tecnologico. Chiedere: 'Chi analizza i dati oggi? Con quali strumenti? Usate solo report statici o anche analisi dinamiche?'",
    },
    {
        "id": "m08_q03", "module": "m08_ai_readiness", "type": "scale",
        "text": "L'azienda usa già i dati per prendere decisioni in modo avanzato (previsioni, segmentazione clienti, ottimizzazione, automazione)?",
        "weight": 1.0, "required": True, "iso_ref": "§8.3",
        "tip": "Esempi concreti: previsioni di vendita automatiche, segmentazione dei clienti per campagne mirate, manutenzione predittiva sulle macchine, ottimizzazione dei percorsi di consegna, rilevamento anomalie nei processi. Anche un cruscotto BI che supporta le decisioni conta.",
    },
    {
        "id": "m08_q04", "module": "m08_ai_readiness", "type": "scale",
        "text": "L'azienda ha l'infrastruttura tecnica per gestire progetti data-intensive o di AI (database strutturati, capacità di calcolo, pipeline dati)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.5",
        "tip": "Per aziende piccole: 'Avete un database centrale o i dati sono in fogli sparsi? Usate un data warehouse o un sistema di BI?' Per aziende più grandi: 'Avete pipeline ETL, ambienti di sviluppo ML, GPU disponibili?' Non tutte le aziende ne hanno bisogno: valutare in base agli obiettivi.",
    },
    {
        "id": "m08_q05", "module": "m08_ai_readiness", "type": "scale",
        "text": "Se l'azienda usa o vuole usare l'AI, ha ragionato su come farlo in modo responsabile (privacy, correttezza, trasparenza)?",
        "weight": 1.0, "required": True, "iso_ref": "§8.2",
        "tip": "Con l'EU AI Act e il GDPR, la governance AI non è più opzionale. Chiedere: 'Se usate un algoritmo per prendere decisioni, sapete come funziona? I dati dei clienti sono protetti? Avete considerato possibili errori o discriminazioni del modello?' Anche una semplice consapevolezza del tema conta.",
    },
    {
        "id": "m08_q06", "module": "m08_ai_readiness", "type": "multi_choice",
        "text": "Quali di queste tecnologie AI/dati l'azienda sta già usando concretamente o sta sperimentando in un pilota?",
        "options": ["Machine learning classico", "Deep learning / reti neurali", "NLP / text mining", "Computer vision", "RAG (Retrieval-Augmented Generation)", "LLM / chatbot AI", "Agenti autonomi / reti agentiche", "Automazione intelligente (RPA+AI)", "Gemelli digitali con AI", "Nessuna"],
        "weight": 0.8, "required": False, "iso_ref": "§8.3",
        "tip": "Selezionare le tecnologie in uso effettivo o in pilota avanzato (non solo 'ci piacerebbe'). Se non le conoscete tutte, è normale: 'Nessuna' è una risposta perfettamente accettabile e utile per l'assessment.",
    },
    {
        "id": "m08_q07", "module": "m08_ai_readiness", "type": "single_choice",
        "text": "Come descriverebbe il livello complessivo di adozione dell'AI in azienda?",
        "options": ["Nessuna adozione", "Esplorazione/awareness", "Pilota/POC in corso", "Produzione su casi d'uso limitati", "Adozione estesa e integrata"],
        "weight": 1.0, "required": True, "iso_ref": "§8.3",
        "tip": "Scegliere il livello più alto effettivamente raggiunto su almeno un caso d'uso concreto. 'Abbiamo fatto un corso sull'AI' = Esplorazione. 'Stiamo testando un chatbot' = Pilota. 'Usiamo un modello predittivo in produzione' = Produzione limitata.",
    },
    {
        "id": "m08_q08", "module": "m08_ai_readiness", "type": "text",
        "text": "Se l'azienda ha già dei progetti AI/dati (anche piccoli), descriverli: cosa fanno, a che punto sono, che risultati hanno dato.",
        "weight": 0, "required": False, "iso_ref": "§8.3",
        "tip": "Per ogni progetto indicare: area (vendite, produzione, HR, customer service), cosa fa (previsioni, classificazione, automazione), stato (idea, pilota, produzione), risultati. Anche un semplice dashboard di BI conta. Se non ci sono progetti, scrivere 'nessuno ad oggi'.",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 9 — ASSESSMENT GESTIONALE E MANAGERIALE
# ═══════════════════════════════════════════════════════════════════════════
M09_QUESTIONS = [
    {
        "id": "m09_q01", "module": "m09_gestionale", "type": "scale",
        "text": "L'organizzazione dell'azienda è chiara: si sa chi fa cosa, chi decide, chi risponde a chi?",
        "weight": 1.0, "required": True, "iso_ref": "§5.5",
        "tip": "Chiedere: 'Esiste un organigramma? È aggiornato? Le persone sanno a chi fare riferimento? I ruoli sono chiari o c'è sovrapposizione?' In molte PMI i ruoli sono fluidi, e va bene, purché non generi confusione nelle decisioni.",
    },
    {
        "id": "m09_q02", "module": "m09_gestionale", "type": "scale",
        "text": "Le decisioni importanti vengono prese in modo strutturato, basandosi su dati e coinvolgendo le persone giuste?",
        "weight": 1.2, "required": True, "iso_ref": "§5.1",
        "tip": "Chiedere: 'Come vengono prese le decisioni importanti? C'è un comitato? Si usano dati? Chi viene coinvolto? Quanto tempo ci vuole?' Se le decisioni sono solo nella testa del titolare e cambiano ogni settimana, c'è un problema. Se sono lente e burocratiche, è un altro problema.",
    },
    {
        "id": "m09_q03", "module": "m09_gestionale", "type": "scale",
        "text": "Quando l'azienda deve introdurre un cambiamento (nuovo software, riorganizzazione, nuovo processo), lo fa in modo pianificato e gestito?",
        "weight": 1.0, "required": True, "iso_ref": "§5.1.3",
        "tip": "Change management non è una buzzword: è 'come facciamo ad assicurarci che il cambiamento venga adottato'. Chiedere un esempio recente: 'Raccontatemi l'ultimo cambiamento importante. Come lo avete preparato? Comunicato? Le persone lo hanno accettato?'",
    },
    {
        "id": "m09_q04", "module": "m09_gestionale", "type": "scale",
        "text": "I processi di lavoro principali (vendita, produzione, acquisti, amministrazione) sono chiari, documentati e funzionano bene?",
        "weight": 1.0, "required": True, "iso_ref": "§8.1",
        "tip": "Non serve una mappatura BPMN da consulente: anche una descrizione semplice di 'come facciamo le cose' è sufficiente. Chiedere: 'Se un nuovo dipendente entra domani, come impara il lavoro? Ci sono procedure scritte o si impara solo affiancando qualcuno?' Se tutto è nella testa delle persone, è un rischio.",
    },
    {
        "id": "m09_q05", "module": "m09_gestionale", "type": "scale",
        "text": "L'azienda investe nello sviluppo delle persone (formazione, crescita professionale, incentivi legati all'innovazione)?",
        "weight": 1.0, "required": True, "iso_ref": "§7.1.2",
        "tip": "Chiedere: 'Quanto spendete in formazione all'anno? Ci sono percorsi di crescita? Le persone vengono premiate quando propongono miglioramenti? C'è un modo per i dipendenti di segnalare idee?' Anche un budget piccolo ma costante per la formazione è un buon segnale.",
    },
    {
        "id": "m09_q06", "module": "m09_gestionale", "type": "scale",
        "text": "L'azienda è capace di reagire agli imprevisti (un cliente perso, un problema nella supply chain, una crisi) senza andare in blocco?",
        "weight": 0.8, "required": True, "iso_ref": "§5.1.3",
        "tip": "La resilienza è la capacità di assorbire gli shock. Chiedere: 'Cosa succederebbe se perdeste il vostro cliente più grande? O il vostro fornitore principale? Avete un piano B?' Non serve un piano di business continuity formale, ma ci vuole almeno una consapevolezza dei rischi principali.",
    },
    {
        "id": "m09_q07", "module": "m09_gestionale", "type": "text",
        "text": "Quali sono i principali punti di forza e le criticità dell'azienda dal punto di vista organizzativo e gestionale?",
        "weight": 0, "required": False, "iso_ref": "§5-§7",
        "tip": "Questa è una domanda aperta per far emergere la percezione interna. Chiedere: 'Se doveste dire 3 cose che funzionano bene nella vostra organizzazione e 3 che non funzionano, quali sarebbero?' Spesso le risposte a questa domanda sono le più utili di tutto l'assessment.",
    },
]
# ═══════════════════════════════════════════════════════════════════════════
# MODULO 10 — MIGLIORAMENTO CONTINUO (§10 ISO 56001)
# ═══════════════════════════════════════════════════════════════════════════
M10_QUESTIONS = [
    {
        "id": "m10_q01", "module": "m10_miglioramento", "type": "scale",
        "text": "Quando qualcosa va storto (un progetto fallisce, un obiettivo non viene raggiunto, un cliente si lamenta), l'azienda lo riconosce e ci lavora sopra?",
        "weight": 1.0, "required": True, "iso_ref": "§10.2",
        "tip": "Chiedere: 'Cosa succede quando un progetto non raggiunge l'obiettivo? Se ne parla? Si cerca di capire perché? Oppure si va avanti sperando che non ricapiti?' Se i problemi vengono nascosti o ignorati, il punteggio è basso. Se vengono analizzati e usati per migliorare, è alto.",
    },
    {
        "id": "m10_q02", "module": "m10_miglioramento", "type": "scale",
        "text": "Quando si identifica un problema, si agisce per risolverlo alla radice (non solo per tamponare)?",
        "weight": 1.0, "required": True, "iso_ref": "§10.2",
        "tip": "Esempio: il prodotto è difettoso → si cambia il pezzo (tampone) vs. si analizza perché è difettoso e si modifica il processo (azione correttiva). Chiedere: 'Quando trovate un errore ricorrente, andate a cercare la causa di fondo o vi limitate a correggere caso per caso?'",
    },
    {
        "id": "m10_q03", "module": "m10_miglioramento", "type": "scale",
        "text": "L'azienda ha l'abitudine di migliorarsi continuamente: rivedere i processi, imparare dagli errori, adottare nuove pratiche?",
        "weight": 1.2, "required": True, "iso_ref": "§10.1",
        "tip": "Il miglioramento continuo è un'attitudine, non un programma. Chiedere: 'Ci sono momenti ricorrenti in cui vi fermate a chiedervi come migliorare? Avete adottato nuove pratiche nell'ultimo anno? Fate benchmark con aziende simili?' Anche piccoli miglioramenti costanti hanno un grande valore.",
    },
    {
        "id": "m10_q04", "module": "m10_miglioramento", "type": "scale",
        "text": "Quando un progetto finisce (bene o male), le lezioni apprese vengono condivise e riutilizzate per i progetti successivi?",
        "weight": 1.0, "required": True, "iso_ref": "§8.2k",
        "tip": "Chiedere: 'Fate mai un post-mortem o una retrospettiva a fine progetto? Le cose che avete imparato vengono scritte da qualche parte? I nuovi progetti partono dalle lezioni dei precedenti o si riparte sempre da zero?' Se ogni progetto reinventa la ruota, c'è un problema di gestione della conoscenza.",
    },
    {
        "id": "m10_q05", "module": "m10_miglioramento", "type": "yes_no",
        "text": "Esiste un modo strutturato per raccogliere, organizzare e condividere le conoscenze dell'azienda (procedure, best practice, lezioni apprese)?",
        "weight": 0.8, "required": True, "iso_ref": "§7.1.6",
        "tip": "Può essere una wiki interna, una cartella strutturata, un gestionale documentale, un manuale operativo, o anche un canale Teams/Slack dedicato. L'importante è che le conoscenze non restino solo nella testa delle persone. Chiedere: 'Se domani il vostro collaboratore chiave si dimette, quanto know-how andrebbe perso?'",
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
