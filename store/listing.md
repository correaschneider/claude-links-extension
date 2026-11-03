# Chrome Web Store — textos do anúncio

Copiar campo a campo no painel do desenvolvedor.

## Nome

Claude Links

## Descrição curta (até 132 caracteres)

Transforma textos de qualquer página em links que abrem uma sessão no Claude Desktop com a mensagem pronta.

## Categoria

Ferramentas para desenvolvedores

## Idioma

Português (Brasil)

## Descrição longa

Claude Links encontra textos que você define numa página e os transforma em links que abrem uma sessão nova na aba Code do Claude Desktop, com a mensagem já digitada.

Exemplo: uma automação manda no Discord um aviso com "/triagem TASK-123". Com uma regra cadastrada, esse texto vira um link. Um clique abre o Claude Desktop com "Rode a skill triagem na TASK-123" no campo de mensagem. Nada é enviado sozinho: você confere e aperta Enter.

Como funciona
• Você cadastra um domínio (ex.: discord.com) e as regras dele.
• Cada regra tem uma chave (expressão regular), um valor (a mensagem, aceitando $1, $2… dos grupos da chave) e, se quiser, uma pasta.
• A extensão procura os textos que casam e cria links claude://code/new, o deep link oficial do Claude Desktop.

Privacidade
• Roda só nos sites que você cadastrou e autorizou; o navegador pede permissão site a site.
• A configuração fica no armazenamento do seu navegador. Não há servidor, coleta nem envio de dados.

Requisitos
• Claude Desktop instalado no computador.

Projeto independente, sem vínculo com a Anthropic. Código aberto: https://github.com/correaschneider/claude-links-extension

## Site

https://correaschneider.github.io/claude-links-extension/

## Política de privacidade (URL)

https://correaschneider.github.io/claude-links-extension/privacy.html

## Aba "Práticas de privacidade"

**Finalidade única:**
Transformar textos escolhidos pelo usuário, nas páginas que ele cadastrou, em links que abrem uma sessão no Claude Desktop com a mensagem preenchida.

**Justificativa — storage:**
Guarda a configuração do usuário (domínios e regras de substituição) no armazenamento do navegador.

**Justificativa — activeTab:**
Quando o usuário clica em + no popup, lê o endereço da aba atual para preencher o domínio da nova página.

**Justificativa — scripting:**
Registra o script de conteúdo apenas nos domínios que o usuário cadastrou e autorizou, em vez de rodar em todos os sites.

**Justificativa — permissões de host (opcionais):**
São pedidas uma a uma, quando o usuário salva uma página no popup, para que a extensão possa ler o texto daquele site e criar os links. Sem a autorização, a extensão não roda no site.

**Código remoto:**
Não. Todo o código está no pacote.

**Uso de dados:** marcar que a extensão **não coleta** nenhum dos tipos de dados listados, e marcar as três declarações:
- não vende nem transfere dados a terceiros fora dos casos permitidos;
- não usa nem transfere dados para fins não relacionados à finalidade única;
- não usa nem transfere dados para avaliar crédito ou conceder empréstimos.

## Imagens

| Campo | Arquivo |
|-------|---------|
| Ícone 128×128 | `icons/icon-128.png` |
| Captura de tela 1280×800 | `store/screenshot-1.png` |
| Bloco promocional pequeno 440×280 | `store/promo-440x280.png` |
