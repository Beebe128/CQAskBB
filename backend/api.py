from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import json

from backend.hd2d.run_prototype import build_render_payload

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@cross_origin()
@app.route("/cad", methods=["GET"])
def cad():
    query = request.args.get("query")

    from backend.codex import generate_cq_obj
    from backend.utils.json import NumpyEncoder
    from backend.utils.tessellate import tessellate

    id, obj = generate_cq_obj(query)
    try:
        converted_obj = tessellate([obj])
        return jsonify(
            {
                "id": id,
                "shapes": json.loads(json.dumps(converted_obj, cls=NumpyEncoder)),
            }
        )
    except Exception as e:
        print(e)
        return jsonify({"error": f"Something went wrong.{e}"})


@cross_origin()
@app.route("/download", methods=["GET"])
def download():
    id = request.args.get("id")
    file_type = request.args.get("file_type")

    from backend.utils.download import get_donwload_string

    file_path = get_donwload_string(id, file_type)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify({"error": f"Something went wrong.{e}"})


@cross_origin()
@app.route("/hd2d/prototype", methods=["GET"])
def hd2d_prototype():
    game = request.args.get("game", "alttp")
    yaw = request.args.get("yaw", default=None, type=float)
    pitch = request.args.get("pitch", default=None, type=float)
    zoom = request.args.get("zoom", default=1.0, type=float)

    try:
        payload = build_render_payload(game=game, yaw_deg=yaw, pitch_deg=pitch, zoom=zoom)
        return jsonify(payload)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as err:
        print(err)
        return jsonify({"error": f"Something went wrong.{err}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
