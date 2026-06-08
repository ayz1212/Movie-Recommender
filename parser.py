import re

GENRE_KEYWORDS = {
    # Action
    "action": "action",
    "fight": "action",
    "combat": "action",
    "martial arts": "action",
    "kung fu": "action",
    "superhero": "action",
    "blockbuster": "action",

    # Adventure
    "adventure": "adventure",
    "quest": "adventure",
    "journey": "adventure",
    "expedition": "adventure",
    "treasure": "adventure",

    # Animation / Anime
    "animation": "animation",
    "animated": "animation",
    "cartoon": "animation",
    "anime": "animation",
    "pixar": "animation",
    "disney animated": "animation",
    "studio ghibli": "animation",

    # Comedy
    "comedy": "comedy",
    "funny": "comedy",
    "humor": "comedy",
    "humour": "comedy",
    "comic": "comedy",
    "laugh": "comedy",
    "sitcom": "comedy",
    "parody": "comedy",
    "satire": "comedy",

    # Crime
    "crime": "crime",
    "criminal": "crime",
    "mafia": "crime",
    "gangster": "crime",
    "heist": "crime",
    "mob": "crime",
    "noir": "crime",
    "drug": "crime",

    # Documentary
    "documentary": "documentary",
    "docuseries": "documentary",
    "true story": "documentary",
    "real events": "documentary",

    # Drama
    "drama": "drama",
    "dramatic": "drama",
    "emotional": "drama",
    "tearjerker": "drama",
    "slice of life": "drama",

    # Family
    "family": "family",
    "kids": "family",
    "children": "family",
    "for kids": "family",
    "pixar": "family",

    # Fantasy
    "fantasy": "fantasy",
    "magical": "fantasy",
    "magic": "fantasy",
    "wizards": "fantasy",
    "dragons": "fantasy",
    "mythological": "fantasy",
    "fairy tale": "fantasy",

    # History
    "history": "history",
    "historical": "history",
    "period": "history",
    "period piece": "history",
    "medieval": "history",
    "ancient": "history",
    "world war": "history",
    "biography": "history",
    "биография": "history",

    # Horror
    "horror": "horror",
    "scary": "horror",
    "fear": "horror",
    "terrifying": "horror",
    "creepy": "horror",
    "haunted": "horror",
    "ghost": "horror",
    "slasher": "horror",
    "zombie": "horror",
    "psychological horror": "horror",

    # Music
    "music": "music",
    "musical": "music",
    "concert": "music",
    "band": "music",
    "rock": "music",

    # Mystery
    "mystery": "mystery",
    "detective": "mystery",
    "whodunit": "mystery",
    "investigation": "mystery",
    "suspense mystery": "mystery",

    # Romance
    "romance": "romance",
    "romantic": "romance",
    "love": "romance",
    "love story": "romance",
    "relationship": "romance",

    # Sci-Fi
    "sci-fi": "science fiction",
    "scifi": "science fiction",
    "sci fi": "science fiction",
    "science fiction": "science fiction",
    "space": "science fiction",
    "futuristic": "science fiction",
    "alien": "science fiction",
    "cyberpunk": "science fiction",
    "dystopia": "science fiction",
    "time travel": "science fiction",
    "robot": "science fiction",
    "ai movie": "science fiction",

    # Thriller
    "thriller": "thriller",
    "suspense": "thriller",
    "psychological thriller": "thriller",
    "espionage": "thriller",
    "spy": "thriller",
    "assassination": "thriller",
    "kidnap": "thriller",

    # War
    "war": "war",
    "military": "war",
    "battle": "war",
    "soldier": "war",
    "wwii": "war",
    "ww2": "war",
    "world war 2": "war",

    # Western
    "western": "western",
    "cowboy": "western",
    "wild west": "western",
    "outlaw": "western",
}

COUNTRY_KEYWORDS = {
    # USA
    "american": "US",
    "america": "US",
    "usa": "US",
    "us movie": "US",
    "hollywood": "US",

    # South Korea
    "korean": "KR",
    "korea": "KR",
    "south korea": "KR",
    "kdrama": "KR",
    "k-drama": "KR",
    "k drama": "KR",

    # Japan
    "japanese": "JP",
    "japan": "JP",
    "anime": "JP",
    "j-horror": "JP",
    "j-drama": "JP",

    # United Kingdom
    "british": "GB",
    "uk": "GB",
    "england": "GB",
    "english film": "GB",
    "bbc": "GB",

    # France
    "french": "FR",
    "france": "FR",

    # Germany
    "german": "DE",
    "germany": "DE",
    "deutsch": "DE",

    # Italy
    "italian": "IT",
    "italy": "IT",

    # Spain
    "spanish": "ES",
    "spain": "ES",

    # China
    "chinese": "CN",
    "china": "CN",

    # Hong Kong
    "hong kong": "HK",
    "hk film": "HK",

    # India
    "indian": "IN",
    "india": "IN",
    "bollywood": "IN",
    "hindi film": "IN",

    # Russia
    "russian": "RU",
    "russia": "RU",

    # Turkey
    "turkish": "TR",
    "turkey": "TR",
    "dizi": "TR",

    # Mexico
    "mexican": "MX",
    "mexico": "MX",

    # Brazil
    "brazilian": "BR",
    "brazil": "BR",

    # Australia
    "australian": "AU",
    "australia": "AU",

    # Thailand
    "thai": "TH",
    "thailand": "TH",

    # Sweden
    "swedish": "SE",
    "sweden": "SE",

    # Denmark
    "danish": "DK",
    "denmark": "DK",

    # Norway
    "norwegian": "NO",
    "norway": "NO",

    # Poland
    "polish": "PL",
    "poland": "PL",

    # Iran
    "iranian": "IR",
    "iran": "IR",
    "persian film": "IR",

    # Argentina
    "argentinian": "AR",
    "argentina": "AR",

    # Canada
    "canadian": "CA",
    "canada": "CA",

    # Israel
    "israeli": "IL",
    "israel": "IL",
}


DIRECTOR_PATTERNS = [
    r"directed by ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"director ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"by ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"([A-Z][a-z]+(?: [A-Z][a-z]+)+)'s (film|movie|work|style|cinema|filmography)",
    r"films? (?:of|by|from) ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
]


ACTOR_PATTERNS = [
    r"starring ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"with ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"actor ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"actress ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"featuring ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"played by ([A-Z][a-z]+(?: [A-Z][a-z]+)+)",
    r"([A-Z][a-z]+(?: [A-Z][a-z]+)+) movies?",
    r"([A-Z][a-z]+(?: [A-Z][a-z]+)+) films?",
]


KNOWN_DIRECTORS = [
    "Christopher Nolan", "Nolan",
    "Steven Spielberg", "Spielberg",
    "Martin Scorsese", "Scorsese",
    "Quentin Tarantino", "Tarantino",
    "James Cameron", "Cameron",
    "Ridley Scott",
    "David Fincher", "Fincher",
    "Denis Villeneuve", "Villeneuve",
    "Wes Anderson",
    "Bong Joon-ho", "Bong Joon ho", "Bong Joonho",
    "Park Chan-wook", "Park Chan wook",
    "Lee Chang-dong",
    "Akira Kurosawa", "Kurosawa",
    "Stanley Kubrick", "Kubrick",
    "Francis Ford Coppola", "Coppola",
    "Tim Burton",
    "Peter Jackson",
    "Guillermo del Toro",
    "Alfonso Cuaron", "Cuarón",
    "Jordan Peele",
    "Darren Aronofsky",
    "David Lynch",
    "Hayao Miyazaki", "Miyazaki",
    "Hirokazu Kore-eda",
    "Wong Kar-wai", "Wong Kar wai",
    "Zhang Yimou",
    "Andrei Tarkovsky", "Tarkovsky",
    "Ingmar Bergman", "Bergman",
    "Federico Fellini", "Fellini",
    "Pedro Almodóvar", "Almodovar",
    "Sergio Leone",
    "Luc Besson",
    "Jean-Pierre Jeunet",
    "Robert Rodriguez",
    "Zack Snyder",
    "Sofia Coppola",
    "Greta Gerwig",
    "Ryan Coogler",
    "Rian Johnson",
    "Edgar Wright",
    "Guy Ritchie",
    "Sam Mendes",
    "Ron Howard",
]



KNOWN_ACTORS = [
    "Tom Hanks", "Leonardo DiCaprio", "DiCaprio",
    "Brad Pitt", "Matt Damon", "Will Smith",
    "Denzel Washington", "Morgan Freeman",
    "Robert De Niro", "Al Pacino",
    "Meryl Streep", "Cate Blanchett",
    "Natalie Portman", "Scarlett Johansson",
    "Ryan Gosling", "Jake Gyllenhaal",
    "Christian Bale", "Tom Hardy",
    "Joaquin Phoenix",
    "Robert Downey Jr",
    "Chris Evans", "Chris Hemsworth",
    "Dwayne Johnson",
    "Keanu Reeves",
    "Johnny Depp",
    "Heath Ledger",
    "Viola Davis",
    "Anthony Hopkins",
    "Daniel Day-Lewis",
    "Charlize Theron",
    "Emma Stone", "Jennifer Lawrence",
    "Song Kang-ho",
    "Chow Yun-fat",
    "Jackie Chan",
    "Jet Li",
    "Amitabh Bachchan",
]


def normalize(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def detect_genre(text):
    text_lower = text.lower()
    for keyword in sorted(GENRE_KEYWORDS.keys(), key=len, reverse=True):
        if keyword in text_lower:
            return GENRE_KEYWORDS[keyword]
    return None


def detect_country(text):
    text_lower = text.lower()
    for keyword in sorted(COUNTRY_KEYWORDS.keys(), key=len, reverse=True):
        if keyword in text_lower:
            return COUNTRY_KEYWORDS[keyword]
    return None


def detect_year_range(text):
    year_from = None
    year_to = None

    # Exact range: "from 2010 to 2020" or "2010-2020"
    range_match = re.search(r"(?:from\s+)?(\d{4})\s*(?:to|-|–)\s*(\d{4})", text)
    if range_match:
        year_from = range_match.group(1)
        year_to = range_match.group(2)
        return year_from, year_to

    # "in the 90s", "90s", "1990s"
    decade_match = re.search(r"(?:in\s+)?(?:the\s+)?(\d{2,4})s", text, re.IGNORECASE)
    if decade_match:
        raw = decade_match.group(1)
        if len(raw) == 2:
            decade = int(raw)
            base = 1900 if decade >= 20 else 2000
            year_from = str(base + decade)
            year_to = str(base + decade + 9)
        elif len(raw) == 4:
            year_from = raw
            year_to = str(int(raw) + 9)
        return year_from, year_to

    # "around 2010"
    approx_match = re.search(r"(?:around|about|circa|near|~)\s*(\d{4})", text, re.IGNORECASE)
    if approx_match:
        year = int(approx_match.group(1))
        year_from = str(year - 2)
        year_to = str(year + 2)
        return year_from, year_to

    # "after 2010", "since 2010"
    after_match = re.search(r"(?:after|since|from)\s+(\d{4})", text, re.IGNORECASE)
    if after_match:
        year_from = after_match.group(1)
        return year_from, year_to

    # "before 2010", "until 2010"
    before_match = re.search(r"(?:before|until|up to)\s+(\d{4})", text, re.IGNORECASE)
    if before_match:
        year_to = before_match.group(1)
        return year_from, year_to

    # Single year
    single_match = re.search(r"\b((?:19|20)\d{2})\b", text)
    if single_match:
        year_from = single_match.group(1)
        year_to = single_match.group(1)
        return year_from, year_to

    return year_from, year_to


def detect_rating(text):
    patterns = [
        r"rating\s+(?:above|over|at least|minimum|min|>|>=)\s*(\d+(?:\.\d+)?)",
        r"(?:above|over|at least|minimum|min|>|>=)\s*(\d+(?:\.\d+)?)\s*(?:rating|stars?|score)?",
        r"rated\s+(?:above|over)?\s*(\d+(?:\.\d+)?)",
        r"imdb\s+(\d+(?:\.\d+)?)\+?",
        r"score\s+(?:above|over|>=)?\s*(\d+(?:\.\d+)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = float(match.group(1))
            if 0 <= val <= 10:
                return val
    return None


def detect_runtime(text):
    min_runtime = None
    max_runtime = None

    short_match = re.search(
        r"(?:shorter than|less than|under|max|maximum)\s*(\d+)\s*(?:hour|hr|h|minute|min|m)",
        text, re.IGNORECASE
    )
    if short_match:
        val = int(short_match.group(1))
        unit = short_match.group(0).lower()
        max_runtime = val * 60 if ("hour" in unit or "hr" in unit or " h" in unit) else val

    long_match = re.search(
        r"(?:longer than|more than|over|min|minimum|at least)\s*(\d+)\s*(?:hour|hr|h|minute|min|m)",
        text, re.IGNORECASE
    )
    if long_match:
        val = int(long_match.group(1))
        unit = long_match.group(0).lower()
        min_runtime = val * 60 if ("hour" in unit or "hr" in unit or " h" in unit) else val

    return min_runtime, max_runtime


def detect_people(text):
    directors = []
    actors = []

    # Check known directors
    for name in KNOWN_DIRECTORS:
        if name.lower() in text.lower():
            if name not in directors:
                directors.append(name)

    # Check known actors
    for name in KNOWN_ACTORS:
        if name.lower() in text.lower():
            if name not in actors and name not in directors:
                actors.append(name)

    # Extract via patterns
    for pattern in DIRECTOR_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            name = match if isinstance(match, str) else match[0]
            if name not in directors and name not in KNOWN_ACTORS:
                directors.append(name)

    for pattern in ACTOR_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            name = match if isinstance(match, str) else match[0]
            if name not in actors and name not in directors:
                actors.append(name)

    return directors[:2], actors[:3]


def parse_query(text):
    """
    Parse a natural language movie query into structured filters.
    Returns dict with: genre, country, year_from, year_to, min_rating,
    min_runtime, max_runtime, directors, actors, raw_query
    """
    text = normalize(text)
    year_from, year_to = detect_year_range(text)
    min_runtime, max_runtime = detect_runtime(text)
    directors, actors = detect_people(text)

    return {
        "genre":       detect_genre(text),
        "country":     detect_country(text),
        "year_from":   year_from,
        "year_to":     year_to,
        "min_rating":  detect_rating(text),
        "min_runtime": min_runtime,
        "max_runtime": max_runtime,
        "directors":   directors,
        "actors":      actors,
        "raw_query":   text,
    }