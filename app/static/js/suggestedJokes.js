document.addEventListener('DOMContentLoaded', () => {
    const leftColumn = document.getElementById('leftColumn');

    function loadJokes() {
        fetch('/admin/get_suggested_jokes')
            .then(response => response.json())
            .then(jokes => {
                leftColumn.innerHTML = '';
                jokes.forEach(joke => {
                    const jokeDiv = document.createElement('div');
                    jokeDiv.className = 'suggestJoke';
                    jokeDiv.innerHTML = `
                        <div class="firstLine">
                            <div class="category geologica-semibold">${joke.category}</div>
                            <div class="userID geologica-semibold">пользователь id${joke.user_id}</div>
                        </div>
                        <div class="text geologica-regular">${joke.text}</div>
                        <div class="buttons">
                            <button class="allow geologica-regular" data-id="${joke.id}">принять</button>
                            <button class="denied geologica-medium" data-id="${joke.id}">отклонить</button>
                        </div>
                    `;
                    leftColumn.appendChild(jokeDiv);
                });

                document.querySelectorAll('.allow').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const id = btn.dataset.id;
                        fetch(`/admin/approve_joke/${id}`, { method: 'POST' })
                            .then(() => loadJokes());
                    });
                });

                document.querySelectorAll('.denied').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const id = btn.dataset.id;
                        fetch(`/admin/deny_joke/${id}`, { method: 'POST' })
                            .then(() => loadJokes());
                    });
                });
            });
    }

    loadJokes();
});
