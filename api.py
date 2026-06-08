import requests

API_KEY  = "f18ae33b44c0b3ae14839b06390fca96"
BASE_URL = "https://api.themoviedb.org/3"

GENRES = {
    "action":           28,
    "adventure":        12,
    "animation":        16,
    "comedy":           35,
    "crime":            80,
    "drama":            18,
    "family":           10751,
    "fantasy":          14,
    "history":          36,
    "horror":           27,
    "music":            10402,
    "mystery":          9648,
    "romance":          10749,
    "science fiction":  878,
    "sci-fi":           878,
    "sci fi":           878,
    "scifi":            878,
    "thriller":         53,
    "war":              10752,
    "western":          37,
    "documentary":      99,
    "biography":        36,
}

# TV genres (TMDB uses different IDs for TV)
TV_GENRES = {
    "action":           10759,
    "adventure":        10759,
    "animation":        16,
    "comedy":           35,
    "crime":            80,
    "documentary":      99,
    "drama":            18,
    "family":           10751,
    "fantasy":          10765,
    "history":          36,
    "horror":           9648,
    "mystery":          9648,
    "romance":          10749,
    "science fiction":  10765,
    "sci-fi":           10765,
    "thriller":         53,
    "war":              10768,
    "western":          37,
}

GENRE_ID_TO_NAME = {v: k.title() for k, v in GENRES.items()}


def _request(endpoint, params=None):
    if params is None:
        params = {}
    params["api_key"] = API_KEY
    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[API ERROR] {e}")
        return {}


def get_movie_details(movie_id):
    return _request(f"movie/{movie_id}")


def search_movies(query, page=1):
    return _request("search/movie", {
        "query": query,
        "page": page,
        "include_adult": False,
    })


def search_tv(query, page=1):
    return _request("search/tv", {
        "query": query,
        "page": page,
        "include_adult": False,
    })


def search_person(name):
    data    = _request("search/person", {"query": name})
    results = data.get("results", [])
    return results[0] if results else None


def get_person_movie_credits(person_id):
    return _request(f"person/{person_id}/movie_credits")


def discover_movies(
    genre=None,
    country=None,
    year_from=None,
    year_to=None,
    min_rating=None,
    sort_by="popularity.desc",
    page=1,
    vote_count_min=50,
):
    params = {
        "page":           page,
        "sort_by":        sort_by,
        "vote_count.gte": vote_count_min,
        "include_adult":  False,
    }
    if genre:
        genre_id = GENRES.get(genre.lower().strip())
        if genre_id:
            params["with_genres"] = genre_id
    if country:
        params["with_origin_country"] = country.upper()
    if year_from:
        params["primary_release_date.gte"] = f"{year_from}-01-01"
    if year_to:
        params["primary_release_date.lte"] = f"{year_to}-12-31"
    if min_rating:
        params["vote_average.gte"] = float(min_rating)
    return _request("discover/movie", params)


def discover_tv(
    genre=None,
    country=None,
    year_from=None,
    year_to=None,
    min_rating=None,
    sort_by="popularity.desc",
    page=1,
):
    """Discover TV series with filters."""
    params = {
        "page":           page,
        "sort_by":        sort_by,
        "vote_count.gte": 30,
        "include_adult":  False,
    }
    if genre:
        genre_id = TV_GENRES.get(genre.lower().strip())
        if genre_id:
            params["with_genres"] = genre_id
    if country:
        params["with_origin_country"] = country.upper()
    if year_from:
        params["first_air_date.gte"] = f"{year_from}-01-01"
    if year_to:
        params["first_air_date.lte"] = f"{year_to}-12-31"
    if min_rating:
        params["vote_average.gte"] = float(min_rating)
    return _request("discover/tv", params)


def get_movie_poster_url(poster_path, size="w500"):
    if poster_path:
        return f"https://image.tmdb.org/t/p/{size}{poster_path}"
    return None