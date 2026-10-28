#!/bin/sh
set -eu

ARGS=""
if [ -n "${COMFY_API_TOKEN:-}" ]; then
    ARGS="--token ${COMFY_API_TOKEN}"
elif [ -f "/run/secrets/comfy_api_token" ]; then
    ARGS="--token $(cat /run/secrets/comfy_api_token)"
else
    ARGS="--allow-insecure-bind"
fi

exec comfy-api-proxy \
    --comfyui "${COMFYUI_URL:-http://comfyui:8188}" \
    --host "${PROXY_HOST:-0.0.0.0}" \
    --port "${PROXY_PORT:-8189}" \
    --comfyui-base-dir "${COMFYUI_BASE_DIR:-/data}" \
    --state-dir "${STATE_DIR:-/data/user/proxy}" \
    $ARGS \
    "$@"
