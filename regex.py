import re
import xml.etree.ElementTree as ET

def process_xml(root):
    pattern = re.compile(r'LS(\d+(?:\.\d+)*)\.B')

    # Обходим все элементы offer в XML
    for offer in root.findall('offer'):
        # Ищем элемент vendorCode (если он есть)
        vendor_code_element = offer.find('vendorCode')
        if vendor_code_element is not None:
            vendor_code = vendor_code_element.text
            # Применяем регулярное выражение к vendorCode
            match = pattern.search(vendor_code)
            if match:
                numbers = match.group(1).replace('.', '')

                # Обновляем id
                offer.set('id', f"legosteel.kiev.ua|{numbers}")

                # Если есть элемент prom_ind_id, обновляем его
                prom_ind_id_element = offer.find('prom_ind_id')
                if prom_ind_id_element is not None:
                    prom_ind_id_element.text = f"legosteel.kiev.ua|{numbers}"

                # Если есть элемент url, обновляем его
                url_element = offer.find('url')
                if url_element is not None:
                    url_element.text = re.sub(r'p\d+-', f'p{numbers}-', url_element.text)

# Пример использования функции process_xml
# Загружаем ваш XML-код в переменную (замените это содержимым вашего файла)
xml_data = '''<offers>
    <!-- Ваш XML код -->
</offers>'''

# Преобразовываем строку в XML
root = ET.fromstring(xml_data)

# Вызываем функцию для обработки XML
process_xml(root)

# Генерируем новый XML из обновленного дерева
new_xml_data = ET.tostring(root, encoding='unicode')

print(new_xml_data)
