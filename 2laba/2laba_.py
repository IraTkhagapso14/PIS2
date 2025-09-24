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

    def add_client(self, client_data):
        try:
            clients = self.read_all()
            if clients:
                max_id = max(client.get("client_id", 0) for client in clients)
                new_id = max_id + 1
            else:
                new_id = 1
        
            new_client = {"client_id": new_id}
            new_client.update(client_data)  
            clients.append(new_client)
            self.write_all(clients)
            return new_client
        except Exception as e:
            print("Ошибка при добавлении клиента:", str(e))
            return None

    def update_client_by_id(self, client_id, updated_data):
        try:
            clients = self.read_all()
            for i, client in enumerate(clients):
                if client.get("client_id") == client_id:
                    for key, value in updated_data.items():
                        if key != "client_id":
                            client[key] = value
                    clients[i] = client
                    self.write_all(clients)
                    return client
            print(f"Клиент с ID={client_id} не найден")
            return None
        except Exception as e:
            print("Ошибка при обновлении клиента:", str(e))
            return None

    def delete_client_by_id(self, client_id):
        try:
            clients = self.read_all()
            for i, client in enumerate(clients):
                if client.get("client_id") == client_id:
                    del clients[i]  
                    self.write_all(clients)
                    return True
            print(f"Клиент с ID={client_id} не найден")
            return False
        except Exception as e:
            print("Ошибка при удалении клиента:", str(e))
            return False

if __name__ == "__main__":
    repo = Clients_rep_json("clients.json")
    result = repo.delete_client_by_id(3)
    if result:
        print("Клиент удалён успешно")

