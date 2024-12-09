from app import *
from quart import *
from app.database.message import Message
from app.database.user import User
import json
import asyncio
import logging

loadMsg_bp = Blueprint('loadMsg', __name__)
user = User()
message = Message()

@loadMsg_bp.websocket('/ws/loadMsg/')
async def loadMsg():
  try:
    ws = websocket
    data = json.loads(await websocket.receive())
    logging.info('someone coming: %s', data)
    session = data.get('session')
    chat_id = data.get('chat_id')
    user_id = str(session.split('@')[0])
    if not session:
      await websocket.send(json.dumps({'error': 'Session required'}))
      await websocket.close(code=1002)
      return
    elif not chat_id:
      await websocket.send(json.dumps({'error': 'Session required'}))
      return await websocket.close(code=1002)
    elif not user_id.isdigit():
      await websocket.send(json.dumps({'error': 'Invalid session'}))
      await websocket.close(code=1002)
      return
    try:
      user_id = int(user_id)
    except ValueError:
      await websocket.send(json.dumps({'error': f"The {user_id} (user_id) in session are invalid. check your session!"}))
      await websocket.close(code=1002)
      return
    user_details = await user.get_user_details(user_id)
    if not user_details or user_details.get('session') != session:
      await websocket.send(json.dumps({"error": "Invalid session or user"}))
      await websocket.close(code=1002)
      return 
    old_msg = []
    await ws.send(json.dumps({"info": "Start listening for new messages!"}))
    while True:
      messages = await message.load_chat(user_id=user_id, session=session, chat_id=chat_id)
      if old_msg != messages:
        if isinstance(messages, str):
          await websocket.send(json.dumps({'error': messages}))
        else:
          await websocket.send(json.dumps({'data': messages}))
          old_msg = messages
        logging.info("Sent a incoming msg notification!")
      await asyncio.sleep(0.3)
  except Exception as e:
    logging.error(str(e))
    await websocket.send(json.dumps({'error': str(e)}))
    await websocket.close(code=1002)
    
    