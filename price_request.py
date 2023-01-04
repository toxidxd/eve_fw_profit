import csv
import json
import requests
from fake_useragent import UserAgent


def data_reader(csv_file):
    csv_data = []
    with open(csv_file) as csv_f:
        reader = csv.reader(csv_f, delimiter=';')
        for i_line in reader:
            csv_data.append(i_line)

    return csv_data  # возвращает список списков из cvs файла


def price_parser(data, hub):
    jdata = requests.post("https://evepraisal.com/appraisal/structured.json",
                          data=json.dumps(data_to_request(data, hub)),
                          headers={'User-Agent': UserAgent().chrome}).text

    data = json.loads(jdata)
    all_prices = dict()

    for material in data["appraisal"]["items"]:
        all_prices[material["name"]] = {'sell': str(material["prices"]["sell"]["min"]),
                                        'buy': str(material["prices"]["buy"]["max"])}
    return all_prices


def data_to_request(data, hub):
    return {"market_name": hub,
            "items": [{'name': i_item} for i_item in data[0][5:]] +
                     [{'name': i_item[0]} for i_item in data[1:]]}


def profit_calc(items_data):
    result = []
    order_type = ['sell', 'buy']
    trade_hub = ['amarr', 'jita', 'dodixie', 'hek']
    for i_hub in trade_hub:
        prices = price_parser(items_data, i_hub)
        for i_type in order_type:
            for i_item in items_data[1:]:
                expenses = int(i_item[2]) + int(i_item[3]) + int(i_item[4])
                materials_cost = 0
                for i, i_material in enumerate(items_data[0][5:]):
                    material_price = int(i_item[5+i]) * float(prices[i_material][i_type])
                    materials_cost += material_price

                ship_price = int(prices[i_item[0]]['sell'])
                profit = ship_price - expenses - materials_cost

                k = round(profit/int(i_item[1])/1000, 2)

                i_result = [i_item[0], i_hub, i_type, i_item[1], expenses, materials_cost, ship_price, profit, k]

                result.append(replace_dots(i_result))

    results_to_file(result)


def results_to_file(results):

    with open(f"result.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(
            ['ship_type', 'hub', 'order_type', 'lp', 'expenses', 'materials_cost', 'ship_price_sell', 'profit', 'k']
        )
        for line in results:
            writer.writerow(line)

    print('Results writed!')


def replace_dots(some_list):
    return [str(i_row).replace('.', ',') for i_row in some_list]


profit_calc(data_reader("data.csv"))
