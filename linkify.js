// Núcleo da troca de textos por links claude://. Fica num objeto global
// (idempotente) porque é carregado pelo content script e também injetado pelo
// botão ▶ do popup na mesma aba; redeclarar const no topo quebraria.

globalThis.ClaudeLinks ??= (() => {
  const MARK = 'data-claude-link';
  // Nós de texto maiores que isso são ignorados: protege a aba de uma regex
  // com backtracking exponencial rodando sobre um texto longo de terceiros.
  const MAX_TEXT = 5000;

  function hostMatches(page) {
    const host = location.hostname;
    return host === page || host.endsWith(`.${page}`);
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

  function makeAnchor(text, href, prompt) {
    const a = document.createElement('a');
    a.href = href;
    a.textContent = text;
    // O título mostra o pedido completo, para conferir antes de clicar.
    a.title = `${chrome.i18n.getMessage('openInClaude')}:\n${prompt}`;
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

  // Troca as ocorrências num nó de texto; devolve quantos links criou.
  function linkify(rules, textNode) {
    const text = textNode.nodeValue;
    if (text.length > MAX_TEXT) return 0;
    let hit = nextMatch(rules, text, 0);
    if (!hit) return 0;

    const frag = document.createDocumentFragment();
    let last = 0;
    let count = 0;
    while (hit) {
      const { rule, m } = hit;
      frag.append(text.slice(last, m.index));
      frag.append(makeAnchor(m[0], buildLink(rule, m), buildPrompt(rule, m)));
      count++;
      last = m.index + m[0].length;
      hit = nextMatch(rules, text, last);
    }
    frag.append(text.slice(last));
    textNode.replaceWith(frag);
    return count;
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
    return nodes.reduce((n, node) => n + linkify(rules, node), 0);
  }

  // Aplica as regras na página e segue aplicando no conteúdo novo
  // (páginas como o Discord montam as mensagens dinamicamente).
  // Devolve quantos links criou na varredura inicial.
  function run(rules) {
    const compiled = compile(rules);
    if (!compiled.length) return 0;
    const count = scan(compiled, document.body);
    new MutationObserver((mutations) => {
      for (const mut of mutations) {
        for (const node of mut.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) scan(compiled, node);
          else if (node.nodeType === Node.TEXT_NODE && node.parentElement) scan(compiled, node.parentElement);
        }
      }
    }).observe(document.body, { childList: true, subtree: true });
    return count;
  }

  return { hostMatches, run };
})();
