# JIRA Analyzer Extension for Goose

A secure, read-only JIRA analysis extension for Goose that provides comprehensive insights and cross-referencing capabilities.

## Key Features

### 1. Secure Read-Only Analysis
- Zero modification capabilities
- Safe for production JIRA instances
- Respects JIRA permissions model

### 2. Deep Issue Analysis
- Complete issue details including comments
- Change history tracking
- Relationship mapping
- Cross-project references

### 3. Content Analysis
- Text pattern recognition
- Common terms identification
- Comment analysis
- Label usage patterns

### 4. Cross-Reference Capabilities
- Project interconnections
- Shared components
- Issue dependencies
- Related work tracking

## Installation

1. From PyPI:
```bash
pip install goose-jira-analyzer
```

2. From source:
```bash
git clone https://github.com/block/goose-jira-analyzer
cd goose-jira-analyzer
pip install -e .
```

## Usage

### 1. Start Goose with the Extension

```bash
goose session --with-extension "python -m jira_analyzer.server"
```

### 2. Connect to JIRA

```text
"Connect to JIRA at https://your-domain.atlassian.net with token YOUR_API_TOKEN"
```

### 3. Analyze Issues and Projects

```text
"Get details for issue PROJ-123"
"Search for issues in project PROJ with label 'important'"
"Analyze relationships for issue PROJ-123"
"Find cross-project references between PROJ and PROJ2"
"Analyze text content patterns in project PROJ"
```

## Security Features

### Read-Only Guarantee
- No modification capabilities
- Cannot create, update, or delete issues
- Cannot modify workflows or states
- Cannot change configurations

### Authentication
- Supports API tokens (recommended)
- Optional basic auth
- No credential storage
- Environment variable configuration

### Data Access
- Respects JIRA permissions
- User-based access control
- Project-level security

## Configuration

### Environment Variables
- `JIRA_SERVER`: Default JIRA server URL
- `JIRA_API_TOKEN`: Default API token
- `JIRA_USERNAME`: Default username (if using basic auth)

## Integration with Other Extensions

The JIRA Analyzer can be used alongside other Goose extensions for enhanced analysis:

1. **Data Analysis**
   - Export JIRA data for analysis
   - Generate reports and visualizations
   - Track metrics over time

2. **Cross-Referencing**
   - Link JIRA issues to code repositories
   - Connect with documentation
   - Integrate with other tools

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Style

```bash
# Format code
black .

# Type checking
mypy jira_analyzer
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure CI passes
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Security

Report security issues to security@block.xyz

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Acknowledgments

Built by Block, Inc. for the Goose platform.