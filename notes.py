import os
import json
import datetime

notes = []

def add_note():
  title = input("Введите заголовок заметки: ")
  body = input("Введите тело заметки: ")
  
  max_id = max(note['id'] for note in notes) if notes else 0
  new_id = max_id + 1
    
  note = {
    "id": new_id, 
    "title": title,
    "body": body,
    "created": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
  }

  notes.append(note)
  print("Заметка добавлена")

def edit_note():
  id = int(input("Введите ID заметки для редактирования: "))
  
  note = next((note for note in notes if note['id'] == id), None)
  if note:
    title = input("Введите новый заголовок заметки: ")
    body = input("Введите новое тело заметки: ")

    note['title'] = title
    note['body'] = body

    print("Заметка обновлена")
  else:
    print("Заметка с таким ID не найдена")

def delete_note():
  id = int(input("Введите ID заметки для удаления: "))

  note = next((note for note in notes if note['id'] == id), None)
  if note:
    notes.remove(note)
    print("Заметка удалена")
  else:
    print("Заметка с таким ID не найдена")

def show_notes(date=None, title=None, note_id=None):
    filtered_notes = notes

    if date:
        filtered_notes = [note for note in filtered_notes if note["created"].startswith(date)]
    if title:
        filtered_notes = [note for note in filtered_notes if title.lower() in note["title"].lower()]
    if note_id:
        filtered_notes = [note for note in filtered_notes if note["id"] == note_id]

    if not filtered_notes:
        print("Заметки не найдены.")
        return

    for note in filtered_notes:
        print(f"ID: {note['id']}")
        print(f"Заголовок: {note['title']}") 
        print(f"Тело: {note['body']}")
        print(f"Дата создания: {note['created']}")
        print("-" * 40)

def save_notes():
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def load_notes():
    global notes
    if os.path.exists("notes.json"):
        with open("notes.json", encoding="utf-8") as f:
            try:
                notes = json.load(f)
            except json.JSONDecodeError:
                print("Ошибка при загрузке заметок. Создан новый список заметок.")
                notes = []
    else:
        print("Файл notes.json не существует. Создан новый список заметок.")
        notes = []


def main():

  while True:
    command = input("Введите команду (add, edit, delete, show, save, exit): ")

    if command == "add":
      add_note()
    elif command == "edit":
      edit_note()
    elif command == "delete":
      delete_note()
    elif command == "show":
            filter_choice = input("Выберите фильтр (date, title, id) или Enter для показа всех: ").strip().lower()
            if filter_choice == "date":
                date = input("Введите дату для фильтрации в формате дд-мм-гггг: ")
                show_notes(date=date)
            elif filter_choice == "title":
                title = input("Введите часть заголовка для фильтрации: ")
                show_notes(title=title)
            elif filter_choice == "id":
                try:
                    note_id = int(input("Введите ID заметки для фильтрации: "))
                    show_notes(note_id=note_id)
                except ValueError:
                    print("Некорректный ID. Пожалуйста, введите целое число.")
            else:
                show_notes()
    elif command == "save":
      save_notes() 
    elif command == "exit":
      save_notes()
      break
    else:
      print("Неизвестная команда")

if __name__ == "__main__":
  load_notes()
  main()