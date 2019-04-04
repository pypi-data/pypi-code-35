def setup_opencode():
    return {
        "command": ["code-server", "-p", "{port}", "--no-auth", "--allow-http", "-d", "/home/jovyan"],
        "absolute_url": False,
        "launcher_entry": {
            "title": "VS Code",
            "icon_path": "https://s3-ap-southeast-1.amazonaws.com/deeplearning-mat/vscode.svg"
        }
    }
