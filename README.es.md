# Claude Links

[English](README.md) · [Português (Brasil)](README.pt-BR.md) · [Português (Portugal)](README.pt-PT.md) · **Español** · [Italiano](README.it.md)

Extensión para Chrome/Brave que encuentra textos en una página (con regex) y
los convierte en enlaces que abren una **nueva sesión en la pestaña Code de
Claude Desktop**, con el mensaje ya escrito.

Ejemplo: una automatización publica en Discord un aviso con `/triaje TASK-123`.
Con una regla configurada, ese texto se convierte en enlace; un clic abre Claude
Desktop con "Ejecuta la skill triaje en TASK-123" en el cuadro de mensaje. El
mensaje **nunca se envía solo**: lo revisas y pulsas Enter.

## Cómo funciona

- El content script solo se ejecuta en las páginas que añadiste **y
  autorizaste**: al guardar una página en el popup, el navegador pide permiso
  para ese dominio. También sigue el contenido nuevo (sitios como Discord
  construyen los mensajes de forma dinámica).
- Cada coincidencia de una regla se convierte en un enlace con este formato:

  ```
  claude://code/new?q=<valor>&folder=<carpeta>
  ```

  Es el deep link oficial de Claude Desktop
  ([documentación](https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link)).
- No se tocan textos dentro de campos editables, inputs ni enlaces existentes.

## Instalación

1. Abre `brave://extensions` (o `chrome://extensions`).
2. Activa el **Modo de desarrollador**.
3. Haz clic en **Cargar descomprimida** y elige esta carpeta.
4. Fija el icono de la extensión en la barra.

Después de cambiar archivos, haz clic en recargar (↻) en la extensión y
recarga la pestaña del sitio.

## Configuración

Haz clic en el icono de la extensión para abrir la lista de páginas.

- **+** añade una página nueva, con el dominio de la pestaña actual ya rellenado.
- Al hacer clic en una página de la lista se abre su formulario.

Cada página tiene una lista de sustituciones:

| Campo | Qué es |
|-------|--------|
| **Página** | Dominio donde se aplican las reglas (p. ej. `discord.com`). Los subdominios también coinciden. |
| **Clave** | Regex que encuentra el texto a sustituir. |
| **Valor** | Mensaje que se envía a Claude (parámetro `q`). Acepta `$1`, `$2`… de los grupos de la clave. |
| **Carpeta** | Opcional. Carpeta donde se abre la sesión. Vacío = carpeta predeterminada de Claude Desktop. |

Ejemplo de regla para Discord:

| Clave | Valor | Carpeta |
|-------|-------|---------|
| `/(triaje\|abrir-ticket)\s+([A-Z][A-Z0-9]*-\d+)` | `Ejecuta la skill $1 en $2` | *(vacío)* |

La clave se valida mientras escribes: una regex no válida queda marcada, con el
error justo debajo. El botón **▶** de cada fila aplica esa regla al momento en
la pestaña abierta, sin guardar ni recargar, e indica cuántas coincidencias se
convirtieron en enlaces. La pestaña debe estar en el dominio de la página (abre
el popup desde el icono de la extensión estando en ella).

Al hacer clic en **Guardar**, el navegador pide permiso para que la extensión
se ejecute en ese dominio. Las páginas sin permiso aparecen marcadas como "sin
permiso" en la lista; basta con abrirlas y guardar de nuevo. Eliminar la página
devuelve el permiso.

La configuración se guarda en `chrome.storage.sync` del navegador. No se
recopila ni se envía nada ([política de privacidad](https://correaschneider.github.io/claude-links-extension/es/privacy.html)).

## Idiomas

La extensión sigue el idioma del navegador: inglés (predeterminado), portugués
(Brasil), portugués (Portugal), español e italiano. Los textos están en
`tools/locales.py`; después de editarlos, ejecuta `python3 tools/locales.py`
para regenerar `_locales/`.

## Limitaciones

- **Los comandos que empiezan por `/` no funcionan en el valor.** Claude
  Desktop reemplaza la barra inicial de `q` por otro carácter, así que el texto
  no se reconoce como comando. Pide la skill con texto ("Ejecuta la skill X en Y").
- **Discord no acepta estos enlaces en un mensaje**: solo hace clicables los
  que empiezan por `http(s)`. Por eso la sustitución ocurre en el navegador.
- El navegador pide confirmación la primera vez que abre un enlace `claude://`.

## Archivos

| Archivo | Función |
|---------|---------|
| `manifest.json` | Manifiesto (Manifest V3). |
| `background.js` | Registra el content script solo en los dominios autorizados. |
| `content.js` | Lee la configuración y aplica las reglas del dominio al cargar la página. |
| `linkify.js` | Núcleo de la sustitución de textos por enlaces (también lo usa ▶). |
| `link.js` | Construye el enlace `claude://`. |
| `defaults.js` | Configuración inicial (vacía). |
| `options.html` / `options.js` | Popup con la lista de páginas y el formulario. |
| `_locales/` | Traducciones (generadas por `tools/locales.py`). |
| `icons/` | Icono en SVG y PNG 16/32/48/128. |
| `store/` | Textos e imágenes de la ficha en Chrome Web Store. |
| `build.sh` | Genera el `.zip` para subir a la tienda. |
| `docs/` | Sitio de GitHub Pages (generado por `docs/build.py`). |
