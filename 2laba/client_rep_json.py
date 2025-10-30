import json
from client import Client, ClientShort


class Client_rep_json:
    def __init__(self, filename: str):
        self.filename = filename
        self.clients = self._read_all_from_file() 

    def _read_all_from_file(self):
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
        except FileNotFoundError:
            clients_list = []
        except json.JSONDecodeError:
            clients_list = []
        return clients_list

    def _write_all_to_file(self):
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

    def get_by_id(self, client_id: int):
        for c in self.clients:
            if c.client_id == client_id:
                return c
        return None

    def get_k_n_short_list(self, n: int, k: int):
        short_list = []
        start = (n - 1) * k 
        end = start + k 

        for i in range(len(self.clients)): 
            if i >= start and i < end:
                short_client = self.clients[i].to_short() 
                short_list.append(short_client)

        return short_list

    def sort_by_field(self, field="last_name", reverse=False):
        valid_fields = Client.FIELDS
        if field not in valid_fields:
            raise ValueError(f"Недопустимое поле для сортировки: {field}. Допустимые поля: {valid_fields}")

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

        return self.clients

    def add_client(self, client_data: dict):
        new_id = 1 
        if len(self.clients) > 0: 
            max_id = self.clients[0].client_id
            for c in self.clients:
                if c.client_id > max_id:
                    max_id = c.client_id
            new_id = max_id + 1

        client_data["client_id"] = new_id

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
        return new_client

    def replace_by_id(self, client_id: int, new_data: dict):
        for i in range(len(self.clients)): 
            if self.clients[i].client_id == client_id:
                new_data["client_id"] = client_id
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
                return True
        return False

    def delete_by_id(self, client_id: int):
        new_list = []
        deleted = False 

        for c in self.clients: 
            if c.client_id != client_id:
                new_list.append(c)
            else:
                deleted = True

        if deleted:  
            self.clients = new_list
            self._write_all_to_file()
            return True
        else:
            return False

    def get_count(self):
        return len(self.clients)


if __name__ == "__main__":
    repo = Client_rep_json("clients.json")

    print("Чтение всех значений из файла:")
    print(repo.clients)
    print()

    print("Запись всех значений в файл:")
    repo._write_all_to_file()
    print("Запись выполнена.\n")

    print("Добавить объект в список:")
    new_client_data = {
        "last_name": "Иванов",
        "first_name": "Иван",
        "otch": "Иванович",
        "address": "г. Краснодар, ул. Мира, 15",
        "phone": "+79123456789",
        "driver_license": "1111222233",
        "email": "ivanov@example.com"
    }
    added_client = repo.add_client(new_client_data)
    print("Добавлен клиент:", added_client)
    print()

    print("Получить объект по ID:")
    client = repo.get_by_id(1)
    print(client)
    print()

    print("Получить список k по счёту n объектов класса short:")
    short_list = repo.get_k_n_short_list(1, 2)
    for s in short_list:
        print(s)
    print()

    print("Сортировать элементы по фамилии:")
    repo.sort_by_field("last_name")
    for c in repo.clients:
        print(c)
    print()

    print("Заменить элемент списка по ID:")
    update_data = {
        "last_name": "Сидоров",
        "first_name": "Павел",
        "otch": "Андреевич",
        "address": "г. Москва, ул. Гагарина, 20",
        "phone": "+79876543210",
        "driver_license": "9999888877",
        "email": "sidorov@mail.ru"
    }
    replaced = repo.replace_by_id(1, update_data)
    print("Результат замены:", replaced)
    print("Обновлённый список:")
    for c in repo.clients:
        print(c)
    print()

    print("Удалить элемент списка по ID:")
    deleted = repo.delete_by_id(2)
    print("Результат удаления:", deleted)
    print("Текущий список:")
    for c in repo.clients:
        print(c)
    print()

    print("Получить количество элементов:")
    print("Количество клиентов:", repo.get_count())
