#!/usr/bin/env python3
import subprocess
import os
import sys

# Configuration
CONFIG = {
    "minikube_driver": "docker",
    "packages": {
        "dnf": ["docker-ce", "docker-ce-cli", "containerd.io"],
        "apt": ["docker.io"]
    },
    "bin_paths": {
        "minikube": "/usr/local/bin/minikube",
        "kubectl": "/usr/local/bin/kubectl"
    }
}

def run_command(cmd, shell=False, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def run_command_no_check(cmd, shell=False):
    """Run a command, ignoring errors."""
    try:
        result = subprocess.run(cmd, shell=shell, check=False, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Warning: Command failed: {cmd} - {e.stderr}")

def check_command(cmd):
    """Check if a command exists."""
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_distro():
    """Detect the Linux distribution."""
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID_LIKE="):
                    return line.strip().split("=")[1].strip('"')
        return "unknown"
    except FileNotFoundError:
        return "unknown"

def get_package_manager():
    """Return the package manager for the current distro."""
    distro = get_distro()
    if any(x in distro for x in ("rhel", "centos", "fedora")):
        return "dnf"
    return "apt"

def ensure_docker_repo():
    """Ensure the Docker repository is configured on RHEL-based systems."""
    if get_package_manager() == "dnf":
        if not check_command(["dnf", "config-manager", "--dump", "docker-ce"]):
            print("Adding Docker repository...")
            run_command(["dnf", "config-manager", "--add-repo", "https://download.docker.com/linux/centos/docker-ce.repo"])

def update_package_cache(pkg_mgr):
    """Update package cache."""
    print(f"Updating {pkg_mgr} cache...")
    if pkg_mgr == "dnf":
        run_command([pkg_mgr, "update", "-y"])
    else:
        run_command([pkg_mgr, "update"])

def install_docker(pkg_mgr):
    """Install Docker if not properly installed."""
    docker_installed = check_command(["docker", "--version"])
    service_exists = check_command(["systemctl", "list-unit-files", "docker.service", "--no-legend"])
    if not docker_installed or not service_exists:
        if docker_installed:
            print("Docker installed but service missing, reinstalling...")
            run_command([pkg_mgr, "remove", "-y"] + CONFIG["packages"][pkg_mgr])
        print("Installing Docker...")
        if pkg_mgr == "dnf":
            run_command([pkg_mgr, "install", "-y", "--allowerasing"] + CONFIG["packages"][pkg_mgr])
        else:
            run_command([pkg_mgr, "install", "-y"] + CONFIG["packages"][pkg_mgr])
    else:
        print("Docker already installed.")

def start_docker_service():
    """Start and enable Docker service."""
    print("Starting Docker service...")
    run_command(["systemctl", "start", "docker"])
    run_command(["systemctl", "enable", "docker"])

def add_user_to_docker_group():
    """Add user to docker group."""
    user = os.environ.get("SUDO_USER") or os.environ.get("USER")
    print(f"Adding {user} to docker group...")
    run_command(["usermod", "-aG", "docker", user])

def install_minikube():
    """Install Minikube if not installed."""
    if not check_command([CONFIG["bin_paths"]["minikube"], "version"]):
        print("Downloading Minikube...")
        run_command(["curl", "-LO", "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"])
        run_command(["chmod", "+x", "minikube-linux-amd64"])
        run_command(["mv", "minikube-linux-amd64", CONFIG["bin_paths"]["minikube"]])
    else:
        print("Minikube already installed.")

def install_kubectl():
    """Install kubectl if not installed."""
    if not check_command([CONFIG["bin_paths"]["kubectl"], "version", "--client"]):
        print("Downloading kubectl...")
        version = run_command(["curl", "-L", "-s", "https://dl.k8s.io/release/stable.txt"])
        run_command(["curl", "-LO", f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl"])
        run_command(["chmod", "+x", "kubectl"])
        run_command(["mv", "kubectl", CONFIG["bin_paths"]["kubectl"]])
    else:
        print("kubectl already installed.")

def start_minikube_cluster():
    """Start Minikube cluster if not running."""
    if not check_command([CONFIG["bin_paths"]["minikube"], "status"]):
        print("Starting Minikube cluster...")
        try:
            run_command([CONFIG["bin_paths"]["minikube"], "start", f"--driver={CONFIG['minikube_driver']}", "--force"])
        except SystemExit:
            print("Minikube start failed. Cleaning up and retrying...")
            run_command_no_check([CONFIG["bin_paths"]["minikube"], "delete", "--all"])
            run_command([CONFIG["bin_paths"]["minikube"], "start", f"--driver={CONFIG['minikube_driver']}", "--force"])

        if not check_command([CONFIG["bin_paths"]["minikube"], "status"]):
            print("Minikube did not start successfully after retry. Please inspect Minikube logs.")
            sys.exit(1)
    else:
        print("Minikube cluster already running.")

def stop_minikube():
    """Stop Minikube if running."""
    if check_command([CONFIG["bin_paths"]["minikube"], "status"]):
        print("Stopping Minikube...")
        run_command_no_check([CONFIG["bin_paths"]["minikube"], "stop"])
    else:
        print("Minikube not running.")

def delete_minikube_cluster():
    """Delete Minikube cluster."""
    print("Deleting Minikube cluster...")
    run_command_no_check([CONFIG["bin_paths"]["minikube"], "delete", "--all"])

def remove_binaries():
    """Remove Minikube and kubectl binaries if exist."""
    if check_command([CONFIG["bin_paths"]["minikube"], "version"]):
        print("Removing Minikube...")
        run_command_no_check(["rm", "-f", CONFIG["bin_paths"]["minikube"]])
    if check_command([CONFIG["bin_paths"]["kubectl"], "version", "--client"]):
        print("Removing kubectl...")
        run_command_no_check(["rm", "-f", CONFIG["bin_paths"]["kubectl"]])

def stop_docker_service():
    """Stop Docker service."""
    print("Stopping Docker...")
    run_command_no_check(["systemctl", "stop", "docker"])

def uninstall_docker(pkg_mgr):
    """Uninstall Docker if installed."""
    if check_command(["docker", "--version"]):
        print("Uninstalling Docker...")
        if pkg_mgr == "dnf":
            run_command_no_check([pkg_mgr, "remove", "-y"] + CONFIG["packages"][pkg_mgr])
            run_command_no_check(["dnf", "autoremove", "-y"])
        else:
            run_command_no_check([pkg_mgr, "remove", "-y"] + CONFIG["packages"][pkg_mgr])
            run_command_no_check(["apt", "autoremove", "-y"])
    else:
        print("Docker not installed.")

def remove_user_from_docker_group():
    """Remove user from docker group."""
    user = os.environ.get("SUDO_USER") or os.environ.get("USER")
    print(f"Removing {user} from docker group...")
    run_command_no_check(["gpasswd", "-d", user, "docker"])