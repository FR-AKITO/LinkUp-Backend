import os
from app import app
from app.functions.login import login_bp
from app.functions.message import message_bp
from app.functions.eval import eval_bp
import asyncio
from quart import request, jsonify, Blueprint

# REGISTER
app.register_blueprint(login_bp)
app.register_blueprint(message_bp)
app.register_blueprint(eval_bp)

@app.route('/')
def home():
    return 'server online'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    
