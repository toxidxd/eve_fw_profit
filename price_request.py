import csv
import json
import requests
from fake_useragent import UserAgent


def data_reader(csv_file):
    csv_data = []
    with open(csv_file) as csv_f:
        reader = csv.reader(csv_f, delimiter=',')
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


def profit_calc(items_data, prices):
    result = []
    for i_item in items_data[1:]:
        expenses_sell = int(i_item[2])  # сразу добавляем стоимость покупки чертежа
        expenses_buy = int(i_item[2])  # сразу добавляем стоимость покупки чертежа

        for i, i_material in enumerate(items_data[0][5:]):
            material_price_sell = int(i_item[5+i]) * float(prices[i_material]['sell'])
            expenses_sell += material_price_sell

            material_price_buy = int(i_item[5+i]) * float(prices[i_material]['buy'])
            expenses_buy += material_price_buy

        i_profit_sell = int(prices[i_item[0]]['sell']) - expenses_sell
        i_profit_buy = int(prices[i_item[0]]['sell']) - expenses_buy

        k_sell = round(i_profit_sell/int(i_item[1])/1000, 2)
        k_buy = round(i_profit_buy/int(i_item[1])/1000, 2)

        result.append([i_item[0], i_item[1], expenses_sell, expenses_buy, i_profit_sell, i_profit_buy, k_sell, k_buy])

    return result


def results_to_file(results, hub):
    with open(f"result_{hub}.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(
            ['item', 'lp', 'expenses_sell', 'expenses_buy', 'i_profit_sell', 'i_profit_buy', 'k_sell', 'k_buy']
        )
        for line in results:
            writer.writerow(line)

    print('File writed!')


production_data = data_reader("data.csv")
trade_hub = 'jita'
price_data = price_parser(production_data, trade_hub)
profit_dict = profit_calc(production_data, price_data)
results_to_file(profit_dict, trade_hub)
