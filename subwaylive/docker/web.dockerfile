# subwqylive/docker/web.dockerfile
# ====== 1) Build stage ======
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# mysqlclient 빌드에 필요한 헤더/툴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ====== 2) Runtime stage ======
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# ✅ 런타임엔 dev 패키지 불필요. 동적 라이브러리만!
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# 빌더에서 설치된 파이썬 패키지들만 복사
COPY --from=builder /install /usr/local

# 앱 소스만 복사 (컨텍스트가 루트라고 가정)
COPY . .

# 비루트 사용자
RUN useradd -m app
COPY --chown=app:app . .

USER app

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000", "-w", "3", "--timeout", "60"]
