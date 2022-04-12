# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import requests
import lxml
import json
import csv

# url = "https://health-diet.ru/table_calorie"
#
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.75 Safari/537.36 '
}
#
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open("index.html", "w") as file:
#     file.write(src)

# with open("index.html") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
#
# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
#
# all_categories_dict = {}
#
# for i in all_products_hrefs:
#     item_text = i.text
#     item_href = 'https://health-diet.ru' + i['href']
#     all_categories_dict[item_text] = item_href


# with open('all_categories_dict.json', 'w') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open('all_categories_dict.json') as file:
    all_categories = json.load(file)

iteration_count = len(all_categories) - 1
count = 0
print(f'Всего итераций: {iteration_count}')

for category_name, category_hrefs in all_categories.items():

    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')

    req = requests.get(category_hrefs, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", 'w', encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    table_head = soup.find(class_='mzr-tc-group-table').find("tr").find_all("th")

    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbs = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbs
            )
        )

    product_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_info = []

    for item in product_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbs = product_tds[4].text

        product_info.append(
            {
                "Title": title,
                'Calories': calories,
                'Proteins': proteins,
                'Fats': fats,
                'Carbs': carbs
            }
        )

        with open(f"data/{count}_{category_name}.csv", 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbs
                )
            )

    with open(f"data/{count}_{category_name}.json", "a", encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'Итерация {count}. {category_name} записан...')
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print('Работа закончена')
        break

    print(f'Осталось итераций: {iteration_count}')
