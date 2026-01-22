# Vue Testing Strategy (2026)

A robust testing strategy follows the "Testing Pyramid": many unit/component tests, fewer integration tests, and even fewer E2E tests.

## 1. Unit & Component Testing: Vitest
**Vitest** is the runner of choice (native Vite support, Jest-compatible).

### Vitest Browser Mode (Recommended for Components)
In 2026, we prefer running component tests in a real browser (via Playwright/WebDriver underneath) rather than JSDOM, for 100% accurate rendering and event handling.

```ts
// Component Test (Button.spec.ts)
import { render, screen, fireEvent } from '@testing-library/vue'; // or @vue/test-utils
import AppButton from './AppButton.vue';
import { describe, it, expect } from 'vitest';

describe('AppButton', () => {
  it('emits click event', async () => {
    const { emitted } = render(AppButton, {
      props: { label: 'Click Me' }
    });
    
    await fireEvent.click(screen.getByText('Click Me'));
    
    expect(emitted()).toHaveProperty('click');
  });
});
```

### Pure Logic Unit Tests
For composables and utility functions, standard Vitest runs are blazingly fast.

```ts
// useCounter.spec.ts
import { describe, it, expect } from 'vitest';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('increments', () => {
    const { count, increment } = useCounter();
    increment();
    expect(count.value).toBe(1);
  });
});
```

## 2. End-to-End (E2E) Testing: Playwright
**Playwright** is the industry standard for E2E. Use it to test critical user journeys (Login -> Checkout).

```ts
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
});
```

## Strategy Summary
| Type | Tool | Scope | When to write? |
|------|------|-------|----------------|
| **Unit** | Vitest | Utils, Composables, Stores | Complex logic, calculations |
| **Component** | Vitest (Browser) | Components (UI + Behavior) | Reusable components, complex interactions |
| **E2E** | Playwright | Full Pages / Flows | Critical business paths, happy paths |
