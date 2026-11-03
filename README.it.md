# Claude Links

[English](README.md) · [Português (Brasil)](README.pt-BR.md) · [Português (Portugal)](README.pt-PT.md) · [Español](README.es.md) · **Italiano**

Estensione per Chrome/Brave che trova testi in una pagina (tramite regex) e li
trasforma in link che aprono una **nuova sessione nella scheda Code di Claude
Desktop**, con il messaggio già scritto.

Esempio: un'automazione pubblica su Discord un avviso con `/triage TASK-123`.
Con una regola impostata, quel testo diventa un link; un clic apre Claude
Desktop con "Esegui la skill triage su TASK-123" nella casella del messaggio.
Il messaggio **non viene mai inviato da solo**: lo controlli e premi Invio.

## Come funziona

- Il content script viene eseguito solo sulle pagine aggiunte **e
  autorizzate**: quando salvi una pagina nel popup, il browser chiede il
  permesso per quel dominio. Segue anche i contenuti nuovi (siti come Discord
  costruiscono i messaggi in modo dinamico).
- Ogni corrispondenza di una regola diventa un link in questo formato:

  ```
  claude://code/new?q=<valore>&folder=<cartella>
  ```

  È il deep link ufficiale di Claude Desktop
  ([documentazione](https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link)).
- I testi dentro campi modificabili, input e link esistenti non vengono toccati.

## Installazione

1. Apri `brave://extensions` (o `chrome://extensions`).
2. Attiva la **Modalità sviluppatore**.
3. Clicca su **Carica estensione non pacchettizzata** e scegli questa cartella.
4. Fissa l'icona dell'estensione nella barra.

Dopo aver modificato i file, clicca su ricarica (↻) nell'estensione e ricarica
la scheda del sito.

## Configurazione

Clicca sull'icona dell'estensione per aprire l'elenco delle pagine.

- **+** aggiunge una nuova pagina, con il dominio della scheda corrente già compilato.
- Cliccando su una pagina dell'elenco si apre il suo modulo.

Ogni pagina ha un elenco di sostituzioni:

| Campo | Che cos'è |
|-------|-----------|
| **Pagina** | Dominio in cui valgono le regole (ad es. `discord.com`). Anche i sottodomini corrispondono. |
| **Chiave** | Regex che trova il testo da sostituire. |
| **Valore** | Messaggio inviato a Claude (parametro `q`). Accetta `$1`, `$2`… dai gruppi della chiave. |
| **Cartella** | Facoltativa. Cartella in cui si apre la sessione. Vuota = cartella predefinita di Claude Desktop. |

Esempio di regola per Discord:

| Chiave | Valore | Cartella |
|--------|--------|----------|
| `/(triage\|apri-ticket)\s+([A-Z][A-Z0-9]*-\d+)` | `Esegui la skill $1 su $2` | *(vuota)* |

La chiave viene validata mentre scrivi: una regex non valida viene evidenziata,
con l'errore subito sotto. Il pulsante **▶** di ogni riga applica subito quella
regola alla scheda aperta, senza salvare né ricaricare, e indica quante
corrispondenze sono diventate link. La scheda deve essere sul dominio della
pagina (apri il popup dall'icona dell'estensione mentre sei lì).

Quando clicchi su **Salva**, il browser chiede il permesso perché l'estensione
funzioni su quel dominio. Le pagine senza permesso sono segnalate come "senza
permesso" nell'elenco; basta aprirle e salvare di nuovo. Eliminare la pagina
restituisce il permesso.

La configurazione è salvata in `chrome.storage.sync` del browser. Nulla viene
raccolto né inviato ([informativa sulla privacy](https://correaschneider.github.io/claude-links-extension/it/privacy.html)).

## Lingue

L'estensione segue la lingua del browser: inglese (predefinita), portoghese
(Brasile), portoghese (Portogallo), spagnolo e italiano. I testi si trovano in
`tools/locales.py`; dopo averli modificati, esegui `python3 tools/locales.py`
per rigenerare `_locales/`.

## Limitazioni

- **I comandi che iniziano con `/` non funzionano nel valore.** Claude Desktop
  sostituisce la barra iniziale di `q` con un altro carattere, quindi il testo
  non viene riconosciuto come comando. Chiedi la skill a parole ("Esegui la skill X su Y").
- **Discord non accetta questi link in un messaggio**: rende cliccabili solo
  quelli che iniziano con `http(s)`. Per questo la sostituzione avviene nel browser.
- Il browser chiede conferma la prima volta che apre un link `claude://`.
- **Con una cartella, Claude Desktop chiede di considerarla attendibile a ogni
  link**, anche se l'hai già autorizzata. Lascia la cartella vuota per evitare la
  domanda.
- **Il testo catturato da `$1`, `$2`… viene dalla pagina**, e chiunque nel
  canale può averlo scritto. A capo e caratteri invisibili diventano spazi e
  ogni gruppo viene tagliato a 200 caratteri; passa il mouse sul link per vedere
  il messaggio completo e controllalo prima di premere Invio.

## File

| File | Scopo |
|------|-------|
| `manifest.json` | Manifest (Manifest V3). |
| `background.js` | Registra il content script solo sui domini autorizzati. |
| `content.js` | Legge la configurazione e applica le regole del dominio al caricamento della pagina. |
| `linkify.js` | Nucleo della sostituzione dei testi con link (usato anche da ▶). |
| `link.js` | Costruisce il link `claude://`. |
| `defaults.js` | Configurazione iniziale (vuota). |
| `options.html` / `options.js` | Popup con l'elenco delle pagine e il modulo. |
| `_locales/` | Traduzioni (generate da `tools/locales.py`). |
| `icons/` | Icona in SVG e PNG 16/32/48/128. |
| `store/` | Testi e immagini della scheda sul Chrome Web Store. |
| `build.sh` | Crea lo `.zip` da caricare nello store. |
| `docs/` | Sito GitHub Pages (generato da `docs/build.py`). |
