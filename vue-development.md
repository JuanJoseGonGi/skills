# Vue Development Skill (2026 Edition)

This skill provides a comprehensive guide to developing Vue.js applications using 2026 best practices. It covers project structure, component patterns, state management, testing, and performance optimization.

## Core Stack (2026 Standards)
- **Framework**: Vue 3 (Composition API + `<script setup>`)
- **Language**: TypeScript (Strict Mode)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Testing**: Vitest (Unit/Component) + Playwright (E2E)
- **Styling**: Tailwind CSS or CSS Modules (Scoped)

## Workflow

1.  **Setup & Structure**: Refer to [Project Structure](./vue-project-structure.md) for organizing your codebase based on scale (Simple vs. Modular/Feature-Sliced).
2.  **Component Development**: Follow [Component Patterns](./vue-component-patterns.md) for clean, reusable, and typed components.
3.  **State Management**: Implement global state using [State Management Guide](./vue-state-management.md).
4.  **Testing**: Apply the [Testing Strategy](./vue-testing-strategy.md) (Test Pyramid: Unit > Component > E2E).
5.  **Optimization**: continuously apply techniques from the [Performance Guide](./vue-performance-guide.md).

## Critical Rules (The "Golden Rules")

1.  **Script Setup**: Always use `<script setup lang="ts">`.
2.  **Composables over Mixins**: Never use Mixins. Use Composables for logic reuse.
3.  **Ref vs Reactive**: Default to `ref()` for consistency. Use `reactive()` only for grouped state where object identity is stable.
4.  **Prop Stability**: Avoid passing new objects/arrays as props to prevent unnecessary re-renders.
5.  **Strict Types**: No `any`. Define interfaces for all Props and Emits.

## Resources
- [Vue.js Official Docs](https://vuejs.org)
- [Vue School](https://vueschool.io)
- [Vue Mastery](https://www.vuemastery.com)
- [Pinia Docs](https://pinia.vuejs.org)
- [Vitest Docs](https://vitest.dev)
