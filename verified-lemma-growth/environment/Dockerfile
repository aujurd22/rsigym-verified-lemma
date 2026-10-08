FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git tar procps elan && \
    rm -rf /var/lib/apt/lists/*

# Lean toolchain matching the pinned mathlib4 olean cache
RUN elan toolchain install leanprover/lean4:v4.35.0-rc3 && \
    elan default leanprover/lean4:v4.35.0-rc3
ENV PATH="/root/.elan/bin:${PATH}"
ENV ELAN_HOME="/root/.elan"

RUN pip3 install --break-system-packages numpy sentence-transformers sqlite-utils

# the immutable library + mathlib olean cache are staged by the task
# packer (mathlib.db ~112MB, mathlib4 cache ~10GB); the mutable agent
# repo and the loop code are copied from the task directory
COPY library/ /workspace/library/
COPY mathlib4/ /workspace/mathlib4/
COPY loop/ /workspace/loop/
COPY agent/ /workspace/agent/

WORKDIR /workspace
