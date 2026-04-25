#!/usr/bin/env python3
import subprocess
import os
import sys

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

def check_command(cmd):
    """Check if a command exists."""
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("Starting setup...")

    distro = get_distro()
    if "rhel" in distro or "centos" in distro or "fedora" in distro:
        pkg_mgr = "dnf"
        docker_pkg = "docker-ce"
        print("Detected RHEL-based distro, using dnf.")
        # Add Docker repo for RHEL if not already added
        if not check_command(["dnf", "config-manager", "--dump", "docker-ce"]):
            print("Adding Docker repository...")
            run_command(["dnf", "config-manager", "--add-repo", "https://download.docker.com/linux/centos/docker-ce.repo"])
    else:
        pkg_mgr = "apt"
        docker_pkg = "docker.io"
        print("Detected Debian-based distro, using apt.")

    # Update package cache
    print(f"Updating {pkg_mgr} cache...")
    if pkg_mgr == "dnf":
        run_command([pkg_mgr, "update", "-y"])
    else:
        run_command([pkg_mgr, "update"])

    # Install Docker if not installed or service not available
    docker_installed = check_command(["docker", "--version"])
    service_exists = check_command(["systemctl", "list-unit-files", "docker.service", "--no-legend"])
    if not docker_installed or not service_exists:
        if docker_installed:
            print("Docker installed but service missing, reinstalling...")
            run_command([pkg_mgr, "remove", "-y", docker_pkg])
            if pkg_mgr == "dnf":
                run_command([pkg_mgr, "remove", "-y", "docker-ce-cli", "containerd.io"])
        print("Installing Docker...")
        if pkg_mgr == "dnf":
            run_command([pkg_mgr, "install", "-y", "--allowerasing", docker_pkg, "docker-ce-cli", "containerd.io"])
        else:
            run_command([pkg_mgr, "install", "-y", docker_pkg])
    else:
        print("Docker already installed.")

    # Start and enable Docker
    print("Starting Docker service...")
    run_command(["systemctl", "start", "docker"])
    run_command(["systemctl", "enable", "docker"])

    # Add user to docker group
    user = os.environ.get("SUDO_USER") or os.environ.get("USER")
    print(f"Adding {user} to docker group...")
    run_command(["usermod", "-aG", "docker", user])

    # Download and install Minikube if not installed
    if not check_command(["/usr/local/bin/minikube", "version"]):
        print("Downloading Minikube...")
        run_command(["curl", "-LO", "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"])
        run_command(["chmod", "+x", "minikube-linux-amd64"])
        run_command(["mv", "minikube-linux-amd64", "/usr/local/bin/minikube"])
    else:
        print("Minikube already installed.")

    # Download and install kubectl if not installed
    if not check_command(["/usr/local/bin/kubectl", "version", "--client"]):
        print("Downloading kubectl...")
        version = run_command(["curl", "-L", "-s", "https://dl.k8s.io/release/stable.txt"])
        run_command(["curl", "-LO", f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl"])
        run_command(["chmod", "+x", "kubectl"])
        run_command(["mv", "kubectl", "/usr/local/bin/"])
    else:
        print("kubectl already installed.")

    # Start Minikube if not running
    if not check_command(["/usr/local/bin/minikube", "status"]):
        print("Starting Minikube cluster...")
        run_command(["/usr/local/bin/minikube", "start", "--driver=docker", "--force"])
    else:
        print("Minikube cluster already running.")

    print("Setup complete! Log out and back in for Docker group changes.")

if __name__ == "__main__":
    main()