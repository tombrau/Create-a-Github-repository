import os
import subprocess
import requests

def read_github_token():
    file_path = r"E:\Projects\_global files\Github API token.txt" # Replace this with the actual path of the file.
    with open(file_path, 'r') as f:
        token = f.read().strip()
    return token

def read_github_name():
    file_path = r"E:\Projects\_global files\Github Name.txt" # Replace this with the actual path of the file.
    with open(file_path, 'r') as f:
        name = f.read().strip()
    return name


def add_recommended_files(path):
    if not os.path.exists(path):
        os.makedirs(path)

        files_to_create = {
            "README.md": "# My Project\n\nThis is my project.",
            os.path.join("src", "main.py"): "# Main program\n\nprint('Hello, world!')",
            os.path.join("tests", "test_main.py"): "# Test main program\n\nimport main\n\ndef test_main():\n    assert True",
            ".gitignore": "*.pyc\n__pycache__/\n*.log\n*.csv\n*.json\n*.yaml\n*.pickle\n*.jpg\n*.png\n*.gz\n*.zip\n*.tar\n*.tar.gz\n*.h5\n*.model\n.eggs/\ndist/\nvenv/\n",
            "requirements.txt": "# Add your Python package dependencies here\n\n# For example:\n# pandas\n# numpy\n# requests",
            "LICENSE": "# Add your license information here\n\n# For example:\n# MIT License\n\n# Copyright (c) [Year] [Your Name]\n\n# Permission is hereby granted, free of charge, to any person obtaining a copy\n# ..."
        }

        folders_to_create = [
            "src",
            "tests",
            "docs",
            "data",
            "configs",
            "scripts",
            "resources"
        ]

        for folder in folders_to_create:
            os.makedirs(os.path.join(path, folder))

        for file, content in files_to_create.items():
            with open(os.path.join(path, file), 'w') as f:
                f.write(content)


def commit_and_push(path):
    subprocess.run(['git', 'add', '.'], cwd=path)
    subprocess.run(['git', 'commit', '-m', 'Add recommended files'], cwd=path)
    subprocess.run(['git', 'push', 'origin', 'master'], cwd=path)

def create_github_repo():
    path = input("Enter the path where you want to create or update the Github repository: ")
    add_recommended_files(path)

    token = read_github_token()
    headers = {'Authorization': f'token {token}'}
    data = {'name': os.path.basename(path)}
    response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)

    if response.status_code != 201:
        print(f"Error creating GitHub repository: {response.json().get('message')}")
        return

    remote_url = response.json()['clone_url']

    if not os.path.exists(os.path.join(path, ".git")):
        subprocess.run(['git', 'init'], cwd=path)

    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd=path)

    commit_and_push(path)

if __name__ == '__main__':
    create_github_repo()
