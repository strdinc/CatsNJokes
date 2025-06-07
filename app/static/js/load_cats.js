document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('statisticsCats');
    const prevButton = document.getElementById('catsPrevPage');
    const nextButton = document.getElementById('catsNextPage');
    let currentPage = 1;

    function loadCats(page = 1) {
        fetch(`/get_suggested_cats?page=${page}`)
            .then(res => res.json())
            .then(data => {
                container.innerHTML = '';

                data.cats.forEach(cat => {
                    const catDiv = document.createElement('div');
                    catDiv.className = 'suggestedCat';

                    const statusDiv = document.createElement('div');
                    statusDiv.className = 'status geologica-semibold';
                    statusDiv.textContent = cat.status;

                    const img = document.createElement('img');
                    img.className = 'image';
                    img.src = `/static/${cat.image_path.replace(/\\/g, '/')}`;
                    img.onload = checkOverflow;

                    catDiv.appendChild(statusDiv);
                    catDiv.appendChild(img);
                    container.appendChild(catDiv);
                });

                currentPage = page;
                // Если меньше трёх картинок — скрываем кнопки
                if (data.cats.length < 3 && page === 1) {
                    prevButton.style.display = 'none';
                    nextButton.style.display = 'none';
                }
            });
    }

    function checkOverflow() {
        // Проверяем, переполнен ли контейнер
        const totalHeight = Array.from(container.children).reduce((sum, el) => sum + el.offsetHeight, 0);
        const visibleHeight = container.offsetHeight;

        if (totalHeight > visibleHeight) {
            nextButton.style.display = 'block';
        } else {
            nextButton.style.display = 'none';
        }

        // Кнопка "назад" показывается только если не первая страница
        prevButton.style.display = currentPage > 1 ? 'block' : 'none';
    }

    prevButton.addEventListener('click', () => {
        if (currentPage > 1) loadCats(currentPage - 1);
    });

    nextButton.addEventListener('click', () => {
        loadCats(currentPage + 1);
    });

    loadCats();
});
