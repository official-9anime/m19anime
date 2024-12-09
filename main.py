from fastapi import FastAPI, Response
import requests

from src.manganato import Manganato
from src.mangareader import Mangareader
from src.mangapill import Mangapill
from src.asurascans import Asurascans
from src.flamescans import Flamescans
from src.mangaworld import Mangaworld
from src.mangapark import Mangapark
from src.scanvf import Scanvf

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

mangareader_genres = ["Action, Adventure, Comedy, Cooking, Doujinshi, Drama, Erotica, Fantasy, Gender Bender, Harem, Historical, Horror, Isekai, Josei, Manhua, Manhwa, Martial arts, Mature, Mecha, Medical, Mystery, One shot, Pornographic, Pschological, Romance, School life, Sci fi, Seinen, Shoujo, Shounen ai, Slice of life, Smut, Sports, Supernatural, Tragedy, Webtoons, Yaoi, Yuri"]

# Allow all origins (no restrictions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (any domain)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def homepage():
	return (
		{
			"message": "Welcome to the manganato scraper"
		}
	)

@app.head("/")
async def read_root_head():
    return Response(headers={"Custom-Header": "Value"})

# Manganato
@app.get("/manganato/{category}/{path:path}")
def manganato(category: str, path: str = None):
    if category == "search":
        if path:
            newQuery = path.replace(" ", "_")
            return Manganato().search(query=newQuery)
    elif category == "info":
        if path:
            return Manganato().info(id=path)
    elif category == "pages":
        if path:
            return Manganato().pages(id=path)
    elif category == "latest":
        if path:
            return Manganato().latest(page=path)
        else:
            return Manganato().latest()
    elif category == "newest":
        if path:
            return Manganato().newest(page=path)
        else:
            return Manganato().newest()
    elif category == "hottest":
        if path:
            return Manganato().hotest(page=path)
        else:
            return Manganato().hotest()
    elif category == "images":
        if path:
            headers = {
                "Referer": "https://chapmanganato.to/"
            }
            content = requests.get(url=path, headers=headers).content
            return Response(content=content, media_type="image/jpg")
    else:
        return {
            "detail": "Invalid parameter"
        }

# Mangareader
@app.get("/mangareader/{category}/{path:path}")
def mangareader(category: str, path: str):
    if category == "search":
        return Mangareader().search(query=path)
    elif category == "info":
        return Mangareader().info(id=path)
    elif category == "pages":
        return Mangareader().pages(id=path)
    elif category == "genre-list":
        return {
            "endpoint": "mangareader",
            "genres": mangareader_genres
        }
    elif category == "latest":
        return Mangareader().latest(genre=path)
    else:
        return {
            "detail": "Invalid parameter"
        }

# Mangapill
@app.get("/mangapill/{category}/{path:path}")
def mangapill(category:str, path:str):
    if category == "search":
        return Mangapill().search(query=path)
    elif category == "info":
        return Mangapill().info(id=path)
    elif category == "pages":
        return Mangapill().pages(id=path)
    elif category == "newest":
        return Mangapill().new()
    elif category == "recent":
        return Mangapill().recent()
    elif category == "images":
        if path:
            headers = {
                "Referer": "https://mangapill.com/"
            }
            content = requests.get(url=path, headers=headers).content
            return Response(content=content, media_type="image/jpg")
        else:
            return {
                "detail": "image url is required"
            }
    else:
        return {
            "detail": "Invalid parameter"
        }
    
# Asurascans
@app.get("/asurascans/{category}/{path:path}")
def asurascans(category:str, path:str):
    if category == "search":
        if path:
            newQuery = path.replace(" ", "+")
            return Asurascans().search(query=newQuery)
    elif category == "info":
        return Asurascans().info(id=path)
    elif category == "pages":
        return Asurascans().pages(id=path)
    elif category == "popular":
        return Asurascans().popular()
    elif category == "latest":
        return Asurascans().latest(page=path)
    elif category == "genres":
        return Asurascans().genres(type=path)
    elif category == "genre-list":
        return {
            "endpoint": "asurascans",
            "genres": "action, adventure, comedy, romance"
        }
    else:
        return {
            "detail": "Invalid parameter"
        }   

# Flamescans
@app.get("/flamescans/{category}/{path:path}")
def flamescans(category:str, path:str):
    if category == "search":
        return Flamescans().search(query=path)
    elif category == "info":
        return Flamescans().info(id=path)
    elif category == "pages":
        return Flamescans().pages(id=path)
    elif category == "sort":
        return Flamescans().sort(type=path)
        # accepts: title, titlereverse, update, popular, added
    else:
        return {
            "detail": "Invalid parameter"
        }   
        
@app.get("/mangaworld/{category}/{path:path}")
def mangaworld(category:str, path:str):
    if category == "search":
        return Mangaworld().search(query=path)
    elif category == "info":
        return Mangaworld().info(id=path)
    elif category == "pages":
        return Mangaworld().pages(id=path)
    elif category == "trending":
        return Mangaworld().trending()
    elif category == "popular":
        return Mangaworld().popular(page=path)
    else:
        return {
            "detail": "Invalid parameter"
        }
    
@app.get("/mangapark/{category}/{path:path}")
def mangapark(category:str, path:str):
    if category == "search":
        return Mangapark().search(query=path)
    elif category == "info":
        return Mangapark().info(id=path)
    elif category == "pages":
        return Mangapark().pages(id=path)
    elif category == "latest":
        return Mangapark().latest(page=path)
    else:
        return {
            "detail": "Invalid parameter"
        }
    
@app.get("/scanvf/{category}/{path:path}")
def scanvf(category:str, path:str):
    if category == "search":
        return Scanvf().search(query=path)
    elif category == "info":
        return Scanvf().info(id=path)
    elif category == "pages":
        return Scanvf().pages(id=path)
    else:
        return {
            "detail": "Invalid parameter"
        }
    
