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

This project supports two ways to create a release:

#### Option 1: Automated Release (Recommended)

Use GitHub Actions to automatically update files, create tag, and release:

1. Go to **Actions** tab in GitHub
2. Select **Release** workflow
3. Click **Run workflow**
4. Enter the version number (e.g., `0.2.0` - without 'v' prefix)
5. Click **Run workflow**

GitHub Actions will automatically:
- Update `manifest.json` to the specified version
- Generate/update `CHANGE_LOG.md` with commit history
- Commit the changes
- Create and push the version tag
- Create a GitHub release with installation instructions

#### Option 2: Manual Release

Follow these steps to manually prepare and tag a release:

1. **Update the version in `.claude-plugin/manifest.json`**
   ```bash
   # Edit the version field to match your new version (e.g., "0.2.0")
   nano .claude-plugin/manifest.json
   ```

2. **Update or create `CHANGE_LOG.md`** (optional but recommended)
   ```bash
   # Add a new entry at the top of CHANGE_LOG.md with your changes
   ```

3. **Commit the changes**
   ```bash
   git add .claude-plugin/manifest.json CHANGE_LOG.md
   git commit -m "chore: prepare release v0.2.0"
   ```

4. **Create and push the version tag**
   ```bash
   git tag v0.2.0
   git push origin main
   git push origin v0.2.0
   ```

5. **GitHub Actions will automatically:**
   - Verify that manifest.json version matches the tag
   - Create a GitHub release with installation instructions
   - Generate release notes from commits

**Important:** The version in `manifest.json` must match the tag version (without the 'v' prefix). For example, tag `v0.2.0` requires manifest version `0.2.0`. The release workflow will fail if versions don't match.

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
