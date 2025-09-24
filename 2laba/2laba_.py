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

    def write_all(self, data):
        try:
            if not isinstance(data, list): 
                raise ValueError("Данные должны быть списком объектов")             
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            print("Данные успешно записаны в файл " + self.file_path)
            return True
        except Exception as e:
            print("Ошибка при записи в файл: " + str(e)) 
            return False

    def get_by_id(self, client_id):
        try:
            clients = self.read_all()
            for client in clients:
                if client.get('client_id') == client_id:
                    return client
            
            return None
        except Exception as e:
            print("Ошибка при поиске клиента по ID: " + str(e))
            return None

if __name__ == "__main__":
    repo = Clients_rep_json("clients.json")
    clients = repo.read_all()
    
    for client in clients:
        print(client)
     new_clients = [
        {
            "client_id": 1,
            "last_name": "Иванов",
            "first_name": "Иван",
            "otch": "Иванович",
            "address": "ул. Северная, 123",
            "phone": "+79123456789",
            "email": "ivanov@mail.ru",
            "driver_license": "1234567890"
        },
        {
            "client_id": 2,
            "last_name": "Петров",
            "first_name": "Петр",
            "otch": "Петрович",
            "address": "ул. Архангельская, 456",
            "phone": "+79123456780",
            "email": "petrov@mail.ru",
            "driver_license": "0987654321"
        }
    ]
    repo.write_all(new_clients)
    client_id = 1
    client = repo.get_by_id(client_id)
    
    if client:
        print("Найден клиент с ID", client_id)
        print(client)
    else:
        print("Клиент с ID", client_id, "не найден")
    

