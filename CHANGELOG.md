# Changelog

Versions follow [Semantic Versioning](https://semver.org/). Each version has a
`vX.Y.Z` tag and a GitHub release with the zip to upload to the Chrome Web Store.

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

[1.1.0]: https://github.com/correaschneider/claude-links-extension/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/correaschneider/claude-links-extension/releases/tag/v1.0.0
