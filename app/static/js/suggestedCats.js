async function loadCats() {
    const response = await fetch('/admin/get_suggested_cats');
    const cats = await response.json();

    const container = document.getElementById('rightColumn');
    container.innerHTML = '';

    cats.forEach(cat => {
        const div = document.createElement('div');
        div.className = 'suggestedCat';
        div.innerHTML = `
            <div class="userID geologica-semibold">пользователь id${cat.user_id}</div>
            <img class="imgCat" src="/static/${cat.image_path}" alt="cat">
            <div class="buttons">
                <button class="allow geologica-regular" data-id="${cat.id}">принять</button>
                <button class="denied geologica-medium" data-id="${cat.id}">отклонить</button>
            </div>
        `;
        container.appendChild(div);
    });

    document.querySelectorAll('.allow').forEach(button => {
        button.onclick = () => moderateCat(button.dataset.id, 'принять');
    });

    document.querySelectorAll('.denied').forEach(button => {
        button.onclick = () => moderateCat(button.dataset.id, 'отклонить');
    });
}

async function moderateCat(id, action) {
    const response = await fetch('/moderate_cat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, action })
    });

    const result = await response.json();
    if (result.success) {
        loadCats(); // перезагрузка списка
    }
}

window.onload = loadCats;
