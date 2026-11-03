# Claude Links

Extensão para Chrome/Brave que encontra textos numa página (por regex) e os
transforma em links que abrem uma **sessão nova na aba Code do Claude Desktop**,
com a mensagem já digitada.

Exemplo: uma automação manda no Discord um aviso com `/triagem TASK-123`.
Com uma regra cadastrada, esse texto vira um link; um clique abre o Claude
Desktop com "Rode a skill triagem na TASK-123" no campo de mensagem. A mensagem **não é enviada sozinha**: você confere e
aperta Enter.

## Como funciona

- O content script roda nas páginas cadastradas e acompanha o conteúdo novo
  (sites como o Discord montam as mensagens dinamicamente).
- Cada trecho que casa com uma regra vira um link no formato:

  ```
  claude://code/new?q=<valor>&folder=<pasta>
  ```

  É o deep link oficial do Claude Desktop
  ([documentação](https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link)).
- Textos dentro de campos de edição, inputs e links existentes não são tocados.

## Instalação

1. Abra `brave://extensions` (ou `chrome://extensions`).
2. Ative o **Modo de desenvolvedor**.
3. Clique em **Carregar sem compactação** e escolha esta pasta.
4. Fixe o ícone da extensão na barra.

Depois de alterar os arquivos, clique em recarregar (↻) na extensão e
recarregue a aba do site.

## Configuração

Clique no ícone da extensão para abrir a lista de páginas.

- **+** cadastra uma página nova, já com o domínio da aba atual preenchido.
- Clicar numa página da lista abre o formulário dela.

Cada página tem uma lista de substituições:

| Campo | O que é |
|-------|---------|
| **Página** | Domínio onde as regras valem (ex.: `discord.com`). Subdomínios também casam. |
| **Chave** | Regex que identifica o texto a trocar. |
| **Valor** | Mensagem que vai para o Claude (parâmetro `q`). Aceita `$1`, `$2`… com os grupos da chave. |
| **Folder** | Opcional. Pasta onde a sessão abre. Vazio = pasta padrão do Claude Desktop. |

Exemplo de regra para o Discord:

| Chave | Valor | Folder |
|-------|-------|--------|
| `/(triagem\|abrir-chamado)\s+([A-Z][A-Z0-9]*-\d+)` | `Rode a skill $1 na $2` | *(vazio)* |

A configuração fica salva no `chrome.storage.sync` do navegador.

## Limitações

- **Comandos com `/` não funcionam no valor.** O Claude Desktop troca a barra
  inicial do `q` por outro caractere, então o texto não é reconhecido como
  comando. Peça a skill em texto ("Rode a skill X na Y").
- **O Discord não aceita esses links direto na mensagem**: ele só torna
  clicável o que começa com `http(s)`. Por isso a troca é feita no navegador.
- O navegador pede confirmação na primeira vez que abre um link `claude://`.

## Arquivos

| Arquivo | Função |
|---------|--------|
| `manifest.json` | Manifesto (Manifest V3). |
| `content.js` | Encontra os textos e cria os links. |
| `defaults.js` | Config inicial (vazia). |
| `options.html` / `options.js` | Popup com a lista de páginas e o formulário. |
