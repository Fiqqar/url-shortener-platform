# Frontend

Vue 3 + TypeScript + Vite client for the URL shortener API.

## Local development

~~~powershell
npm install
npm run dev
npm test -- --run
npm run typecheck
npm run build
~~~

The dev server expects the backend at `http://localhost:8000` by default. Set `VITE_API_BASE_URL` before `npm run dev` to use another API origin. Docker builds bake this value into the static bundle; pass `--build-arg VITE_API_BASE_URL=...` when building an image for another backend host or port. It cannot be changed by setting a container environment variable after the image is built. The GHCR release workflow uses the repository variable `VITE_API_BASE_URL`; if it is unset, the published bundle still points to localhost and is only suitable for local use.

`npm run lint` and `npm run format` are not defined in `package.json`.
