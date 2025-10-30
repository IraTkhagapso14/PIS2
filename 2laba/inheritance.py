import json
import yaml
from client import Client, ClientShort


class ClientRepository:
    def __init__(self, filename: str):
        self.filename = filename
        self.clients = self._read_all_from_file()

    def get_by_id(self, client_id: int):
        print(f"Поиск клиента с ID: {client_id}")
        for c in self.clients:
            if c.client_id == client_id:
                print(f"Найден клиент: {c.full_repr()}")
                return c
        print(f"Клиент с ID {client_id} не найден")
        return None

    def get_k_n_short_list(self, n: int, k: int):
        print(f"Получение {k} клиентов на странице {n}")
        short_list = []
        start = (n - 1) * k
        end = start + k

        for i in range(len(self.clients)):
            if i >= start and i < end:
                short_client = self.clients[i].to_short()
                short_list.append(short_client)

        print(f"Получено {len(short_list)} клиентов (страница {n}):")
        for i, client in enumerate(short_list, 1): 
            print(f"   {i}. {client}")
        return short_list

    def sort_by_field(self, field="last_name", reverse=False):
        print(f"Сортировка по полю '{field}' ({'по убыванию' if reverse else 'по возрастанию'})")

        valid_fields = Client.FIELDS
        if field not in valid_fields:
            error_msg = f"Недопустимое поле для сортировки: {field}. Допустимые поля: {valid_fields}"
            print(error_msg)
            raise ValueError(error_msg)

        sort_list = []

        for client in self.clients:
            value = getattr(client, field)

            if value is None:
                if field == "client_id":
                    key = 0
                else:
                    key = ""
            else:
                key = value

            sort_list.append((key, client))

        sort_list.sort(key=lambda x: x[0], reverse=reverse)
        self.clients = [client for key, client in sort_list]
        self._write_all_to_file()

        print("Список отсортирован:")
        for i, client in enumerate(self.clients, 1):
            print(f"   {i}. {client.short_repr()}")

        return self.clients

    def add_client(self, client_data: dict):
        print("Добавление нового клиента")

        new_id = 1
        if len(self.clients) > 0:
            max_id = self.clients[0].client_id
            for c in self.clients:
                if c.client_id > max_id:
                    max_id = c.client_id
            new_id = max_id + 1

        client_data["client_id"] = new_id

        try:
            new_client = Client(
                client_id=client_data["client_id"],
                last_name=client_data["last_name"],
                first_name=client_data["first_name"],
                otch=client_data.get("otch"),
                address=client_data["address"],
                phone=client_data["phone"],
                driver_license=client_data["driver_license"],
                email=client_data.get("email")
            )

            self.clients.append(new_client)
            self._write_all_to_file()
            print(f"Клиент успешно добавлен с ID {new_id}: {new_client.full_repr()}")
            return new_client

        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except Exception as e:
            print(f"Ошибка при добавлении: {e}")
            return None

    def replace_by_id(self, client_id: int, new_data: dict):
        print(f"Замена клиента с ID: {client_id}")

        for i in range(len(self.clients)):
            if self.clients[i].client_id == client_id:
                new_data["client_id"] = client_id
                try:
                    updated_client = Client(
                        client_id=new_data["client_id"],
                        last_name=new_data["last_name"],
                        first_name=new_data["first_name"],
                        otch=new_data.get("otch"),
                        address=new_data["address"],
                        phone=new_data["phone"],
                        driver_license=new_data["driver_license"],
                        email=new_data.get("email")
                    )
                    self.clients[i] = updated_client
                    self._write_all_to_file()
                    print(f"Клиент с ID {client_id} успешно заменен: {updated_client.full_repr()}")
                    return True
                except ValueError as e:
                    print(f"Ошибка валидации: {e}")
                    return False
                except KeyError as e:
                    print(f"Отсутствует обязательное поле: {e}")
                    return False

        print(f"Клиент с ID {client_id} не найден")
        return False

    def delete_by_id(self, client_id: int):
        print(f"Удаление клиента с ID: {client_id}")

        new_list = []
        deleted = False
        deleted_client = None

        for c in self.clients:
            if c.client_id != client_id:
                new_list.append(c)
            else:
                deleted = True
                deleted_client = c

        if deleted:
            self.clients = new_list
            self._write_all_to_file()
            print(f"Клиент с ID {client_id} удален: {deleted_client.short_repr()}")
            return True
        else:
            print(f"Клиент с ID {client_id} не найден")
            return False

    def get_count(self):
        count = len(self.clients)
        print(f"Количество клиентов в репозитории: {count}")
        return count

    def display_all_clients(self):
        print("\n текущий список клиентов:")
        if not self.clients:
            print("Список пуст")
        for i, client in enumerate(self.clients, 1):
            print(f"   {i}. {client.full_repr()}")


class ClientRepJSON(ClientRepository):

    def _read_all_from_file(self):
        print(f"Чтение JSON файла: {self.filename}")
        clients_list = []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    client = Client(
                        client_id=item["client_id"],
                        last_name=item["last_name"],
                        first_name=item["first_name"],
                        otch=item.get("otch"),
                        address=item["address"],
                        phone=item["phone"],
                        driver_license=item["driver_license"],
                        email=item.get("email")
                    )
                    clients_list.append(client)
            print(f"Успешно прочитано {len(clients_list)} клиентов из JSON")
        except FileNotFoundError:
            print(" Файл не найден, создан пустой список")
            clients_list = []
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON, создан пустой список")
            clients_list = []
        except Exception as e:
            print(f"Ошибка при чтении JSON: {e}")
            clients_list = []
        return clients_list

    def _write_all_to_file(self):
        print(f"Запись в JSON файл: {self.filename}")
        try:
            data_to_save = []
            for c in self.clients:
                obj = {
                    "client_id": c.client_id,
                    "last_name": c.last_name,
                    "first_name": c.first_name,
                    "otch": c.otch,
                    "address": c.address,
                    "phone": c.phone,
                    "email": c.email,
                    "driver_license": c.driver_license
                }
                data_to_save.append(obj)

            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
            print(f"Успешно записано {len(data_to_save)} клиентов в JSON")
            return True
        except Exception as e:
            print(f"Ошибка при записи JSON: {e}")
            return False


class ClientRepYAML(ClientRepository):

    def _read_all_from_file(self):
        print(f"Чтение YAML файла: {self.filename}")
        clients_list = []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data is None:
                    clients_list = []
                else:
                    for item in data:
                        client = Client(
                            client_id=item["client_id"],
                            last_name=item["last_name"],
                            first_name=item["first_name"],
                            otch=item.get("otch"),
                            address=item["address"],
                            phone=item["phone"],
                            driver_license=item["driver_license"],
                            email=item.get("email")
                        )
                        clients_list.append(client)
            print(f"Успешно прочитано {len(clients_list)} клиентов из YAML")
        except FileNotFoundError:
            print("Файл не найден, создан пустой список")
            clients_list = []
        except Exception as e:
            print(f"Ошибка при чтении YAML: {e}")
            clients_list = []
        return clients_list

    def _write_all_to_file(self):
        print(f"Запись в YAML файл: {self.filename}")
        try:
            data_to_save = []
            for c in self.clients:
                obj = {
                    "client_id": c.client_id,
                    "last_name": c.last_name,
                    "first_name": c.first_name,
                    "otch": c.otch,
                    "address": c.address,
                    "phone": c.phone,
                    "email": c.email,
                    "driver_license": c.driver_license
                }
                data_to_save.append(obj)

            with open(self.filename, "w", encoding="utf-8") as f:
                yaml.safe_dump(data_to_save, f, allow_unicode=True, default_flow_style=False)
            print(f"Успешно записано {len(data_to_save)} клиентов в YAML")
            return True
        except Exception as e:
            print(f"Ошибка при записи YAML: {e}")
            return False


def test_repository(repo, repo_name):

    print("\nТекущие данные:")
    repo.display_all_clients()

    print("\n Добавление клиента:")
    new_client_data = {
        "last_name": "Петров",
        "first_name": "Петр",
        "otch": "Петрович",
        "address": "г. Москва, ул. Ленина, 1",
        "phone": "+79161234567",
        "driver_license": "1234567890",
        "email": "petrov@mail.ru"
    }
    added_client = repo.add_client(new_client_data)

    if added_client:
        print(f"\n поиск по id({added_client.client_id}):")
        found_client = repo.get_by_id(added_client.client_id)

    print(f"\n пагинация (страница 1, 2 клиента):")
    short_list = repo.get_k_n_short_list(1, 2)

    print(f"\n сортировка по фамилии:")
    repo.sort_by_field("last_name")

    if added_client:
        print(f"\nзамена клиента (ID: {added_client.client_id}):")
        update_data = {
            "last_name": "Сидоров",
            "first_name": "Сидор",
            "otch": "Сидорович",
            "address": "г. СПб, Невский пр., 100",
            "phone": "+79998887766",
            "driver_license": "0987654321",
            "email": "sidorov@mail.ru"
        }
        repo.replace_by_id(added_client.client_id, update_data)

    if added_client:
        print(f"\n удаление клиента(ID: {added_client.client_id}):")
        repo.delete_by_id(added_client.client_id)

    print(f"\nкол-во клиентов:")
    repo.get_count()


    print(f"\n данные:")
    repo.display_all_clients()


if __name__ == "__main__":
    repo_json = ClientRepJSON("clients.json")
    test_repository(repo_json, "JSON репозиторий")

    repo_yaml = ClientRepYAML("clients.yaml")
    test_repository(repo_yaml, "YAML репозиторий")


