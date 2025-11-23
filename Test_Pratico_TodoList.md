


depp-todo-list
├── .gitignore
├── Test_Pratico_TodoList.md
├── backend
│   ├── api
│   │   ├── middleware
│   │   └── v1
│   │       ├── tag
│   │       └── todo
│   │           └── id
│   ├── database
│   │   └── models
│   │       ├── tag
│   │       ├── todo_tag_relation
│   │       └── todo
│   └── test
├── frontend
└── requirements.txt

---------------------------------------------------------

# Test Pratico Developer DEPP - Todo List Application

**Candidato:** Enrique Taietta
**Data assegnazione:** mercoledì 19 nov
**Consegna:** lun 21 / mart 22 alle 15.00
**Tempo stimato:** 1-2 ore

---

## Obiettivo

Costruire una semplice **Todo List application** con backend API REST e frontend che la consuma.

**Non serve:**
- Design perfetto o CSS elaborato
- Autenticazione/autorizzazione
- Database production-ready (va bene SQLite o in-memory)
- Deployment o containerizzazione

**Serve:**
- Backend funzionante con API REST
- Frontend che consuma le API
- Codice pulito e leggibile
- README con istruzioni setup

---

## Parte 1: Backend API (Python)

### Stack Consigliato
Flask o FastAPI (a tua scelta, quello con cui ti senti più a tuo agio).
Puoi usare SQLite, anche in memory, come DB, senza dover mettere in piedi un database vero e proprio.

### Model

```python
Todo:
  - id: integer (auto-increment)
  - title: string (required, max 200 chars)
  - completed: boolean (default: false)
  - created_at: datetime (auto-generated)
```

### API Endpoints Richiesti

| Metodo HTTP | Endpoint | Descrizione |
|-------------|----------|-------------|
| GET | `/api/todos` | Ottieni lista di tutti i todo |
| POST | `/api/todos` | Crea un nuovo todo |
| PUT | `/api/todos/{id}` | Aggiorna un todo esistente (es: toggle completed) |
| DELETE | `/api/todos/{id}` | Elimina un todo |

### Validazione

- `title` deve essere presente (obbligatorio)
- `title` massimo 200 caratteri
- Ritornare codici HTTP appropriati:
  - `200 OK` per successo
  - `201 Created` per creazione
  - `400 Bad Request` per validazione fallita
  - `404 Not Found` per risorsa non trovata

### Formato JSON

**Esempio richiesta POST `/api/todos`:**
```json
{
  "title": "Comprare il latte"
}
```

**Esempio risposta:**
```json
{
  "id": 1,
  "title": "Comprare il latte",
  "completed": false,
  "created_at": "2025-11-19T10:30:00"
}
```

**Esempio GET `/api/todos`:**
```json
[
  {
    "id": 1,
    "title": "Comprare il latte",
    "completed": false,
    "created_at": "2025-11-19T10:30:00"
  },
  {
    "id": 2,
    "title": "Scrivere email",
    "completed": true,
    "created_at": "2025-11-19T11:00:00"
  }
]
```

### BONUS Backend (non obbligatorio, ma apprezzato)

- Filtro query string: `GET /api/todos?completed=true` oppure `completed=false`
- Test unitari per almeno 2-3 endpoint
- CORS configurato per permettere chiamate da frontend locale

---

## Parte 2: Frontend (JavaScript)

### Stack Consigliato
- Vue.js 3 / Nuxt.js (se lo conosci)
- React / Next.js (alternativa valida)
- HTML + JavaScript vanilla (se preferisci semplificare)

### Funzionalità Minime Richieste

1. **Visualizza lista todo**
   - Mostra tutti i todo caricati dal backend
   - Ogni todo mostra: titolo, stato completato/non completato

2. **Aggiungi nuovo todo**
   - Form con input text per il titolo
   - Bottone "Aggiungi" che chiama POST `/api/todos`
   - Dopo creazione, aggiorna la lista

3. **Marca come completato**
   - Checkbox o bottone per toggle dello stato `completed`
   - Chiama PUT `/api/todos/{id}` con nuovo stato

4. **Elimina todo**
   - Bottone "Elimina" per ogni todo
   - Chiama DELETE `/api/todos/{id}`
   - Rimuove dalla lista dopo eliminazione

### UI/UX

- **Non serve CSS elaborato** - va benissimo anche senza framework CSS
- L'importante è che sia **funzionale e comprensibile**
- Layout semplice: lista verticale di todo va benissimo

### BONUS Frontend (non obbligatorio)

- Filtro visuale per vedere solo completati o solo non completati
- Contatore "X task rimanenti"
- Gestione errori visibile (es: mostra messaggio se API fallisce)
- Input validation client-side (max 200 caratteri)

---

## Struttura Progetto Consigliata

```
todo-app/
├── backend/
│   ├── app.py                 # Entry point Flask/FastAPI
│   ├── requirements.txt       # Dependencies Python
│   ├── models.py              # (opzionale) Model definition
│   └── tests/                 # (opzionale) Test unitari
│       └── test_api.py
│
├── frontend/
│   ├── index.html             # (se vanilla JS)
│   ├── package.json           # (se Vue/React/Next)
│   ├── src/
│   │   ├── App.vue            # Componente principale (Vue)
│   │   ├── components/        # (opzionale) Componenti
│   │   └── ...
│   └── ...
│
└── README.md                  # Istruzioni setup (IMPORTANTE!)
```

---

## README.md - Contenuto Richiesto

Il README deve contenere almeno:

### 1. Setup Backend
```bash
# Esempio (adatta al tuo setup)
cd backend
python -m venv venv
source venv/bin/activate  # su Linux/Mac
# oppure: venv\Scripts\activate  # su Windows
pip install -r requirements.txt
python app.py
```

### 2. Setup Frontend
```bash
# Esempio (adatta al tuo setup)
cd frontend
npm install
npm run dev
```

### 3. URL Applicazione
- Backend API: `http://localhost:5000` (o porta che usi)
- Frontend: `http://localhost:3000` (o porta che usi)

### 4. Come Testare (se hai test)
```bash
cd backend
pytest
# o altro comando per i tuoi test
```

### 5. Note (opzionale ma apprezzato)
- Scelte tecniche che hai fatto e perché
- Cosa miglioreresti con più tempo
- Tool o AI che hai usato (se applicabile)
- Problemi incontrati e come li hai risolti

---

## Valutazione

### Cosa NON Valutiamo
- Completezza al 100% (va bene anche parziale se ben fatto)
- Design grafico o CSS professionale
- Configurazione avanzata (Docker, CI/CD, deploy)
- Performance o scalabilità

### Cosa Valutiamo

**1. Funzionalità (40%)**
- ✅ Backend API funzionanti e corrette
- ✅ Frontend che consuma correttamente le API
- ✅ Validazione input base
- ✅ Gestione errori HTTP appropriata

**2. Qualità Codice (30%)**
- ✅ Codice pulito e leggibile
- ✅ Naming sensato (variabili, funzioni, endpoint)
- ✅ Struttura chiara e logica
- ✅ Separazione responsabilità (model/route/view)

**3. Documentazione (15%)**
- ✅ README con istruzioni funzionanti
- ✅ Setup rapido e chiaro (no errori quando seguo i comandi)
- ✅ Eventuali note sulle scelte fatte

**4. Approccio e Problem Solving (15%)**
- ✅ Pragmatismo (focus su ciò che conta)
- ✅ Gestione priorità (prima funziona, poi raffina)
- ✅ Uso appropriato di tool/risorse

---

## Note Importanti

### Risorse Permesse
✅ **Puoi usare qualsiasi risorsa:**
- Documentazione ufficiale (Flask, FastAPI, Vue, React, Next.js, etc.)
- StackOverflow
- Tutorial online
- **AI tools** (ChatGPT, Claude, GitHub Copilot, Cursor, etc.) se vuoi sperimentare

### Tempo
⏱️ **Il tempo limite (1-2h) è indicativo:**
- Se finisci in 1 ora va benissimo
- Se ci metti 2.5 ore va bene ugualmente
- Preferiamo codice funzionante e pulito a codice perfetto incompleto

### Comunicazione
📧 **Se hai dubbi o problemi:**
- Scrivi pure email per chiarimenti
- Non serve perfezione, serve onestà nel mostrare come lavori

### Cosa fare se ti blocchi
Se incontri un blocco e non riesci a proseguire:
- Documenta nel README cosa avresti voluto fare
- Spiega cosa ti ha bloccato
- Consegna comunque quello che hai fatto

---

## Consegna

**Modalità:**
1. Crea repository GitHub (pubblico o privato)
2. Push del codice completo
3. Invia link repository via email

**Se repository privato:**
- Aggiungi come collaboratore: @gugielmo

**Deadline:** [INSERIRE DATA E ORA CONCORDATA]

---

## Dopo la Consegna

Revisioneremo il codice durante il breve secondo colloquio (30 min) in cui:
- Farai screen share del progetto
- Spiegherai le scelte fatte
- Discuteremo eventuali miglioramenti

---

**Buon lavoro!**

Se hai domande, scrivi pure.

Guglielmo Celata
DEPP Srl
