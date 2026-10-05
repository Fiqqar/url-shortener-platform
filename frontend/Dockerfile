# Build stage
FROM node:26-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# Build-time API base URL (Vite bakes this into the bundle).
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# Runtime stage: current nginx on fresh Alpine (slim = static serving only).
# No digest pin on purpose: CI builds with --pull and Dependabot (docker,
# /frontend) proposes tag bumps, so the base cannot silently go stale the
# way 1.27-alpine did (44 HIGH/CRITICAL on alpine 3.21.3). apk upgrade
# picks up any patched libs published after the base image was cut.
FROM nginx:1.31-alpine-slim AS runtime
RUN apk upgrade --no-cache
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
