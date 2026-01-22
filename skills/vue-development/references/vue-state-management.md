# Vue State Management (2026)

## Pinia: The Standard
Vuex is deprecated. **Pinia** is the standard state management library for Vue 3. It is type-safe, modular, and simpler to use.

## Setup Stores (Recommended)
Pinia supports two syntaxes: Option Stores and Setup Stores. **Setup Stores** are recommended as they align perfectly with the Composition API.

```ts
// stores/counter.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCounterStore = defineStore('counter', () => {
  // STATE (ref() becomes state)
  const count = ref(0);
  const name = ref('Eduardo');

  // GETTERS (computed() becomes getters)
  const doubleCount = computed(() => count.value * 2);

  // ACTIONS (function() becomes actions)
  function increment() {
    count.value++;
  }

  return { count, name, doubleCount, increment };
});
```

## Usage in Components

```vue
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter';
import { storeToRefs } from 'pinia';

const store = useCounterStore();

// Destructuring state/getters requires storeToRefs to maintain reactivity
const { count, doubleCount } = storeToRefs(store);

// Actions can be destructured directly
const { increment } = store;
</script>

<template>
  <button @click="increment">Count is {{ count }}</button>
</template>
```

## Best Practices

1.  **Keep it Flat**: Avoid nesting state too deeply.
2.  **Modularize**: Create separate stores for distinct domains (e.g., `useAuthStore`, `useCartStore`) rather than one giant store.
3.  **Persistence**: Use plugins like `pinia-plugin-persistedstate` for local storage syncing.
4.  **No Mutations**: Pinia allows direct state modification (`store.count++`), but wrapping logic in actions (`store.increment()`) is better for debugging and devtools.

## When to use Local State vs. Pinia?
-   **Local State (`ref`/`reactive`)**: UI state specific to a component (e.g., "is modal open", form inputs).
-   **Pinia**: Data shared across multiple components (e.g., User profile, Shopping cart, Theme settings).
