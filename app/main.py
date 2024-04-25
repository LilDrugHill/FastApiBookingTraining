from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.booking.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels

from app.pages.router import router as router_pages
from app.images.router import router as router_images


app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)

app.include_router(router_pages)
app.include_router(router_images)