# AskTheBio GUI

Modern React + Vite frontend for the AskTheBio experience. This project powers the public-facing interface while other services in the repository handle agents, crawling, and worker functionality.

## Tech Stack
- Vite + React 18 (TypeScript)
- Tailwind CSS with shadcn/ui components
- React Router, TanStack Query, Zod, and supporting UI libraries

## Local Development
```sh
# install dependencies (prefers pnpm)
pnpm install

# start the dev server on http://localhost:5173
pnpm dev

# run a production build into dist/
pnpm build

# optional preview of the last build
pnpm preview
```

Use Node 18+ (22.x is fine) and ensure your editor respects the repo’s ESLint and Prettier configuration.

## Project Structure
- `src/main.tsx` bootstraps React Router and global providers.
- `src/App.tsx` hosts shared layout and top-level routes.
- `src/pages/` contains higher-level views; `src/components/` stores reusable primitives.
- Utilities and hooks live under `src/lib/` and `src/hooks/`.
- Static assets belong in `src/assets/` for bundling or `public/` for raw serving.

## Deployment on Cloudflare Pages
Cloudflare Pages is the recommended hosting target.

1. **Connect GitHub**
   - In the Cloudflare dashboard go to **Pages → Create application → Connect to Git** and choose this repository (or specify the `gui/` folder if the repo hosts additional services).
2. **Build Configuration**
   - Framework preset: `None`.
   - Root directory: `gui`.
   - Build command: `pnpm build`.
   - Build output directory: `dist`.
   Cloudflare detects `pnpm-lock.yaml` and installs dependencies with pnpm automatically.
3. **Environment Variables (optional)**
   - Add keys under **Environment variables (advanced)** for both Production and Preview environments if the UI requires runtime configuration.
4. **Deploy & Preview**
   - Trigger the initial deployment; Cloudflare will publish to a `*.pages.dev` URL.
   - Enable preview deployments to build every pull request automatically.
5. **Custom Domains**
   - From the Pages dashboard, open **Custom domains**, enter your hostname, and follow the DNS prompts.

## Testing & Linting
- `pnpm lint` runs ESLint across the TypeScript codebase.
- Automated testing isn’t configured yet; if you add Vitest/RTL suites, place specs in `src/__tests__/`.
- Document any manual verification steps when introducing new features.

## Contributing
- Use concise, imperative commit messages (`Add onboarding hero`, `Refactor navbar spacing`).
- Keep PRs focused and include context, screenshots, and verification notes.
- When modifying shared primitives, check for Tailwind class reuse and adhere to existing patterns.
