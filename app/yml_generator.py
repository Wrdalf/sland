import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone
# import send_file_to_server

class YMLGenerator:
    def prettify_xml(self, elem):
        """
        Форматирует XML-элемент в удобный для чтения формат.
        :param elem: Корневой элемент XML.
        :return: Строка XML с отступами.
        """
        rough_string = ET.tostring(elem, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def create_yml_file(self, order_id, items, api_client):
        """
        Создает YML-файл на основе данных заказа.
        :param order_id: Идентификатор заказа.
        :param items: Список товаров.
        :param api_client: Клиент API для получения данных.
        """
        # Создание корневого элемента YML
        yml_catalog = ET.Element("yml_catalog", date=datetime.now(timezone.utc).isoformat())
        shop = ET.SubElement(yml_catalog, "shop")
        offers = ET.SubElement(shop, "offers")

        # Добавление товаров в YML
        for item in items:
            offer = ET.SubElement(offers, "offer", id=str(item.get("item_sid")))
            ET.SubElement(offer, "name").text = item.get("item_name", "Нет названия")
            ET.SubElement(offer, "barcode").text = item.get("barcode", "Нет штрихкода")

        # Форматирование и сохранение XML
        pretty_xml = self.prettify_xml(yml_catalog)
        filename = f"order_{order_id}.yml"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

    def create_yml_file_from_excel(self, mapped_data):
        """
        Создает YML-файл на основе данных из Excel.
        :param mapped_data: Сопоставленные данные из Excel (словарь с ключами 'Артикул', 'Название', 'Штрихкод').
        """
        # Создание корневого элемента YML
        yml_catalog = ET.Element("yml_catalog", date=datetime.now(timezone.utc).isoformat())
        shop = ET.SubElement(yml_catalog, "shop")
        offers = ET.SubElement(shop, "offers")

        # Добавление товаров в YML
        for idx in range(len(mapped_data["Артикул"])):
            offer = ET.SubElement(offers, "offer", id=str(mapped_data["Артикул"].iloc[idx]))

            # Добавление названия, если доступно
            if mapped_data["Название"] is not None:
                ET.SubElement(offer, "name").text = str(mapped_data["Название"].iloc[idx])

            # Добавление штрихкода
            ET.SubElement(offer, "barcode").text = str(mapped_data["Штрихкод"].iloc[idx])

        # Форматирование и сохранение XML
        pretty_xml = self.prettify_xml(yml_catalog)
        filename = "github_rep/output.yml"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)
     #   send_file_to_server()