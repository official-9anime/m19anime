from fastapi import FastAPI, Response
import requests
import uvicorn

from src.manganato import Manganato
from src.mangareader import Mangareader
from src.mangapill import Mangapill
from src.asurascans import Asurascans

app = FastAPI()

mangareader_genres = ["Action, Adventure, Comedy, Cooking, Doujinshi, Drama, Erotica, Fantasy, Gender Bender, Harem, Historical, Horror, Isekai, Josei, Manhua, Manhwa, Martial arts, Mature, Mecha, Medical, Mystery, One shot, Pornographic, Pschological, Romance, School life, Sci fi, Seinen, Shoujo, Shounen ai, Slice of life, Smut, Sports, Supernatural, Tragedy, Webtoons, Yaoi, Yuri"]

@app.get("/")
def homepage():
	return (
		{
			"message": "Welcome to the manganato scraper"
		}
	)

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
    elif category == "hotest":
        if path:
            return Manganato().hotest(page=path)
        else:
            return Manganato().hotest()
    elif category == "image":
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
        return Asurascans().search(query=path)
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
        
if __name__ == "__main__":
	uvicorn.run(app=app)