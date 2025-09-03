from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from typing import Dict, List, Optional, Any
import json
import os
from datetime import datetime
from .analyzer import JiraAnalyzer

# Initialize MCP server
mcp = FastMCP("JIRA Analyzer")
analyzer = JiraAnalyzer()

@mcp.tool()
def connect_to_jira(server: str, username: str = None, api_token: str = None) -> str:
    """
    Connect to a JIRA server using basic auth or token authentication (READ-ONLY mode).
    
    Args:
        server: JIRA server URL (e.g., 'https://your-domain.atlassian.net')
        username: Optional username for basic auth
        api_token: API token or password
    """
    result = analyzer.connect(server, username, api_token)
    if result is True:
        return "Successfully connected to JIRA in read-only mode"
    return f"Failed to connect: {result}"

@mcp.tool()
def get_issue_details(issue_key: str) -> Dict[str, Any]:
    """
    Get comprehensive details about a JIRA issue including comments and history.
    
    Args:
        issue_key: The issue key (e.g., 'PROJ-123')
    
    Returns:
        Dict containing issue details, comments, and history
    """
    return analyzer.get_issue_details(issue_key)

@mcp.tool()
def search_issues(project_key: str, jql_filters: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
    """
    Search for issues in a project with optional JQL filters.
    
    Args:
        project_key: The project key (e.g., 'PROJ')
        jql_filters: Optional additional JQL filters
        max_results: Maximum number of results to return (default: 100)
    
    Returns:
        List of matching issues with basic details
    """
    return analyzer.search_issues(project_key, jql_filters, max_results)

@mcp.tool()
def analyze_issue_relationships(issue_key: str, depth: int = 2) -> Dict[str, Any]:
    """
    Analyze relationships between issues (dependencies, links, etc.).
    
    Args:
        issue_key: The issue key to analyze (e.g., 'PROJ-123')
        depth: How many levels of relationships to analyze (default: 2)
    
    Returns:
        Dict containing relationship analysis
    """
    return analyzer.analyze_issue_relationships(issue_key, depth)

@mcp.tool()
def analyze_text_content(project_key: str, days: int = 30) -> Dict[str, Any]:
    """
    Analyze text content patterns in issues, comments, and descriptions.
    
    Args:
        project_key: The project key (e.g., 'PROJ')
        days: Number of days of history to analyze (default: 30)
    
    Returns:
        Dict containing text analysis results
    """
    return analyzer.analyze_text_content(project_key, days)

@mcp.tool()
def get_cross_project_references(project_key: str, related_projects: List[str]) -> Dict[str, Any]:
    """
    Find and analyze references between projects.
    
    Args:
        project_key: The main project key (e.g., 'PROJ')
        related_projects: List of related project keys to analyze
    
    Returns:
        Dict containing cross-project reference analysis
    """
    return analyzer.get_cross_project_references(project_key, related_projects)

@mcp.resource("jira-help://{topic}")
def get_help(topic: str) -> str:
    """Provide help documentation for JIRA analysis features"""
    help_topics = {
        "connection": """
        # JIRA Connection Help
        
        To connect to JIRA in read-only mode, you'll need:
        1. JIRA server URL (e.g., https://your-domain.atlassian.net)
        2. Either:
           - Username and API token
           - API token only
        
        API tokens can be generated from your Atlassian account settings.
        
        Note: This extension operates in read-only mode and cannot modify any JIRA data.
        """,
        
        "analysis": """
        # JIRA Analysis Features
        
        Available analysis tools:
        1. Issue Details
           - Full issue content
           - Comment history
           - Change history
           - Related issues
        
        2. Search & Discovery
           - Flexible issue search
           - JQL filtering
           - Cross-project references
        
        3. Content Analysis
           - Text pattern analysis
           - Common terms identification
           - Comment patterns
           - Label usage
        
        4. Relationship Analysis
           - Issue dependencies
           - Cross-project references
           - Component sharing
        """,
        
        "security": """
        # Security Best Practices
        
        1. Read-Only Access
           - This extension cannot modify JIRA data
           - All operations are read-only
           - No state changes are possible
        
        2. Authentication
           - Never store credentials in code
           - Use environment variables for sensitive data
           - Prefer API tokens over username/password
           - Regularly rotate API tokens
        
        3. Data Access
           - Only access projects you have permission to view
           - Respect JIRA's security model
           - Don't share sensitive data
        """
    }
    return help_topics.get(topic, "Topic not found. Available topics: connection, analysis, security")

if __name__ == "__main__":
    mcp.run()