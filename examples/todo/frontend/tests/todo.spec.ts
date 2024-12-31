import {expect, test} from "@playwright/test";
import axios from "axios";

const API_URL = "http://localhost:8000";

test.describe('To-Do List App', () => {

  test.beforeEach(async ({ page }) => {
    // Begin an atomic context
    await axios.get(`${API_URL}/atomic/begin/`);
    await page.goto("/");
  });

  test.afterEach(async ({page}) => {
    // Rollback the atomic context
    // Notice that this resets the count of the task items despite us creating many tasks
    await axios.get(`${API_URL}/atomic/rollback/`);
  })

  test('should add a new task', async ({ page }) => {
    const taskInput = page.locator('#task-input');
    const taskForm = page.locator('#task-form');
    const taskList = page.locator('#task-list');

    await taskInput.fill('Buy groceries');
    await taskForm.press('Enter');

    await expect(taskList).toContainText('Buy groceries');

    const tasks = await page.locator('#task-list li').count();
    expect(tasks).toBe(1);
  });

  test('should toggle task completion', async ({ page }) => {
    const taskInput = page.locator('#task-input');
    const taskForm = page.locator('#task-form');
    const taskList = page.locator('#task-list');

    await taskInput.fill('Complete homework');
    await taskForm.press('Enter');

    const taskItem = taskList.locator('text=Complete homework');
    await expect(taskItem).toBeVisible();

    await taskItem.click();
    await expect(taskItem).toHaveCSS('text-decoration', 'line-through solid rgb(0, 0, 0)');

    const tasks = await page.locator('#task-list li').count();
    expect(tasks).toBe(1);
  });

  test('should handle multiple tasks', async ({ page }) => {
    const taskInput = page.locator('#task-input');
    const taskForm = page.locator('#task-form');
    const taskList = page.locator('#task-list');

    await taskInput.fill('Task 1');
    await taskForm.press('Enter');
    await taskInput.fill('Task 2');
    await taskForm.press('Enter');
    await taskInput.fill('Task 3');
    await taskForm.press('Enter');

    await expect(taskList).toContainText('Task 1');
    await expect(taskList).toContainText('Task 2');
    await expect(taskList).toContainText('Task 3');

    const task1 = taskList.locator('text=Task 1');
    await task1.click();
    await expect(task1).toHaveCSS('text-decoration', 'line-through solid rgb(0, 0, 0)');

    const tasks = await page.locator('#task-list li').count();
    expect(tasks).toBe(3);
  });
});
