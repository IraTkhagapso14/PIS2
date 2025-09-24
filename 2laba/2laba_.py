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
            print("Ошибка при сортировке:", str(e))
            return clients

if __name__ == "__main__":
    repo = Clients_rep_json("clients.json")

    sorted_clients = repo.sort_by_field("last_name")
    print("\nКлиенты, отсортированные по фамилии:")
    for c in sorted_clients:
        print(c)
