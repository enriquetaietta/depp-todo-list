# 🚀 Todo App

Applicazione **Full-Stack** composta da:

* **Backend** → FastAPI (Python)
* **Frontend** → Nuxt.js + Tailwind CSS

---

# 📦 Backend

## ✅ Prerequisiti

* Python **3.12.11**
* `pip`

## 🛠 Setup

1. **Crea un ambiente virtuale**

   ```bash
   python -m venv venv
   ```

2. **Attivalo**

   * **Windows**

     ```bash
     venv\Scripts\activate
     ```
   * **macOS / Linux**

     ```bash
     source venv/bin/activate
     ```

3. **Installa le dipendenze**

   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Avviare il Backend

1. **Start del server FastAPI**

   ```bash
   fastapi dev main.py
   ```
   All'interno della directory backend.

2. **Endpoints disponibili**

   * API base → `http://127.0.0.1:8000`
   * Swagger UI → `http://127.0.0.1:8000/docs`
   * ReDoc → `http://127.0.0.1:8000/redoc`

## 🧪 Test

Esegui i test con:

```bash
pytest
```

All'interno della directory root.
---

# 🎨 Frontend

## ✅ Prerequisiti

* Node.js **v24.11.1**
* npm **v11.6.2**

## 🛠 Setup

1. **Installa le dipendenze**

   ```bash
   npm install
   ```

## ▶️ Avviare il Frontend

```bash
npm run dev
```

L’applicazione sarà disponibile su:

👉 **[http://localhost:3000](http://localhost:3000)**

---

# 💡 Scelte Tecniche e Difficoltà

## 🔧 Backend (FastAPI)

La scelta di **FastAPI** è stata motivata dalla volontà di sperimentare un framework backend in Python. Dopo aver valutato Flask e FastAPI, ho preferito quest'ultimo per:

* Documentazione chiara e moderna
* Generazione automatica della documentazione OpenAPI
* Tipizzazione integrata
* Modello di sviluppo molto vicino a standard già conosciuti

### Difficoltà riscontrate, mancanze, annotazioni

* Adattamento alla gestione delle rotte non basata sulla struttura delle directory (come avviene in Next.js).
* Implementazione parziale della gestione dei **Tag**, con tabelle e rotte dedicate ancora da completare.
* Problemi di avvio di pytest a causa della struttura delle directories. 
* Inseriti solo test per la rotta principale api/v1/todo GET e POST

### Scelte progettuali

* **Nessuna rotta DELETE reale**: eliminare fisicamente record dal database è rischioso.
  Ho preferito un approccio *soft delete* tramite il campo `deleted_at`.
* La “cancellazione” avviene quindi tramite la rotta **PUT**, non DELETE.
* Numerose note di miglioramento sono presenti nel codice, marcate con `# TODO`.

---

## 🎨 Frontend (Nuxt.js)

La scelta di **Nuxt** deriva dalla volontà di rimettere mano al framework dopo averlo già usato in passato e confrontarlo con l’esperienza recente fatta in Next.js.

### Tecnologie utilizzate

* **Nuxt.js 3+**
* **Tailwind CSS** per lo styling
* **vue-toastification** per le notifiche

### Difficoltà riscontrate, mancanze, annotazioni

* Problemi iniziali con le versioni di Node e npm.
* Incompatibilità tra pacchetti pensati per versioni precedenti di Vue/Nuxt.
* Gestione delle dipendenze in un ecosistema ancora in evoluzione dopo Nuxt 3.
* Come per il backend, è stata avviata ma non completata la gestione dei **Tag** con componenti dedicati.
* Manca una corretta gestione del reset dei filtri durante le varie azioni
* Manca una gestione corretta di un file .env

---

# 📝 Note di Sviluppo

Per lo sviluppo è stata utilizzata l’estensione **Continue.dev** per VS Code:

**Continue – Open-source AI Code Agent**, configurato con il modello **Mistral "codestral"**.

