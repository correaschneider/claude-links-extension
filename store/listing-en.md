# Chrome Web Store — listing (English, default language)

Images to upload are in `store/upload/` (24-bit PNG, no alpha).

## Description

Claude Links turns text you choose on a web page into links that open a new session in the Code tab of Claude Desktop, with the message already typed.

Example: an automation posts "/triage TASK-123" in a Discord channel. With a rule in place, that text becomes a link. One click opens Claude Desktop with "Run the skill triage on TASK-123" in the message box. Nothing is sent on its own: you review it and press Enter.

How it works
• Add a domain (e.g. discord.com) and its rules from the toolbar popup.
• Each rule has a key (regular expression), a value (the message, accepting $1, $2… from the key's groups) and an optional folder.
• Matching text becomes a claude://code/new link, Claude Desktop's official deep link.
• The ▶ button applies a rule to the open tab right away, to test it.
• The key is validated as you type, with warnings for rules that won't behave as expected.

Privacy and safety
• Runs only on the sites you add and authorize; the browser asks for permission site by site.
• Text captured from the page is cleaned (no line breaks or invisible characters) and capped before going into the message; hover a link to see the full message.
• Your configuration stays in your browser's storage. No server, no tracking, no data collection.

Languages: English, Portuguese (Brazil and Portugal), Spanish and Italian.

Requires Claude Desktop installed on your computer.

Independent open-source project, not affiliated with Anthropic: https://github.com/correaschneider/claude-links-extension

## Category

Developer Tools

## Graphic assets

| Field | File |
|-------|------|
| Store icon (128×128) | `store/upload/icon-128.png` |
| Screenshots (1280×800) | `store/upload/screenshot-1-in-context.png`, `store/upload/screenshot-2-before-after.png` |
| Small promo tile (440×280) | `store/upload/promo-440x280.png` |

## Additional fields

- Official URL / Homepage: https://correaschneider.github.io/claude-links-extension/
- Support URL: https://github.com/correaschneider/claude-links-extension/issues

## Privacy tab

**Single purpose:**
Turn text chosen by the user, on pages the user added, into links that open a Claude Desktop session with the message filled in.

**Justification — storage:**
Stores the user's configuration (domains and replacement rules) in the browser's storage.

**Justification — activeTab:**
When the user clicks + in the popup, reads the current tab's address to prefill the new page's domain; the ▶ button uses it to apply a rule to the open tab on demand.

**Justification — scripting:**
Registers the content script only on the domains the user added and authorized, instead of running on every site, and injects it into the active tab when the user clicks ▶.

**Justification — host permissions (optional):**
Requested one by one when the user saves a page, so the extension can read that site's visible text and create the links. Without the user's authorization the extension does not run on the site.

**Remote code:** No. All code is in the package.

**Data usage:** the extension collects none of the listed data types. Check the three certifications (no selling/transfer to third parties, no use unrelated to the single purpose, no use for creditworthiness or lending).

**Privacy policy URL:** https://correaschneider.github.io/claude-links-extension/privacy.html
