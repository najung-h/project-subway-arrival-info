# ====== 1) Build stage ======
FROM python:3.11-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# mysqlclient/cryptography 컴파일 대비: 빌드 툴 + 헤더
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ make pkg-config python3-dev \
    default-libmysqlclient-dev libmariadb-dev libmariadb-dev-compat libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# 컨텍스트가 compose 기준 ../ (== subwaylive 루트)니까 여기서 requirements.txt가 보여야 함
COPY requirements.txt ./requirements.txt

# 최신 빌드 툴로 업그레이드 후 설치 (자세한 로그 위해 -vv 선택)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt -vv

# ====== 2) Runtime stage ======
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 런타임엔 클라이언트 라이브러리만 필요
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
  && rm -rf /var/lib/apt/lists/*


# 🔒 비루트 유저 생성 (그룹 먼저, 홈=/app, 셸 없음)
RUN groupadd -r app \
 && useradd -r -g app -d /app -s /usr/sbin/nologin app \
 && id app && getent passwd app

COPY --from=builder /usr/local /usr/local

# 소스 복사 (app 사용자 소유)
COPY --chown=app:app . .

USER app
EXPOSE 8000
CMD ["gunicorn","config.wsgi:application","-b","0.0.0.0:8000","-w","3","--timeout","90","--log-file","-"]  # ✅ stdout
