import pandas as pd
from flask import Flask, render_template , make_response
from flask_restful import Resource, Api
import json
from main import *


app = Flask(__name__)
api = Api(app)


class Render_page(Resource):
    def get(self):
        print('scraping data for website please wait..........')
        main()
        df = pd.read_excel('./scrape_data.xlsx')
        # print(df)
        out = df.to_json(orient='index')
        data = json.loads(out)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', data=data), 200, headers)


api.add_resource(Render_page, '/')

if __name__ == '__main__':
    app.run(debug=True)



