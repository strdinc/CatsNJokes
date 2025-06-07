import os

def print_tree(startpath, prefix=""):
    for item in sorted(os.listdir(startpath)):
        path = os.path.join(startpath, item)
        if os.path.isdir(path):
            print(f"{prefix}📁 {item}/")
            print_tree(path, prefix + "    ")
        else:
            print(f"{prefix}📄 {item}")

# Задай путь к корню проекта
project_root = "C:/Users/nik-f/PycharmProjects/CatsNJokes"
print(f"Проект: {project_root}")
print_tree(project_root)
