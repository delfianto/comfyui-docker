# comfyui-docker

Multi-stage Docker builds and Docker Buildx Bake configuration for ComfyUI runtime and the official local API proxy.

Built images:
- **`ghcr.io/delfianto/comfyui-cuda:13.4.2-base-ubuntu26.04`**: CUDA 13.4.2, Ubuntu 26.04 LTS, Python 3.14, matched PyTorch 2.11 / TorchVision 0.26 / TorchAudio 2.11 runtime base.
- **`ghcr.io/delfianto/comfyui-app:latest`** (and version tags, e.g. `:v0.3.60`): ComfyUI application runtime, bundled stable release, Proton DLSS compatibility support.
- **`ghcr.io/delfianto/comfyui-proxy:latest`** (and `:0.1.6`): Official local API proxy exposing Comfy API v2 for SDK integration.

## Directory Layout

```
.
├── build.sh                  # Release resolution & build entrypoint
├── docker-bake.hcl           # Multi-target Buildx Bake definition
├── Dockerfile                # ComfyUI runtime build
├── Dockerfile.base           # Reusable CUDA & PyTorch base build
├── Dockerfile.proxy          # Official local API proxy build
├── docker-entrypoint.sh      # ComfyUI runtime entrypoint
├── entrypoint-proxy.sh       # Local API proxy entrypoint
├── init-dlss-prefix.sh       # Proton DLSS prefix initializer
├── resolve-comfy-ref.py      # Upstream release resolver
├── smoke-test-proxy.py       # Proxy and SDK validation script
├── .env.example              # Build configuration template
├── .dockerignore
└── README.md
```

## Building Images

Build settings are configured in `.env` (copy from `.env.example`).

```bash
# Build the reusable CUDA/Torch base image (run once or when updating CUDA/PyTorch)
./build.sh --pull base

# Build both ComfyUI runtime and API proxy for the latest stable ComfyUI release
./build.sh

# Build a specific ComfyUI release version
./build.sh --version v0.3.60

# Build only the official local API proxy
./build.sh proxy

# Inspect bake targets without building
./build.sh --print

# Validate Dockerfiles without exporting images
./build.sh --check
```

## Targets in `docker-bake.hcl`

| Target | Dockerfile | Output Tags | Description |
|---|---|---|---|
| `base` | `Dockerfile.base` | `ghcr.io/delfianto/comfyui-cuda:13.4.2-base-ubuntu26.04` | Reusable base with CUDA, Python 3.14, and Torch |
| `comfyui` | `Dockerfile` | `ghcr.io/delfianto/comfyui-app:latest`, `:vX.Y.Z` | ComfyUI runtime with Proton DLSS |
| `proxy` | `Dockerfile.proxy` | `ghcr.io/delfianto/comfyui-proxy:latest`, `:0.1.6` | Official local API proxy (v2 API) |

## Testing

With ComfyUI and the proxy running, test the API proxy and SDK connectivity:

```bash
python3 smoke-test-proxy.py
```
