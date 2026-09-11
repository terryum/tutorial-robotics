#!/bin/sh
# Works before Python or pal exists. Default invocation is strictly read-only.
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mode=${1:---plan}
case "$mode" in --plan|--apply) ;; *) echo 'Usage: sh bootstrap.sh [--plan|--apply]' >&2; exit 2;; esac
os_name=$(uname -s)
cpu_arch=$(uname -m)
echo "Host: $os_name $cpu_arch"
case "$os_name/$cpu_arch" in Darwin/arm64|Linux/x86_64) ;; *) echo 'Unsupported Core platform'; exit 2;; esac
df -h "$repo_dir"
echo "Python 3.12: $(command -v python3.12 || echo missing)"
echo "uv: $(command -v uv || echo missing)"
echo "Environment: $repo_dir/.venv"
echo "Purpose: locked Core simulation dependencies; no learning/ROS/GPU extras"
echo 'Commands: uv sync --locked --python 3.12 --no-dev; .venv/bin/pal setup verify --profile core --json'
echo "Missing uv would be installed under $repo_dir/.local/bin; managed Python under .local/python."
echo 'Apply with: sh bootstrap.sh --apply'
[ "$mode" = --apply ] || exit 0
free_kb=$(df -Pk "$repo_dir" | awk 'NR==2 {print $4}')
[ "$free_kb" -ge 2097152 ] || { echo 'Need at least 2 GiB free space'; exit 2; }
cd "$repo_dir"
mkdir -p .local
if command -v uv >/dev/null 2>&1; then
    uv_command=$(command -v uv)
elif [ -x .local/bin/uv ]; then
    uv_command="$repo_dir/.local/bin/uv"
else
    command -v curl >/dev/null || { echo 'Install curl or uv, then rerun.'; exit 2; }
    curl --fail --location --proto '=https' https://astral.sh/uv/install.sh -o .local/uv-install.sh
    UV_INSTALL_DIR="$repo_dir/.local/bin" UV_NO_MODIFY_PATH=1 sh .local/uv-install.sh
    uv_command="$repo_dir/.local/bin/uv"
fi
UV_PYTHON_INSTALL_DIR="$repo_dir/.local/python" "$uv_command" sync --locked --python 3.12 --no-dev
.venv/bin/pal setup verify --profile core --json > .local/bootstrap-verification.json
cat .local/bootstrap-verification.json
echo 'Ready. Run: source .venv/bin/activate'
echo 'Then: pal course init --through core; pal course next --json'
