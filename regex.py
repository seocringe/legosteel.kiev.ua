import re
import xml.etree.ElementTree as ET
from datetime import datetime  # Импортируем модуль для работы с датой и временем


# Определяем функцию для обработки XML-дерева
def process_xml(root):
    pattern = re.compile(
        r"LS(\d+(?:\.\d+)*)\.B"
    )  # Компилируем шаблон регулярного выражения

    # Проходим по всем элементам offer внутри корня XML
    for offer in root.findall("offer"):
        # Пытаемся найти элемент vendorCode
        vendor_code_element = offer.find("vendorCode")
        if vendor_code_element is not None:  # Если элемент найден
            vendor_code = vendor_code_element.text  # Получаем его текст
            # Ищем соответствие заданному регулярному выражению в тексте
            match = pattern.search(vendor_code)
            if match:  # Если соответствие найдено
                numbers = match.group(1).replace(
                    ".", ""
                )  # Убираем точки из захваченной группы

                # Обновляем атрибут id элемента offer
                offer.set("id", f"legosteel.kiev.ua|{numbers}")

                # Если есть элемент prom_ind_id, то обновляем его текст
                prom_ind_id_element = offer.find("prom_ind_id")
                if prom_ind_id_element is not None:
                    prom_ind_id_element.text = f"legosteel.kiev.ua|{numbers}"

                # Если есть элемент url, то обновляем его текст
                url_element = offer.find("url")
                if url_element is not None:
                    # Заменяем паттерн в тексте элемента url
                    url_element.text = re.sub(
                        r"p\d+-", f"p{numbers}-", url_element.text
                    )


# Открываем файл final_updated_skprometey.yml для чтения
with open("20231123_004422_processed_skprometey.xml", "r") as file:
    xml_data = file.read()  # Читаем содержимое файла

# Преобразуем прочитанные данные в XML-дерево
root = ET.fromstring(xml_data)

# Вызываем функцию process_xml для обработки XML
process_xml(root)

# Генерируем новую строку XML из обновленного дерева
new_xml_data = ET.tostring(root, encoding="unicode")

# Выводим новые данные XML
print(new_xml_data)
# Получаем текущую дату и время в формате ГГГГММДД_ЧЧММСС
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Создаем имя файла с префиксом в виде текущей даты и времени
output_filename = f"{current_time}_processed_skprometey.xml"

# Сохраняем новые данные XML в файл с заданным именем
with open(output_filename, "w") as file:
    file.write(new_xml_data)
