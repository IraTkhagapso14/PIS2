import json

class Clients_rep_json:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_all(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON должен содержать список объектов")
                return data
        except FileNotFoundError:
            print("Ошибка: Файл " + self.file_path + " не найден")
            return []
        except json.JSONDecodeError:
            print("Ошибка: Файл " + self.file_path + " содержит некорректный JSON")
            return []
        except Exception as e:
            print("Неизвестная ошибка при чтении файла: " + str(e))
            return []

if __name__ == "__main__":
    repo = Clients_rep_json("clients.json")
    clients = repo.read_all()
    
    for client in clients:
        print(client)
