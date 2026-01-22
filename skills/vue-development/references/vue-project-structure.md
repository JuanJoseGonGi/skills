# Vue Project Structure (2026)

Choosing the right structure is critical for maintainability. In 2026, we lean towards **Feature-Based** or **Feature-Sliced** architectures for medium-to-large applications, while keeping a **Flat** structure for small projects.

## 1. Modular / Feature-Based Structure (Recommended for most Apps)
Group files by *feature* (domain) rather than *file type*. This co-locates logic, views, and tests.

```text
src/
├── assets/             # Global assets (logos, base styles)
├── components/         # Global shared UI components (Buttons, Inputs)
│   ├── AppButton.vue
│   └── AppInput.vue
├── composables/        # Global shared logic
│   └── useTheme.ts
├── features/           # DOMAIN MODULES
│   ├── auth/
│   │   ├── components/ # Auth-specific components
│   │   │   └── LoginForm.vue
│   │   ├── composables/
│   │   │   └── useAuth.ts
│   │   ├── services/   # API calls
│   │   │   └── authService.ts
│   │   └── stores/     # Auth state
│   │       └── authStore.ts
│   └── dashboard/
│       ├── components/
│       └── views/
├── layouts/            # App layouts (Default, Auth, Admin)
├── router/             # Routing configuration
├── App.vue
└── main.ts
```

## 2. Feature-Sliced Design (FSD) (For Enterprise / Very Large Apps)
Strict architectural boundaries. See `feature-sliced.design` for full spec.

```text
src/
├── app/                # Global app setup (styles, providers, router)
├── processes/          # Complex inter-page scenarios (deprecated in v2 but still used)
├── pages/              # Composition layer for routes
│   └── user-profile/
├── widgets/            # Self-contained UI blocks (Header, Sidebar, Feed)
├── features/           # User scenarios (LikeButton, UserSearch)
├── entities/           # Business entities (User, Post, Comment)
└── shared/             # Reusable infrastructure (UI Kit, API client, libs)
```

## 3. Flat Structure (Small Projects / POCs)
Traditional Vue structure. Good for starting out but hard to scale.

```text
src/
├── components/
├── composables/
├── stores/
├── views/
├── App.vue
└── main.ts
```

## Best Practices
1.  **Colocation**: Keep tests (`*.spec.ts`) next to the component (`Component.vue`) or in a `__tests__` folder within the feature.
2.  **Barrel Files**: Use `index.ts` in feature folders to export public API, keeping internal implementation private.
3.  **Naming**:
    -   Components: PascalCase (e.g., `UserProfile.vue`)
    -   Composables: camelCase with `use` prefix (e.g., `useUser.ts`)
    -   Stores: camelCase with `Store` suffix or `use...Store` (e.g., `useAuthStore.ts`)
