# File to plot graphs using different git api endpoints

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import credentials as creds

def plot_commits():
    # Get commits
    commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    commits_response = requests.get(commits_url, headers=headers)
    commits_data = commits_response.json()

    commit_dates = [datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') for commit in commits_data]
    
    # Plot "commits" over time
    plt.figure(figsize=(10, 5))
    plt.plot(commit_dates, range(1, len(commit_dates) + 1))
    plt.title('Commits Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Commits')
    plt.show()

def plot_commits_per_contributor():
    # Get commits
    commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    commits_response = requests.get(commits_url, headers=headers)
    commits_data = commits_response.json()

    # Count commits per contributor
    commit_counts = {}
    for commit in commits_data:
        author = commit['commit']['author']['name']  # You can use 'login' for GitHub username
        commit_counts[author] = commit_counts.get(author, 0) + 1

    # Plot bar graph for "commits" data
    plt.figure(figsize=(12, 6))
    plt.bar(commit_counts.keys(), commit_counts.values(), color='skyblue')
    plt.title('Commits per Contributor')
    plt.xlabel('Contributor')
    plt.ylabel('Number of Commits')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def get_top_contributors(owner, repo, token, top_n):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get contributors
    contributors_url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    contributors_response = requests.get(contributors_url, headers=headers)
    contributors_data = contributors_response.json()

    # Sort contributors by contributions
    sorted_contributors = sorted(contributors_data, key=lambda x: x['contributions'], reverse=True)

    # Extract top contributors
    top_contributors = sorted_contributors[:top_n]

    return top_contributors

def plot_contributions_distribution(contributors):
    labels = [contributor['login'] for contributor in contributors]
    contributions = [contributor['contributions'] for contributor in contributors]

    # Plot pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(contributions, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Contributions Distribution Among Top Contributors')
    plt.show()

def get_code_changes_over_time():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get weekly additions and deletions
    code_frequency_url = f'https://api.github.com/repos/{owner}/{repo}/stats/code_frequency'
    code_frequency_response = requests.get(code_frequency_url, headers=headers)
    code_frequency_data = code_frequency_response.json()

    # Extract dates and additions/deletions
    dates = [datetime.utcfromtimestamp(week[0]).strftime('%Y-%m-%d') for week in code_frequency_data]
    additions = [week[1] for week in code_frequency_data]
    deletions = [-week[2] for week in code_frequency_data]  # Negative to represent deletions

    return dates, additions, deletions

def plot_code_changes_over_time(dates, additions, deletions):
    # Plot area chart
    plt.figure(figsize=(12, 6))
    plt.fill_between(dates, additions, label='Lines Added', color='green', alpha=0.5)
    plt.fill_between(dates, deletions, label='Lines Deleted', color='red', alpha=0.5)
    plt.title('Code Changes Over Time')
    plt.xlabel('Date')
    plt.ylabel('Lines Changed')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.show()

def get_contributions_by_contributor():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get weekly additions and deletions
    code_frequency_url = f'https://api.github.com/repos/{owner}/{repo}/stats/code_frequency'
    code_frequency_response = requests.get(code_frequency_url, headers=headers)
    code_frequency_data = code_frequency_response.json()

    # Extract contributors and contributions
    contributors = [contributor['author']['login'] for contributor in code_frequency_data]
    additions = [week[1] for week in code_frequency_data]
    deletions = [-week[2] for week in code_frequency_data]  # Negative to represent deletions

    return contributors, additions, deletions

def plot_stacked_bar_chart_line_changes(contributors, additions, deletions):
    # Plot stacked bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(contributors, additions, label='Additions', color='green')
    plt.bar(contributors, deletions, label='Deletions', color='red', bottom=additions)
    plt.title('Contributions by Contributor (Additions and Deletions)')
    plt.xlabel('Contributor')
    plt.ylabel('Lines Changed')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_pull_requests_over_time():

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get pull requests
    pull_requests_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    pull_requests_response = requests.get(pull_requests_url, headers=headers)
    pull_requests_data = pull_requests_response.json()

    # Extract dates of pull requests
    pull_request_dates = [datetime.strptime(pull_request['created_at'], '%Y-%m-%dT%H:%M:%SZ') for pull_request in pull_requests_data]


    # Plot line chart
    plt.figure(figsize=(12, 6))
    plt.plot(pull_request_dates, range(1, len(pull_request_dates) + 1), marker='o')
    plt.title('Number of Pull Requests Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Pull Requests')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def get_pull_request_status():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get pull requests
    pull_requests_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    pull_requests_response = requests.get(pull_requests_url, headers=headers)
    pull_requests_data = pull_requests_response.json()

    # Count the number of open, closed, and merged pull requests
    open_count = sum(1 for pr in pull_requests_data if pr['state'] == 'open')
    closed_count = sum(1 for pr in pull_requests_data if pr['state'] == 'closed' and pr['merged_at'] is None)
    merged_count = sum(1 for pr in pull_requests_data if pr['state'] == 'closed' and pr['merged_at'] is not None)

    return open_count, closed_count, merged_count

def plot_pull_request_status(open_count, closed_count, merged_count):
    # Plot bar chart
    statuses = ['Open', 'Closed (Not Merged)', 'Merged']
    counts = [open_count, closed_count, merged_count]

    plt.figure(figsize=(10, 6))
    plt.bar(statuses, counts, color=['orange', 'red', 'green'])
    plt.title('Pull Request Status')
    plt.xlabel('Status')
    plt.ylabel('Number of Pull Requests')
    plt.show()

def plot_pull_request_contributions():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get pull requests
    pull_requests_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    pull_requests_response = requests.get(pull_requests_url, headers=headers)
    pull_requests_data = pull_requests_response.json()

    # Initialize a dictionary to store contributions per contributor
    contributions_by_contributor = {}

    # Collect contributions data
    for pr in pull_requests_data:
        contributor = pr['user']['login']
        additions = pr['additions']
        deletions = pr['deletions']
        
        if contributor not in contributions_by_contributor:
            contributions_by_contributor[contributor] = {'additions': 0, 'deletions': 0}

        contributions_by_contributor[contributor]['additions'] += additions
        contributions_by_contributor[contributor]['deletions'] += deletions

    # Extract contributor names and contributions
    contributors = list(contributions_by_contributor.keys())
    additions = [data['additions'] for data in contributions_by_contributor.values()]
    deletions = [data['deletions'] for data in contributions_by_contributor.values()]

    # Plot stacked bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(contributors, additions, label='Additions', color='green')
    plt.bar(contributors, deletions, label='Deletions', color='red', bottom=additions)
    plt.title('Pull Request Contributions by Contributor')
    plt.xlabel('Contributor')
    plt.ylabel('Lines Changed')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_issues_over_time():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get issues
    issues_url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    issues_response = requests.get(issues_url, headers=headers)
    issues_data = issues_response.json()

    # Extract dates of issue creation
    issue_dates = [datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ') for issue in issues_data]


    # Plot line chart
    plt.figure(figsize=(12, 6))
    plt.plot(issue_dates, range(1, len(issue_dates) + 1), marker='o')
    plt.title('Number of Issues Created Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def get_issue_status():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get issues
    issues_url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    issues_response = requests.get(issues_url, headers=headers)
    issues_data = issues_response.json()

    # Count the number of open and closed issues
    open_count = sum(1 for issue in issues_data if issue['state'] == 'open')
    closed_count = sum(1 for issue in issues_data if issue['state'] == 'closed')

    return open_count, closed_count

def plot_issue_status(open_count, closed_count):
    # Plot bar chart
    statuses = ['Open', 'Closed']
    counts = [open_count, closed_count]

    plt.figure(figsize=(8, 6))
    plt.bar(statuses, counts, color=['orange', 'green'])
    plt.title('Issue Status')
    plt.xlabel('Status')
    plt.ylabel('Number of Issues')
    plt.show()

def plot_comments_over_time():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get comments on issues and pull requests
    comments_url = f'https://api.github.com/repos/{owner}/{repo}/issues/comments'
    comments_response = requests.get(comments_url, headers=headers)
    comments_data = comments_response.json()

    # Extract dates of comments
    comment_dates = [datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M:%SZ') for comment in comments_data]

    # Plot line chart
    plt.figure(figsize=(12, 6))
    plt.plot(comment_dates, range(1, len(comment_dates) + 1), marker='o')
    plt.title('Number of Comments on Issues and Pull Requests Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Comments')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_stacked_bar_chart_comments():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get comments on issues and pull requests
    comments_url = f'https://api.github.com/repos/{owner}/{repo}/issues/comments'
    comments_response = requests.get(comments_url, headers=headers)
    comments_data = comments_response.json()

    # Initialize a dictionary to store comments per contributor
    comments_by_contributor = {}

    # Collect comments data
    for comment in comments_data:
        contributor = comment['user']['login']
        
        if contributor not in comments_by_contributor:
            comments_by_contributor[contributor] = 0

        comments_by_contributor[contributor] += 1
    # Extract contributor names and comments
    contributors = list(comments_by_contributor.keys())
    comment_counts = list(comments_by_contributor.values())

    # Plot stacked bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(contributors, comment_counts, color='skyblue')
    plt.title('Comments by Contributor')
    plt.xlabel('Contributor')
    plt.ylabel('Number of Comments')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def get_repository_events():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get repository events
    events_url = f'https://api.github.com/repos/{owner}/{repo}/events'
    events_response = requests.get(events_url, headers=headers)
    events_data = events_response.json()

    # Extract event types and creation dates
    event_types = [event['type'] for event in events_data]
    event_dates = [datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ') for event in events_data]

    return event_types, event_dates

def plot_repository_events(event_types, event_dates, chart_type='line'):
    # Plot line chart or bar chart
    plt.figure(figsize=(12, 6))

    if chart_type == 'line':
        plt.plot(event_dates, range(1, len(event_dates) + 1), marker='o')
    elif chart_type == 'bar':
        plt.bar(event_types, range(1, len(event_dates) + 1), color='skyblue')

    plt.title('Repository Events Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Events')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_language_distribution(chart_type='pie'):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get repository languages
    languages_url = f'https://api.github.com/repos/{owner}/{repo}/languages'
    languages_response = requests.get(languages_url, headers=headers)
    languages_data = languages_response.json()

    labels = list(languages_data.keys())
    values = list(languages_data.values())

    plt.figure(figsize=(8, 8))

    if chart_type == 'pie':
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Language Distribution in Repository')
    elif chart_type == 'bar':
        plt.bar(labels, values, color='skyblue')
        plt.title('Language Distribution in Repository')

    plt.show()

def get_repo_license():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get repository information
    repo_url = f'https://api.github.com/repos/{owner}/{repo}'
    repo_response = requests.get(repo_url, headers=headers)
    repo_data = repo_response.json()

    # Check if the repository has a license
    if 'license' in repo_data and repo_data['license']:
        license_name = repo_data['license']['name']
        license_url = repo_data['license']['url']

        print(f"Repository License: {license_name}")
        print(f"License URL: {license_url}")
    else:
        print("Repository does not have a specified license.")

def get_repository_traffic():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get repository traffic data
    traffic_url = f'https://api.github.com/repos/{owner}/{repo}/traffic/views'
    traffic_response = requests.get(traffic_url, headers=headers)
    traffic_data = traffic_response.json()

    # Extract views and clones data
    views_count = traffic_data.get('count', 0)
    views_uniques = traffic_data.get('uniques', 0)

    # Get repository clones data
    clones_url = f'https://api.github.com/repos/{owner}/{repo}/traffic/clones'
    clones_response = requests.get(clones_url, headers=headers)
    clones_data = clones_response.json()

    clones_count = clones_data.get('count', 0)
    clones_uniques = clones_data.get('uniques', 0)

    return views_count, views_uniques, clones_count, clones_uniques

def plot_repository_traffic(views_count, views_uniques, clones_count, clones_uniques, chart_type='bar'):
    categories = ['Views', 'Clones']
    counts = [views_count, clones_count]
    uniques = [views_uniques, clones_uniques]

    if chart_type == 'bar':
        plt.figure(figsize=(10, 6))
        plt.bar(categories, counts, color=['skyblue', 'lightcoral'])
        plt.xlabel('Traffic Category')
        plt.ylabel('Count')
        plt.title('Repository Traffic: Views and Clones')
        plt.show()
    elif chart_type == 'line':
        plt.figure(figsize=(10, 6))
        plt.plot(categories, counts, marker='o', label='Count')
        plt.plot(categories, uniques, marker='o', label='Unique')
        plt.xlabel('Traffic Category')
        plt.ylabel('Count')
        plt.title('Repository Traffic: Views and Clones')
        plt.legend()
        plt.show()

def fetch_and_plot_repo_stats(owner, repo, token):
    global headers 
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get contributors
    contributors_url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    contributors_response = requests.get(contributors_url, headers=headers)
    contributors_data = contributors_response.json()
    # print(contributors_data)
    contributors = [contributor['login'] for contributor in contributors_data]

    
    # Line chart showing the number of commits over time
    plot_commits()

    # Bar chart showing the number of commits per contributor.
    plot_commits_per_contributor()

    # Pie chart or bar chart illustrating the distribution of contributions among top contributors.
    top_contributors = get_top_contributors(owner, repo, token, 5)
    plot_contributions_distribution(top_contributors)

    # Line chart or area chart showing the lines added and deleted over time.
    dates, additions, deletions = get_code_changes_over_time()
    plot_code_changes_over_time(dates, additions, deletions)

    # Stacked bar chart showing contributions by each contributor (additions and deletions).
    contributors, additions, deletions = get_contributions_by_contributor()
    plot_stacked_bar_chart_line_changes(contributors, additions, deletions)

    # Line chart displaying the number of pull requests over time.
    plot_pull_requests_over_time()

    # Bar chart showing the status of open, closed, and merged pull requests.
    open_count, closed_count, merged_count = get_pull_request_status()
    plot_pull_request_status(open_count, closed_count, merged_count)

    # Stacked bar chart illustrating pull request contributions by each contributor.
    plot_pull_request_contributions()

    # Line chart showing the number of issues created over time.
    plot_issues_over_time()

    # Bar chart indicating the status of open and closed issues.
    open_count, closed_count = get_issue_status()
    plot_issue_status(open_count, closed_count)

    # Line chart representing the number of comments on issues and pull requests over time.
    plot_comments_over_time()

    # Stacked bar chart showing comments by each contributor.
    plot_stacked_bar_chart_comments()

    # Line chart or bar chart displaying various repository events like pushes, forks, etc., over time.
    event_types, event_dates = get_repository_events()
    plot_repository_events(event_types, event_dates, chart_type='bar')

    # Pie chart or bar chart illustrating the distribution of programming languages in the repository.
    plot_language_distribution(chart_type='pie')

    # Displaying information about the repository's license.
    get_repo_license()

    # Bar chart or line chart showing repository views, clones, and unique visitors.
    views_count, views_uniques, clones_count, clones_uniques = get_repository_traffic()
    plot_repository_traffic(views_count, views_uniques, clones_count, clones_uniques, chart_type='line')

if __name__ == "__main__":
    global owner, repo, token
    owner = creds.OWNER
    repo = creds.REPO
    token = creds.TOKEN

    fetch_and_plot_repo_stats(owner, repo, token)
