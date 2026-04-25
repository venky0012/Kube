#!/usr/bin/env python3
from minikube_utils import *

def main():
    print("Starting cleanup...")

    pkg_mgr = get_package_manager()
    if pkg_mgr == "dnf":
        print("Detected RHEL-based distro, using dnf.")
    else:
        print("Detected Debian-based distro, using apt.")

    stop_minikube()
    delete_minikube_cluster()
    remove_binaries()
    stop_docker_service()
    uninstall_docker(pkg_mgr)
    remove_user_from_docker_group()

    print("Cleanup complete!")

if __name__ == "__main__":
    main()