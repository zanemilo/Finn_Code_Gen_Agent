#!/usr/bin/env python3
import os
import subprocess
import argparse
import sys

def run_command(command, cwd=None):
    """Run a shell command in the given directory and exit if it fails."""
    result = subprocess.run(command, cwd=cwd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(description="Initialize a new Git repository.")
    parser.add_argument("-n", "--name", required=True, help="Name of the repository")
    parser.add_argument("-b", "--branch", default="main", help="Default branch name (default: main)")
    parser.add_argument("-r", "--remote", help="Remote repository URL (optional)")
    args = parser.parse_args()

    # Determine repository path relative to current directory
    repo_path = os.path.join(os.getcwd(), args.name)
    try:
        os.makedirs(repo_path, exist_ok=False)
    except FileExistsError:
        print(f"Error: Directory '{repo_path}' already exists.")
        sys.exit(1)

    # Initialize the Git repository
    run_command("git init", cwd=repo_path)

    # Create essential files: README.md and .gitignore
    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "w") as readme:
        readme.write(f"# {args.name}\n")

    gitignore_path = os.path.join(repo_path, ".gitignore")
    open(gitignore_path, "w").close()

    # Stage and commit the initial files
    run_command("git add README.md .gitignore", cwd=repo_path)
    run_command('git commit -m "Initial commit"', cwd=repo_path)

    # Rename the default branch if necessary
    run_command(f"git branch -M {args.branch}", cwd=repo_path)

    # Add a remote origin if a remote URL is provided
    if args.remote:
        run_command(f"git remote add origin {args.remote}", cwd=repo_path)

    print(f"Repository '{args.name}' initialized successfully with branch '{args.branch}'.")

if __name__ == "__main__":
    main()

    # This script initializes a new Git repository with a README.md and .gitignore file.
    # It allows specifying the default branch name and an optional remote repository URL.
    # The script uses subprocess to run shell commands and argparse to parse command-line arguments.
    # The run_command function is a helper function to run shell commands and exit if they fail.
    # The main function parses the command-line arguments, creates the repository directory,
    # initializes the Git repository, creates the README.md and .gitignore files, stages and commits them,
    # renames the default branch if necessary, and adds a remote origin if provided.
    # Finally, it prints a success message with the repository name and default branch.

    # Example Use Case:
    # python init_repo.py -n myrepo -b main -r
    # the -n flag specifies the repository name, -b specifies the default branch name,
    # and -r specifies the remote repository URL (optional).