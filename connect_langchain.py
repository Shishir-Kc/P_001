import os
import json
import sys

# Configuration to add
NEW_SERVER_CONFIG = {
    "docs-langchain": {
        "url": "https://docs.langchain.com/mcp",
        "transport": "sse"
    }
}

def find_config_file():
    """Searches for mcp_config.json in common configuration directories."""
    home = os.path.expanduser("~")
    search_paths = [
        os.path.join(home, ".config"),
        os.path.join(home, ".local", "share"),
        os.path.join(home, "Library", "Application Support") # Mac
    ]
    
    found_files = []
    print("Searching for mcp_config.json...")
    
    for path in search_paths:
        if not os.path.exists(path):
            continue
        for root, dirs, files in os.walk(path):
            if "mcp_config.json" in files:
                found_files.append(os.path.join(root, "mcp_config.json"))
                
    return found_files

def update_config(file_path):
    """Updates the config file with the new server."""
    print(f"Updating {file_path}...")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if not content.strip():
                config = {"mcpServers": {}}
            else:
                config = json.loads(content)
    except json.JSONDecodeError:
        print(f"Error: {file_path} contains invalid JSON.")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Add/Update the server
    config["mcpServers"].update(NEW_SERVER_CONFIG)

    try:
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("Success! Configuration updated.")
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

def main():
    files = find_config_file()
    
    if not files:
        print("Could not find mcp_config.json automatically.")
        print("Please create it manually or use the VS Code 'MCP: Manage MCP Servers' command.")
        sys.exit(1)
        
    if len(files) == 1:
        update_config(files[0])
    else:
        print(f"Found multiple config files:")
        for i, f in enumerate(files):
            print(f"{i+1}: {f}")
        
        try:
            choice = input("Select file to update (number): ")
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                update_config(files[idx])
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

if __name__ == "__main__":
    main()
