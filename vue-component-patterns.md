# Vue Component Patterns (2026)

## 1. Script Setup & TypeScript
The standard way to write components.

```vue
<script setup lang="ts">
import { computed } from 'vue';

// PROPS: Use interface for strict typing
interface Props {
  title: string;
  count?: number; // Optional
  user: {
    id: string;
    name: string;
  };
}

// withDefaults is optional in Vue 3.3+ if using destructuring (experimental)
// but standard generic definition is safer:
const props = withDefaults(defineProps<Props>(), {
  count: 0,
});

// EMITS: Typed events
const emit = defineEmits<{
  (e: 'update', value: number): void;
  (e: 'close'): void;
}>();

// COMPUTED
const displayTitle = computed(() => `${props.title} (${props.count})`);

// HANDLERS
function handleClick() {
  emit('update', props.count + 1);
}
</script>

<template>
  <div class="card">
    <h2>{{ displayTitle }}</h2>
    <button @click="handleClick">Increment</button>
  </div>
</template>
```

## 2. Reusable Logic (Composables)
Extract logic into standard functions.

```ts
// composables/useCounter.ts
import { ref, computed } from 'vue';

export function useCounter(initialValue = 0) {
  const count = ref(initialValue);
  const double = computed(() => count.value * 2);

  function increment() {
    count.value++;
  }

  return { count, double, increment };
}
```

## 3. Component Communication
-   **Props Down, Events Up**: The classic data flow.
-   **Provide/Inject**: Use for deep dependency injection (e.g., themes, global config) to avoid prop drilling. Use `InjectionKey` for type safety.

```ts
// keys.ts
import type { InjectionKey, Ref } from 'vue';
export const ThemeKey: InjectionKey<Ref<'light' | 'dark'>> = Symbol('Theme');
```

## 4. Slots for Flexibility
Use named and scoped slots for reusable layouts.

```vue
<!-- BaseLayout.vue -->
<template>
  <div class="layout">
    <header>
      <slot name="header">Default Header</slot>
    </header>
    <main>
      <slot :user="user" /> <!-- Default scoped slot -->
    </main>
  </div>
</template>
```

## Anti-Patterns to Avoid
-   **Smart/Dumb components distinction**: Don't over-engineer this. Co-locate logic where it makes sense.
-   **Prop Drilling**: Use Pinia or Provide/Inject instead.
-   **Global Event Bus**: **Do not use**. Use Pinia or Mitt (if absolutely necessary) but standard props/emits are preferred.
