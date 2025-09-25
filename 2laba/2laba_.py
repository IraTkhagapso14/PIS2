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

    def get_by_id(self, client_id):
        clients = self.read_all()
        for client in clients:
            if client.get("client_id") == client_id:
                return client
        print("Клиент с ID=" + str(client_id) + " не найден")
        return None

    def get_k_n_short_list(self, n, k):
        clients = self.read_all()
        start_index = (n - 1) * k
        end_index = start_index + k
        return clients[start_index:end_index]
        
    def sort_by_field(self, field_name, reverse=False):
        clients = self.read_all()
        try:
            sorted_clients = sorted(clients, key=lambda x: x.get(field_name, ""), reverse=reverse)
            return sorted_clients
        except Exception as e:
            print("Ошибка при сортировке: " + str(e))
            return clients

if __name__ == "__main__":
    repo = Clients_rep_yaml("clients.yaml")
    sorted_clients = repo.sort_by_field("last_name")
    print("Клиенты, отсортированные по фамилии:")
    for client in sorted_clients:
        print(client)
