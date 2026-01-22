# Vue Performance Guide (2026)

## 1. Code Splitting & Async Components
Don't load everything upfront. Use `defineAsyncComponent` for heavy components (modals, complex charts, drawers).

```ts
import { defineAsyncComponent } from 'vue';

const HeavyChart = defineAsyncComponent(() =>
  import('./components/HeavyChart.vue')
);
```

For routes, Vue Router handles this automatically if you use dynamic imports:
```ts
const routes = [
  { path: '/admin', component: () => import('./views/Admin.vue') }
];
```

## 2. v-memo (Vue 3.2+)
Memoize parts of the template that rarely change. This skips Virtual DOM diffing entirely for that subtree.

```vue
<div v-for="item in bigList" :key="item.id" v-memo="[item.id === selectedId]">
  <!-- complex markup -->
</div>
```

## 3. Prop Stability
Avoid passing new object/array references to child components unless data actually changed. This triggers child updates.

**Bad:**
```vue
<ChildComponent :options="{ color: 'red' }" /> <!-- New object every render -->
```

**Good:**
```vue
<script setup>
const options = { color: 'red' }; // Defined once outside or in script setup
</script>
<template>
  <ChildComponent :options="options" />
</template>
```

## 4. Virtualization
For long lists (100+ items), use **VueUse `useVirtualList`** or libraries like `vue-virtual-scroller`. DOM nodes are expensive; keep the DOM size low.

## 5. Shallow Refs
If you have large objects that don't need deep reactivity (e.g., a large JSON config or immutable data), use `shallowRef()`. Vue won't make every property reactive, saving performance.

```ts
const config = shallowRef(largeConfigObject);
```

## 6. Build Optimization (Vite)
-   **Visualizer**: Use `rollup-plugin-visualizer` to analyze bundle size.
-   **Tree Shaking**: Ensure you import only what you need (e.g., `import { isEmpty } from 'lodash-es'` instead of full lodash).
