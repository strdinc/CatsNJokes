import os

EXCLUDED_EXTENSIONS = {'.csv', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.bmp', '.svg', '.pdf', '.zip', '.exe'}

def count_lines_with_logging(directory):
    total_with_css = 0
    total_without_css = 0

    print(f"[INFO] Начинаем обход директории: {directory}\n")

    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXCLUDED_EXTENSIONS:
                print(f"[SKIP] {file} — исключён по расширению ({ext})")
                continue

            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = sum(1 for _ in f)
                    total_with_css += lines
                    if ext != '.css':
                        total_without_css += lines

                    suffix = " (исключён из второго счёта)" if ext == '.css' else ""
                    print(f"[OK] {filepath} — {lines} строк{suffix}")

            except Exception as e:
                print(f"[ERROR] Не удалось прочитать {filepath}: {e}")

    print("\n[INFO] Подсчёт завершён.\n")
    return total_with_css, total_without_css

# Указанный путь
directory_path = 'C:/Users/nik-f/PycharmProjects/CatsNJokes/app'

lines_with_css, lines_without_css = count_lines_with_logging(directory_path)

print("====== 📊 РЕЗУЛЬТАТ ======")
print(f"📄 Всего строк (включая .css): {lines_with_css}")
print(f"📄 Всего строк (без .css):     {lines_without_css}")
