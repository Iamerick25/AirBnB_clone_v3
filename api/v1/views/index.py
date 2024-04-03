#!/USR/bin/python3
""" TODO """
from api.v1.views import app_views
from flask import jsonify
from models import storage


# @app_views.route('/status', methods=['GET'], strict_slashes=False)
@app_views.route('/status')
def status_json_return():
    ''' Returns a JSON file with "status": "OK" '''
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_class_count():
    ''' TODO '''
    classes = [("Amenity", "amenities"), ("City", "cities"), (
            "Place", "places"), ("Review", "reviews"), ("State", "states"), (
                "User", "users")]
    stats_dict = {}
    for cl in classes:
        stats_dict[cl[1]] = storage.count(cl[0])
    return jsonify(stats_dict)
