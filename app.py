from flask import Flask, render_template
import requests
from datetime import datetime
import credentials as creds

app = Flask(__name__)

global owner, repo, token 
owner = creds.OWNER
repo = creds.REPO
token = creds.TOKEN
global headers 
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_top_contributors(top_n):
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

def get_contributors_details():
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get contributors list
    contributors_url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    contributors_response = requests.get(contributors_url, headers=headers)
    contributors_data = contributors_response.json()

    contributors_details = []

    for contributor in contributors_data:
        # Get detailed information for each contributor
        contributor_login = contributor['login']

        # Get user details
        user_url = f'https://api.github.com/users/{contributor_login}'
        user_response = requests.get(user_url, headers=headers)
        user_data = user_response.json()

        # Extract relevant information
        last_login = user_data.get('updated_at', '')
        last_login = datetime.strptime(last_login, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')

        total_commits = contributor['contributions']

        # Add contributor details to the list
        contributors_details.append({
            'username': contributor_login,
            'last_login': last_login,
            'total_commits': total_commits
            # Add more details as needed
        })

    return contributors_details

def get_commits_over_time():
    # Get commit history
    commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    commits_response = requests.get(commits_url, headers=headers)
    commits_data = commits_response.json()

    commit_dates = []
    total_commits = []

    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        commit_date = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        commit_dates.append(commit_date)
    
    # Create a dictionary to count commits per day
    commit_counts = {}
    for date in commit_dates:
        day = date.date()
        if day in commit_counts:
            commit_counts[day] += 1
        else:
            commit_counts[day] = 1

    # Sort the dictionary by date
    sorted_commits = sorted(commit_counts.items(), key=lambda x: x[0])

    for date, count in sorted_commits:
        total_commits.append(count)

    return commit_dates, total_commits


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contributors')
def contributors():
    top_contributors = get_top_contributors(5)

    contributors = top_contributors
    pie_labels = [contributor['login'] for contributor in contributors]
    pie_sizes = [contributor['contributions'] for contributor in contributors]
    contributors_details = get_contributors_details()
    return render_template('contributors.html', contributors=contributors_details, pie_labels = pie_labels, pie_sizes = pie_sizes)

@app.route('/commits')
def commits():
    # Prepare data for the line chart
    commit_dates, total_commits = get_commits_over_time()
    dates = [str(date) for date in commit_dates]
    line_chart_data = [{'x': str(date), 'y': count} for date, count in zip(commit_dates, total_commits)]

    contributors_details = get_contributors_details()

    # Prepare data for the bar chart
    bar_chart_data = [{'x': contributor['username'], 'y': contributor['total_commits']} for contributor in contributors_details]

    return render_template('commits.html', line_chart_data=line_chart_data, dates = dates, bar_chart_data=bar_chart_data)

if __name__ == '__main__':
    app.run(debug=True)
