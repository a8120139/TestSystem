from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheetsへの書き込み処理
@app.route('/submit', methods=['POST'])
def submit():
    name = request.json['name']
    age = request.json['age']

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR_KEY.json', scope)
    gc = gspread.authorize(credentials)

    SPREADSHEET_KEY = 'YOUR_SPREADSHEET_KEY'
    sheet = gc.open_by_key(SPREADSHEET_KEY).sheet1  # シート1を開く

    # データを書き込む
    row_values = [name, age]
    sheet.append_row(row_values)

    return '', 200  # 成功を示すレスポンスコード

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
