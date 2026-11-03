# Changelog

Versions follow [Semantic Versioning](https://semver.org/). Each version has a
`vX.Y.Z` tag and a GitHub release with the zip to upload to the Chrome Web Store.

## [1.1.4] - 2026-11-03

### Fixed
- Icon: the hand-drawn interlocking link left a thin seam on one ring. The link
  is now the Material Icons "link" glyph (Apache 2.0): filled shapes with no
  overlap, crisp from 16 to 128 px. Icons are rendered with Chrome.
- Promo tile uses the new icon and English text.

## [1.1.3] - 2026-11-03

### Fixed
- 128×128 icon follows the Chrome Web Store guidelines: artwork in 96×96 with
  16 px of transparent padding, and a lighter outline so it stands out on dark
  themes. The 16/32/48 toolbar icons stay full-bleed.

## [1.1.2] - 2026-11-03

### Security
- Text captured by `$1`, `$2`… comes from the page and may be written by anyone.
  Line breaks and control/invisible characters now become spaces and each
  group is capped at 200 characters before going into the message.
- The popup no longer loads fonts from Google: nothing is fetched from outside
  the extension.
- Text nodes longer than 5,000 characters are skipped, so a regex with
  exponential backtracking can't freeze the tab on long third-party text; the
  popup warns about keys with a repetition inside a repeated group, like `(a+)+`.

### Added
- Hovering a link shows the full message that will go to Claude.
- Warning that, with a folder, Claude Desktop asks to trust it on every link,
  even if it was already trusted.

## [1.1.1] - 2026-11-03

### Fixed
- Domains are normalized before saving: `discord.com/`, `https://www.Discord.com/channels/…`,
  `*.discord.com` and `discord.com:443` all become `discord.com`, so they no
  longer create duplicate pages. Pages saved in those forms are fixed and merged
  when the popup opens.
- Invalid domains (e.g. `discord`) and pages with no replacements are refused.
- **+** on a subdomain tab (e.g. `ptb.discord.com`) opens the parent domain's
  page when it already covers it.
- Identical rules in the same page are saved only once.

### Added
- Warnings for rules that save but won't behave as expected: key that matches
  empty text, value starting with `/`, and a folder that isn't a full path.

## [1.1.0] - 2026-11-03

### Added
- Interface, messages and docs in English (default), Portuguese (Brazil),
  Portuguese (Portugal), Spanish and Italian.
- Key validated as you type, with readable regex errors and a warning for
  `{,n}` (not a quantifier in JavaScript).
- ▶ button on each replacement: applies the rule to the open tab right away and
  explains when nothing became a link.
- Adding a page for a domain that already exists opens the existing page;
  saving a duplicate domain offers to merge both. Duplicates saved before this
  version are merged automatically.

## [1.0.0] - 2026-11-03

### Added
- Turns text matched by regex rules into `claude://code/new` links that open a
  Claude Desktop session with the message ready.
- Popup with page list and form (key, value, optional folder).
- Per-site permission on demand: runs only on domains you added and authorized.
- Icon, privacy policy and Chrome Web Store listing material.

[1.1.4]: https://github.com/correaschneider/claude-links-extension/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/correaschneider/claude-links-extension/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/correaschneider/claude-links-extension/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/correaschneider/claude-links-extension/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/correaschneider/claude-links-extension/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/correaschneider/claude-links-extension/releases/tag/v1.0.0
