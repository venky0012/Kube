#!/usr/bin/env python3
import subprocess
import os
import sys

def run_command(cmd, shell=False, check=False):
    """Run a command, ignoring errors."""
    try:
        result = subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Warning: Command failed: {cmd} - {e.stderr}")

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
    print("Starting cleanup...")

    distro = get_distro()
    if "rhel" in distro or "centos" in distro or "fedora" in distro:
        pkg_mgr = "dnf"
        docker_pkg = "docker-ce"
        print("Detected RHEL-based distro, using dnf.")
    else:
        pkg_mgr = "apt"
        docker_pkg = "docker.io"
        print("Detected Debian-based distro, using apt.")

    # Stop Minikube if running
    if check_command(["/usr/local/bin/minikube", "status"]):
        print("Stopping Minikube...")
        run_command(["/usr/local/bin/minikube", "stop"])
    else:
        print("Minikube not running.")

    # Delete Minikube cluster
    print("Deleting Minikube cluster...")
    run_command(["/usr/local/bin/minikube", "delete", "--all"])

    # Remove binaries if exist
    if check_command(["/usr/local/bin/minikube", "version"]):
        print("Removing Minikube...")
        run_command(["rm", "-f", "/usr/local/bin/minikube"])
    if check_command(["/usr/local/bin/kubectl", "version", "--client"]):
        print("Removing kubectl...")
        run_command(["rm", "-f", "/usr/local/bin/kubectl"])

    # Stop Docker if running
    print("Stopping Docker...")
    run_command(["systemctl", "stop", "docker"])

    # Uninstall Docker if installed
    if check_command(["docker", "--version"]):
        print("Uninstalling Docker...")
        if pkg_mgr == "dnf":
            run_command([pkg_mgr, "remove", "-y", docker_pkg, "docker-ce-cli", "containerd.io"])
            run_command(["dnf", "autoremove", "-y"])
        else:
            run_command([pkg_mgr, "remove", "-y", docker_pkg])
            run_command(["apt", "autoremove", "-y"])
    else:
        print("Docker not installed.")

    # Remove user from docker group
    user = os.environ.get("SUDO_USER") or os.environ.get("USER")
    print(f"Removing {user} from docker group...")
    run_command(["gpasswd", "-d", user, "docker"], check=False)

    print("Cleanup complete!")

if __name__ == "__main__":
    main()