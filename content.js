// Troca textos configurados (regex) por links claude://code/new, que abrem uma
// sessão nova na aba Code do Claude Desktop com o pedido já digitado (sem enviar).
// A config fica em chrome.storage.sync (página de opções); padrão em defaults.js.

const MARK = 'data-claude-link';

function hostMatches(page) {
  const host = location.hostname;
  return host === page || host.endsWith(`.${page}`);
}

function buildLink(rule, m) {
  const q = rule.q.replace(/\$(\d+)/g, (_, n) => m[n] ?? '');
  let url = `claude://code/new?q=${encodeURIComponent(q)}`;
  // Sem folder, o Desktop abre na pasta padrão.
  if (rule.folder) url += `&folder=${encodeURIComponent(rule.folder)}`;
  return url;
}

function compile(rules) {
  return rules.flatMap((r) => {
    try {
      return [{ ...r, re: new RegExp(r.match, 'g') }];
    } catch (e) {
      console.warn('[Claude Links] regex inválida, ignorada:', r.match, e);
      return [];
    }
  });
}

function makeAnchor(text, href) {
  const a = document.createElement('a');
  a.href = href;
  a.textContent = text;
  a.title = 'Abrir no Claude';
  a.setAttribute(MARK, '');
  a.style.cssText = 'color:#00a8fc;text-decoration:underline;cursor:pointer';
  // Sites como o Discord interceptam cliques em links; abre o esquema direto.
  a.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    window.location.href = href;
  }, true);
  return a;
}

// Acha a primeira ocorrência de qualquer regra a partir de `from`.
function nextMatch(rules, text, from) {
  let best = null;
  for (const rule of rules) {
    rule.re.lastIndex = from;
    const m = rule.re.exec(text);
    if (m && m[0] && (!best || m.index < best.m.index)) best = { rule, m };
  }
  return best;
}

function linkify(rules, textNode) {
  const text = textNode.nodeValue;
  let hit = nextMatch(rules, text, 0);
  if (!hit) return;

  const frag = document.createDocumentFragment();
  let last = 0;
  while (hit) {
    const { rule, m } = hit;
    frag.append(text.slice(last, m.index));
    frag.append(makeAnchor(m[0], buildLink(rule, m)));
    last = m.index + m[0].length;
    hit = nextMatch(rules, text, last);
  }
  frag.append(text.slice(last));
  textNode.replaceWith(frag);
}

function scan(rules, root) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const p = node.parentElement;
      if (!p || p.closest(`a, [${MARK}], [contenteditable="true"], textarea, input, script, style`)) {
        return NodeFilter.FILTER_REJECT;
      }
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach((n) => linkify(rules, n));
}

chrome.storage.sync.get({ config: DEFAULT_CONFIG }, ({ config }) => {
  const rules = compile(
    config.filter((p) => hostMatches(p.page)).flatMap((p) => p.replacements || []),
  );
  if (!rules.length) return;

  scan(rules, document.body);

  // Páginas como o Discord montam o conteúdo dinamicamente.
  new MutationObserver((mutations) => {
    for (const mut of mutations) {
      for (const node of mut.addedNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) scan(rules, node);
        else if (node.nodeType === Node.TEXT_NODE && node.parentElement) scan(rules, node.parentElement);
      }
    }
  }).observe(document.body, { childList: true, subtree: true });
});
