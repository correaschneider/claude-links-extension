// Monta o deep link do Claude Desktop para uma regra. Usado pelo content
// script (linkify.js).

// O texto capturado vem da página, e qualquer pessoa pode tê-lo escrito
// (ex.: outro membro do canal do Discord). Antes de ir para o pedido do
// Claude: sem quebras de linha nem caracteres de controle/invisíveis, espaços
// colapsados e tamanho limitado, para não virar um bloco de instruções.
// Sem const no topo: o ▶ injeta este arquivo de novo na mesma aba.
function sanitizeGroup(text) {
  const max = 200; // tamanho máximo de cada grupo ($1, $2…) no pedido
  const clean = String(text ?? '')
    .replace(/[\u0000-\u001f\u007f-\u009f\u200b-\u200f\u2028-\u202e\u2060-\u206f\ufeff]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  return clean.length > max ? `${clean.slice(0, max)}…` : clean;
}

// Texto final do pedido: o valor da regra com $1, $2… preenchidos.
// `m` é o resultado do RegExp; sem `m`, os $n somem.
function buildPrompt(rule, m = []) {
  return rule.q.replace(/\$(\d+)/g, (_, n) => sanitizeGroup(m[n]));
}

function buildLink(rule, m = []) {
  let url = `claude://code/new?q=${encodeURIComponent(buildPrompt(rule, m))}`;
  // Sem folder, o Desktop abre na pasta padrão.
  if (rule.folder) url += `&folder=${encodeURIComponent(rule.folder)}`;
  return url;
}
