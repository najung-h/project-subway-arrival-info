# ===== 1단계: 빌드 =====
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# mysqlclient 빌드를 위한 헤더/도구 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements.txt만 먼저 복사 → 캐시 활용
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ===== 2단계: 런타임 =====
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 런타임에 필요한 mysqlclient 라이브러리 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
WORKDIR /app
COPY . .

# 보안상 비루트 사용자 실행
RUN useradd -m app && chown -R app:app /app
USER app

# 헬스체크 (선택)
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD \
  wget -qO- http://127.0.0.1:8000/ || exit 1

EXPOSE 8000

# Gunicorn으로 서버 실행 (운영 환경에서는 prod 세팅)
CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000", "-w", "3", "--timeout", "60"]
