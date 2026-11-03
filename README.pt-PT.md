# Claude Links

[English](README.md) · [Português (Brasil)](README.pt-BR.md) · **Português (Portugal)** · [Español](README.es.md) · [Italiano](README.it.md)

Extensão para Chrome/Brave que encontra textos numa página (por regex) e os
transforma em ligações que abrem uma **nova sessão no separador Code do Claude
Desktop**, com a mensagem já escrita.

Exemplo: uma automatização publica no Discord um aviso com `/triagem TASK-123`.
Com uma regra configurada, esse texto passa a ser uma ligação; um clique abre o
Claude Desktop com "Executa a skill triagem na TASK-123" no campo de mensagem.
A mensagem **nunca é enviada sozinha**: verifica-a e prime Enter.

## Como funciona

- O content script só corre nas páginas adicionadas **e autorizadas**: ao
  guardar uma página no popup, o navegador pede permissão para esse domínio.
  Também acompanha o conteúdo novo (sites como o Discord constroem as mensagens
  dinamicamente).
- Cada trecho que corresponde a uma regra passa a ser uma ligação neste formato:

  ```
  claude://code/new?q=<valor>&folder=<pasta>
  ```

  É o deep link oficial do Claude Desktop
  ([documentação](https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link)).
- Textos dentro de campos de edição, inputs e ligações existentes não são alterados.

## Instalação

1. Abra `brave://extensions` (ou `chrome://extensions`).
2. Ative o **Modo de programador**.
3. Clique em **Carregar expandida** e escolha esta pasta.
4. Fixe o ícone da extensão na barra.

Depois de alterar ficheiros, clique em recarregar (↻) na extensão e recarregue
o separador do site.

## Configuração

Clique no ícone da extensão para abrir a lista de páginas.

- **+** adiciona uma página nova, já com o domínio do separador atual preenchido.
- Clicar numa página da lista abre o respetivo formulário.

Cada página tem uma lista de substituições:

| Campo | O que é |
|-------|---------|
| **Página** | Domínio onde as regras se aplicam (ex.: `discord.com`). Os subdomínios também correspondem. |
| **Chave** | Regex que identifica o texto a substituir. |
| **Valor** | Mensagem enviada ao Claude (parâmetro `q`). Aceita `$1`, `$2`… dos grupos da chave. |
| **Pasta** | Opcional. Pasta onde a sessão abre. Vazio = pasta predefinida do Claude Desktop. |

Exemplo de regra para o Discord:

| Chave | Valor | Pasta |
|-------|-------|-------|
| `/(triagem\|abrir-pedido)\s+([A-Z][A-Z0-9]*-\d+)` | `Executa a skill $1 na $2` | *(vazio)* |

A chave é validada enquanto escreve: uma regex inválida fica assinalada, com o
erro logo abaixo. O botão **▶** de cada linha aplica essa regra de imediato no
separador aberto, sem guardar nem recarregar, e indica quantos trechos passaram
a ligação. O separador tem de estar no domínio da página (abra o popup pelo
ícone da extensão estando nele).

Ao clicar em **Guardar**, o navegador pede permissão para a extensão correr
nesse domínio. Páginas sem permissão aparecem assinaladas como "sem permissão"
na lista; basta abrir e guardar de novo. Eliminar a página devolve a permissão.

A configuração fica guardada no `chrome.storage.sync` do navegador. Nada é
recolhido nem enviado ([política de privacidade](https://correaschneider.github.io/claude-links-extension/pt/privacy.html)).

## Idiomas

A extensão segue o idioma do navegador: inglês (predefinido), português
(Brasil), português (Portugal), espanhol e italiano. Os textos estão em
`tools/locales.py`; depois de editar, execute `python3 tools/locales.py` para
gerar novamente a pasta `_locales/`.

## Limitações

- **Comandos começados por `/` não funcionam no valor.** O Claude Desktop
  substitui a barra inicial do `q` por outro carácter, por isso o texto não é
  reconhecido como comando. Peça a skill por texto ("Executa a skill X na Y").
- **O Discord não aceita estas ligações diretamente na mensagem**: só torna
  clicáveis as que começam por `http(s)`. Por isso a substituição é feita no
  navegador.
- O navegador pede confirmação na primeira vez que abre uma ligação `claude://`.
- **Com pasta, o Claude Desktop pede para confiar nela em cada ligação**, mesmo
  que já a tenha autorizado antes. Deixe a pasta vazia para evitar essa pergunta.
- **O texto capturado por `$1`, `$2`… vem da página**, e qualquer pessoa do
  canal pode tê-lo escrito. Quebras de linha e caracteres invisíveis passam a
  espaço e cada grupo é cortado em 200 caracteres; passe o rato sobre a ligação
  para ver a mensagem completa e verifique-a antes de premir Enter.

## Ficheiros

| Ficheiro | Função |
|----------|--------|
| `manifest.json` | Manifesto (Manifest V3). |
| `background.js` | Regista o content script apenas nos domínios autorizados. |
| `content.js` | Lê a configuração e aplica as regras do domínio ao carregar a página. |
| `linkify.js` | Núcleo da substituição de textos por ligações (usado também pelo ▶). |
| `link.js` | Constrói a ligação `claude://`. |
| `defaults.js` | Configuração inicial (vazia). |
| `options.html` / `options.js` | Popup com a lista de páginas e o formulário. |
| `_locales/` | Traduções (geradas por `tools/locales.py`). |
| `icons/` | Ícone em SVG e PNG 16/32/48/128. |
| `store/` | Textos e imagens do anúncio na Chrome Web Store. |
| `build.sh` | Gera o `.zip` para enviar para a loja. |
| `docs/` | Site do GitHub Pages (gerado por `docs/build.py`). |
