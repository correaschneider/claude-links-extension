// Registra o content script só nas páginas cadastradas cuja permissão o
// usuário concedeu (optional_host_permissions). Roda de novo sempre que a
// config ou as permissões mudam.

const SCRIPT_ID = 'claude-links';

function originsFor(page) {
  return [`*://${page}/*`, `*://*.${page}/*`];
}

async function sync() {
  const { config = [] } = await chrome.storage.sync.get('config');
  const matches = [];
  for (const p of config) {
    const origins = originsFor(p.page);
    if (await chrome.permissions.contains({ origins })) matches.push(...origins);
  }

  const existing = await chrome.scripting.getRegisteredContentScripts({ ids: [SCRIPT_ID] });
  if (existing.length) await chrome.scripting.unregisterContentScripts({ ids: [SCRIPT_ID] });
  if (!matches.length) return;

  await chrome.scripting.registerContentScripts([{
    id: SCRIPT_ID,
    matches,
    js: ['defaults.js', 'content.js'],
    runAt: 'document_idle',
  }]);
}

chrome.runtime.onInstalled.addListener(sync);
chrome.runtime.onStartup.addListener(sync);
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'sync' && changes.config) sync();
});
chrome.permissions.onAdded.addListener(sync);
chrome.permissions.onRemoved.addListener(sync);
