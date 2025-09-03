from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from jira import JIRA
import pandas as pd
import numpy as np
from collections import defaultdict

class JiraAnalyzer:
    def __init__(self):
        self.jira = None
        
    def connect(self, server: str, username: str = None, api_token: str = None) -> bool:
        """Connect to JIRA server using basic auth or token - READ ONLY"""
        try:
            options = {
                'verify': True,
                'read_timeout': 30,
                'server': server
            }
            
            if username and api_token:
                self.jira = JIRA(options=options, basic_auth=(username, api_token))
            else:
                self.jira = JIRA(options=options, token_auth=api_token)
                
            return True
        except Exception as e:
            return str(e)

    def get_issue_details(self, issue_key: str) -> Dict[str, Any]:
        """Get comprehensive issue details including comments and history"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
        
        issue = self.jira.issue(issue_key, expand='changelog,comments')
        
        # Extract comments
        comments = []
        for comment in issue.fields.comment.comments:
            comments.append({
                'author': comment.author.displayName,
                'created': comment.created,
                'body': comment.body,
                'updated': comment.updated
            })
            
        # Extract change history
        history = []
        if hasattr(issue, 'changelog'):
            for history_item in issue.changelog.histories:
                for item in history_item.items:
                    history.append({
                        'date': history_item.created,
                        'author': history_item.author.displayName,
                        'field': item.field,
                        'from': item.fromString,
                        'to': item.toString
                    })
        
        # Extract linked issues
        links = []
        if hasattr(issue.fields, 'issuelinks'):
            for link in issue.fields.issuelinks:
                if hasattr(link, 'outwardIssue'):
                    links.append({
                        'type': link.type.outward,
                        'key': link.outwardIssue.key,
                        'status': link.outwardIssue.fields.status.name
                    })
                if hasattr(link, 'inwardIssue'):
                    links.append({
                        'type': link.type.inward,
                        'key': link.inwardIssue.key,
                        'status': link.inwardIssue.fields.status.name
                    })
        
        return {
            'key': issue.key,
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'issue_type': issue.fields.issuetype.name,
            'status': issue.fields.status.name,
            'priority': issue.fields.priority.name if issue.fields.priority else None,
            'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
            'reporter': issue.fields.reporter.displayName,
            'created': issue.fields.created,
            'updated': issue.fields.updated,
            'components': [c.name for c in issue.fields.components],
            'labels': issue.fields.labels,
            'comments': comments,
            'history': history,
            'links': links,
            'url': f"{self.jira.server_url}/browse/{issue.key}"
        }

    def search_issues(self, project_key: str, jql_filters: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """Search for issues with custom JQL filters"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
        
        base_jql = f"project = {project_key}"
        if jql_filters:
            base_jql += f" AND {jql_filters}"
            
        issues = self.jira.search_issues(base_jql, maxResults=max_results)
        
        return [{
            'key': issue.key,
            'summary': issue.fields.summary,
            'type': issue.fields.issuetype.name,
            'status': issue.fields.status.name,
            'priority': issue.fields.priority.name if issue.fields.priority else None,
            'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
            'created': issue.fields.created,
            'updated': issue.fields.updated,
            'url': f"{self.jira.server_url}/browse/{issue.key}"
        } for issue in issues]

    def analyze_issue_relationships(self, issue_key: str, depth: int = 2) -> Dict[str, Any]:
        """Analyze issue relationships and dependencies"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
            
        def get_linked_issues(key: str, current_depth: int, visited: set) -> Dict[str, Any]:
            if current_depth > depth or key in visited:
                return {}
                
            visited.add(key)
            issue = self.jira.issue(key)
            links = {}
            
            if hasattr(issue.fields, 'issuelinks'):
                for link in issue.fields.issuelinks:
                    if hasattr(link, 'outwardIssue'):
                        linked_key = link.outwardIssue.key
                        links[linked_key] = {
                            'type': link.type.outward,
                            'summary': link.outwardIssue.fields.summary,
                            'status': link.outwardIssue.fields.status.name,
                            'links': get_linked_issues(linked_key, current_depth + 1, visited)
                        }
                    if hasattr(link, 'inwardIssue'):
                        linked_key = link.inwardIssue.key
                        links[linked_key] = {
                            'type': link.type.inward,
                            'summary': link.inwardIssue.fields.summary,
                            'status': link.inwardIssue.fields.status.name,
                            'links': get_linked_issues(linked_key, current_depth + 1, visited)
                        }
            
            return links
            
        return {
            'key': issue_key,
            'relationships': get_linked_issues(issue_key, 1, set())
        }

    def analyze_text_content(self, project_key: str, days: int = 30) -> Dict[str, Any]:
        """Analyze text content patterns in issues, comments, and descriptions"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
            
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        jql = f'project = {project_key} AND updated >= "{start_date.strftime("%Y-%m-%d")}"'
        issues = self.jira.search_issues(jql, maxResults=1000, expand='changelog,comments')
        
        analysis = {
            'common_terms': defaultdict(int),
            'mentions': defaultdict(int),
            'labels': defaultdict(int),
            'components_referenced': defaultdict(int),
            'comment_patterns': {
                'total_comments': 0,
                'avg_comment_length': 0,
                'comment_frequency': defaultdict(int)
            }
        }
        
        total_comment_length = 0
        
        for issue in issues:
            # Analyze description
            if issue.fields.description:
                words = issue.fields.description.lower().split()
                for word in words:
                    if len(word) > 3:  # Skip short words
                        analysis['common_terms'][word] += 1
            
            # Analyze comments
            if hasattr(issue.fields, 'comment'):
                for comment in issue.fields.comment.comments:
                    analysis['comment_patterns']['total_comments'] += 1
                    total_comment_length += len(comment.body)
                    
                    # Track comment frequency by date
                    comment_date = datetime.strptime(comment.created[:10], "%Y-%m-%d")
                    analysis['comment_patterns']['comment_frequency'][comment_date.strftime("%Y-%m-%d")] += 1
            
            # Track labels
            for label in issue.fields.labels:
                analysis['labels'][label] += 1
            
            # Track component references
            for component in issue.fields.components:
                analysis['components_referenced'][component.name] += 1
        
        # Calculate average comment length
        if analysis['comment_patterns']['total_comments'] > 0:
            analysis['comment_patterns']['avg_comment_length'] = \
                total_comment_length / analysis['comment_patterns']['total_comments']
        
        # Sort and limit results
        analysis['common_terms'] = dict(sorted(analysis['common_terms'].items(), 
                                             key=lambda x: x[1], reverse=True)[:50])
        analysis['labels'] = dict(sorted(analysis['labels'].items(), 
                                       key=lambda x: x[1], reverse=True))
        analysis['components_referenced'] = dict(sorted(analysis['components_referenced'].items(), 
                                                      key=lambda x: x[1], reverse=True))
        
        return analysis

    def get_cross_project_references(self, project_key: str, related_projects: List[str]) -> Dict[str, Any]:
        """Find and analyze references between projects"""
        if not self.jira:
            raise Exception("Not connected to JIRA")
            
        references = {
            'outgoing': defaultdict(list),
            'incoming': defaultdict(list),
            'shared_components': defaultdict(set),
            'related_issues': []
        }
        
        # Search for cross-project references
        for related_project in related_projects:
            # Find issues in the main project that reference the related project
            jql = f'project = {project_key} AND (description ~ "{related_project}-" OR comment ~ "{related_project}-")'
            outgoing_issues = self.jira.search_issues(jql, maxResults=100)
            
            # Find issues in the related project that reference the main project
            jql = f'project = {related_project} AND (description ~ "{project_key}-" OR comment ~ "{project_key}-")'
            incoming_issues = self.jira.search_issues(jql, maxResults=100)
            
            for issue in outgoing_issues:
                references['outgoing'][related_project].append({
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'type': issue.fields.issuetype.name,
                    'status': issue.fields.status.name,
                    'url': f"{self.jira.server_url}/browse/{issue.key}"
                })
                
            for issue in incoming_issues:
                references['incoming'][related_project].append({
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'type': issue.fields.issuetype.name,
                    'status': issue.fields.status.name,
                    'url': f"{self.jira.server_url}/browse/{issue.key}"
                })
                
            # Find issues with shared components
            if hasattr(self.jira, 'project_components'):
                main_components = {c.name for c in self.jira.project_components(project_key)}
                related_components = {c.name for c in self.jira.project_components(related_project)}
                shared = main_components.intersection(related_components)
                
                if shared:
                    references['shared_components'][related_project] = shared
        
        return dict(references)