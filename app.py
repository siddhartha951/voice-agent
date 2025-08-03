from flask import Flask, jsonify, render_template, request
from retell import Retell, APIStatusError

app = Flask(__name__, template_folder="templates")

retell = Retell(api_key="key_c4c91d9723a5cdeb2c14f9b18919")

AGENTS = {
    "real_estate": "agent_47bcafb59b39c5e0a488edf4d9",
    "debits": "agent_b1329cafcfb061e2bad5e7ee6f",
    "insurance": "agent_49db8c2060bf33531273213e05",
    'healthcare': 'agent_cdd1db6ff8c3fcbbb7e624d82f',
    'school': 'agent_42244218fe2434b394823229f3',
    "ecommerce": "agent_6f60a841012f3b6caa758cced7",
    'travel':"agent_90bbd9f42b1e8991c6354f2d18",
    "fintech": "agent_c3d2c3598247fc9c9f876a842c",
    "utility": "agent_ae0cbbbc5847928a53c9fc7ca3",
    "restaurant": "agent_085d0c296fb0aa4c4623faff24",
    

}

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/start-call', methods=['POST'])
def start_call():
    try:
        # Ensure the request has JSON data
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        agent_type = data.get("agent")

        if not agent_type or agent_type not in AGENTS:
            return jsonify({"error": "Invalid or missing agent type"}), 400

        agent_id = AGENTS[agent_type]
        response = retell.call.create_web_call(agent_id=agent_id)
        return jsonify(response.to_dict())

    except APIStatusError as e:
        # Handle API status errors with proper error message extraction
        error_message = str(e)
        if hasattr(e, 'get_body_text'):
            error_message = e.get_body_text()
        
        return jsonify({
            "error": "Retell API error",
            "status_code": getattr(e, 'status_code', 500),
            "message": error_message
        }), getattr(e, 'status_code', 500)
    except Exception as e:
        return jsonify({
            "error": "Unexpected error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
