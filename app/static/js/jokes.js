let currentPage = 0;

// Загрузка всех анекдотов и котов
async function loadContent(page) {
    try {
        const container = document.querySelector('.CatNJokesContainer');

        const children = Array.from(container.children);
        children.forEach(el => el.classList.add('fade-out'));
        await new Promise(resolve => setTimeout(resolve, 600));
        container.innerHTML = '';

        const response = await fetch(`/get_content?page=${page}`);
        const data = await response.json();

        const combined = [
            ...data.jokes.map(joke => ({ type: 'joke', data: joke })),
            ...data.images.map(image => ({ type: 'image', data: image }))
        ];

        for (let i = combined.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [combined[i], combined[j]] = [combined[j], combined[i]];
        }

        combined.forEach((item, index) => {
            const delay = index * 120;

            setTimeout(() => {
                let el;
                if (item.type === 'joke') {
                    el = document.createElement('div');
                    el.className = 'joke fade-in';

                    const textDiv = document.createElement('div');
                    textDiv.className = 'jokeText geologica-light';
                    textDiv.textContent = item.data.text;

                    el.appendChild(textDiv);
                } else {
                    el = document.createElement('div');
                    el.className = 'CatImage fade-in';

                    const img = document.createElement('img');
                    img.src = "/static/CatsImages/" + item.data.path;
                    img.alt = 'cat';

                    el.appendChild(img);
                }

                container.appendChild(el);
                setTimeout(() => el.classList.add('show'), 20);
            }, delay);
        });

    } catch (error) {
        console.error('Ошибка загрузки контента:', error);
    }
}

// Загрузка анекдотов определённой категории
async function loadCategory(category, clickedButton) {
    try {
        const container = document.querySelector('.CatNJokesContainer');

        const children = Array.from(container.children);
        children.forEach(el => el.classList.add('fade-out'));
        await new Promise(resolve => setTimeout(resolve, 600));
        container.innerHTML = '';

        const response = await fetch(`/get_category_jokes?category=${encodeURIComponent(category)}`);
        const data = await response.json();

        const combined = [
            ...data.jokes.map(joke => ({ type: 'joke', data: joke })),
            ...data.images.map(image => ({ type: 'image', data: image }))
        ];

        for (let i = combined.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [combined[i], combined[j]] = [combined[j], combined[i]];
        }

        combined.forEach((item, index) => {
            const delay = index * 120;

            setTimeout(() => {
                let el;
                if (item.type === 'joke') {
                    el = document.createElement('div');
                    el.className = 'joke fade-in';

                    const textDiv = document.createElement('div');
                    textDiv.className = 'jokeText geologica-light';
                    textDiv.textContent = item.data.text;

                    el.appendChild(textDiv);
                } else {
                    el = document.createElement('div');
                    el.className = 'CatImage fade-in';

                    const img = document.createElement('img');
                    img.src = "/static/CatsImages/" + item.data.path;
                    img.alt = 'cat';

                    el.appendChild(img);
                }

                container.appendChild(el);
                setTimeout(() => el.classList.add('show'), 20);
            }, delay);
        });

        // Обработка активного состояния кнопок категорий
        document.querySelectorAll('.categoryButton').forEach(btn => {
            btn.classList.remove('active-category');
        });
        if (clickedButton) {
            clickedButton.classList.add('active-category');
        }

        scrollToTop();
    } catch (error) {
        console.error('Ошибка при загрузке категории:', error);
    }
}

// Загрузка анекдота дня
function loadDayJoke() {
    fetch('/get_day_joke')
        .then(res => res.json())
        .then(data => {
            const el = document.querySelector('.dayJoke');
            el.textContent = data.text;
        })
        .catch(err => {
            console.error('Ошибка при загрузке анекдота дня:', err);
        });
}

// Загрузка категорий из БД и добавление кнопок
function loadCategories() {
    fetch('/get_categories')
        .then(res => res.json())
        .then(categories => {
            const container = document.querySelector('.otherButtons');
            container.innerHTML = '';

            categories.forEach(cat => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'otherButton categoryButton geologica-regular';
                btn.textContent = cat;

                btn.addEventListener('click', () => {
                    loadCategory(cat, btn);
                });

                container.appendChild(btn);
            });
        })
        .catch(err => {
            console.error('Ошибка при загрузке категорий:', err);
        });
}

// Скролл к началу
function scrollToTop() {
    const container = document.querySelector('.leftColumn');
    if (container) {
        const rect = container.getBoundingClientRect();
        const scrollY = window.scrollY || window.pageYOffset;
        window.scrollTo({
            top: rect.top + scrollY,
            behavior: 'smooth'
        });
    }
}

// Обработка кнопки "все анекдоты"
function setupAllJokesButton() {
    const btn = document.querySelector('.allJokes');
    if (btn) {
        btn.addEventListener('click', () => {
            // Убираем активность с кнопок категорий
            document.querySelectorAll('.categoryButton').forEach(b => {
                b.classList.remove('active-category');
            });

            loadContent(currentPage);
        });
    }
}

// Инициализация при загрузке страницы
window.addEventListener('DOMContentLoaded', () => {
    loadContent(currentPage);
    loadCategories();
    loadDayJoke();
    setupAllJokesButton();
});
