from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def pokemon():
    name = request.form.get('name', 'pikachu').lower()
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    s = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name}")
    if r.ok and s.ok:
        p = r.json()
        sp = s.json()
        p_data = p['sprites']['front_shiny']
        p_name = p['name']
        p_height = p['height']
        p_color = sp['color']['name']
        p_gen = sp['generation']['name']
        p_shape = sp['shape']['name']
        p_legend = sp['is_legendary']
        p_rate = sp['growth_rate']['name']
        descriptions = [entry['flavor_text'].replace('\n', ' ') for entry in sp['flavor_text_entries'] if entry['language']['name'] == 'en'][1:5]
        readable_descriptions = '\n'.join(descriptions)
        return render_template('index.html', p_data=p_data, p_height=p_height, p_name=p_name, p_color=p_color, p_gen=p_gen, p_shape=p_shape, readable_descriptions=readable_descriptions, p_legend=p_legend)
    else:
        return "Could not fetch information"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)

