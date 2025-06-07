from flask import Blueprint, render_template, request
from .services import get_bi_weekly_stats, get_monthly_stats

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats/bi-weekly', methods=['GET'])
def bi_weekly_stats():
    personnel = request.args.get('personnel')
    team = request.args.get('team')
    stats = get_bi_weekly_stats(personnel, team)
    return render_template('index.html', stats=stats)

@app.route('/stats/monthly', methods=['GET'])
def monthly_stats():
    personnel = request.args.get('personnel')
    team = request.args.get('team')
    stats = get_monthly_stats(personnel, team)
    return render_template('index.html', stats=stats)