from flask import Flask, render_template, request
import pandas as pd


# Признаки
# В реальном проекте я бы заморочилась и подобрала информативные имена
features = {
    'var1': 'Соотношение матрица-наполнитель',
    'var2': 'Плотность, кг/м3',
    'var3': 'Модуль упругости, ГПа',
    'var4': 'Количество отвердителя, м.%',
    'var5': 'Содержание эпоксидных групп,%_2',
    'var6': 'Температура вспышки, С_2',
    'var7': 'Поверхностная плотность, г/м2',
    'var8': 'Модуль упругости при растяжении, ГПа',
    'var9': 'Прочность при растяжении, МПа',
    'var10': 'Потребление смолы, г/м2',
    'var11': 'Угол нашивки, град',
    'var12': 'Шаг нашивки',
    'var13': 'Плотность нашивки'
}


# Функция для извлечения признаков из данных формы
def get_data_from_form(params):
    error = ''
    data = {}
    # Преобразование из строк в числа
    for param_name in features.keys():
        pvalue = params.get(param_name)
        if pvalue is not None and pvalue.strip(' \t') != '':
            try:
                data[param_name] = float(pvalue)
            except:
                error += f'{features[param_name]} - некорректное значение "{pvalue}"\n'
        else:
            error += f'{features[param_name]} - значение отсутствует\n'
    # Проверка допустимых диапазонов
    # Соотношение матрица-наполнитель (0..6)
    if data.get('var1') and (data['var1'] < 0 or data['var1'] > 6):
        error += f'{features["var1"]} - значение вне корректного диапазона\n'
    # Плотность, кг/м3 (1700...2300)
    if data.get('var2') and (data['var2'] < 1700 or data['var2'] > 2300):
        error += f'{features["var2"]} - значение вне корректного диапазона\n'
    # Модуль упругости, ГПа (2...2000)
    if data.get('var3') and (data['var3'] < 2 or data['var3'] > 2000):
        error += f'{features["var3"]} - значение вне корректного диапазона\n'
    # 'Количество отвердителя, м.% (17...200)
    if data.get('var4') and (data['var4'] < 17 or data['var4'] > 200):
        error += f'{features["var4"]} - значение вне корректного диапазона\n'
    # Содержание эпоксидных групп,%_2 (14...34)
    if data.get('var5') and (data['var5'] < 14 or data['var5'] > 34):
        error += f'{features["var5"]} - значение вне корректного диапазона\n'
    # Температура вспышки, С_2 (100...414)
    if data.get('var6') and (data['var6'] < 100 or data['var6'] > 414):
        error += f'{features["var6"]} - значение вне корректного диапазона\n'
    # Поверхностная плотность, г/м2 (0.6...1400)
    if data.get('var7') and (data['var7'] < 0.6 or data['var7'] > 1400):
        error += f'{features["var7"]} - значение вне корректного диапазона\n'
    # Модуль упругости при растяжении, ГПа (64...83)
    if data.get('var8') and (data['var8'] < 64 or data['var8'] > 83):
        error += f'{features["var8"]} - значение вне корректного диапазона\n'
    # Прочность при растяжении, МПа (1036...3849)
    if data.get('var9') and (data['var9'] < 1036 or data['var9'] > 3849):
        error += f'{features["var9"]} - значение вне корректного диапазона\n'
    # Потребление смолы, г/м2 (33...414)
    if data.get('var10') and (data['var10'] < 33 or data['var10'] > 414):
        error += f'{features["var10"]} - значение вне корректного диапазона\n'
    # Угол нашивки, град(0 или 90)
    if data.get('var11') and (data['var11'] != 0.0 and data['var11'] != 90.0):
        error += f'{features["var11"]} - значение вне корректного диапазона\n'
    # Шаг нашивки(0...15)
    if data.get('var12') and (data['var12'] < 0 or data['var12'] > 15):
        error += f'{features["var12"]} - значение вне корректного диапазона\n'
    # Плотность нашивки (0...104)
    if data.get('var13') and (data['var13'] < 0 or data['var13'] > 104):
        error += f'{features["var13"]} - значение вне корректного диапазона\n'
    return data, error


app = Flask(__name__)


@app.route('/features', methods=['post', 'get'])
def features_page():
    # params = dict.fromkeys(features.keys(), '')
    params = {'var1': '3', 'var2': '2000', 'var3': '1999', 'var4': '95', 'var5': '25', 'var6': '255', 'var7': '720',
              'var8': '70', 'var9': '2300', 'var10': '180', 'var11': '0', 'var12': '8', 'var13': '52'}
    error = ''
    result = ''
    if request.method == 'POST':
        params = request.form.to_dict()
        data, error = get_data_from_form(params)
        if error == '':
            x = pd.DataFrame(data, index=[0])
            x.columns = list(features.values())
            result = str(x.to_html())
    return render_template('features.html', params=params, error=error, result=result)


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/url_map/')
def url_map():
    return str(app.url_map)


app.run()
