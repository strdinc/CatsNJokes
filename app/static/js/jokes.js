let currentPage = 0;

async function loadContent(page) {
    try {
        const container = document.querySelector('.CatNJokesContainer');

        // Плавно скрыть текущие элементы
        const children = Array.from(container.children);
        children.forEach(el => el.classList.add('fade-out'));

        // Подождать перед удалением
        await new Promise(resolve => setTimeout(resolve, 600));
        container.innerHTML = '';

        const response = await fetch(`/get_content?page=${page}`);
        const data = await response.json();

        const combined = [
            ...data.jokes.map(joke => ({ type: 'joke', data: joke })),
            ...data.images.map(image => ({ type: 'image', data: image }))
        ];

        // Перемешать
        for (let i = combined.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [combined[i], combined[j]] = [combined[j], combined[i]];
        }

        // Постепенно добавлять элементы с плавным появлением
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

                // Триггер показа
                setTimeout(() => {
                    el.classList.add('show');
                }, 20);
            }, delay);
        });

    } catch (error) {
        console.error('Ошибка загрузки контента:', error);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    loadContent(currentPage);
});

function scrollToTop() {
    const container = document.querySelector('.CatNJokesContainer');
    if (container) {
        const rect = container.getBoundingClientRect();
        const scrollY = window.scrollY || window.pageYOffset;
        window.scrollTo({
            top: rect.top + scrollY,
            behavior: 'smooth'
        });
    }
}
