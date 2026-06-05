"""
Gemeinsame Hilfsfunktionen für alle github-cowork Scripts.
"""
import hashlib
import re
import os


def load_config(skill_dir):
    """Liest resources/github.config und gibt dict zurück."""
    config_path = os.path.join(skill_dir, "resources", "github.config")
    config = {}
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line:
                key, _, val = line.partition("=")
                config[key.strip()] = val.strip()
    return config


def parse_remote(repo_dir):
    """Liest GH_OWNER und GH_REPO aus .git/config (kein git CLI nötig)."""
    git_config_path = os.path.join(repo_dir, ".git", "config")
    with open(git_config_path) as f:
        txt = f.read()
    url = re.search(r'url = (.+)', txt).group(1).strip()
    m = re.search(r'github\.com[:/](.+?)/(.+?)(?:\.git)?$', url)
    return m.group(1), m.group(2)


def local_head(repo_dir, branch="main"):
    """Liest lokalen HEAD SHA aus .git/refs (kein git CLI nötig)."""
    ref_path = os.path.join(repo_dir, ".git", "refs", "heads", branch)
    with open(ref_path) as f:
        return f.read().strip()


def update_refs(repo_dir, sha, branch="main"):
    """Schreibt neuen SHA in .git/refs und FETCH_HEAD."""
    ref_path = os.path.join(repo_dir, ".git", "refs", "heads", branch)
    with open(ref_path, "w") as f:
        f.write(sha + "\n")
    with open(os.path.join(repo_dir, ".git", "FETCH_HEAD"), "w") as f:
        f.write(sha + "\n")


def blob_sha(filepath):
    """Berechnet den Git-Blob-SHA einer lokalen Datei (ohne git CLI)."""
    with open(filepath, "rb") as f:
        content = f.read()
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content).hexdigest()


def auth_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }


def get_remote_tree(api_base, token, sha):
    """Holt den vollständigen Remote-Tree als {path: sha} dict."""
    import requests
    data = requests.get(
        f"{api_base}/git/trees/{sha}?recursive=1",
        headers=auth_headers(token)
    ).json()
    return {item["path"]: item["sha"] for item in data.get("tree", []) if item["type"] == "blob"}


def scan_local_files(repo_dir):
    """Gibt alle lokalen Dateien (ohne .git/) als {rel_path: blob_sha} zurück."""
    result = {}
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fname in files:
            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, repo_dir)
            result[rel_path] = blob_sha(abs_path)
    return result
