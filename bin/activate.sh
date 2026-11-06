# Check if script is executed directly instead of sourced
if [ -n "$ZSH_VERSION" ]; then
  case $ZSH_EVAL_CONTEXT in *:file*) ;; *) 
    echo "⚠️  Do not run this script directly with './bin/activate.sh'."
    echo "👉  Run: source bin/activate.sh"
    return 1 2>/dev/null || exit 1
  ;; esac
  SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"
elif [ -n "$BASH_VERSION" ]; then
  if [ "$0" = "$BASH_SOURCE" ]; then
    echo "⚠️  Do not run this script directly with './bin/activate.sh'."
    echo "👉  Run: source bin/activate.sh"
    exit 1
  fi
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Activate Python virtual environment if it exists
if [ -f "${WORKSPACE_DIR}/.venv/bin/activate" ]; then
  . "${WORKSPACE_DIR}/.venv/bin/activate"
fi

export PATH="${SCRIPT_DIR}:${PATH}"
echo "✓ Workspace environment activated (Python .venv + local ffmpeg ready)."
