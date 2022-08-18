from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)

actions = pd.read_excel("actions.xlsx")
actions = actions.set_index('action_id').T.to_dict()


@app.route('/')
def hello_world():  # put application's code here
    return "Hello World!"


@app.route('/about')
def about():
    return "<p>This is the about us page.</p>"


class Posts(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('action_id', type=int, help="The action id is missing")

    def get(self, action_id=None):
        if not action_id:
            return actions
        if "," in str(action_id):
            action_ids = action_id.split(",")
            action = {}
            for id in action_ids:
                action[int(id)] = actions[int(id)]
            return action
        else:
            action = {}
            action[action_id] = actions[int(action_id)]
            return action



api.add_resource(Posts, '/api/posts', '/api/posts/<action_id>')

if __name__ == '__main__':
    app.run(debug=True)
