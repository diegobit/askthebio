# Repository Guidelines

## Project Structure & Module Organization
- Core client code lives in `src/`, with routing initialized in `src/main.tsx` and shared layout in `src/App.tsx`.
- UI primitives and composables are grouped under `src/components`, while higher-level views sit in `src/pages`.
- Shared hooks and utilities are placed in `src/hooks` and `src/lib`; keep new helpers close to their usage.
- Static assets go in `src/assets` for imports or `public/` for files served as-is.

## Build, Test, and Development Commands
- `pnpm install` (or `npm install`) resolves dependencies.
- `pnpm dev` starts the Vite dev server with fast HMR.
- `pnpm build` generates a production bundle in `dist/`; use `pnpm build:dev` when you need an unminified bundle for debugging.
- `pnpm preview` serves the last build locally to verify production output.
- `pnpm lint` runs ESLint against the entire project; fix findings before pushing.

## Coding Style & Naming Conventions
- The codebase uses TypeScript, React function components, and Tailwind CSS. Prefer hooks over class components.
- Follow Prettier-style two-space indentation, single quotes inside JSX attributes, and trailing commas where possible.
- Keep component filenames in PascalCase (e.g., `AgentInbox.tsx`), hooks in camelCase (`useAgentState.ts`), and utility modules in kebab-case when exporting multiple helpers.
- Use ESLint to enforce the shared style; rely on Tailwind utility classes instead of ad-hoc CSS where feasible.

## Testing Guidelines
- Automated testing is not yet configured. When adding tests, favor Vitest with React Testing Library and place specs in `src/__tests__` mirroring component names (`ComponentName.test.tsx`).
- Until automated coverage exists, document manual verification steps in your pull request, especially for UI flows.

## Commit & Pull Request Guidelines
- Write concise, imperative commits (e.g., `Add persona chat route`, `Refactor: tighten prompt flow`). Keep subject lines under ~70 characters.
- Scope each PR around a single feature or fix. Include a summary, screenshots for UI changes, linked issues, and any manual/automated test notes.
- Request review once linting passes and the preview build succeeds; highlight any known follow-up work or risks.
