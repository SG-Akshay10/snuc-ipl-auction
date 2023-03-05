from flask import Flask, jsonify, request, render_template, redirect
import random
import csv
import json
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv("ipl_auction.csv")
df1 = df.copy()
sets = df['Set'].unique()

@app.route('/')
def index():
    return render_template('index.html',sets=sets)

displayed_players = {lot: [] for lot in sets}

@app.route('/result', methods=['POST', 'GET'])
def result():

    global displayed_players
    
    if request.method == 'POST':
        # Get the selected set from the form
        set_value = request.form['set']
        # Get the players from the selected set
        set_players = df1[df1.Set == set_value]
        num_players = len(set_players)
        
        if len(displayed_players[set_value]) == num_players:
            displayed_players[set_value] = []
            return redirect('/')
        # Choose a random player from the selected set
        while True:
            random_player = set_players.sample()
            if random_player.index[0] not in displayed_players[set_value]:
                displayed_players[set_value].append(random_player.index[0])
                break

        # Extract the player details
        player_detail = random_player.drop(columns=['LOT','Sale Price','Team'])
        player_detail = player_detail.values.tolist()[0]
        main_detail = player_detail[:6]
        batting_stats = player_detail[6:18]
        bowling_stats = player_detail[18:]
        updated_sets = df1['Set'].unique()
        s_no = random_player['S. NO'].values[0]
        pl_img = f"static/img/{s_no}.jpg"

        return render_template('result.html',pl_img=pl_img, sets=updated_sets, main_detail=main_detail, batting_stats=batting_stats, bowling_stats=bowling_stats, updated_sets=updated_sets, player=random_player, set_value=set_value, num_players=num_players)

    elif request.method == 'GET':
        # Get the selected set from the query parameter
        set_value = request.args.get('set')
        # Get the players from the selected set
        set_players = df1[df1.Set == set_value]
        num_players = len(set_players)
        if set_value not in displayed_players:
            displayed_players[set_value] = []
        # Choose a random player from the selected set
        while True:
            random_player = set_players.sample()
            if random_player.index[0] not in displayed_players[set_value]:
                displayed_players[set_value].append(random_player.index[0])
                break
        # Extract the player details
        player_detail = random_player.drop(columns=['LOT','Sale Price','Team'])
        player_detail = player_detail.values.tolist()[0]
        main_detail = player_detail[:6]
        batting_stats = player_detail[6:18]
        bowling_stats = player_detail[18:]
        s_no = random_player['S. NO'].values[0]
        pl_img = f"static/images/{s_no}.jpg"
        updated_sets = df1['Set'].unique()

        return render_template('result.html', pl_img=pl_img,sets=updated_sets, main_detail=main_detail, batting_stats=batting_stats, bowling_stats=bowling_stats, updated_sets=updated_sets, player=random_player, set_value=set_value, num_players=num_players)

    else:
        return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True)
