import psycopg2
import re
from client import Client, ClientShort


class ClientRepDB:
    def __init__(self, host='localhost', user='postgres', password='123',
                 database='clients_auto', port='5432'):
        self.host = host 
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None 
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            print(f"Успешное подключение к базе данных '{self.database}'")
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def execute_query(self, query, params=None, fetch=False):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
            self.connection.commit()
            cursor.close()
            return result
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Ошибка выполнения запроса: {e}")
            return None
        except Exception as e:
            self.connection.rollback()
            print(f"Общая ошибка: {e}")
            return None

    def _read_all_from_file(self):
        print(f"Чтение всех клиентов из базы данных")
        query = "SELECT client_id, last_name, first_name, otch, address, phone, email, driver_license FROM client"
        result = self.execute_query(query, fetch=True)
        clients_list = []
        if result:
            for row in result:
                client = Client(
                    client_id=row[0],
                    last_name=row[1],
                    first_name=row[2],
                    otch=row[3],
                    address=row[4],
                    phone=row[5],
                    email=row[6],
                    driver_license=row[7]
                )
                clients_list.append(client)
        print(f"Успешно прочитано {len(clients_list)} клиентов из базы данных")
        return clients_list

    def _write_all_to_file(self):
        print("Запись")
        return True

    def get_max_client_id(self):
        query = "SELECT COALESCE(MAX(client_id), 0) FROM client"
        result = self.execute_query(query, fetch=True)
        if result:
            return result[0][0]
        return 0

    def get_by_id(self, client_id: int):
        print(f"Поиск клиента с ID: {client_id}")
        query = """
        SELECT client_id, last_name, first_name, otch, address, phone, email, driver_license 
        FROM client WHERE client_id = %s
        """
        result = self.execute_query(query, (client_id,), fetch=True)
        if result and len(result) > 0:
            row = result[0]
            client = Client(
                client_id=row[0],
                last_name=row[1],
                first_name=row[2],
                otch=row[3],
                address=row[4],
                phone=row[5],
                email=row[6],
                driver_license=row[7]
            )
            print(f"Найден клиент: {client.full_repr()}")
            return client
        print(f"Клиент с ID {client_id} не найден")
        return None

    def get_k_n_short_list(self, n: int, k: int):
        print(f"Получение {k} клиентов на странице {n}")
        offset = (n - 1) * k
        query = """
        SELECT client_id, last_name, first_name, otch, phone, email
        FROM client
        ORDER BY client_id
        LIMIT %s OFFSET %s
        """
        result = self.execute_query(query, (k, offset), fetch=True)
        short_clients = []
        for row in result:
            contact = row[5] if row[5] else row[4]
            short_client = ClientShort(
                client_id=row[0],
                last_name=row[1],
                first_name=row[2],
                otch=row[3],
                contact=contact
            )
            short_clients.append(short_client)

        print(f"Получено {len(short_clients)} клиентов (страница {n}):")
        for i, client in enumerate(short_clients, 1):
            print(f"   {i}. {client}")
        return short_clients

    def sort_by_field(self, field="last_name", reverse=False):
        print(f"Сортировка по полю '{field}' ({'по убыванию' if reverse else 'по возрастанию'})")

        valid_fields = Client.FIELDS
        if field not in valid_fields:
            error_msg = f"Недопустимое поле для сортировки: {field}. Допустимые поля: {valid_fields}"
            print(error_msg)
            raise ValueError(error_msg)

        query = f"SELECT client_id, last_name, first_name, otch, address, phone, email, driver_license FROM client"
        result = self.execute_query(query, fetch=True)

        if not result:
            print("В базе нет клиентов для сортировки")
            return []

        sort_list = []
        clients_map = {}

        for row in result:
            client = Client(
                client_id=row[0],
                last_name=row[1],
                first_name=row[2],
                otch=row[3],
                address=row[4],
                phone=row[5],
                email=row[6],
                driver_license=row[7]
            )
            clients_map[row[0]] = client

            value = getattr(client, field)

            if value is None:
                if field == "client_id":
                    key = 0  
                else:
                    key = ""  
            else:
                key = value

            sort_list.append((key, row[0]))

        sort_list.sort(key=lambda x: x[0], reverse=reverse)

        sorted_clients = [clients_map[client_id] for key, client_id in sort_list]

        print("Список отсортирован:")
        for i, client in enumerate(sorted_clients, 1):
            print(f"   {i}. {client.short_repr()}")

        return sorted_clients

    def add_client(self, client_data: dict):
        print("Добавление нового клиента")
        try:
            max_id = self.get_max_client_id()
            new_id = max_id + 1

            client = Client(
                client_id=new_id,
                last_name=client_data["last_name"],
                first_name=client_data["first_name"],
                address=client_data["address"],
                phone=client_data["phone"],
                driver_license=client_data["driver_license"],
                otch=client_data.get("otch"),
                email=client_data.get("email")
            )

            query = """
            INSERT INTO client (client_id, last_name, first_name, otch, address, phone, email, driver_license)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                new_id,
                client_data["last_name"],
                client_data["first_name"],
                client_data.get("otch"),
                client_data["address"],
                client_data["phone"],
                client_data.get("email"),
                client_data["driver_license"]
            )
            result = self.execute_query(query, params)

            if result:
                new_client = Client(
                    client_id=new_id,
                    last_name=client_data["last_name"],
                    first_name=client_data["first_name"],
                    address=client_data["address"],
                    phone=client_data["phone"],
                    driver_license=client_data["driver_license"],
                    otch=client_data.get("otch"),
                    email=client_data.get("email")
                )
                print(f"Клиент успешно добавлен с ID {new_id}: {new_client.full_repr()}")
                return new_client
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except Exception as e:
            print(f"Ошибка при добавлении: {e}")
            return None

    def replace_by_id(self, client_id: int, new_data: dict):
        print(f"Замена клиента с ID: {client_id}")

        existing_client = self.get_by_id(client_id)
        if not existing_client:
            print(f"Клиент с ID {client_id} не найден")
            return False

        try:
            new_data["client_id"] = client_id

            updated_client = Client(
                client_id=new_data["client_id"],
                last_name=new_data["last_name"],
                first_name=new_data["first_name"],
                address=new_data["address"],
                phone=new_data["phone"],
                driver_license=new_data["driver_license"],
                otch=new_data.get("otch"),
                email=new_data.get("email")
            )

            query = """
            UPDATE client 
            SET last_name = %s, first_name = %s, otch = %s, address = %s, 
                phone = %s, email = %s, driver_license = %s
            WHERE client_id = %s
            """
            params = (
                new_data["last_name"],
                new_data["first_name"],
                new_data.get("otch"),
                new_data["address"],
                new_data["phone"],
                new_data.get("email"),
                new_data["driver_license"],
                client_id
            )
            rows_affected = self.execute_query(query, params)
            if rows_affected:
                print(f"Клиент с ID {client_id} успешно заменен: {updated_client.full_repr()}")
                return True
            return False
        except ValueError as e:
            print(f"Ошибка валидации данных: {e}")
            return False
        except Exception as e:
            print(f"Ошибка при замене клиента: {e}")
            return False

    def delete_by_id(self, client_id: int):
        print(f"Удаление клиента с ID: {client_id}")

        client_to_delete = self.get_by_id(client_id)
        if not client_to_delete:
            print(f"Клиент с ID {client_id} не найден")
            return False

        query = "DELETE FROM client WHERE client_id = %s"
        rows_affected = self.execute_query(query, (client_id,))
        if rows_affected:
            print(f"Клиент с ID {client_id} успешно удален: {client_to_delete.short_repr()}")
            return True
        return False

    def get_count(self):
        query = "SELECT COUNT(*) FROM client"
        result = self.execute_query(query, fetch=True)
        count = result[0][0] if result else 0
        print(f"Количество клиентов в базе: {count}")
        return count

    def display_all_clients(self):
        clients = self._read_all_from_file()
        print("\nсписок клиентов:")
        if not clients:
            print("   Список пуст")
        for i, client in enumerate(clients, 1):
            print(f"   {i}. {client.full_repr()}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")


if __name__ == "__main__":
    try:
        repo_db = ClientRepDB(
            host='localhost',
            user='postgres',
            password='123',
            database='clients_auto',
            port='5432'
        )


        print("\n текущие данные:")
        repo_db.display_all_clients()

        print("\nдобавление клиента:")
        new_client_data = {
            "last_name": "Иванов",
            "first_name": "Иван",
            "otch": "Иванович",
            "address": "г. Москва, ул. Ленина, 10",
            "phone": "+79161234567",
            "driver_license": "1234567890",
            "email": "ivanov@mail.ru"
        }
        added_client = repo_db.add_client(new_client_data)

        if not added_client:
            print("Ошибка при добавлении клиента")
            exit()

        print(f"\n поиск по id ({added_client.client_id}):")
        client = repo_db.get_by_id(added_client.client_id)

        print(f"\n пагинация (страница 1, 2 клиента):")
        short_clients = repo_db.get_k_n_short_list(1, 2)

        print(f"\nсортировка по фамилии:")
        repo_db.sort_by_field("last_name")

        print(f"\nзамена клиента (ID: {added_client.client_id}):")
        update_data = {
            "last_name": "Сидоров",
            "first_name": "Павел",
            "otch": "Андреевич",
            "address": "г. Москва, ул. Гагарина, 20",
            "phone": "+79876543210",
            "driver_license": "9999888877",
            "email": "sidorov@mail.ru"
        }
        replaced = repo_db.replace_by_id(added_client.client_id, update_data)
        print(f"Результат замены: {'Успешно' if replaced else 'Ошибка'}")

        print(f"\nудаление клиента (ID: {added_client.client_id}):")
        deleted = repo_db.delete_by_id(added_client.client_id)
        print(f"Результат удаления: {'Успешно' if deleted else 'Ошибка'}")

        print(f"\nподсчет клиентов:")
        count = repo_db.get_count()


        print(f"\nфинальные данные:")
        repo_db.display_all_clients()


    except Exception as e:
        print(f"Произошла ошибка при тестировании: {e}")
    finally:
        repo_db.close()
