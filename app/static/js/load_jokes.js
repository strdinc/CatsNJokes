document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.statisticsJokes');
    const prevBtn = document.querySelector('.jokes-prev');
    const nextBtn = document.querySelector('.jokes-next');
    if (!container || !prevBtn || !nextBtn) return;

    let jokes = [];
    let pageStartIndex = 0;

    async function fetchJokes() {
        try {
            const response = await fetch('/get_suggested_jokes');
            const data = await response.json();
            jokes = data.jokes || [];
            pageStartIndex = 0;
            renderPage();
        } catch (error) {
            console.error('Ошибка при загрузке анекдотов:', error);
        }
    }

    function renderPage() {
        container.innerHTML = '';
        let i = pageStartIndex;
        let lastHeight = container.scrollHeight;

        while (i < jokes.length) {
            const jokeData = jokes[i];
            const jokeDiv = document.createElement('div');
            jokeDiv.className = 'suggestedJoke';

            const statusDiv = document.createElement('div');
            statusDiv.className = 'status geologica-semibold';
            statusDiv.textContent = jokeData.status;

            const textDiv = document.createElement('div');
            textDiv.className = 'text geologica-regular';
            textDiv.textContent = jokeData.text;

            jokeDiv.appendChild(statusDiv);
            jokeDiv.appendChild(textDiv);
            container.appendChild(jokeDiv);

            // Проверка на выход за границу видимой высоты
            if (container.scrollHeight > container.clientHeight) {
                container.removeChild(jokeDiv);
                break;
            }

            i++;
        }

        // Обновляем видимость кнопок
        prevBtn.style.display = pageStartIndex > 0 ? 'inline-block' : 'none';
        nextBtn.style.display = i < jokes.length ? 'inline-block' : 'none';

        // Обновляем начальный индекс следующей страницы
        visibleCount = i - pageStartIndex;
    }

    let visibleCount = 0;

    nextBtn.addEventListener('click', function () {
        if (pageStartIndex + visibleCount < jokes.length) {
            pageStartIndex += visibleCount;
            renderPage();
        }
    });

    prevBtn.addEventListener('click', function () {
        if (pageStartIndex - visibleCount >= 0) {
            pageStartIndex -= visibleCount;
        } else {
            pageStartIndex = 0;
        }
        renderPage();
    });

    fetchJokes();
});
