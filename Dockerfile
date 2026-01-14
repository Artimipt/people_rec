FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 


ENV CUDA_HOME=/usr/local/cuda
ENV PATH=/usr/local/cuda/bin:$PATH
ENV FORCE_CUDA=1
ENV TORCH_CUDA_ARCH_LIST="7.0;7.5;8.0;8.6;8.9;9.0"

ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash appuser
    

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget git curl ca-certificates \
    build-essential cmake ninja-build \
    libglib2.0-0 libsm6 libxext6 libxrender1 \
    libgl1 libegl1 \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /workspace

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install rfdetr
RUN chown -R appuser:appuser /workspace 
USER appuser

WORKDIR /workspace
CMD ["bash"]