// Monta o deep link do Claude Desktop para uma regra. Usado pelo content
// script e pelo botão "executar agora" do popup.
// `m` é o resultado do RegExp (grupos para $1, $2…); sem `m`, os $n somem.
function buildLink(rule, m = []) {
  const q = rule.q.replace(/\$(\d+)/g, (_, n) => m[n] ?? '');
  let url = `claude://code/new?q=${encodeURIComponent(q)}`;
  // Sem folder, o Desktop abre na pasta padrão.
  if (rule.folder) url += `&folder=${encodeURIComponent(rule.folder)}`;
  return url;
}
