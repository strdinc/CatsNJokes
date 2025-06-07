document.addEventListener('DOMContentLoaded', function () {
    const selectContainer = document.querySelector('.custom-select-container');
    const selected = document.querySelector('.selected-option');
    const options = document.querySelectorAll('.option-item');

    selected.addEventListener('click', () => {
        selectContainer.classList.toggle('open');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            selected.textContent = option.textContent;
            selectContainer.classList.remove('open');
            console.log("Выбрана категория:", option.textContent);
        });
    });

    document.addEventListener('click', (e) => {
        if (!selectContainer.contains(e.target)) {
            selectContainer.classList.remove('open');
        }
    });
});

document.querySelectorAll('.option-item').forEach(item => {
    item.addEventListener('click', function () {
        const selectedText = this.textContent;
        document.querySelector('.selected-option').textContent = selectedText;
        document.getElementById('selected-category').value = selectedText;
        document.querySelector('.options-list').style.display = 'none';
    });
});

    document.querySelector('.selected-option').addEventListener('click', function () {
    const list = document.querySelector('.options-list');
    list.style.display = (list.style.display === 'block') ? 'none' : 'block';
});

