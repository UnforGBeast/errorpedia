from github import Github
from stackapi import StackAPI
import time
from config import CONFIG  # Ensure CONFIG includes 'GITHUB_TOKEN' and 'STACK_OVERFLOW_KEY' if necessary


class ErrorCollector:
    def __init__(self):
        # Initialize GitHub API with the provided token
        self.github = Github(CONFIG['GITHUB_TOKEN'])

        # Initialize StackAPI for Stack Overflow
        self.stack = StackAPI('stackoverflow')
        self.stack.max_pages = 1  # Limits to one page of results
        self.stack.page_size = 100  # Fetches up to 100 questions per request

    def collect_github_errors(self, language, max_issues=100):
        query = f"language:{language} label:bug"
        issues = self.github.search_issues(query)

        collected_errors = []
        for issue in issues[:max_issues]:
            collected_errors.append({
                'title': issue.title,
                'body': issue.body,
                'labels': [label.name for label in issue.labels],
                'state': issue.state,
                'url': issue.html_url,
                'source': 'github'
            })
            time.sleep(1)  # Rate limiting

        return collected_errors

    def collect_stackoverflow_errors(self, tag, max_questions=100):
        # Fetch questions from Stack Overflow with the specified tag
        questions = self.stack.fetch('questions', tagged=tag, sort='votes', filter='withbody')

        collected_errors = []
        for question in questions['items'][:max_questions]:
            collected_errors.append({
                'title': question['title'],
                'body': question.get('body', ''),
                'tags': question['tags'],
                'answered': question['is_answered'],
                'url': question['link'],
                'source': 'stackoverflow'
            })
            time.sleep(1)  # Rate limiting

        return collected_errors
