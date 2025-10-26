# kdccai-plugin

Claude Code plugin for KDC (Korea Digital Contents) club activity management and automation.

## Description

This plugin extends Claude Code with tools and capabilities specifically designed for managing KDC club activities, workflows, and automation tasks.

## Installation

### Using Claude Code Plugin Command

```bash
/plugin install https://github.com/mnthe/kdccai-plugin
```

### Manual Installation

1. Clone this repository to your Claude plugins directory:
```bash
git clone https://github.com/mnthe/kdccai-plugin ~/.claude/plugins/kdccai-plugin
```

2. The plugin will be automatically loaded by Claude Code on next restart.

## Plugin Structure

```
kdccai-plugin/
├── .claude-plugin/
│   └── manifest.json       # Plugin metadata and configuration
├── .github/
│   └── workflows/
│       └── release.yml     # Automated release workflow
├── LICENSE
└── README.md
```

## Versioning

This plugin uses semantic versioning (SemVer) and automated releases via GitHub Actions:

- Version format: `vMAJOR.MINOR.PATCH` (e.g., `v0.1.0`, `v1.0.0`)
- Releases are automatically created when version tags are pushed
- Each release includes the plugin files and installation instructions

### Creating a Release

To create a new release:

1. Update the version in `.claude-plugin/manifest.json`
2. Commit the changes
3. Create and push a version tag:
```bash
git tag v0.1.0
git push origin v0.1.0
```

4. GitHub Actions will automatically:
   - Validate the manifest.json
   - Create a GitHub release
   - Attach release notes with installation instructions

## Development

### Plugin Manifest

The plugin configuration is defined in `.claude-plugin/manifest.json`:

```json
{
  "name": "kdccai-plugin",
  "version": "0.1.0",
  "description": "Claude plugin for KDC (Korea Digital Contents) club activity management and automation",
  "author": "Junghun Kim"
}
```

Required fields:
- `name`: Unique plugin identifier
- `version`: Semantic version number
- `description`: Brief description of the plugin
- `author`: Plugin creator or organization

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Junghun Kim

## References

- [Claude Code Plugin Documentation](https://docs.claude.com/en/docs/claude-code/plugins-reference)
- [Claude Code Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
