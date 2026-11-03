#!/usr/bin/env python3
"""Gera o site do GitHub Pages nos 5 idiomas.

Inglês fica na raiz de docs/; os outros em docs/<pasta>/. Textos na tabela
T (uma entrada por idioma); o layout está em PAGE, INDEX e PRIVACY.

    python3 docs/build.py
"""
from html import escape
from urllib.parse import quote
from pathlib import Path

DOCS = Path(__file__).resolve().parent
REPO = 'https://github.com/correaschneider/claude-links-extension'
SITE = 'https://correaschneider.github.io/claude-links-extension/'

# código -> (pasta, nome no seletor, atributo lang)
LANGS = {
    'en': ('', 'English', 'en'),
    'pt-br': ('pt-br', 'Português (Brasil)', 'pt-BR'),
    'pt': ('pt', 'Português (Portugal)', 'pt-PT'),
    'es': ('es', 'Español', 'es'),
    'it': ('it', 'Italiano', 'it'),
}

T = {
    'en': {
        'description': 'Chrome/Brave extension that turns text on a page into links that open a Claude Desktop session with the message ready.',
        'nav_how': 'How it works', 'nav_install': 'Installation', 'nav_config': 'Configuration',
        'hero_kicker': '// chrome · brave extension',
        'hero_title': 'From text on a page to a Claude session, in one click.',
        'hero_lead': 'Claude Links finds text you define with a regex and turns it into links that open a new session in the Code tab of Claude Desktop, with the message already typed.',
        'btn_github': 'View on GitHub', 'btn_install': 'Install',
        'how_kicker': '// how it works', 'how_title': 'A notice becomes a shortcut',
        'how_sub': 'An automation posts a command as text in Discord. With a rule in place, the command becomes a link; one click opens Claude with the request ready.',
        'before': 'Before · plain text', 'after': 'After · link',
        'task_title': '[TASK-123] Error sending message', 'task_line': 'Run the triage with',
        'cmd': '/triage TASK-123', 'composer_label': 'Claude Desktop · new session',
        'composer': 'Run the skill triage on TASK-123',
        's1_t': 'Finds', 's1_p': 'The script runs on the pages you added and follows new content as it arrives, like new Discord messages.',
        's2_t': 'Replaces', 's2_p': 'Each match of a rule becomes a <code>claude://code/new</code> link, built from the rule’s value and folder.',
        's3_t': 'Opens', 's3_p': 'The click opens a Claude Desktop session with the message typed. Nothing is sent on its own: you review it and press Enter.',
        'inst_kicker': '// installation', 'inst_title': 'Load it in the browser',
        'inst_sub': 'Until it is on the Chrome Web Store, the extension is loaded from the source code.',
        'steps_label': 'Step by step',
        'inst_steps': ['Download or clone the <a href="{repo}">repository</a>.', 'Open <code>brave://extensions</code> or <code>chrome://extensions</code>.', 'Turn on <strong>Developer mode</strong>.', 'Click <strong>Load unpacked</strong> and pick the folder.', 'Pin the extension icon to the toolbar.'],
        'term_label': 'From the terminal', 'term_clone': '# clone the code', 'term_after': '# after changing files:', 'term_reload': '# ↻ on the extension + reload the tab',
        'cfg_kicker': '// configuration', 'cfg_title': 'Rules per page',
        'cfg_sub': 'Click the extension icon to see the list of pages. The <strong>+</strong> button adds a new one with the current tab’s domain filled in. When you save, the browser asks for permission for the extension to run on that site; without it, the extension does not touch the page.',
        'th_field': 'Field', 'th_what': 'What it is',
        'f_page': 'Page', 'f_page_d': 'Domain where the rules apply, e.g. <code>discord.com</code>. Subdomains match too.',
        'f_key': 'Key', 'f_key_d': 'Regex that finds the text to replace. Validated as you type.',
        'f_value': 'Value', 'f_value_d': 'Message sent to Claude (the <code>q</code> parameter). Accepts <code>$1</code>, <code>$2</code>… from the key’s groups.',
        'f_folder': 'Folder', 'f_folder_d': 'Optional. Folder where the session opens. Empty = Claude Desktop’s default folder.',
        'f_run': '▶', 'f_run_d': 'Applies the rule to the open tab right away, without saving, and tells you how many matches became links.',
        'example_label': 'Example rule', 'ex_key': 'key  ', 'ex_value': 'value', 'ex_link': 'link ',
        'ex_regex': '/(triage|open-ticket)\\s+([A-Z][A-Z0-9]*-\\d+)', 'ex_q': 'Run the skill $1 on $2',
        'lim_kicker': '// limitations', 'lim_title': 'Good to know',
        'lim_sub': 'Claude Desktop and website behaviors that shaped the extension.',
        'lim1': '<strong>Commands with a slash don’t work in the value.</strong> Claude Desktop replaces the leading slash of <code>q</code> with another character, so the text is not a command. Ask for the skill in words: “Run the skill X on Y”.',
        'lim2': '<strong>Discord doesn’t accept these links in a message.</strong> It only makes <code>http(s)</code> links clickable. That’s why the replacement happens in the browser.',
        'lim3': '<strong>Confirmation the first time.</strong> The browser asks whether it may open Claude when you click the first <code>claude://</code> link.',
        'privacy': 'Privacy policy',
        'pv_title': 'Privacy policy',
        'pv_lead': 'Claude Links does not collect, send or sell any data. Everything it uses stays in your browser.',
        'pv_store_l': 'What the extension stores',
        'pv_store': 'Only the configuration you enter in the popup: page domains and rules (key, value and folder). It lives in the browser’s <code>chrome.storage.sync</code>, which the browser itself may sync across your devices when you are signed in. The extension has no server and sends this configuration nowhere.',
        'pv_read_l': 'What it reads on pages',
        'pv_read': 'It runs only on the domains you added and authorized. On those pages, it looks in the visible text for snippets that match your rules and turns them into links. Page text is neither stored nor sent.',
        'pv_click_l': 'When you click a link',
        'pv_click': 'The <code>claude://</code> link is handed to the operating system, which opens the Claude Desktop installed on your computer with the message filled in. From then on, Claude’s privacy policy applies. The extension takes no part in that conversation.',
        'pv_perm_l': 'Permissions', 'th_perm': 'Permission', 'th_why': 'Why',
        'pv_storage': 'Store your configuration.',
        'pv_active': 'Fill in the current tab’s domain when you click + in the popup.',
        'pv_scripting': 'Enable the text replacement only on the domains you added, and run a rule on demand with ▶.',
        'pv_hosts_n': 'Site access (optional)',
        'pv_hosts': 'Requested one by one, when you save a page. Without your authorization, the extension does not run on the site.',
        'pv_contact_l': 'Contact',
        'pv_contact': 'Questions or problems: open an issue at <a href="{repo}/issues">github.com/correaschneider/claude-links-extension</a>.',
        'pv_updated': 'Last updated November 3, 2026',
    },
    'pt-br': {
        'description': 'Extensão para Chrome/Brave que transforma textos de uma página em links que abrem uma sessão no Claude Desktop com a mensagem pronta.',
        'nav_how': 'Como funciona', 'nav_install': 'Instalação', 'nav_config': 'Configuração',
        'hero_kicker': '// extensão chrome · brave',
        'hero_title': 'Do texto na página à sessão no Claude, em um clique.',
        'hero_lead': 'A Claude Links encontra textos que você define por regex e os transforma em links que abrem uma sessão nova na aba Code do Claude Desktop, com a mensagem já digitada.',
        'btn_github': 'Ver no GitHub', 'btn_install': 'Instalar',
        'how_kicker': '// como funciona', 'how_title': 'Um aviso vira um atalho',
        'how_sub': 'Uma automação manda no Discord um aviso com um comando em texto. Com uma regra cadastrada, o comando vira um link; o clique abre o Claude com o pedido pronto.',
        'before': 'Antes · texto puro', 'after': 'Depois · link',
        'task_title': '[TASK-123] Erro ao enviar mensagem', 'task_line': 'Fazer a triagem com',
        'cmd': '/triagem TASK-123', 'composer_label': 'Claude Desktop · nova sessão',
        'composer': 'Rode a skill triagem na TASK-123',
        's1_t': 'Encontra', 's1_p': 'O script roda nas páginas cadastradas e acompanha o conteúdo que vai chegando, como as mensagens novas do Discord.',
        's2_t': 'Troca', 's2_p': 'Cada trecho que casa com uma regra vira um link <code>claude://code/new</code>, montado com o valor e a pasta da regra.',
        's3_t': 'Abre', 's3_p': 'O clique abre uma sessão no Claude Desktop com a mensagem digitada. Nada é enviado sozinho: você confere e aperta Enter.',
        'inst_kicker': '// instalação', 'inst_title': 'Carregar no navegador',
        'inst_sub': 'Enquanto não está na Chrome Web Store, a extensão é carregada a partir do código.',
        'steps_label': 'Passo a passo',
        'inst_steps': ['Baixe ou clone o <a href="{repo}">repositório</a>.', 'Abra <code>brave://extensions</code> ou <code>chrome://extensions</code>.', 'Ative o <strong>Modo de desenvolvedor</strong>.', 'Clique em <strong>Carregar sem compactação</strong> e escolha a pasta.', 'Fixe o ícone da extensão na barra.'],
        'term_label': 'Via terminal', 'term_clone': '# clona o código', 'term_after': '# depois de mudar arquivos:', 'term_reload': '# ↻ na extensão + recarregar a aba',
        'cfg_kicker': '// configuração', 'cfg_title': 'Regras por página',
        'cfg_sub': 'Clique no ícone da extensão para ver a lista de páginas. O botão <strong>+</strong> cadastra uma nova, já com o domínio da aba atual preenchido. Ao salvar, o navegador pede permissão para a extensão rodar naquele site; sem ela, a extensão não toca na página.',
        'th_field': 'Campo', 'th_what': 'O que é',
        'f_page': 'Página', 'f_page_d': 'Domínio onde as regras valem, ex.: <code>discord.com</code>. Subdomínios também casam.',
        'f_key': 'Chave', 'f_key_d': 'Regex que identifica o texto a trocar. Validada enquanto você digita.',
        'f_value': 'Valor', 'f_value_d': 'Mensagem que vai para o Claude (parâmetro <code>q</code>). Aceita <code>$1</code>, <code>$2</code>… com os grupos da chave.',
        'f_folder': 'Pasta', 'f_folder_d': 'Opcional. Pasta onde a sessão abre. Vazio = pasta padrão do Claude Desktop.',
        'f_run': '▶', 'f_run_d': 'Aplica a regra na hora na aba aberta, sem salvar, e diz quantos trechos viraram link.',
        'example_label': 'Exemplo de regra', 'ex_key': 'chave', 'ex_value': 'valor', 'ex_link': 'link ',
        'ex_regex': '/(triagem|abrir-chamado)\\s+([A-Z][A-Z0-9]*-\\d+)', 'ex_q': 'Rode a skill $1 na $2',
        'lim_kicker': '// limitações', 'lim_title': 'Bom saber',
        'lim_sub': 'Comportamentos do Claude Desktop e dos sites que moldaram a extensão.',
        'lim1': '<strong>Comandos com barra não funcionam no valor.</strong> O Claude Desktop troca a barra inicial do <code>q</code> por outro caractere, então o texto não vira comando. Peça a skill em texto: “Rode a skill X na Y”.',
        'lim2': '<strong>O Discord não aceita esses links na mensagem.</strong> Ele só torna clicável o que começa com <code>http(s)</code>. Por isso a troca acontece no navegador.',
        'lim3': '<strong>Confirmação na primeira vez.</strong> O navegador pergunta se pode abrir o Claude ao clicar no primeiro link <code>claude://</code>.',
        'privacy': 'Política de privacidade',
        'pv_title': 'Política de privacidade',
        'pv_lead': 'A Claude Links não coleta, não envia e não vende nenhum dado. Tudo o que ela usa fica no seu navegador.',
        'pv_store_l': 'O que a extensão guarda',
        'pv_store': 'Só a configuração que você cadastra no popup: os domínios das páginas e as regras (chave, valor e pasta). Ela fica no <code>chrome.storage.sync</code> do navegador, que o próprio navegador pode sincronizar entre os seus dispositivos quando você está logado nele. A extensão não tem servidor e não envia essa configuração para lugar nenhum.',
        'pv_read_l': 'O que ela lê nas páginas',
        'pv_read': 'Ela roda somente nos domínios que você cadastrou e autorizou. Nessas páginas, procura no texto visível os trechos que casam com as suas regras e os transforma em links. O texto da página não é guardado nem enviado.',
        'pv_click_l': 'Quando você clica num link',
        'pv_click': 'O link <code>claude://</code> é entregue ao sistema operacional, que abre o Claude Desktop instalado no seu computador com a mensagem preenchida. A partir daí vale a política de privacidade do Claude. A extensão não participa dessa conversa.',
        'pv_perm_l': 'Permissões', 'th_perm': 'Permissão', 'th_why': 'Para quê',
        'pv_storage': 'Guardar a sua configuração.',
        'pv_active': 'Preencher o domínio da aba atual quando você clica em + no popup.',
        'pv_scripting': 'Ativar a troca de textos só nos domínios cadastrados e executar uma regra na hora com o ▶.',
        'pv_hosts_n': 'Acesso a sites (opcional)',
        'pv_hosts': 'Pedido um a um, quando você salva uma página. Sem a sua autorização, a extensão não roda no site.',
        'pv_contact_l': 'Contato',
        'pv_contact': 'Dúvidas ou problemas: abra uma issue em <a href="{repo}/issues">github.com/correaschneider/claude-links-extension</a>.',
        'pv_updated': 'Atualizada em 3 de novembro de 2026',
    },
    'pt': {
        'description': 'Extensão para Chrome/Brave que transforma textos de uma página em ligações que abrem uma sessão no Claude Desktop com a mensagem pronta.',
        'nav_how': 'Como funciona', 'nav_install': 'Instalação', 'nav_config': 'Configuração',
        'hero_kicker': '// extensão chrome · brave',
        'hero_title': 'Do texto na página à sessão no Claude, num clique.',
        'hero_lead': 'A Claude Links encontra textos que define por regex e transforma-os em ligações que abrem uma nova sessão no separador Code do Claude Desktop, com a mensagem já escrita.',
        'btn_github': 'Ver no GitHub', 'btn_install': 'Instalar',
        'how_kicker': '// como funciona', 'how_title': 'Um aviso passa a atalho',
        'how_sub': 'Uma automatização publica no Discord um aviso com um comando em texto. Com uma regra configurada, o comando passa a ser uma ligação; o clique abre o Claude com o pedido pronto.',
        'before': 'Antes · texto simples', 'after': 'Depois · ligação',
        'task_title': '[TASK-123] Erro ao enviar mensagem', 'task_line': 'Fazer a triagem com',
        'cmd': '/triagem TASK-123', 'composer_label': 'Claude Desktop · nova sessão',
        'composer': 'Executa a skill triagem na TASK-123',
        's1_t': 'Encontra', 's1_p': 'O script corre nas páginas adicionadas e acompanha o conteúdo que vai chegando, como as mensagens novas do Discord.',
        's2_t': 'Substitui', 's2_p': 'Cada trecho que corresponde a uma regra passa a ser uma ligação <code>claude://code/new</code>, construída com o valor e a pasta da regra.',
        's3_t': 'Abre', 's3_p': 'O clique abre uma sessão no Claude Desktop com a mensagem escrita. Nada é enviado sozinho: verifica-a e prime Enter.',
        'inst_kicker': '// instalação', 'inst_title': 'Carregar no navegador',
        'inst_sub': 'Enquanto não está na Chrome Web Store, a extensão é carregada a partir do código.',
        'steps_label': 'Passo a passo',
        'inst_steps': ['Transfira ou clone o <a href="{repo}">repositório</a>.', 'Abra <code>brave://extensions</code> ou <code>chrome://extensions</code>.', 'Ative o <strong>Modo de programador</strong>.', 'Clique em <strong>Carregar expandida</strong> e escolha a pasta.', 'Fixe o ícone da extensão na barra.'],
        'term_label': 'Pelo terminal', 'term_clone': '# clona o código', 'term_after': '# depois de alterar ficheiros:', 'term_reload': '# ↻ na extensão + recarregar o separador',
        'cfg_kicker': '// configuração', 'cfg_title': 'Regras por página',
        'cfg_sub': 'Clique no ícone da extensão para ver a lista de páginas. O botão <strong>+</strong> adiciona uma nova, já com o domínio do separador atual preenchido. Ao guardar, o navegador pede permissão para a extensão correr nesse site; sem ela, a extensão não altera a página.',
        'th_field': 'Campo', 'th_what': 'O que é',
        'f_page': 'Página', 'f_page_d': 'Domínio onde as regras se aplicam, ex.: <code>discord.com</code>. Os subdomínios também correspondem.',
        'f_key': 'Chave', 'f_key_d': 'Regex que identifica o texto a substituir. Validada enquanto escreve.',
        'f_value': 'Valor', 'f_value_d': 'Mensagem enviada ao Claude (parâmetro <code>q</code>). Aceita <code>$1</code>, <code>$2</code>… dos grupos da chave.',
        'f_folder': 'Pasta', 'f_folder_d': 'Opcional. Pasta onde a sessão abre. Vazio = pasta predefinida do Claude Desktop.',
        'f_run': '▶', 'f_run_d': 'Aplica a regra de imediato no separador aberto, sem guardar, e indica quantos trechos passaram a ligação.',
        'example_label': 'Exemplo de regra', 'ex_key': 'chave', 'ex_value': 'valor', 'ex_link': 'link ',
        'ex_regex': '/(triagem|abrir-pedido)\\s+([A-Z][A-Z0-9]*-\\d+)', 'ex_q': 'Executa a skill $1 na $2',
        'lim_kicker': '// limitações', 'lim_title': 'Bom saber',
        'lim_sub': 'Comportamentos do Claude Desktop e dos sites que moldaram a extensão.',
        'lim1': '<strong>Comandos com barra não funcionam no valor.</strong> O Claude Desktop substitui a barra inicial do <code>q</code> por outro carácter, por isso o texto não é um comando. Peça a skill por texto: “Executa a skill X na Y”.',
        'lim2': '<strong>O Discord não aceita estas ligações na mensagem.</strong> Só torna clicáveis as que começam por <code>http(s)</code>. Por isso a substituição acontece no navegador.',
        'lim3': '<strong>Confirmação na primeira vez.</strong> O navegador pergunta se pode abrir o Claude ao clicar na primeira ligação <code>claude://</code>.',
        'privacy': 'Política de privacidade',
        'pv_title': 'Política de privacidade',
        'pv_lead': 'A Claude Links não recolhe, não envia e não vende quaisquer dados. Tudo o que utiliza fica no seu navegador.',
        'pv_store_l': 'O que a extensão guarda',
        'pv_store': 'Apenas a configuração que introduz no popup: os domínios das páginas e as regras (chave, valor e pasta). Fica no <code>chrome.storage.sync</code> do navegador, que o próprio navegador pode sincronizar entre os seus dispositivos quando tem sessão iniciada. A extensão não tem servidor e não envia esta configuração para lado nenhum.',
        'pv_read_l': 'O que lê nas páginas',
        'pv_read': 'Corre apenas nos domínios que adicionou e autorizou. Nessas páginas, procura no texto visível os trechos que correspondem às suas regras e transforma-os em ligações. O texto da página não é guardado nem enviado.',
        'pv_click_l': 'Quando clica numa ligação',
        'pv_click': 'A ligação <code>claude://</code> é entregue ao sistema operativo, que abre o Claude Desktop instalado no seu computador com a mensagem preenchida. A partir daí aplica-se a política de privacidade do Claude. A extensão não participa nessa conversa.',
        'pv_perm_l': 'Permissões', 'th_perm': 'Permissão', 'th_why': 'Para quê',
        'pv_storage': 'Guardar a sua configuração.',
        'pv_active': 'Preencher o domínio do separador atual quando clica em + no popup.',
        'pv_scripting': 'Ativar a substituição de textos apenas nos domínios adicionados e executar uma regra de imediato com o ▶.',
        'pv_hosts_n': 'Acesso a sites (opcional)',
        'pv_hosts': 'Pedido um a um, quando guarda uma página. Sem a sua autorização, a extensão não corre no site.',
        'pv_contact_l': 'Contacto',
        'pv_contact': 'Dúvidas ou problemas: abra uma issue em <a href="{repo}/issues">github.com/correaschneider/claude-links-extension</a>.',
        'pv_updated': 'Atualizada a 3 de novembro de 2026',
    },
    'es': {
        'description': 'Extensión para Chrome/Brave que convierte textos de una página en enlaces que abren una sesión en Claude Desktop con el mensaje listo.',
        'nav_how': 'Cómo funciona', 'nav_install': 'Instalación', 'nav_config': 'Configuración',
        'hero_kicker': '// extensión chrome · brave',
        'hero_title': 'Del texto en la página a una sesión de Claude, en un clic.',
        'hero_lead': 'Claude Links encuentra textos que defines con una regex y los convierte en enlaces que abren una nueva sesión en la pestaña Code de Claude Desktop, con el mensaje ya escrito.',
        'btn_github': 'Ver en GitHub', 'btn_install': 'Instalar',
        'how_kicker': '// cómo funciona', 'how_title': 'Un aviso se convierte en atajo',
        'how_sub': 'Una automatización publica en Discord un aviso con un comando en texto. Con una regla configurada, el comando se convierte en enlace; el clic abre Claude con la petición lista.',
        'before': 'Antes · texto plano', 'after': 'Después · enlace',
        'task_title': '[TASK-123] Error al enviar el mensaje', 'task_line': 'Hacer el triaje con',
        'cmd': '/triaje TASK-123', 'composer_label': 'Claude Desktop · nueva sesión',
        'composer': 'Ejecuta la skill triaje en TASK-123',
        's1_t': 'Encuentra', 's1_p': 'El script se ejecuta en las páginas que añadiste y sigue el contenido que va llegando, como los mensajes nuevos de Discord.',
        's2_t': 'Sustituye', 's2_p': 'Cada coincidencia de una regla se convierte en un enlace <code>claude://code/new</code>, construido con el valor y la carpeta de la regla.',
        's3_t': 'Abre', 's3_p': 'El clic abre una sesión de Claude Desktop con el mensaje escrito. No se envía nada solo: lo revisas y pulsas Enter.',
        'inst_kicker': '// instalación', 'inst_title': 'Cargar en el navegador',
        'inst_sub': 'Mientras no esté en Chrome Web Store, la extensión se carga desde el código fuente.',
        'steps_label': 'Paso a paso',
        'inst_steps': ['Descarga o clona el <a href="{repo}">repositorio</a>.', 'Abre <code>brave://extensions</code> o <code>chrome://extensions</code>.', 'Activa el <strong>Modo de desarrollador</strong>.', 'Haz clic en <strong>Cargar descomprimida</strong> y elige la carpeta.', 'Fija el icono de la extensión en la barra.'],
        'term_label': 'Desde la terminal', 'term_clone': '# clona el código', 'term_after': '# después de cambiar archivos:', 'term_reload': '# ↻ en la extensión + recargar la pestaña',
        'cfg_kicker': '// configuración', 'cfg_title': 'Reglas por página',
        'cfg_sub': 'Haz clic en el icono de la extensión para ver la lista de páginas. El botón <strong>+</strong> añade una nueva, con el dominio de la pestaña actual ya rellenado. Al guardar, el navegador pide permiso para que la extensión se ejecute en ese sitio; sin él, la extensión no toca la página.',
        'th_field': 'Campo', 'th_what': 'Qué es',
        'f_page': 'Página', 'f_page_d': 'Dominio donde se aplican las reglas, p. ej. <code>discord.com</code>. Los subdominios también coinciden.',
        'f_key': 'Clave', 'f_key_d': 'Regex que encuentra el texto a sustituir. Se valida mientras escribes.',
        'f_value': 'Valor', 'f_value_d': 'Mensaje que se envía a Claude (parámetro <code>q</code>). Acepta <code>$1</code>, <code>$2</code>… de los grupos de la clave.',
        'f_folder': 'Carpeta', 'f_folder_d': 'Opcional. Carpeta donde se abre la sesión. Vacío = carpeta predeterminada de Claude Desktop.',
        'f_run': '▶', 'f_run_d': 'Aplica la regla al momento en la pestaña abierta, sin guardar, e indica cuántas coincidencias se convirtieron en enlaces.',
        'example_label': 'Ejemplo de regla', 'ex_key': 'clave', 'ex_value': 'valor', 'ex_link': 'enlace',
        'ex_regex': '/(triaje|abrir-ticket)\\s+([A-Z][A-Z0-9]*-\\d+)', 'ex_q': 'Ejecuta la skill $1 en $2',
        'lim_kicker': '// limitaciones', 'lim_title': 'Conviene saber',
        'lim_sub': 'Comportamientos de Claude Desktop y de los sitios que dieron forma a la extensión.',
        'lim1': '<strong>Los comandos con barra no funcionan en el valor.</strong> Claude Desktop reemplaza la barra inicial de <code>q</code> por otro carácter, así que el texto no es un comando. Pide la skill con texto: “Ejecuta la skill X en Y”.',
        'lim2': '<strong>Discord no acepta estos enlaces en un mensaje.</strong> Solo hace clicables los que empiezan por <code>http(s)</code>. Por eso la sustitución ocurre en el navegador.',
        'lim3': '<strong>Confirmación la primera vez.</strong> El navegador pregunta si puede abrir Claude al hacer clic en el primer enlace <code>claude://</code>.',
        'privacy': 'Política de privacidad',
        'pv_title': 'Política de privacidad',
        'pv_lead': 'Claude Links no recopila, no envía ni vende ningún dato. Todo lo que usa se queda en tu navegador.',
        'pv_store_l': 'Qué guarda la extensión',
        'pv_store': 'Solo la configuración que introduces en el popup: los dominios de las páginas y las reglas (clave, valor y carpeta). Se guarda en <code>chrome.storage.sync</code> del navegador, que el propio navegador puede sincronizar entre tus dispositivos cuando has iniciado sesión. La extensión no tiene servidor y no envía esta configuración a ningún sitio.',
        'pv_read_l': 'Qué lee en las páginas',
        'pv_read': 'Solo se ejecuta en los dominios que añadiste y autorizaste. En esas páginas, busca en el texto visible los fragmentos que coinciden con tus reglas y los convierte en enlaces. El texto de la página no se guarda ni se envía.',
        'pv_click_l': 'Cuando haces clic en un enlace',
        'pv_click': 'El enlace <code>claude://</code> se entrega al sistema operativo, que abre el Claude Desktop instalado en tu ordenador con el mensaje rellenado. A partir de ahí se aplica la política de privacidad de Claude. La extensión no participa en esa conversación.',
        'pv_perm_l': 'Permisos', 'th_perm': 'Permiso', 'th_why': 'Para qué',
        'pv_storage': 'Guardar tu configuración.',
        'pv_active': 'Rellenar el dominio de la pestaña actual al hacer clic en + en el popup.',
        'pv_scripting': 'Activar la sustitución de textos solo en los dominios añadidos y ejecutar una regla al momento con ▶.',
        'pv_hosts_n': 'Acceso a sitios (opcional)',
        'pv_hosts': 'Se pide uno a uno, al guardar una página. Sin tu autorización, la extensión no se ejecuta en el sitio.',
        'pv_contact_l': 'Contacto',
        'pv_contact': 'Dudas o problemas: abre una issue en <a href="{repo}/issues">github.com/correaschneider/claude-links-extension</a>.',
        'pv_updated': 'Actualizada el 3 de noviembre de 2026',
    },
    'it': {
        'description': 'Estensione per Chrome/Brave che trasforma i testi di una pagina in link che aprono una sessione di Claude Desktop con il messaggio pronto.',
        'nav_how': 'Come funziona', 'nav_install': 'Installazione', 'nav_config': 'Configurazione',
        'hero_kicker': '// estensione chrome · brave',
        'hero_title': 'Dal testo nella pagina a una sessione di Claude, con un clic.',
        'hero_lead': 'Claude Links trova i testi che definisci con una regex e li trasforma in link che aprono una nuova sessione nella scheda Code di Claude Desktop, con il messaggio già scritto.',
        'btn_github': 'Vedi su GitHub', 'btn_install': 'Installa',
        'how_kicker': '// come funziona', 'how_title': 'Un avviso diventa una scorciatoia',
        'how_sub': 'Un’automazione pubblica su Discord un avviso con un comando in testo. Con una regola impostata, il comando diventa un link; il clic apre Claude con la richiesta pronta.',
        'before': 'Prima · testo semplice', 'after': 'Dopo · link',
        'task_title': '[TASK-123] Errore nell’invio del messaggio', 'task_line': 'Fare il triage con',
        'cmd': '/triage TASK-123', 'composer_label': 'Claude Desktop · nuova sessione',
        'composer': 'Esegui la skill triage su TASK-123',
        's1_t': 'Trova', 's1_p': 'Lo script viene eseguito sulle pagine aggiunte e segue i contenuti che arrivano, come i nuovi messaggi di Discord.',
        's2_t': 'Sostituisce', 's2_p': 'Ogni corrispondenza di una regola diventa un link <code>claude://code/new</code>, costruito con il valore e la cartella della regola.',
        's3_t': 'Apre', 's3_p': 'Il clic apre una sessione di Claude Desktop con il messaggio scritto. Nulla viene inviato da solo: lo controlli e premi Invio.',
        'inst_kicker': '// installazione', 'inst_title': 'Caricarla nel browser',
        'inst_sub': 'Finché non è sul Chrome Web Store, l’estensione si carica dal codice sorgente.',
        'steps_label': 'Passo dopo passo',
        'inst_steps': ['Scarica o clona il <a href="{repo}">repository</a>.', 'Apri <code>brave://extensions</code> o <code>chrome://extensions</code>.', 'Attiva la <strong>Modalità sviluppatore</strong>.', 'Clicca su <strong>Carica estensione non pacchettizzata</strong> e scegli la cartella.', 'Fissa l’icona dell’estensione nella barra.'],
        'term_label': 'Dal terminale', 'term_clone': '# clona il codice', 'term_after': '# dopo aver modificato i file:', 'term_reload': '# ↻ sull’estensione + ricarica la scheda',
        'cfg_kicker': '// configurazione', 'cfg_title': 'Regole per pagina',
        'cfg_sub': 'Clicca sull’icona dell’estensione per vedere l’elenco delle pagine. Il pulsante <strong>+</strong> ne aggiunge una nuova con il dominio della scheda corrente già compilato. Quando salvi, il browser chiede il permesso perché l’estensione funzioni su quel sito; senza, l’estensione non tocca la pagina.',
        'th_field': 'Campo', 'th_what': 'Che cos’è',
        'f_page': 'Pagina', 'f_page_d': 'Dominio in cui valgono le regole, ad es. <code>discord.com</code>. Anche i sottodomini corrispondono.',
        'f_key': 'Chiave', 'f_key_d': 'Regex che trova il testo da sostituire. Validata mentre scrivi.',
        'f_value': 'Valore', 'f_value_d': 'Messaggio inviato a Claude (parametro <code>q</code>). Accetta <code>$1</code>, <code>$2</code>… dai gruppi della chiave.',
        'f_folder': 'Cartella', 'f_folder_d': 'Facoltativa. Cartella in cui si apre la sessione. Vuota = cartella predefinita di Claude Desktop.',
        'f_run': '▶', 'f_run_d': 'Applica subito la regola alla scheda aperta, senza salvare, e indica quante corrispondenze sono diventate link.',
        'example_label': 'Esempio di regola', 'ex_key': 'chiave', 'ex_value': 'valore', 'ex_link': 'link  ',
        'ex_regex': '/(triage|apri-ticket)\\s+([A-Z][A-Z0-9]*-\\d+)', 'ex_q': 'Esegui la skill $1 su $2',
        'lim_kicker': '// limitazioni', 'lim_title': 'Da sapere',
        'lim_sub': 'Comportamenti di Claude Desktop e dei siti che hanno dato forma all’estensione.',
        'lim1': '<strong>I comandi con la barra non funzionano nel valore.</strong> Claude Desktop sostituisce la barra iniziale di <code>q</code> con un altro carattere, quindi il testo non è un comando. Chiedi la skill a parole: “Esegui la skill X su Y”.',
        'lim2': '<strong>Discord non accetta questi link in un messaggio.</strong> Rende cliccabili solo quelli che iniziano con <code>http(s)</code>. Per questo la sostituzione avviene nel browser.',
        'lim3': '<strong>Conferma la prima volta.</strong> Il browser chiede se può aprire Claude quando clicchi sul primo link <code>claude://</code>.',
        'privacy': 'Informativa sulla privacy',
        'pv_title': 'Informativa sulla privacy',
        'pv_lead': 'Claude Links non raccoglie, non invia e non vende alcun dato. Tutto ciò che usa resta nel tuo browser.',
        'pv_store_l': 'Cosa salva l’estensione',
        'pv_store': 'Solo la configurazione che inserisci nel popup: i domini delle pagine e le regole (chiave, valore e cartella). Si trova in <code>chrome.storage.sync</code> del browser, che il browser stesso può sincronizzare tra i tuoi dispositivi quando hai effettuato l’accesso. L’estensione non ha un server e non invia questa configurazione da nessuna parte.',
        'pv_read_l': 'Cosa legge nelle pagine',
        'pv_read': 'Funziona solo sui domini che hai aggiunto e autorizzato. In quelle pagine cerca nel testo visibile i frammenti che corrispondono alle tue regole e li trasforma in link. Il testo della pagina non viene salvato né inviato.',
        'pv_click_l': 'Quando clicchi su un link',
        'pv_click': 'Il link <code>claude://</code> viene passato al sistema operativo, che apre il Claude Desktop installato sul tuo computer con il messaggio compilato. Da quel momento si applica l’informativa sulla privacy di Claude. L’estensione non partecipa a quella conversazione.',
        'pv_perm_l': 'Permessi', 'th_perm': 'Permesso', 'th_why': 'A cosa serve',
        'pv_storage': 'Salvare la tua configurazione.',
        'pv_active': 'Compilare il dominio della scheda corrente quando clicchi su + nel popup.',
        'pv_scripting': 'Attivare la sostituzione dei testi solo sui domini aggiunti ed eseguire subito una regola con ▶.',
        'pv_hosts_n': 'Accesso ai siti (facoltativo)',
        'pv_hosts': 'Richiesto uno alla volta, quando salvi una pagina. Senza la tua autorizzazione, l’estensione non funziona sul sito.',
        'pv_contact_l': 'Contatti',
        'pv_contact': 'Domande o problemi: apri una issue su <a href="{repo}/issues">github.com/correaschneider/claude-links-extension</a>.',
        'pv_updated': 'Aggiornata il 3 novembre 2026',
    },
}

PAGE = """<!doctype html>
<html lang="{lang_attr}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{alternates}
<link rel="icon" type="image/svg+xml" href="{root}icon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,600;0,700;1,500&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>

<header class="appbar">
  <div class="inner">
    <a class="brand" href="{home}"><img src="{root}icon.svg" alt="" width="28" height="28" style="vertical-align:middle;margin-right:10px;border-radius:5px">Claude Links</a>
    <nav>
      <a href="{home}#how">{nav_how}</a>
      <a href="{home}#install">{nav_install}</a>
      <a href="{home}#config">{nav_config}</a>
      <a href="{repo}">GitHub</a>
    </nav>
    <details class="lang">
      <summary aria-label="Language">{lang_name} ▾</summary>
      <ul>{lang_menu}</ul>
    </details>
  </div>
</header>

{body}

<footer>
  <div class="container">
    <span class="stack"><a href="{privacy_url}">{privacy}</a> · Manifest V3 · JavaScript · chrome.storage · claude:// deep links</span>
    <a href="{repo}">correaschneider/claude-links-extension</a>
  </div>
</footer>

</body>
</html>
"""

INDEX = """<div class="hero">
  <div class="container">
    <p class="kicker">{hero_kicker}</p>
    <h1>{hero_title}</h1>
    <p class="lead">{hero_lead}</p>
    <div class="actions">
      <a class="btn btn-contained" href="{repo}">{btn_github}</a>
      <a class="btn btn-outlined" href="#install">{btn_install}</a>
    </div>
  </div>
</div>

<main>
  <section id="how">
    <div class="container">
      <p class="kicker">{how_kicker}</p>
      <h2>{how_title}</h2>
      <p class="section-sub">{how_sub}</p>

      <div class="compare">
        <div class="paper">
          <p class="label">{before}</p>
          <div class="rule-line rule-before"></div>
          <p class="msg"><b>{task_title}</b></p>
          <p class="msg">{task_line} <span class="plain">{cmd}</span></p>
        </div>
        <div class="arrow" aria-hidden="true">→</div>
        <div class="paper">
          <p class="label">{after}</p>
          <div class="rule-line rule-after"></div>
          <p class="msg"><b>{task_title}</b></p>
          <p class="msg">{task_line} <span class="fake-link">{cmd}</span></p>
          <div class="composer"><small>{composer_label}</small>{composer}</div>
        </div>
      </div>

      <div class="steps" style="margin-top:32px">
        <div class="paper step"><h3>{s1_t}</h3><p>{s1_p}</p></div>
        <div class="paper step"><h3>{s2_t}</h3><p>{s2_p}</p></div>
        <div class="paper step"><h3>{s3_t}</h3><p>{s3_p}</p></div>
      </div>
    </div>
  </section>

  <section id="install">
    <div class="container">
      <p class="kicker">{inst_kicker}</p>
      <h2>{inst_title}</h2>
      <p class="section-sub">{inst_sub}</p>
      <div class="two">
        <div class="paper">
          <p class="label">{steps_label}</p>
          <div class="rule-line rule-after"></div>
          <ol class="install">{inst_list}</ol>
        </div>
        <div class="paper">
          <p class="label">{term_label}</p>
          <div class="rule-line rule-after"></div>
          <pre><span class="c">{term_clone}</span>
git clone {repo}.git

<span class="c">{term_after}</span>
<span class="c">{term_reload}</span></pre>
        </div>
      </div>
    </div>
  </section>

  <section id="config">
    <div class="container">
      <p class="kicker">{cfg_kicker}</p>
      <h2>{cfg_title}</h2>
      <p class="section-sub">{cfg_sub}</p>

      <div class="paper table-wrap">
        <table>
          <thead><tr><th>{th_field}</th><th>{th_what}</th></tr></thead>
          <tbody>
            <tr><td>{f_page}</td><td>{f_page_d}</td></tr>
            <tr><td>{f_key}</td><td>{f_key_d}</td></tr>
            <tr><td>{f_value}</td><td>{f_value_d}</td></tr>
            <tr><td>{f_folder}</td><td>{f_folder_d}</td></tr>
            <tr><td>{f_run}</td><td>{f_run_d}</td></tr>
          </tbody>
        </table>
      </div>

      <div class="paper" style="margin-top:20px">
        <p class="label">{example_label}</p>
        <div class="rule-line rule-after"></div>
        <pre><span class="c">{ex_key}</span>  {ex_regex_html}
<span class="c">{ex_value}</span>  {ex_q_html}
<span class="c">{ex_link}</span>  {ex_url}</pre>
      </div>
    </div>
  </section>

  <section id="limits">
    <div class="container">
      <p class="kicker">{lim_kicker}</p>
      <h2>{lim_title}</h2>
      <p class="section-sub">{lim_sub}</p>
      <div class="alerts">
        <div class="alert"><span class="ico">/</span><p>{lim1}</p></div>
        <div class="alert"><span class="ico">#</span><p>{lim2}</p></div>
        <div class="alert"><span class="ico">!</span><p>{lim3}</p></div>
      </div>
    </div>
  </section>
</main>"""

PRIVACY = """<div class="hero">
  <div class="container">
    <p class="kicker">// privacy</p>
    <h1>{pv_title}</h1>
    <p class="lead">{pv_lead}</p>
  </div>
</div>
<main>
  <section>
    <div class="container">
      <div class="paper">
        <p class="label">{pv_store_l}</p>
        <div class="rule-line rule-after"></div>
        <p>{pv_store}</p>
      </div>
      <div class="paper" style="margin-top:20px">
        <p class="label">{pv_read_l}</p>
        <div class="rule-line rule-after"></div>
        <p>{pv_read}</p>
      </div>
      <div class="paper" style="margin-top:20px">
        <p class="label">{pv_click_l}</p>
        <div class="rule-line rule-after"></div>
        <p>{pv_click}</p>
      </div>
      <div class="paper" style="margin-top:20px">
        <p class="label">{pv_perm_l}</p>
        <div class="rule-line rule-after"></div>
        <div class="table-wrap"><table>
          <thead><tr><th>{th_perm}</th><th>{th_why}</th></tr></thead>
          <tbody>
            <tr><td>storage</td><td>{pv_storage}</td></tr>
            <tr><td>activeTab</td><td>{pv_active}</td></tr>
            <tr><td>scripting</td><td>{pv_scripting}</td></tr>
            <tr><td>{pv_hosts_n}</td><td>{pv_hosts}</td></tr>
          </tbody>
        </table></div>
      </div>
      <div class="paper" style="margin-top:20px">
        <p class="label">{pv_contact_l}</p>
        <div class="rule-line rule-after"></div>
        <p>{pv_contact}</p>
        <p class="label" style="margin-top:16px">{pv_updated}</p>
      </div>
    </div>
  </section>
</main>"""


def url_for(code, page):
    folder = LANGS[code][0]
    return f"{SITE}{folder + '/' if folder else ''}{page}"


def render(code, page):
    folder, name, lang_attr = LANGS[code]
    t = dict(T[code])
    root = '../' if folder else ''
    file = 'index.html' if page == 'index' else 'privacy.html'

    def rel(other):
        other_folder = LANGS[other][0]
        return root + (other_folder + '/' if other_folder else '') + ('' if page == 'index' else file)

    current = ' aria-current="page"'
    lang_menu = ''.join(
        f'<li><a href="{rel(c) or "./"}" hreflang="{LANGS[c][2]}"'
        f'{current if c == code else ""}>{LANGS[c][1]}</a></li>'
        for c in LANGS
    )
    alternates = '\n'.join(
        f'<link rel="alternate" hreflang="{LANGS[c][2]}" href="{url_for(c, "" if page == "index" else file)}">'
        for c in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{url_for("en", "" if page == "index" else file)}">'

    t.update(repo=REPO)
    if page == 'index':
        t['inst_list'] = ''.join(f'<li>{s.format(repo=REPO)}</li>' for s in t['inst_steps'])
        t['ex_regex_html'] = escape(t['ex_regex'])
        t['ex_q_html'] = escape(t['ex_q'])
        sample = t['composer']
        t['ex_url'] = 'claude://code/new?q=' + quote(sample, safe='')
        body = INDEX.format(**t)
        title = 'Claude Links'
    else:
        t['pv_contact'] = t['pv_contact'].format(repo=REPO)
        body = PRIVACY.format(**t)
        title = f"Claude Links · {t['pv_title']}"

    home = './'  # index e privacy de cada idioma ficam na mesma pasta
    html = PAGE.format(
        lang_attr=lang_attr, title=title, description=escape(t['description']),
        alternates=alternates, root=root, home=home, repo=REPO,
        nav_how=t['nav_how'], nav_install=t['nav_install'], nav_config=t['nav_config'],
        lang_name=name, lang_menu=lang_menu, body=body,
        privacy_url='privacy.html',
        privacy=t['privacy'],
    )
    out = DOCS / folder / file if folder else DOCS / file
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    return out.relative_to(DOCS)


def main():
    for code in LANGS:
        for page in ('index', 'privacy'):
            print(render(code, page))


if __name__ == '__main__':
    main()
