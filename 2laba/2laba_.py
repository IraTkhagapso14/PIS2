import yaml

class Clients_rep_yaml:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_all(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if data is None:
                    return []
                if not isinstance(data, list):
                    raise ValueError("YAML должен содержать список объектов")
                return data
        except FileNotFoundError:
            print("Файл не найден: " + self.file_path)
            return []
        except yaml.YAMLError:
            print("Некорректный YAML в файле: " + self.file_path)
            return []
        except Exception as e:
            print("Неизвестная ошибка при чтении файла: " + str(e))
            return []


    def write_all(self, data):
        try:
            if not isinstance(data, list):
                raise ValueError("Данные должны быть списком объектов")
            
            with open(self.file_path, 'w', encoding='utf-8') as file:
                yaml.dump(
                    data,
                    file,
                    allow_unicode=True,
                    default_flow_style=False,
                    indent=2,
                    sort_keys=False   
                )
            return True
        except Exception as e:
            print("Ошибка при записи в файл: " + str(e))
            return False

if __name__ == "__main__":
    repo = Clients_rep_yaml("clients.yaml")
    clients = [
        {
            "client_id": 1,
            "last_name": "Сергеев",
            "first_name": "Федор",
            "otch": "Иннокеньевич",
            "address": "ул. Примерная, 19",
            "phone": "+79123456789",
            "email": "seryi@mail.ru",
            "driver_license": "1234567890"
        },
        {
            "client_id": 2,
            "last_name": "Кривцов",
            "first_name": "Никита",
            "otch": "Сергеевич",
            "address": "ул. Тестовая, 7",
            "phone": "+79123456780",
            "email": "petrov@mail.ru",
            "driver_license": "0987654321"
        }
    ]
    
    if repo.write_all(clients):
        print("Данные успешно записаны")
    
    clients = repo.read_all()
    for client in clients:
        print(client)
