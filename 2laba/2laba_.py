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

if __name__ == "__main__":
    repo = Clients_rep_yaml("clients.yaml")
    clients = repo.read_all()
    
    for client in clients:
        print(client)
