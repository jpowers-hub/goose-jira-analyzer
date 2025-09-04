from mcp.server import FastMCP
from typing import Dict, List, Optional
import json
from jira import JIRA
import os

class JiraAnalyzer:
    def __init__(self):
        self.jira = None
        self.server = None
        
    def connect(self, server: str, api_token: str):
        """Connect to JIRA server using token auth"""
        try:
            self.server = server
            self.jira = JIRA(server=server, token_auth=api_token)
            # Test connection by trying to access current user
            self.jira.myself()
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

    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """Search for issues using JQL"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
        
        issues = self.jira.search_issues(jql, maxResults=max_results)
        return [{
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "created": issue.fields.created,
            "updated": issue.fields.updated,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
            "priority": issue.fields.priority.name if issue.fields.priority else None,
            "issue_type": issue.fields.issuetype.name
        } for issue in issues]

    def get_issue_details(self, issue_key: str) -> Dict:
        """Get detailed information about a specific issue"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
        
        issue = self.jira.issue(issue_key)
        comments = [{
            "author": comment.author.displayName,
            "body": comment.body,
            "created": comment.created,
            "updated": comment.updated
        } for comment in issue.fields.comment.comments]
        
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name,
            "created": issue.fields.created,
            "updated": issue.fields.updated,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
            "reporter": issue.fields.reporter.displayName,
            "priority": issue.fields.priority.name if issue.fields.priority else None,
            "issue_type": issue.fields.issuetype.name,
            "labels": issue.fields.labels,
            "comments": comments
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
def connect_to_jira(server: str = "https://block.atlassian.net", api_token: str = None) -> str:
    """
    Connect to Block's JIRA server using token authentication.
    
    Args:
        server: JIRA server URL (defaults to Block's JIRA)
        api_token: Your JIRA API token
    """
    if not api_token:
        return "Please provide your JIRA API token"
    
    result = analyzer.connect(server, api_token)
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
def search_jira_issues(jql: str, max_results: int = 50) -> List[Dict]:
    """
    Search for JIRA issues using JQL (JIRA Query Language).
    
    Args:
        jql: The JQL query string (e.g., 'project = PROJ AND status = "In Progress"')
        max_results: Maximum number of results to return (default: 50)
    """
    return analyzer.search_issues(jql, max_results)

@mcp.tool()
def get_issue_details(issue_key: str) -> Dict:
    """
    Get detailed information about a specific JIRA issue including comments.
    
    Args:
        issue_key: The issue key (e.g., 'PROJ-123')
    """
    return analyzer.get_issue_details(issue_key)

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