// Troca textos configurados (regex) por links claude://code/new, que abrem uma
// sessão nova na aba Code do Claude Desktop com o pedido já digitado (sem enviar).
// A config fica em chrome.storage.sync (página de opções); padrão em defaults.js.
// O núcleo da troca está em linkify.js.

chrome.storage.sync.get({ config: DEFAULT_CONFIG }, ({ config }) => {
  const rules = config
    .filter((p) => ClaudeLinks.hostMatches(p.page))
    .flatMap((p) => p.replacements || []);
  ClaudeLinks.run(rules);
});
