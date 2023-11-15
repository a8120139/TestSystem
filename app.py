from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheetsへの書き込み処理
@app.route('/submit', methods=['POST'])
def submit():
    name = request.json['name']
    age = request.json['age']

    # Google Sheetsへのアクセス
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("C:\Users\ibkts\マイドライブ\ゼミ\卒研\google api system\my-project-test-405202-fe81b9896c8f.json", scope)
    gc = gspread.authorize(credentials)

    SPREADSHEET_KEY = 'https://docs.google.com/spreadsheets/d/11UkXbnWDS1LaQ-7H2g4xI_K_FtOAxlAZDnV85kww77Q/edit?usp=sharing'
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
