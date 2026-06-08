from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from api import (
    discover_movies, discover_tv,
    search_movies, search_tv,
    get_movie_details,
    search_person, get_person_movie_credits,
    get_movie_poster_url,
    GENRE_ID_TO_NAME,
)
from parser import parse_query

app = Flask(__name__, static_folder=".")
CORS(app)


def ask_ollama(prompt: str) -> str:
    try:
        import ollama
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": (
                    "You are Movie Recommender Assistant — a helpful AI for discovering movies and TV series. "
                    "You help users find films, explain plots, compare titles, and give recommendations "
                    "based on mood, occasion, or preferences. "
                    "Keep answers concise (2-4 sentences). Be friendly and enthusiastic."
                )},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]
    except ImportError:
        return "⚠ Ollama not installed. Run: pip install ollama"
    except Exception as e:
        err = str(e)
        if "connection" in err.lower() or "refused" in err.lower():
            return "⚠ Ollama is not running. Start with: ollama serve"
        return f"⚠ Ollama error: {err}"


def format_movie(movie, details=None, media_type="movie"):
    poster   = get_movie_poster_url(movie.get("poster_path"))
    backdrop = get_movie_poster_url(movie.get("backdrop_path"), size="w780")
    genre_ids = movie.get("genre_ids", [])
    genres    = [GENRE_ID_TO_NAME.get(gid, "") for gid in genre_ids if gid in GENRE_ID_TO_NAME]

    is_tv = media_type == "tv"
    title = movie.get("name") or movie.get("title", "Unknown")
    orig  = movie.get("original_name") or movie.get("original_title", "")
    date  = movie.get("first_air_date") or movie.get("release_date", "")

    result = {
        "id":             movie.get("id"),
        "type":           media_type,
        "title":          title,
        "original_title": orig,
        "overview":       movie.get("overview", "No description available."),
        "rating":         round(movie.get("vote_average", 0), 1),
        "votes":          movie.get("vote_count", 0),
        "release_date":   date,
        "year":           date[:4] if date else "",
        "poster":         poster,
        "backdrop":       backdrop,
        "genres":         genres,
        "popularity":     movie.get("popularity", 0),
        "is_tv":          is_tv,
    }
    if details:
        result["runtime"]   = details.get("runtime", 0)
        result["tagline"]   = details.get("tagline", "")
        result["countries"] = [c["iso_3166_1"] for c in details.get("production_countries", [])]
        result["budget"]    = details.get("budget", 0)
        result["revenue"]   = details.get("revenue", 0)
    return result


def collect_movies_by_person(person_name, role="actor"):
    person = search_person(person_name)
    if not person:
        return [], None
    credits = get_person_movie_credits(person["id"])
    info = {"name": person.get("name"), "id": person.get("id"), "role": role}
    if role == "director":
        movies = [m for m in credits.get("crew", []) if m.get("job") == "Director"]
    else:
        movies = credits.get("cast", [])
    return movies, info


def apply_filters(movies, filters, media_type="movie"):
    from api import GENRES, TV_GENRES
    result = []

    genre_ids_target = set()
    genres_list = filters.get("genres") or ([filters["genre"]] if filters.get("genre") else [])
    genre_map = TV_GENRES if media_type == "tv" else GENRES
    for g in genres_list:
        gid = genre_map.get(g.lower().strip())
        if gid:
            genre_ids_target.add(gid)

    countries_target = set()
    countries_list = filters.get("countries") or ([filters["country"].upper()] if filters.get("country") else [])
    for c in countries_list:
        countries_target.add(c.upper())

    for movie in movies:
        rating   = movie.get("vote_average", 0)
        date_str = movie.get("first_air_date") or movie.get("release_date", "")
        year_str = date_str[:4]
        year     = int(year_str) if year_str.isdigit() else 0

        if filters.get("min_rating") and rating < filters["min_rating"]:
            continue
        if filters.get("max_rating") and rating > filters["max_rating"]:
            continue
        if filters.get("year_from") and year and year < int(filters["year_from"]):
            continue
        if filters.get("year_to") and year and year > int(filters["year_to"]):
            continue

        if countries_target and media_type == "tv":
            oc = movie.get("origin_country", [])
            if not oc or not countries_target.intersection(set(oc)):
                continue

        if genre_ids_target:
            gids = set(movie.get("genre_ids", []))
            if not genre_ids_target.intersection(gids):
                continue

        result.append(movie)
    return result


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/agent", methods=["POST"])
def agent():
    data  = request.get_json() or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"answer": "Please ask me something!"})
    return jsonify({"answer": ask_ollama(query)})


@app.route("/api/search", methods=["POST"])
def search():
    body  = request.get_json() or {}
    query = body.get("query", "").strip()
    limit = int(body.get("limit", 24))

    explicit_countries  = body.get("countries") or ([body["country"]] if body.get("country") else [])
    explicit_genres     = body.get("genres")    or ([body["genre"]]   if body.get("genre")   else [])
    explicit_min_rating = body.get("min_rating")
    explicit_max_rating = body.get("max_rating")
    explicit_year_from  = body.get("year_from")
    explicit_year_to    = body.get("year_to")
    is_title_search     = body.get("title_search", False)
    media_type          = body.get("media_type", "movie")

    if is_title_search and query:
        movies_raw = []
        if media_type in ("movie", "both"):
            for page in range(1, 4):
                movies_raw.extend(search_movies(query, page).get("results", []))
        if media_type in ("tv", "both"):
            for page in range(1, 4):
                movies_raw.extend(search_tv(query, page).get("results", []))

        manual_filters = {}
        if explicit_countries:  manual_filters["countries"]  = explicit_countries
        if explicit_genres:     manual_filters["genres"]     = explicit_genres
        if explicit_min_rating: manual_filters["min_rating"] = float(explicit_min_rating)
        if explicit_max_rating: manual_filters["max_rating"] = float(explicit_max_rating)
        if explicit_year_from:  manual_filters["year_from"]  = explicit_year_from
        if explicit_year_to:    manual_filters["year_to"]    = explicit_year_to

        filtered = apply_filters(movies_raw, manual_filters, media_type) if manual_filters else movies_raw
        seen, unique = set(), []
        for m in filtered:
            mid = m.get("id")
            if mid not in seen:
                seen.add(mid); unique.append(m)
        results = []
        for m in unique[:limit]:
            mt = "tv" if m.get("name") else "movie"
            results.append(format_movie(m, media_type=mt))
        return jsonify({"results": results, "filters": manual_filters, "person": None, "total": len(results)})

    if not query and (explicit_genres or explicit_countries or explicit_min_rating or explicit_year_from or body.get("sort_by")):
        movies_raw = []
        genre_to_use   = explicit_genres[0]    if explicit_genres    else None
        country_to_use = explicit_countries[0] if explicit_countries else None
        sort_by        = body.get("sort_by", "popularity.desc")
        vote_count_min = int(body.get("vote_count_min", 30))

        if media_type == "tv":
            for page in range(1, 6):
                movies_raw.extend(discover_tv(
                    genre=genre_to_use, country=country_to_use,
                    year_from=explicit_year_from, year_to=explicit_year_to,
                    min_rating=float(explicit_min_rating) if explicit_min_rating else None,
                    sort_by=sort_by, page=page,
                ).get("results", []))
        elif media_type == "both":
            for page in range(1, 4):
                movies_raw.extend(discover_movies(
                    genre=genre_to_use, country=country_to_use,
                    year_from=explicit_year_from, year_to=explicit_year_to,
                    min_rating=float(explicit_min_rating) if explicit_min_rating else None,
                    sort_by=sort_by, page=page, vote_count_min=vote_count_min,
                ).get("results", []))
                movies_raw.extend(discover_tv(
                    genre=genre_to_use, country=country_to_use,
                    year_from=explicit_year_from, year_to=explicit_year_to,
                    min_rating=float(explicit_min_rating) if explicit_min_rating else None,
                    sort_by=sort_by, page=page,
                ).get("results", []))
        else:
            for page in range(1, 6):
                movies_raw.extend(discover_movies(
                    genre=genre_to_use, country=country_to_use,
                    year_from=explicit_year_from, year_to=explicit_year_to,
                    min_rating=float(explicit_min_rating) if explicit_min_rating else None,
                    sort_by=sort_by, page=page, vote_count_min=vote_count_min,
                ).get("results", []))

        manual_filters = {}
        if explicit_countries:  manual_filters["countries"]  = explicit_countries
        if explicit_genres:     manual_filters["genres"]     = explicit_genres
        if explicit_min_rating: manual_filters["min_rating"] = float(explicit_min_rating)
        if explicit_max_rating: manual_filters["max_rating"] = float(explicit_max_rating)
        if explicit_year_from:  manual_filters["year_from"]  = explicit_year_from
        if explicit_year_to:    manual_filters["year_to"]    = explicit_year_to

        filtered = apply_filters(movies_raw, manual_filters, media_type)
        seen, unique = set(), []
        for m in filtered:
            mid = m.get("id")
            if mid not in seen:
                seen.add(mid); unique.append(m)
        results = [format_movie(m, media_type=media_type) for m in unique[:limit]]
        return jsonify({"results": results, "filters": manual_filters, "person": None, "total": len(results)})

    filters = parse_query(query) if query else {}
    if explicit_countries:          filters["countries"]  = explicit_countries
    if explicit_genres:             filters["genres"]     = explicit_genres
    if explicit_min_rating is not None: filters["min_rating"] = float(explicit_min_rating)
    if explicit_max_rating is not None: filters["max_rating"] = float(explicit_max_rating)
    if explicit_year_from  is not None: filters["year_from"]  = explicit_year_from
    if explicit_year_to    is not None: filters["year_to"]    = explicit_year_to

    movies_raw = []; person_info = None

    if filters.get("directors"):
        movies_raw, person_info = collect_movies_by_person(filters["directors"][0], "director")
    elif filters.get("actors"):
        movies_raw, person_info = collect_movies_by_person(filters["actors"][0], "actor")
    elif any(filters.get(k) for k in ("genres", "genre", "countries", "country", "year_from", "year_to", "min_rating")):
        g = (filters.get("genres") or [filters.get("genre")])[0] if (filters.get("genres") or filters.get("genre")) else None
        c = (filters.get("countries") or [filters.get("country")])[0] if (filters.get("countries") or filters.get("country")) else None
        for page in range(1, 5):
            movies_raw.extend(discover_movies(
                genre=g, country=c,
                year_from=filters.get("year_from"), year_to=filters.get("year_to"),
                min_rating=filters.get("min_rating"),
                sort_by="vote_average.desc" if filters.get("min_rating") else "popularity.desc",
                page=page,
            ).get("results", []))
    else:
        for page in range(1, 3):
            movies_raw.extend(search_movies(query, page).get("results", []))

    filtered = apply_filters(movies_raw, filters, "movie")
    seen, unique = set(), []
    for m in filtered:
        mid = m.get("id")
        if mid not in seen:
            seen.add(mid); unique.append(m)
    unique = unique[:limit]

    results = []
    for m in unique:
        details = None
        if filters.get("min_runtime") or filters.get("max_runtime"):
            details = get_movie_details(m["id"])
            if details:
                rt = details.get("runtime", 0)
                if filters.get("min_runtime") and rt < filters["min_runtime"]:
                    continue
                if filters.get("max_runtime") and rt > filters["max_runtime"]:
                    continue
        results.append(format_movie(m, details))

    return jsonify({"results": results, "filters": filters, "person": person_info, "total": len(results)})


@app.route("/api/movie/<int:movie_id>")
def movie_detail(movie_id):
    details = get_movie_details(movie_id)
    if not details:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(format_movie(details, details))


if __name__ == "__main__":
    print("🎬  Movie Recommender running at http://localhost:5000")
    app.run(debug=True, port=5000)