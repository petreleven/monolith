from flask import Blueprint, jsonify

DEVS = ['peter', 'samuel']
OPS = ['Bill']
_TEAMS = {1: DEVS, 2: OPS}

teams = Blueprint('teams', __name__)


@teams.route('/teams')
def get_all():
    return jsonify(_TEAMS)

@teams.route('/teams/<int:team_id>')
def get_team(team_id):
    return jsonify(_TEAMS[team_id])
