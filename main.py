import json
from fastapi import FastAPI, HTTPException
import subprocess
import uvicorn


app = FastAPI()
config = None


@app.get("/")
async def hook_listen(token: str = None, hook: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    if token != config.get('token'):
        raise HTTPException(status_code=401, detail="Invalid token")

    if not hook:
        raise HTTPException(status_code=400, detail="No hook provided")

    hook_value = config['hooks'].get(hook)
    if not hook_value:
        raise HTTPException(status_code=404, detail="Hook not found")

    try:
        subprocess.call(hook_value)
        return {'success': True}
    except OSError as e:
        raise HTTPException(status_code=400, detail=str(e))


def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    config = load_config()
    uvicorn.run(app, host=config.get('host', 'localhost'),
                port=int(config.get('port', 8000)))
