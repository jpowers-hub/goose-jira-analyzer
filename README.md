# JIRA Analyzer Extension for Goose

[![CI/CD](https://github.com/jpowers-hub/goose-jira-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/jpowers-hub/goose-jira-analyzer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A secure, read-only JIRA analysis extension for Goose that provides comprehensive insights and cross-referencing capabilities.

## 🔒 Security First

This extension is designed with security in mind:
- Strictly read-only operations
- No modification capabilities
- Respects JIRA permissions
- Secure authentication handling

## 🚀 Key Features

### 1. Deep Issue Analysis
- Complete issue details and history
- Full comment threads
- Change tracking
- Relationship mapping
- Cross-project references

### 2. Content Analysis
- Text pattern recognition
- Common terms identification
- Comment analysis
- Label usage patterns

### 3. Cross-Reference Capabilities
- Project interconnections
- Shared components
- Issue dependencies
- Related work tracking

## 📋 Prerequisites

- Python 3.9 or higher
- Goose Desktop App
- JIRA API access token

## 🛠️ Installation

### From PyPI
```bash
pip install goose-jira-analyzer
```

### From Source
```bash
git clone https://github.com/jpowers-hub/goose-jira-analyzer
cd goose-jira-analyzer
pip install -e .
```

## 🔧 Usage

### 1. Start Goose with the Extension
```bash
goose session --with-extension "python -m jira_analyzer.server"
```

### 2. Connect to JIRA
```text
"Connect to JIRA at https://your-domain.atlassian.net with token YOUR_API_TOKEN"
```

### 3. Example Commands
```text
# Get issue details
"Get details for issue PROJ-123"

# Search issues
"Search for issues in project PROJ with label 'important'"

# Analyze relationships
"Analyze relationships for issue PROJ-123"

# Cross-project analysis
"Find cross-project references between PROJ and PROJ2"

# Content analysis
"Analyze text content patterns in project PROJ"
```

## 🔐 Security Features

### Read-Only Guarantee
- No modification capabilities
- Cannot create, update, or delete issues
- Cannot modify workflows or states
- Cannot change configurations

### Authentication
- API token support (recommended)
- Optional basic auth
- No credential storage
- Environment variable configuration

### Data Access
- Respects JIRA permissions
- User-based access control
- Project-level security

## ⚙️ Configuration

### Environment Variables
```bash
# Default JIRA server URL
export JIRA_SERVER="https://your-domain.atlassian.net"

# Default API token
export JIRA_API_TOKEN="your-api-token"

# Default username (if using basic auth)
export JIRA_USERNAME="your-username"
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 🔒 Security

Report security issues to security@block.xyz

## 💡 Support

For issues and feature requests, please use the GitHub issue tracker.

## 🙏 Acknowledgments

Built with ❤️ by Block, Inc. for the Goose platform.