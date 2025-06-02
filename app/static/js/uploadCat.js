document.getElementById('customFileButton').addEventListener('click', function () {
    document.getElementById('catFileInput').click();
});

document.getElementById('catFileInput').addEventListener('change', function () {
    const fileName = this.files[0]?.name || 'Файл не выбран';
    document.getElementById('fileNameLabel').textContent = fileName;
});
