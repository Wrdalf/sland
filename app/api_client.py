import requests

class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.order_url = "https://www.sima-land.ru/api/v3/order/"
        self.barcode_url = "https://www.sima-land.ru/api/v3/item-barcode/"

    def get_order_items(self, order_id):
        url = f"{self.order_url}{order_id}/?expand=items,interests,check_items_count"
        headers = {"Authorization": self.api_key, "Accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            raise Exception(f"Ошибка при получении заказа: {response.status_code}, {response.text}")

    def get_item_barcode(self, item_id):
        url = f"{self.barcode_url}{item_id}/"
        headers = {"Authorization": self.api_key, "Accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("barcode", "Штрихкод не найден")
        else:
            raise Exception(f"Ошибка при получении штрихкода: {response.status_code}, {response.text}")
