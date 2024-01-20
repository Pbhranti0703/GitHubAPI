# File to plot graphs using different git api endpoints

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import credentials as creds
import pprint

def plot_commits():
    # Get commits
    commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    commits_response = requests.get(commits_url, headers=headers)
    commits_data = commits_response.json()

    commit_dates = [datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') for commit in commits_data]

    # Plot commits over time
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

    # Plot bar graph
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

def plot_stacked_bar_chart(contributors, additions, deletions):
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
    contributors = [contributor['login'] for contributor in contributors_data]

    # # Line chart showing the number of commits over time
    # plot_commits()

    # # Bar chart showing the number of commits per contributor.
    # plot_commits_per_contributor()

    # # Pie chart or bar chart illustrating the distribution of contributions among top contributors.
    # top_contributors = get_top_contributors(owner, repo, token, 5)
    # plot_contributions_distribution(top_contributors)

    # # Line chart or area chart showing the lines added and deleted over time.
    # dates, additions, deletions = get_code_changes_over_time()
    # plot_code_changes_over_time(dates, additions, deletions)

    # # Stacked bar chart showing contributions by each contributor (additions and deletions).
    # contributors, additions, deletions = get_contributions_by_contributor()
    # plot_stacked_bar_chart(contributors, additions, deletions)

    # Line chart displaying the number of pull requests over time.
    # plot_pull_requests_over_time()

    # Bar chart showing the status of open, closed, and merged pull requests.
    open_count, closed_count, merged_count = get_pull_request_status()
    plot_pull_request_status(open_count, closed_count, merged_count)


if __name__ == "__main__":
    global owner, repo, token
    owner = creds.OWNER
    repo = creds.REPO
    token = creds.TOKEN

    fetch_and_plot_repo_stats(owner, repo, token)
