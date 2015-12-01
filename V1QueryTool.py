import logging
from flask import Flask, render_template, json, request
from v1pysdk import V1Meta

VENTYX_PROD = 'https://www11.v1host.com/VentyxProd'

app = Flask(__name__)


def get_defects(user, pwd, ids):
    defects = []
    with V1Meta(instance_url=VENTYX_PROD, username=user, password=pwd) as v1:
        for defect in v1.Defect.filter(ids):
            defects.append(defect)

    return defects


def get_stories(user, pwd, ids):
    stories = []
    with V1Meta(instance_url='https://www11.v1host.com/VentyxProd', username=user, password=pwd) as v1:
        for story in v1.Story.filter(ids):
            stories.append(story)

    return stories


def query(user, pwd, ids):
    assets = []
    story_ids = [story_id for story_id in ids if story_id.find('B') == 0]
    stories = ''
    if len(story_ids) == 1:
        stories = 'Number="'+story_ids[0]+'"'
    elif len(story_ids) > 1:
        stories = 'Number="' + '"|Number="'.join(story_ids) + '"'
    if stories != '':
        assets = assets + get_stories(user, pwd, stories)

    defect_ids = [defect_id for defect_id in ids if defect_id.find('D') == 0]
    defects = ''
    if len(defect_ids) == 1:
        defects = 'Number="'+defect_ids[0]+'"'
    elif len(defect_ids) > 1:
        defects = 'Number="' + '"|Number="'.join(defect_ids) + '"'

    if defects != '':
        assets = assets + get_defects(user, pwd, defects)

    return assets


@app.route('/search', methods=['POST', 'GET'])
def search():
    _user = request.form['usr']
    _pwd = request.form['pwd']
    _assets = request.form['assets'].split(',')
    _results = query(_user, _pwd, _assets)
    return render_template('results.html', assets=_results, ids=_assets)


@app.route('/')
def hello_world():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
