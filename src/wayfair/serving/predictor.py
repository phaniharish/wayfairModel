"""
This is the file that implements a flask server to do inferences.
"""
import flask
from flask import jsonify
from wayfair.data_preprocessing.feature_extraction import FeatureExtractor
from wayfair.data_preprocessing.data_models import Orders
from wayfair.utils.config import config
from wayfair.utils.logging import logger
from wayfair.model.model import model_v1, Features, predict


# The flask app for serving predictions
app = flask.Flask(config.app_name)

features_data = FeatureExtractor().extract_features()


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy. In this container, we declare
    it healthy if we can load the module successfully."""
    return jsonify("OK")


@app.route("/invocations", methods=["POST"])
def transformation():
    """
    Method to serve inference requests.
    We serialize and deserialize requests and responses with json format
    """

    order_data = Orders(**flask.request.get_json())
    logger.debug("Data payload: %s", order_data)
    features = Features(**features_data.loc[order_data.order_id].to_dict())
    recommendations = predict(model_v1, features)

    return jsonify(
        {"order_id": order_data.order_id, "recommendation": recommendations.value}
    )
