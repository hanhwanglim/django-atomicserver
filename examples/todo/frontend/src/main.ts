import axios from 'axios';

const apiBase = 'http://127.0.0.1:8000/tasks/';

const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');

async function fetchTasks() {
    const response = await axios.get(apiBase);
    const tasks = response.data;
    taskList.innerHTML = '';
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.textContent = task.title;
        if (task.completed) li.style.textDecoration = 'line-through';
        li.addEventListener('click', () => toggleTask(task));
        taskList.appendChild(li);
    });
}

taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const taskTitle = taskInput.value;
    if (taskTitle.trim() !== '') {
        await axios.post(`${apiBase}`, { title: taskTitle });
        taskInput.value = '';
        fetchTasks();
    }
});

async function toggleTask(task) {
    await axios.patch(`${apiBase}${task.id}/`, { ...task, completed: !task.completed });
    fetchTasks();
}

fetchTasks();
