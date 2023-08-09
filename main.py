import json
import logging
from fastapi import FastAPI, HTTPException
import subprocess
import uvicorn
from uvicorn.config import LOGGING_CONFIG


app = FastAPI()
config = None


@app.get("/")
async def hook_listen(token: str = None, hook: str = None, tag: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    if token != config.get('token'):
        raise HTTPException(status_code=401, detail="Invalid token")

    if not hook:
        raise HTTPException(status_code=400, detail="No hook provided")

    hook_value = config['hooks'].get(hook)
    if not hook_value:
        raise HTTPException(status_code=404, detail="Hook not found")

    # if tag:
    #     hook_value = f'{hook_value} {tag}'

    try:
        if tag:
            subprocess.call([hook_value, tag])
        else:
            subprocess.call(hook_value)
        return {'success': True}
    except OSError as e:
        raise HTTPException(status_code=400, detail=str(e))


def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    config = load_config()
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app, host=config.get('host', 'localhost'),
                port=int(config.get('port', 8000)),
                log_config=log_config)
