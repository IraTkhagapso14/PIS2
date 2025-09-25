import json
import yaml

class ClientsRepoBase:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_all(self):
        raise NotImplementedError

    def write_all(self, data):
        raise NotImplementedError

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

    def add_client(self, client_data):
        clients = self.read_all()
        new_id = max([c.get("client_id", 0) for c in clients], default=0) + 1
        new_client = {"client_id": new_id}
        new_client.update(client_data)
        clients.append(new_client)
        self.write_all(clients)
        return new_client

    def update_client_by_id(self, client_id, updated_data):
        clients = self.read_all()
        for i, client in enumerate(clients):
            if client.get("client_id") == client_id:
                for key, value in updated_data.items():
                    if key != "client_id":
                        client[key] = value
                clients[i] = client
                self.write_all(clients)
                return client
        print("Клиент с ID=" + str(client_id) + " не найден")
        return None

    def delete_client_by_id(self, client_id):
        clients = self.read_all()
        for i, client in enumerate(clients):
            if client.get("client_id") == client_id:
                del clients[i]
                self.write_all(clients)
                print("Клиент с ID=" + str(client_id) + " удалён")
                return True
        print("Клиент с ID=" + str(client_id) + " не найден")
        return False

    def get_count(self):
        clients = self.read_all()
        return len(clients)


class ClientsRepJSON(ClientsRepoBase):
    def read_all(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Данные должны быть списком объектов")
                return data
        except Exception:
            return []

    def write_all(self, data):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False


class ClientsRepYAML(ClientsRepoBase):
    def read_all(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data is None:
                    return []
                if not isinstance(data, list):
                    raise ValueError("Данные должны быть списком объектов")
                return data
        except Exception:
            return []

    def write_all(self, data):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, indent=2, sort_keys=False)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    repo_json = ClientsRepJSON("clients.json")
    repo_yaml = ClientsRepYAML("clients.yaml")

    print("JSON клиентов:", repo_json.get_count())
    print("YAML клиентов:", repo_yaml.get_count())

