from fastapi import FastAPI, APIRouter
import uvicorn


app = FastAPI(title="Python Learning API")

router = APIRouter(prefix="", tags=["Hello Controller"])


@router.get("/", summary="Say Hello", description="Returns a friendly greeting.")
def read_root():
    return {"message": "Hello World"}


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8888, reload=False)


