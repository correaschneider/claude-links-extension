const $ = (id) => document.getElementById(id);
const tplRep = $('tpl-rep');

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
    count.textContent = `${n} substituiç${n === 1 ? 'ão' : 'ões'}`;
    li.append(host, count);
    granted(p.page).then((ok) => {
      if (ok) return;
      const warn = document.createElement('span');
      warn.className = 'no-perm';
      warn.textContent = 'sem permissão';
      warn.title = 'Abra a página e clique em Salvar para permitir a extensão neste site.';
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

// Valida a chave enquanto digita; devolve o RegExp ou null.
function checkMatch(row) {
  const input = row.querySelector('.match');
  const msg = row.querySelector('.row-msg');
  const value = input.value.trim();
  let re = null;
  let error = '';
  if (value) {
    try { re = new RegExp(value); } catch (e) { error = `Regex inválida: ${e.message}`; }
  }
  input.classList.toggle('invalid', Boolean(error));
  msg.textContent = error;
  msg.hidden = !error;
  return re;
}

function rowRule(row) {
  return {
    q: row.querySelector('.q').value.trim(),
    folder: row.querySelector('.folder').value.trim(),
  };
}

// Abre o deep link pela aba atual: o navegador entrega o claude:// ao sistema
// sem sair da página.
function openLink(url) {
  chrome.tabs.update({ url }).catch(() => { window.location.href = url; });
}

// Preenche $1, $2… a partir do texto de exemplo e mostra o que casou.
function testSample(row) {
  const re = checkMatch(row);
  const result = row.querySelector('.result');
  const sample = row.querySelector('.sample').value;
  const m = re && sample ? sample.match(re) : null;
  result.textContent = !sample ? '' : m ? `casou: ${m[0]}` : 'não casou com a chave';
  return m;
}

function runRep(row) {
  const rule = rowRule(row);
  if (!rule.q) {
    row.querySelector('.q').classList.add('invalid');
    row.querySelector('.q').focus();
    return;
  }
  row.querySelector('.q').classList.remove('invalid');
  const test = row.querySelector('.row-test');
  // Sem $n, abre direto; com $n, pede um texto de exemplo.
  if (!/\$\d/.test(rule.q)) {
    test.hidden = true;
    return openLink(buildLink(rule));
  }
  test.hidden = !test.hidden;
  if (!test.hidden) row.querySelector('.sample').focus();
}

function addRep(r = {}) {
  const row = tplRep.content.firstElementChild.cloneNode(true);
  row.querySelector('.match').value = r.match || '';
  row.querySelector('.q').value = r.q || '';
  row.querySelector('.folder').value = r.folder || '';
  row.querySelector('.match').addEventListener('input', () => { checkMatch(row); testSample(row); });
  row.querySelector('.sample').addEventListener('input', () => testSample(row));
  row.querySelector('.run-rep').addEventListener('click', () => runRep(row));
  row.querySelector('.run-sample').addEventListener('click', () => {
    const m = testSample(row);
    if (m) openLink(buildLink(rowRule(row), m));
  });
  row.querySelector('.del-rep').addEventListener('click', () => row.remove());
  $('reps').append(row);
  checkMatch(row);
}

function openForm(index, host = '') {
  editing = index;
  const p = index >= 0 ? config[index] : { page: host, replacements: [] };
  $('form-title').textContent = index >= 0 ? p.page : 'Nova página';
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
  if (!page) fail($('host'), 'falta o domínio da página');

  const replacements = [...$('reps').querySelectorAll('.rep')].flatMap((row) => {
    const [mEl, qEl, fEl] = ['.match', '.q', '.folder'].map((s) => row.querySelector(s));
    const match = mEl.value.trim();
    const q = qEl.value.trim();
    const folder = fEl.value.trim();
    if (!match && !q && !folder) return []; // linha vazia é ignorada
    if (!match) fail(mEl, 'falta a chave');
    if (!q) fail(qEl, 'falta o valor');
    if (!checkMatch(row)) fail(mEl, 'regex inválida na chave');
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
    return show(`Não salvei: ${e.message}`, false);
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
  if (editing < 0 || !confirm(`Deletar ${config[editing].page}?`)) return;
  const [removed] = config.splice(editing, 1);
  releaseIfUnused(removed.page);
  persist(showList);
});

chrome.storage.sync.get({ config: DEFAULT_CONFIG }, (data) => {
  config = data.config;
  showList();
});
