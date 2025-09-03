from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from typing import Dict, List, Optional
import json
from jira import JIRA

class JiraAnalyzer:
    def __init__(self):
        self.jira = None
        
    def connect(self, server: str, username: str = None, api_token: str = None):
        """Connect to JIRA server using basic auth or token"""
        try:
            if username and api_token:
                self.jira = JIRA(server=server, basic_auth=(username, api_token))
            else:
                # Assume token auth
                self.jira = JIRA(server=server, token_auth=api_token)
            return True
        except Exception as e:
            return str(e)

    def get_project_info(self, project_key: str) -> Dict:
        """Get basic project information"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
        
        project = self.jira.project(project_key)
        return {
            "key": project.key,
            "name": project.name,
            "lead": project.lead.displayName,
            "description": project.description
        }

    def analyze_project_metrics(self, project_key: str) -> Dict:
        """Analyze project metrics including issue counts by type and status"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
        
        issues = self.jira.search_issues(f'project = {project_key}', maxResults=1000)
        
        metrics = {
            "total_issues": len(issues),
            "by_type": {},
            "by_status": {},
            "by_priority": {}
        }
        
        for issue in issues:
            # Count by type
            issue_type = issue.fields.issuetype.name
            metrics["by_type"][issue_type] = metrics["by_type"].get(issue_type, 0) + 1
            
            # Count by status
            status = issue.fields.status.name
            metrics["by_status"][status] = metrics["by_status"].get(status, 0) + 1
            
            # Count by priority
            priority = issue.fields.priority.name if issue.fields.priority else "No Priority"
            metrics["by_priority"][priority] = metrics["by_priority"].get(priority, 0) + 1
        
        return metrics

# Initialize MCP server
mcp = FastMCP("JIRA Analyzer")
analyzer = JiraAnalyzer()

@mcp.tool()
def connect_to_jira(server: str, username: str = None, api_token: str = None) -> str:
    """
    Connect to a JIRA server using basic auth or token authentication.
    
    Args:
        server: JIRA server URL (e.g., 'https://your-domain.atlassian.net')
        username: Optional username for basic auth
        api_token: API token or password
    """
    result = analyzer.connect(server, username, api_token)
    if result is True:
        return "Successfully connected to JIRA"
    return f"Failed to connect: {result}"

@mcp.tool()
def get_project_info(project_key: str) -> Dict:
    """
    Get basic information about a JIRA project.
    
    Args:
        project_key: The project key (e.g., 'PROJ')
    """
    return analyzer.get_project_info(project_key)

@mcp.tool()
def analyze_project(project_key: str) -> Dict:
    """
    Analyze project metrics including issue counts by type, status, and priority.
    
    Args:
        project_key: The project key (e.g., 'PROJ')
    """
    return analyzer.analyze_project_metrics(project_key)

if __name__ == "__main__":
    mcp.run()