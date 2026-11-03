const $ = (id) => document.getElementById(id);
const tplRep = $('tpl-rep');

// Texto traduzido (_locales); {0}, {1}… recebem os argumentos.
function t(key, ...args) {
  const text = chrome.i18n.getMessage(key) || key;
  return text.replace(/\{(\d)\}/g, (_, i) => args[i] ?? '');
}

// Traduz o HTML: data-i18n (texto), data-i18n-title, data-i18n-placeholder.
function translate(root) {
  root.querySelectorAll('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
  root.querySelectorAll('[data-i18n-title]').forEach((el) => { el.title = t(el.dataset.i18nTitle); });
  root.querySelectorAll('[data-i18n-placeholder]').forEach((el) => { el.placeholder = t(el.dataset.i18nPlaceholder); });
}

let config = [];
let editing = -1; // índice da página no formulário; -1 = nova

function show(msg, ok) {
  $('status').textContent = msg;
  $('status').className = ok ? 'ok' : 'err';
}

function persist(done) {
  chrome.storage.sync.set({ config }, done);
}

function originsFor(page) {
  return [`*://${page}/*`, `*://*.${page}/*`];
}

// Páginas sem permissão concedida aparecem marcadas na lista.
async function granted(page) {
  try {
    return await chrome.permissions.contains({ origins: originsFor(page) });
  } catch {
    return false;
  }
}

// ---- Listagem ----

function renderList() {
  const list = $('list');
  list.replaceChildren();
  config.forEach((p, i) => {
    const li = document.createElement('li');
    li.className = 'item';
    const host = document.createElement('span');
    host.className = 'host';
    host.textContent = p.page;
    const count = document.createElement('span');
    count.className = 'count';
    const n = (p.replacements || []).length;
    count.textContent = n === 1 ? t('countOne') : t('countMany', n);
    li.append(host, count);
    granted(p.page).then((ok) => {
      if (ok) return;
      const warn = document.createElement('span');
      warn.className = 'no-perm';
      warn.textContent = t('noPerm');
      warn.title = t('noPermTitle');
      host.after(warn);
    });
    li.addEventListener('click', () => openForm(i));
    list.append(li);
  });
  $('empty').hidden = config.length > 0;
}

function showList() {
  $('view-form').hidden = true;
  $('view-list').hidden = false;
  renderList();
}

// ---- Formulário ----

// Mensagem abaixo da linha: erro (escuro) ou resultado do ▶ (neutro).
// Trechos entre `crases` viram <code>.
function rowMessage(row, text, isError) {
  const msg = row.querySelector('.row-msg');
  msg.replaceChildren(...text.split('`').map((part, i) => {
    if (i % 2 === 0) return part;
    const code = document.createElement('code');
    code.textContent = part;
    return code;
  }));
  msg.classList.toggle('info', !isError);
  msg.hidden = !text;
}

// O erro nativo repete a regex entre barras (/…/) e fica confuso; fica só o
// motivo, traduzido quando é um dos casos comuns.
const REGEX_ERRORS = [
  [/\\ at end of pattern/, 'reBackslash'],
  [/Unterminated group/, 'reGroupOpen'],
  [/Unmatched '\)'/, 'reGroupClose'],
  [/Unterminated character class/, 'reClass'],
  [/Nothing to repeat/, 'reNothing'],
  [/numbers out of order/, 'reRangeNum'],
  [/Range out of order/, 'reRangeChar'],
  [/Invalid group/, 'reGroupInvalid'],
];

function regexError(e) {
  const reason = e.message.replace(/^Invalid regular expression: \/.*\/[a-z]*: /, '');
  const known = REGEX_ERRORS.find(([pattern]) => pattern.test(reason));
  return t('regexInvalid', known ? t(known[1]) : reason);
}

// Valida a chave enquanto digita; devolve o RegExp ou null.
function checkMatch(row) {
  const input = row.querySelector('.match');
  const value = input.value.trim();
  let re = null;
  let error = '';
  if (value) {
    try { re = new RegExp(value); } catch (e) { error = regexError(e); }
  }
  input.classList.toggle('invalid', Boolean(error));
  if (error) {
    rowMessage(row, error, true);
  } else {
    // `{,n}` é válido mas não repete nada: casa o texto "{,n}" literal.
    const loose = value.match(/(?<!\\)\{,(\d+)\}/);
    rowMessage(row, loose
      ? t('looseQuant', loose[0], loose[1])
      : '', false);
  }
  return re;
}

// Aplica só esta regra na aba aberta, sem salvar nem recarregar a página.
async function runOnPage(row) {
  const rule = {
    match: row.querySelector('.match').value.trim(),
    q: row.querySelector('.q').value.trim(),
    folder: row.querySelector('.folder').value.trim(),
  };
  if (!rule.match || !checkMatch(row)) return rowMessage(row, t('fillKey'), true);
  if (!rule.q) return rowMessage(row, t('fillValue'), true);
  if (!rule.folder) delete rule.folder;

  const page = $('host').value.trim();
  let tab;
  try {
    [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  } catch {
    tab = null;
  }
  let host = '';
  try { host = new URL(tab.url).hostname; } catch { /* aba sem URL legível */ }
  if (!host || !(host === page || host.endsWith(`.${page}`))) {
    return rowMessage(row, t('openTab', page || t('theDomain')), true);
  }

  try {
    const target = { tabId: tab.id };
    await chrome.scripting.executeScript({ target, files: ['link.js', 'linkify.js'] });
    const [{ result }] = await chrome.scripting.executeScript({
      target,
      // Além de aplicar, conta quantas vezes a chave casa no texto visível,
      // para explicar quando nada vira link.
      func: (r) => {
        const created = globalThis.ClaudeLinks.run([r]);
        const inText = (document.body.innerText.match(new RegExp(r.match, 'g')) || []).length;
        const linked = document.querySelectorAll('[data-claude-link]').length;
        return { created, inText, linked };
      },
      args: [rule],
    });
    const { created, inText, linked } = result;
    let text;
    if (created) text = created === 1 ? t('runOne') : t('runMany', created);
    else if (!inText) text = t('noMatch');
    else if (linked >= inText) text = t('allLinked', inText);
    else text = t('splitText', inText);
    rowMessage(row, text, !created && !inText);
  } catch (e) {
    rowMessage(row, t('runFailed', e.message), true);
  }
}

function addRep(r = {}) {
  const row = tplRep.content.firstElementChild.cloneNode(true);
  translate(row);
  row.querySelector('.match').value = r.match || '';
  row.querySelector('.q').value = r.q || '';
  row.querySelector('.folder').value = r.folder || '';
  row.querySelector('.match').addEventListener('input', () => checkMatch(row));
  row.querySelector('.run-rep').addEventListener('click', () => runOnPage(row));
  row.querySelector('.del-rep').addEventListener('click', () => row.remove());
  $('reps').append(row);
  checkMatch(row);
}

function openForm(index, host = '') {
  editing = index;
  const p = index >= 0 ? config[index] : { page: host, replacements: [] };
  $('form-title').textContent = index >= 0 ? p.page : t('newPage');
  $('host').value = p.page;
  $('reps').replaceChildren();
  (p.replacements.length ? p.replacements : [{}]).forEach(addRep);
  $('del-page').hidden = index < 0;
  show('', true);
  $('view-list').hidden = true;
  $('view-form').hidden = false;
  (index >= 0 || host ? $('reps').querySelector('.match') : $('host')).focus();
}

// Lê o formulário; marca o primeiro campo inválido e lança erro.
function collect() {
  document.querySelectorAll('#host, .q').forEach((i) => i.classList.remove('invalid'));
  const fail = (input, msg) => { input.classList.add('invalid'); input.focus(); throw new Error(msg); };

  const page = $('host').value.trim();
  if (!page) fail($('host'), t('errMissingDomain'));

  const replacements = [...$('reps').querySelectorAll('.rep')].flatMap((row) => {
    const [mEl, qEl, fEl] = ['.match', '.q', '.folder'].map((s) => row.querySelector(s));
    const match = mEl.value.trim();
    const q = qEl.value.trim();
    const folder = fEl.value.trim();
    if (!match && !q && !folder) return []; // linha vazia é ignorada
    if (!match) fail(mEl, t('errMissingKey'));
    if (!q) fail(qEl, t('errMissingValue'));
    if (!checkMatch(row)) fail(mEl, t('errInvalidKey'));
    return [folder ? { match, q, folder } : { match, q }];
  });
  return { page, replacements };
}

// Domínio da aba ativa (quando aberto pelo ícone da extensão); vazio se não der.
async function activeHost() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = new URL(tab && tab.url);
    return /^https?:$/.test(url.protocol) ? url.hostname.replace(/^www\./, '') : '';
  } catch {
    return '';
  }
}

// ---- Eventos ----

$('add-page').addEventListener('click', async () => openForm(-1, await activeHost()));
$('add-rep').addEventListener('click', () => addRep());
$('back').addEventListener('click', showList);

$('save').addEventListener('click', () => {
  let page;
  try {
    page = collect();
  } catch (e) {
    return show(t('notSaved', e.message), false);
  }
  // O pedido de permissão precisa sair no clique, antes de qualquer await.
  // Não esperamos a resposta para salvar: em alguns sistemas o popup fecha
  // quando o diálogo de permissão abre. O background registra o script
  // quando a permissão chega.
  chrome.permissions.request({ origins: originsFor(page.page) }).catch(() => {});
  const previous = editing >= 0 ? config[editing].page : null;
  if (editing >= 0) config[editing] = page;
  else config.push(page);
  if (previous && previous !== page.page) releaseIfUnused(previous);
  persist(showList);
});

// Devolve a permissão de um domínio que nenhuma página usa mais.
function releaseIfUnused(host) {
  if (config.some((p) => p.page === host)) return;
  chrome.permissions.remove({ origins: originsFor(host) }).catch(() => {});
}

$('del-page').addEventListener('click', () => {
  if (editing < 0 || !confirm(t('confirmDelete', config[editing].page))) return;
  const [removed] = config.splice(editing, 1);
  releaseIfUnused(removed.page);
  persist(showList);
});

translate(document);
document.documentElement.lang = chrome.i18n.getUILanguage();

chrome.storage.sync.get({ config: DEFAULT_CONFIG }, (data) => {
  config = data.config;
  showList();
});
