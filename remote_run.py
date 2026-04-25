#!/usr/bin/env python3
import argparse
import os
import socket
import subprocess
import sys
from pathlib import Path

SCRIPT_FILES = ["minikube_utils.py", "setup_modular.py", "cleanup_modular.py"]


def run_local(cmd, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Local command failed: {' '.join(cmd)}")
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)
    return result


def is_local_host(host):
    if host in ("localhost", "127.0.0.1", "::1"):
        return True
    try:
        local_names = {socket.gethostname(), socket.getfqdn()}
        local_addresses = {
            socket.gethostbyname(socket.gethostname()),
            socket.gethostbyname(socket.getfqdn())
        }
        return host in local_names or host in local_addresses
    except socket.error:
        return False


def parse_inventory(path):
    hosts = []
    with open(path, "r") as f:
        for line in f:
            clean = line.split("#", 1)[0].strip()
            if not clean:
                continue
            parts = [p.strip() for p in clean.replace(";", ",").split(",") if p.strip()]
            host = parts[0]
            user = parts[1] if len(parts) >= 2 else os.environ.get("USER")
            port = int(parts[2]) if len(parts) >= 3 else 22
            hosts.append((host, user, port))
    return hosts


def parse_args():
    parser = argparse.ArgumentParser(description="Run Minikube setup or cleanup on one or more hosts without permanently copying files.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--host", help="Remote target hostname or IP")
    group.add_argument("--inventory", help="Inventory file with host[,user[,port]] entries")
    parser.add_argument("--user", default=os.environ.get("USER"), help="SSH user for remote hosts")
    parser.add_argument("--port", type=int, default=22, help="SSH port")
    parser.add_argument("--action", choices=["setup", "cleanup"], default="setup", help="Action to perform on the target hosts")
    return parser.parse_args()


def build_combined_script(action):
    local_dir = Path(__file__).resolve().parent
    util_path = local_dir / "minikube_utils.py"
    action_path = local_dir / ("setup_modular.py" if action == "setup" else "cleanup_modular.py")

    util_content = util_path.read_text()
    action_content = action_path.read_text()
    action_lines = [line for line in action_content.splitlines() if not line.startswith("from minikube_utils import *")]
    return util_content + "\n\n" + "\n".join(action_lines) + "\n"


def run_on_host(host, user, port, action):
    if is_local_host(host):
        print(f"Processing {host} (local host) as {user}...")
    else:
        print(f"Processing {host}:{port} as {user}...")
    script = build_combined_script(action)

    if is_local_host(host):
        print("Detected local host; running locally.")
        proc = subprocess.run(["python3", "-"], input=script, text=True)
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr)
            sys.exit(proc.returncode)
        return

    print("Checking SSH connectivity...")
    run_local(["ssh", "-p", str(port), f"{user}@{host}", "true"])
    print("Running remote action without permanently copying files...")
    ssh_proc = subprocess.Popen(
        ["ssh", "-p", str(port), f"{user}@{host}", "sudo python3 -"],
        stdin=subprocess.PIPE,
        text=True
    )
    stdout, stderr = ssh_proc.communicate(script)
    if ssh_proc.returncode != 0:
        print(stdout or "")
        print(stderr or "")
        sys.exit(ssh_proc.returncode)
    print("Remote action complete.")


def main():
    args = parse_args()
    targets = []
    if args.inventory:
        targets = parse_inventory(args.inventory)
    else:
        targets = [(args.host, args.user, args.port)]

    for host, user, port in targets:
        run_on_host(host, user, port, args.action)

    print("All target actions completed.")


if __name__ == "__main__":
    main()
