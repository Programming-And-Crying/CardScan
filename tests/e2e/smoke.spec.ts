import { test, expect } from '@playwright/test';

test('login page is reachable', async ({ page }) => {
  await page.goto('/login/');
  await expect(page.getByText('Login')).toBeVisible();
});
