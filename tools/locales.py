#!/usr/bin/env python3
"""Gera _locales/<idioma>/messages.json a partir da tabela abaixo.

Uma linha por texto: chave -> {idioma: texto}. Placeholders {0}, {1}… são
preenchidos pelo t() do options.js; trechos entre `crases` viram <code>.
"$" literal é escapado ("$$") só no JSON, aqui escreva normal.

    python3 tools/locales.py
"""
import json
from pathlib import Path

LANGS = ['en', 'pt_BR', 'pt_PT', 'es', 'it']

STRINGS = {
    'extDescription': {
        'en': 'Turns text you choose on any page into links that open a Claude Desktop session with the message ready.',
        'pt_BR': 'Transforma textos de qualquer página em links que abrem uma sessão no Claude Desktop com a mensagem pronta.',
        'pt_PT': 'Transforma textos de qualquer página em ligações que abrem uma sessão no Claude Desktop com a mensagem pronta.',
        'es': 'Convierte textos de cualquier página en enlaces que abren una sesión en Claude Desktop con el mensaje listo.',
        'it': 'Trasforma i testi di qualsiasi pagina in link che aprono una sessione di Claude Desktop con il messaggio pronto.',
    },
    'pagesKicker': {'en': '// pages', 'pt_BR': '// páginas', 'pt_PT': '// páginas', 'es': '// páginas', 'it': '// pagine'},
    'addPage': {'en': 'Add page', 'pt_BR': 'Adicionar página', 'pt_PT': 'Adicionar página', 'es': 'Añadir página', 'it': 'Aggiungi pagina'},
    'emptyList': {
        'en': 'No pages yet. Click + to add one.',
        'pt_BR': 'Nenhuma página. Clique em + para adicionar.',
        'pt_PT': 'Nenhuma página. Clique em + para adicionar.',
        'es': 'No hay páginas. Haz clic en + para añadir una.',
        'it': 'Nessuna pagina. Clicca su + per aggiungerne una.',
    },
    'back': {'en': '← Back', 'pt_BR': '← Voltar', 'pt_PT': '← Voltar', 'es': '← Volver', 'it': '← Indietro'},
    'newPage': {'en': 'New page', 'pt_BR': 'Nova página', 'pt_PT': 'Nova página', 'es': 'Nueva página', 'it': 'Nuova pagina'},
    'pageLabel': {'en': 'Page', 'pt_BR': 'Página', 'pt_PT': 'Página', 'es': 'Página', 'it': 'Pagina'},
    'domainLabel': {'en': 'Domain', 'pt_BR': 'Domínio', 'pt_PT': 'Domínio', 'es': 'Dominio', 'it': 'Dominio'},
    'replacementsLabel': {'en': 'Replacements', 'pt_BR': 'Substituições', 'pt_PT': 'Substituições', 'es': 'Sustituciones', 'it': 'Sostituzioni'},
    'colKey': {'en': 'Key (regex)', 'pt_BR': 'Chave (regex)', 'pt_PT': 'Chave (regex)', 'es': 'Clave (regex)', 'it': 'Chiave (regex)'},
    'colValue': {'en': 'Value · $1, $2…', 'pt_BR': 'Valor · $1, $2…', 'pt_PT': 'Valor · $1, $2…', 'es': 'Valor · $1, $2…', 'it': 'Valore · $1, $2…'},
    'colFolder': {'en': 'Folder', 'pt_BR': 'Pasta', 'pt_PT': 'Pasta', 'es': 'Carpeta', 'it': 'Cartella'},
    'folderTip': {
        'en': 'Optional. If empty, the link has no folder and Claude Desktop opens in its default folder.',
        'pt_BR': 'Opcional. Se ficar vazio, o link não leva pasta e o Claude Desktop abre na pasta padrão.',
        'pt_PT': 'Opcional. Se ficar vazio, a ligação não leva pasta e o Claude Desktop abre na pasta predefinida.',
        'es': 'Opcional. Si queda vacío, el enlace no lleva carpeta y Claude Desktop abre en su carpeta predeterminada.',
        'it': 'Facoltativo. Se vuoto, il link non include una cartella e Claude Desktop si apre in quella predefinita.',
    },
    'addReplacement': {'en': '+ Replacement', 'pt_BR': '+ Substituição', 'pt_PT': '+ Substituição', 'es': '+ Sustitución', 'it': '+ Sostituzione'},
    'deletePage': {'en': 'Delete page', 'pt_BR': 'Deletar página', 'pt_PT': 'Eliminar página', 'es': 'Eliminar página', 'it': 'Elimina pagina'},
    'save': {'en': 'Save', 'pt_BR': 'Salvar', 'pt_PT': 'Guardar', 'es': 'Guardar', 'it': 'Salva'},
    'hintSlash': {
        'en': 'Starting the value with “/” does not work: Claude Desktop replaces the slash. Ask for the skill in words, e.g. “Run the skill X on Y”.',
        'pt_BR': 'Começar o valor com “/” não funciona: o Claude Desktop troca a barra. Peça a skill em texto, ex.: “Rode a skill X na Y”.',
        'pt_PT': 'Começar o valor com “/” não funciona: o Claude Desktop substitui a barra. Peça a skill por texto, ex.: “Executa a skill X na Y”.',
        'es': 'Empezar el valor con “/” no funciona: Claude Desktop reemplaza la barra. Pide la skill con texto, p. ej.: “Ejecuta la skill X en Y”.',
        'it': 'Iniziare il valore con “/” non funziona: Claude Desktop sostituisce la barra. Chiedi la skill a parole, ad es.: “Esegui la skill X su Y”.',
    },
    'phKey': {'en': '/(triage)\\s+(TASK-\\d+)', 'pt_BR': '/(triagem)\\s+(TASK-\\d+)', 'pt_PT': '/(triagem)\\s+(TASK-\\d+)', 'es': '/(triaje)\\s+(TASK-\\d+)', 'it': '/(triage)\\s+(TASK-\\d+)'},
    'phValue': {'en': 'Run the skill $1 on $2', 'pt_BR': 'Rode a skill $1 na $2', 'pt_PT': 'Executa a skill $1 na $2', 'es': 'Ejecuta la skill $1 en $2', 'it': 'Esegui la skill $1 su $2'},
    'phFolder': {'en': '(default folder)', 'pt_BR': '(pasta padrão)', 'pt_PT': '(pasta predefinida)', 'es': '(carpeta predeterminada)', 'it': '(cartella predefinita)'},
    'runTitle': {
        'en': 'Run now: apply this rule to the open tab',
        'pt_BR': 'Executar agora: aplica esta regra na aba aberta',
        'pt_PT': 'Executar agora: aplica esta regra no separador aberto',
        'es': 'Ejecutar ahora: aplica esta regla en la pestaña abierta',
        'it': 'Esegui ora: applica questa regola alla scheda aperta',
    },
    'deleteRepTitle': {'en': 'Delete replacement', 'pt_BR': 'Deletar substituição', 'pt_PT': 'Eliminar substituição', 'es': 'Eliminar sustitución', 'it': 'Elimina sostituzione'},
    'countOne': {'en': '1 replacement', 'pt_BR': '1 substituição', 'pt_PT': '1 substituição', 'es': '1 sustitución', 'it': '1 sostituzione'},
    'countMany': {'en': '{0} replacements', 'pt_BR': '{0} substituições', 'pt_PT': '{0} substituições', 'es': '{0} sustituciones', 'it': '{0} sostituzioni'},
    'noPerm': {'en': 'no permission', 'pt_BR': 'sem permissão', 'pt_PT': 'sem permissão', 'es': 'sin permiso', 'it': 'senza permesso'},
    'noPermTitle': {
        'en': 'Open the page and click Save to allow the extension on this site.',
        'pt_BR': 'Abra a página e clique em Salvar para permitir a extensão neste site.',
        'pt_PT': 'Abra a página e clique em Guardar para permitir a extensão neste site.',
        'es': 'Abre la página y haz clic en Guardar para permitir la extensión en este sitio.',
        'it': 'Apri la pagina e clicca su Salva per consentire l’estensione su questo sito.',
    },
    'regexInvalid': {'en': 'Invalid regex: {0}.', 'pt_BR': 'Regex inválida: {0}.', 'pt_PT': 'Regex inválida: {0}.', 'es': 'Regex no válida: {0}.', 'it': 'Regex non valida: {0}.'},
    'reBackslash': {'en': 'stray backslash `\\` at the end', 'pt_BR': 'barra invertida `\\` sobrando no fim', 'pt_PT': 'barra invertida `\\` a mais no fim', 'es': 'barra invertida `\\` sobrante al final', 'it': 'barra rovesciata `\\` in più alla fine'},
    'reGroupOpen': {'en': 'parenthesis `(` opened but not closed', 'pt_BR': 'parêntese `(` aberto sem fechar', 'pt_PT': 'parêntese `(` aberto sem fechar', 'es': 'paréntesis `(` abierto sin cerrar', 'it': 'parentesi `(` aperta e non chiusa'},
    'reGroupClose': {'en': 'parenthesis `)` closed without opening', 'pt_BR': 'parêntese `)` fechando sem abrir', 'pt_PT': 'parêntese `)` a fechar sem abrir', 'es': 'paréntesis `)` cerrado sin abrir', 'it': 'parentesi `)` chiusa senza essere aperta'},
    'reClass': {'en': 'bracket `[` opened but not closed', 'pt_BR': 'colchete `[` aberto sem fechar', 'pt_PT': 'parêntese reto `[` aberto sem fechar', 'es': 'corchete `[` abierto sin cerrar', 'it': 'parentesi quadra `[` aperta e non chiusa'},
    'reNothing': {'en': '`*`, `+`, `?` or `{n}` with nothing before it to repeat', 'pt_BR': '`*`, `+`, `?` ou `{n}` sem nada antes para repetir', 'pt_PT': '`*`, `+`, `?` ou `{n}` sem nada antes para repetir', 'es': '`*`, `+`, `?` o `{n}` sin nada antes que repetir', 'it': '`*`, `+`, `?` o `{n}` senza nulla prima da ripetere'},
    'reRangeNum': {'en': 'range `{min,max}` with min greater than max', 'pt_BR': 'intervalo `{min,max}` com o mínimo maior que o máximo', 'pt_PT': 'intervalo `{min,max}` com o mínimo maior que o máximo', 'es': 'rango `{min,max}` con el mínimo mayor que el máximo', 'it': 'intervallo `{min,max}` con il minimo maggiore del massimo'},
    'reRangeChar': {'en': 'range in `[a-z]` with the start after the end', 'pt_BR': 'intervalo em `[a-z]` com o início depois do fim', 'pt_PT': 'intervalo em `[a-z]` com o início depois do fim', 'es': 'rango en `[a-z]` con el inicio después del final', 'it': 'intervallo in `[a-z]` con l’inizio dopo la fine'},
    'reGroupInvalid': {'en': 'group `(?…)` with invalid syntax', 'pt_BR': 'grupo `(?…)` com sintaxe inválida', 'pt_PT': 'grupo `(?…)` com sintaxe inválida', 'es': 'grupo `(?…)` con sintaxis no válida', 'it': 'gruppo `(?…)` con sintassi non valida'},
    'looseQuant': {
        'en': 'Heads up: `{0}` is not a quantifier here; it looks for the literal text "{0}". Use `{0,{1}}` or `{1,{1}}`.',
        'pt_BR': 'Atenção: `{0}` não é quantificador aqui, procura o texto "{0}". Use `{0,{1}}` ou `{1,{1}}`.',
        'pt_PT': 'Atenção: `{0}` não é quantificador aqui, procura o texto "{0}". Use `{0,{1}}` ou `{1,{1}}`.',
        'es': 'Atención: `{0}` no es un cuantificador aquí; busca el texto literal "{0}". Usa `{0,{1}}` o `{1,{1}}`.',
        'it': 'Attenzione: `{0}` qui non è un quantificatore; cerca il testo letterale "{0}". Usa `{0,{1}}` o `{1,{1}}`.',
    },
    'fillKey': {'en': 'Fill in a valid key.', 'pt_BR': 'Preencha uma chave válida.', 'pt_PT': 'Preencha uma chave válida.', 'es': 'Escribe una clave válida.', 'it': 'Inserisci una chiave valida.'},
    'fillValue': {'en': 'Fill in the value.', 'pt_BR': 'Preencha o valor.', 'pt_PT': 'Preencha o valor.', 'es': 'Escribe el valor.', 'it': 'Inserisci il valore.'},
    'openTab': {
        'en': 'Open a tab on `{0}` and click the extension icon to run it.',
        'pt_BR': 'Abra uma aba em `{0}` e clique no ícone da extensão para executar.',
        'pt_PT': 'Abra um separador em `{0}` e clique no ícone da extensão para executar.',
        'es': 'Abre una pestaña en `{0}` y haz clic en el icono de la extensión para ejecutarla.',
        'it': 'Apri una scheda su `{0}` e clicca sull’icona dell’estensione per eseguirla.',
    },
    'theDomain': {'en': 'the page domain', 'pt_BR': 'o domínio da página', 'pt_PT': 'o domínio da página', 'es': 'el dominio de la página', 'it': 'il dominio della pagina'},
    'runOne': {'en': '1 match became a link in this tab.', 'pt_BR': '1 trecho virou link nesta aba.', 'pt_PT': '1 trecho passou a ligação neste separador.', 'es': '1 coincidencia se convirtió en enlace en esta pestaña.', 'it': '1 corrispondenza è diventata un link in questa scheda.'},
    'runMany': {'en': '{0} matches became links in this tab.', 'pt_BR': '{0} trechos viraram link nesta aba.', 'pt_PT': '{0} trechos passaram a ligação neste separador.', 'es': '{0} coincidencias se convirtieron en enlaces en esta pestaña.', 'it': '{0} corrispondenze sono diventate link in questa scheda.'},
    'noMatch': {
        'en': 'The key does not match any visible text in this tab. Check the regex.',
        'pt_BR': 'A chave não casa com nenhum texto visível desta aba. Confira a regex.',
        'pt_PT': 'A chave não corresponde a nenhum texto visível deste separador. Verifique a regex.',
        'es': 'La clave no coincide con ningún texto visible de esta pestaña. Revisa la regex.',
        'it': 'La chiave non corrisponde a nessun testo visibile in questa scheda. Controlla la regex.',
    },
    'allLinked': {
        'en': 'The {0} matching snippets are already links.',
        'pt_BR': 'Os {0} trechos que casam já são links.',
        'pt_PT': 'Os {0} trechos que correspondem já são ligações.',
        'es': 'Las {0} coincidencias ya son enlaces.',
        'it': 'Le {0} corrispondenze sono già link.',
    },
    'splitText': {
        'en': 'The key matches {0} time(s) in the text, but the snippet is split across page elements (e.g. part bold or a link) and did not become a link.',
        'pt_BR': 'A chave casa {0} vez(es) no texto, mas o trecho está dividido entre elementos da página (ex.: parte em negrito ou link) e não virou link.',
        'pt_PT': 'A chave corresponde {0} vez(es) no texto, mas o trecho está dividido entre elementos da página (ex.: parte a negrito ou ligação) e não passou a ligação.',
        'es': 'La clave coincide {0} vez/veces en el texto, pero el fragmento está dividido entre elementos de la página (p. ej. parte en negrita o un enlace) y no se convirtió en enlace.',
        'it': 'La chiave corrisponde {0} volta/e nel testo, ma il frammento è diviso tra elementi della pagina (ad es. parte in grassetto o un link) e non è diventato un link.',
    },
    'runFailed': {'en': 'Could not run in this tab: {0}', 'pt_BR': 'Não consegui executar na aba: {0}', 'pt_PT': 'Não foi possível executar no separador: {0}', 'es': 'No se pudo ejecutar en la pestaña: {0}', 'it': 'Impossibile eseguire nella scheda: {0}'},
    'errMissingDomain': {'en': 'the page domain is missing', 'pt_BR': 'falta o domínio da página', 'pt_PT': 'falta o domínio da página', 'es': 'falta el dominio de la página', 'it': 'manca il dominio della pagina'},
    'errMissingKey': {'en': 'the key is missing', 'pt_BR': 'falta a chave', 'pt_PT': 'falta a chave', 'es': 'falta la clave', 'it': 'manca la chiave'},
    'errMissingValue': {'en': 'the value is missing', 'pt_BR': 'falta o valor', 'pt_PT': 'falta o valor', 'es': 'falta el valor', 'it': 'manca il valore'},
    'errInvalidKey': {'en': 'invalid regex in the key', 'pt_BR': 'regex inválida na chave', 'pt_PT': 'regex inválida na chave', 'es': 'regex no válida en la clave', 'it': 'regex non valida nella chiave'},
    'notSaved': {'en': 'Not saved: {0}', 'pt_BR': 'Não salvei: {0}', 'pt_PT': 'Não guardado: {0}', 'es': 'No se guardó: {0}', 'it': 'Non salvato: {0}'},
    'confirmDelete': {'en': 'Delete {0}?', 'pt_BR': 'Deletar {0}?', 'pt_PT': 'Eliminar {0}?', 'es': '¿Eliminar {0}?', 'it': 'Eliminare {0}?'},
    'pageExists': {
        'en': '{0} already exists.',
        'pt_BR': '{0} já existe.',
        'pt_PT': '{0} já existe.',
        'es': '{0} ya existe.',
        'it': '{0} esiste già.',
    },
    'merge': {'en': 'Merge', 'pt_BR': 'Mesclar', 'pt_PT': 'Juntar', 'es': 'Combinar', 'it': 'Unisci'},
    'errInvalidDomain': {
        'en': '“{0}” is not a valid domain (e.g. discord.com)',
        'pt_BR': '“{0}” não é um domínio válido (ex.: discord.com)',
        'pt_PT': '“{0}” não é um domínio válido (ex.: discord.com)',
        'es': '“{0}” no es un dominio válido (p. ej. discord.com)',
        'it': '“{0}” non è un dominio valido (ad es. discord.com)',
    },
    'errNoReplacements': {
        'en': 'add at least one replacement',
        'pt_BR': 'adicione ao menos uma substituição',
        'pt_PT': 'adicione pelo menos uma substituição',
        'es': 'añade al menos una sustitución',
        'it': 'aggiungi almeno una sostituzione',
    },
    'matchesEmpty': {
        'en': 'Heads up: this key also matches empty text, so it never becomes a link. Use `+` instead of `*` or require at least one character.',
        'pt_BR': 'Atenção: esta chave casa também com texto vazio, então nunca vira link. Use `+` no lugar de `*` ou exija ao menos um caractere.',
        'pt_PT': 'Atenção: esta chave também corresponde a texto vazio, por isso nunca passa a ligação. Use `+` em vez de `*` ou exija pelo menos um carácter.',
        'es': 'Atención: esta clave también coincide con texto vacío, así que nunca se convierte en enlace. Usa `+` en lugar de `*` o exige al menos un carácter.',
        'it': 'Attenzione: questa chiave corrisponde anche a testo vuoto, quindi non diventa mai un link. Usa `+` al posto di `*` o richiedi almeno un carattere.',
    },
    'valueSlash': {
        'en': 'Heads up: a value starting with `/` does not become a command in Claude Desktop. Ask for the skill in words.',
        'pt_BR': 'Atenção: valor começando com `/` não vira comando no Claude Desktop. Peça a skill em texto.',
        'pt_PT': 'Atenção: um valor começado por `/` não passa a comando no Claude Desktop. Peça a skill por texto.',
        'es': 'Atención: un valor que empieza por `/` no se convierte en comando en Claude Desktop. Pide la skill con texto.',
        'it': 'Attenzione: un valore che inizia con `/` non diventa un comando in Claude Desktop. Chiedi la skill a parole.',
    },
    'folderRelative': {
        'en': 'Heads up: use the full folder path (e.g. `/home/me/project` or `C:\\projects`).',
        'pt_BR': 'Atenção: use o caminho completo da pasta (ex.: `/home/eu/projeto` ou `C:\\projetos`).',
        'pt_PT': 'Atenção: use o caminho completo da pasta (ex.: `/home/eu/projeto` ou `C:\\projetos`).',
        'es': 'Atención: usa la ruta completa de la carpeta (p. ej. `/home/yo/proyecto` o `C:\\proyectos`).',
        'it': 'Attenzione: usa il percorso completo della cartella (ad es. `/home/io/progetto` o `C:\\progetti`).',
    },
    'openInClaude': {'en': 'Open in Claude', 'pt_BR': 'Abrir no Claude', 'pt_PT': 'Abrir no Claude', 'es': 'Abrir en Claude', 'it': 'Apri in Claude'},
}


def main():
    root = Path(__file__).resolve().parent.parent / '_locales'
    for lang in LANGS:
        messages = {}
        for key, texts in STRINGS.items():
            text = texts[lang]
            messages[key] = {'message': text.replace('$', '$$')}
        out = root / lang / 'messages.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(messages, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(out.relative_to(root.parent))


if __name__ == '__main__':
    main()
