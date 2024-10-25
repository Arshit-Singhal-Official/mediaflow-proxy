import logging
from importlib import resources
import uuid

from fastapi import FastAPI, Depends, Security, HTTPException, BackgroundTasks
from fastapi.security import APIKeyQuery, APIKeyHeader
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from mediaflow_proxy.configs import settings
from mediaflow_proxy.routes import proxy_router
from mediaflow_proxy.schemas import GenerateUrlRequest
from mediaflow_proxy.utils.crypto_utils import EncryptionHandler, EncryptionMiddleware
from mediaflow_proxy.utils.rd_speedtest import run_speedtest, prune_task, results
from mediaflow_proxy.utils.http_utils import encode_mediaflow_proxy_url

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
app = FastAPI()
api_password_query = APIKeyQuery(name="api_password", auto_error=False)
api_password_header = APIKeyHeader(name="api_password", auto_error=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(EncryptionMiddleware)


async def verify_api_key(api_key: str = Security(api_password_query), api_key_alt: str = Security(api_password_header)):
    """
    Verifies the API key for the request.

    Args:
        api_key (str): The API key to validate.
        api_key_alt (str): The alternative API key to validate.

    Raises:
        HTTPException: If the API key is invalid.
    """
    if api_key == settings.api_password or api_key_alt == settings.api_password:
        return

    raise HTTPException(status_code=403, detail="Could not validate credentials")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/speedtest")
async def trigger_speedtest(background_tasks: BackgroundTasks, api_password: str = Depends(verify_api_key)):
    # Generate a random UUID as task_id
    task_id = str(uuid.uuid4())  # Generate unique task ID
    background_tasks.add_task(run_speedtest, task_id)
    
    # Schedule the task to be pruned after 1 hour
    background_tasks.add_task(prune_task, task_id)

    return RedirectResponse(url=f"/speedtest_progress.html?task_id={task_id}")


@app.get("/speedtest/results/{task_id}", response_class=JSONResponse)
async def get_speedtest_result(task_id: str):
    if task_id in results:
        return results[task_id]
    else:
        return {"message": "Speedtest is still running, please wait or the task may have expired."}


@app.get("/favicon.ico")
async def get_favicon():
    return RedirectResponse(url="/logo.png")


@app.post("/generate_encrypted_or_encoded_url")
async def generate_encrypted_or_encoded_url(request: GenerateUrlRequest):
    if "api_password" not in request.query_params:
        request.query_params["api_password"] = request.api_password

    encoded_url = encode_mediaflow_proxy_url(
        request.mediaflow_proxy_url,
        request.endpoint,
        request.destination_url,
        request.query_params,
        request.request_headers,
        request.response_headers,
        EncryptionHandler(request.api_password) if request.api_password else None,
        request.expiration,
        str(request.ip) if request.ip else None,
    )
    return {"encoded_url": encoded_url}


app.include_router(proxy_router, prefix="/proxy", tags=["proxy"], dependencies=[Depends(verify_api_key)])

static_path = resources.files("mediaflow_proxy").joinpath("static")
app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")


def run():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info", workers=3)


if __name__ == "__main__":
    run()