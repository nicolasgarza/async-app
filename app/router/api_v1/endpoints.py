from fastapi import APIRouter

from app.heroes.api import router as blog_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (blog_router, "blog", "Blog API"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")