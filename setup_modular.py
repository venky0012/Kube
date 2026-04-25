#!/usr/bin/env python3
from minikube_utils import *

def main():
    print("Starting setup...")

    pkg_mgr = get_package_manager()
    if pkg_mgr == "dnf":
        print("Detected RHEL-based distro, using dnf.")
        ensure_docker_repo()
    else:
        print("Detected Debian-based distro, using apt.")

    update_package_cache(pkg_mgr)
    install_docker(pkg_mgr)
    start_docker_service()
    add_user_to_docker_group()
    install_minikube()
    install_kubectl()
    start_minikube_cluster()

    print("Setup complete! Log out and back in for Docker group changes.")

if __name__ == "__main__":
    main()