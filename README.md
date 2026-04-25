# Minikube Setup and Cleanup Scripts

These Python scripts automate the setup and cleanup of Docker and Minikube on a local Linux machine.

## Prerequisites
- Python 3 installed.
- Run with sudo privileges.
- Tested on Ubuntu/Debian and RHEL/CentOS/Rocky Linux; scripts auto-detect the distro.

## Setup
Run `sudo python3 setup.py` or `sudo python3 setup_modular.py` to install Docker, Minikube, kubectl, and start a single-node cluster.

The scripts are idempotent: running them multiple times will not cause errors if components are already installed/running.

After setup, log out and back in for Docker group changes.

Verify with:
- `minikube status`
- `kubectl get nodes`

## Cleanup
Run `sudo python3 cleanup.py` or `sudo python3 cleanup_modular.py` to stop/delete the cluster and uninstall everything.

The scripts are idempotent: safe to run multiple times.

## Modular Version
- `setup_modular.py` and `cleanup_modular.py` are modular versions that import functions from `minikube_utils.py`.
- `minikube_utils.py` contains shared functions and configuration.
- Easier to customize and maintain; edit `CONFIG` in `minikube_utils.py` for changes.

## Notes
- For multi-node cluster, edit the `minikube_driver` in config or script.
- If issues occur, check outputs or run commands manually.

## Remote installation
Use `remote_run.py` to run Minikube setup or cleanup on one or more hosts over SSH without permanently copying the local files.

Single-host example:
```bash
python3 remote_run.py --host 10.0.0.5 --user venkat --action setup
```

Inventory example:
```bash
python3 remote_run.py --inventory inventory.example --action setup
```

The inventory file format is:
- `host`
- `host,user`
- `host,user,port`

Blank lines and comments starting with `#` are ignored.

Example inventory file is provided in `inventory.example`.
