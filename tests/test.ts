import { expect, test } from '@playwright/test';


test('NotebookFunctionality', async ({ page }) => {
  await page.goto('/');
  await page.locator('input[name="email"]').click();
  await page.locator('input[name="email"]').fill('parapallidev@gmail.com');
  await page.locator('input[name="password"]').click();
  await page.locator('input[name="password"]').fill('123456');
  await page.getByRole('button').first().click();
  await expect(page.locator('input[name="password"]')).toHaveValue('123456');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.getByRole('link', { name: 'New Notebook' }).click();
  await page.locator('input[name="name"]').click();
  await page.locator('input[name="name"]').fill('__Playwright__');
  await page.locator('input[name="notes"]').click();
  await page.locator('input[name="notes"]').fill('__PlaywrightTest__');
  await page.getByRole('button', { name: 'Create' }).click();
  await page.getByRole('button', { name: 'Local' }).click();
  await expect(page.getByRole('button', { name: 'Add AI Cell' })).toBeVisible();
  await expect(page.locator('.btn').first()).toBeVisible();
  await page.locator('.btn').first().click();
  await expect(page.locator('.skeleton').first()).toBeVisible();
  await page.getByRole('link', { name: 'Home' }).click();
  await page.getByPlaceholder('Search').click();
  await page.getByPlaceholder('Search').fill('__Playwright__');
  await page.getByRole('link', { name: '__Playwright__ Public' }).getByRole('button').click();
  await expect(page.getByRole('link', { name: '__Playwright__ Public' }).getByRole('button')).toHaveCount(0);
});

test('AICellPrompt', async ({ page }) => {
  await page.goto('/notebook/95934e45-8b5f-4351-8c2b-c2d803bc9ccb');
  await page.getByRole('button', { name: 'Local' }).click();
// Check if sources is displayed properly
  await expect(page.locator('#sources-container-ebe93ccb-72f5-4ed9-b808-7c12fa638839')).toContainText('Weights & Biases');
// If this is not complete, the runners are not working properly
  await page.getByRole('button', { name: 'Add AI Cell' }).click();
  await page.getByPlaceholder('Give instructions for setting').fill('Hello!');
});

test('Login_Register', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('button', { name: 'ARA' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Login' })).toBeVisible();
    await expect(page.getByRole('heading')).toContainText('Log in');
    await page.getByRole('link', { name: 'Register' }).click();
    await expect(page.getByRole('heading', { name: 'Register' })).toBeVisible();
  });

  test('Settings_TestPage', async ({ page }) => {
    await page.goto('/');
    await page.locator('input[name="email"]').click();
    await page.locator('input[name="email"]').fill('parapallidev@gmail.com');
    await page.locator('input[name="password"]').click();
    await page.locator('input[name="password"]').fill('123456');
    await page.getByRole('button', { name: 'Login' }).click();
    await expect(page.getByRole('list')).toContainText('parapallidev@gmail.com');
    await page.getByRole('link', { name: 'parapallidev@gmail.com' }).click();
    await expect(page.locator('body')).toContainText('Settings');
    await expect(page.locator('body')).toContainText('53346e8f-d7d0-4705-ac34-815e128b77f5');
    await page.getByRole('button', { name: 'ARA' }).dblclick();
    await expect(page.getByRole('paragraph')).toContainText('dev 123 abc');
  });