#!/usr/bin/env python3
"""Build recipes.json — an index of the BBQ creators' own recipe pages.

Reads each site's public sitemap (or recipe listing page), keeps only recipe
pages, turns the page address into a readable title and tags each recipe with
the one dish it's mainly about, so the Cookout tab can link chilli weather to
real chilli recipes. Only titles, links, creator and tags are stored — never
recipe content.

Run from the repo root:  python scripts/build_recipes.py
"""
import gzip, json, re, sys, time, urllib.request

UA = {"User-Agent": "NestonWeatherDesk-recipe-index/1.0 (+https://mattlloyddavies.github.io/neston-weather/)"}

# creator key -> (sitemap or listing URL, regex a recipe URL must match)
SOURCES = {
    "meatchurch": ("https://www.meatchurch.com/sitemap_articles_1.xml", r"/blogs/recipes/"),
    "heath":      ("https://www.heathrilesbbq.com/sitemap_articles_1.xml", r"/blogs/favorite-recipes/"),
    "pitboys":    ("https://bbqpitboys.com/sitemap_articles_1.xml", r"/blogs/recipes/"),
    "atbbq":      ("https://www.atbbq.com/sitemap_articles_1.xml https://www.atbbq.com/sitemap_articles_2.xml", r"/blogs/recipes/"),
    "htbr":       ("https://howtobbqright.com/post-sitemap.xml", r"howtobbqright\.com/\d{4}/\d{2}/\d{2}/"),
    "pnp":        ("https://pelletsandpits.com/post-sitemap.xml", r"pelletsandpits\.com/[^/]+/$"),
    "chuds":      ("https://www.chudsbbq.com/pages/recipes", r"/pages/recipe/"),
}

# One main dish per recipe: the first rule that matches wins, so "brisket-chili" is chilli,
# "brisket-tacos" is tacos and "pulled-pork-pizza" is pizza. Keys match DISHES in index.html.
RULES = [  # matched against how the recipe name ends (see dish_for)
    ("chili", r"\bchil(i|li)( con carne)?$|texas red$"),
    ("tacos", r"\btacos?$"),
    ("quesadilla", r"quesadillas?$"),
    ("crunchwrap", r"crunchwraps?$"),
    ("pattymelt", r"patty melts?$"),
    ("cheesesteak", r"cheese ?steaks?$|\bphilly\b"),
    ("friedrice", r"fried rice$"),
    ("pizza", r"pizzas?$|pizza pie$|calzones?$|pizza dough$"),
    ("flatbread", r"flatbreads?$|\bnaan$|focaccia$|garlic bread$"),
    ("breakfast", r"breakfast( sandwich(es)?| burritos?| skillet| hash| casserole| fatty)?$|pancakes?$|french toast$|hash ?browns?$|biscuits and gravy$"),
    ("burntends", r"burnt ends?$"),
    ("fajitas", r"fajitas?$"),
    ("wings", r"\bwings?$"),
    ("salmon", r"salmon( fillets?| filets?)?$"),
    ("prawns", r"(shrimp|prawns?)$"),
    ("skewers", r"(kebabs?|kabobs?|skewers?|souvlaki)$"),
    ("smash", r"(smash ?burgers?|smashburgers?|burgers?|cheeseburgers?)$"),
    ("picanha", r"picanha$"),
    ("tomahawk", r"tomahawk( steaks?| ribeyes?)?$"),
    ("asado", r"asado|(leg|shoulder|rack) of lamb$|lamb (leg|shoulder|rack)$|\blamb$"),
    ("beefribs", r"(beef|short|dino|plate) ribs?$"),
    ("ribs", r"(?<!prime )\bribs?$|spare ?ribs$|baby backs?$"),
    ("porkbutt", r"(pork butt|pulled pork|pork shoulder|boston butt|carnitas)$"),
    ("brisket", r"brisket( flat| point)?$"),
    ("chicken", r"(spatchcock|whole|beer can|smoked|roast(ed)?|rotisserie|half|grilled)\b.{0,15}chickens?( halves)?$|chicken halves$"),
    ("chops", r"pork chops?$"),
    ("reversesear", r"reverse sear|(?<!hamburg )(?<!pan )(steaks?|ribeyes?|rib eyes?)$"),
    ("firepot", r"(stew|gumbo|jambalaya|chowder|pot roast)$|dutch oven"),
    ("plancha", r"plancha"),
]
# skip pages that are a sauce/rub on its own, or not a recipe at all
SKIP = r"\b(sauce|rub|seasoning|marinade|glaze|dip)( recipe)?$|\b(giveaway|review|unboxing|contest|cook ?off|announc\w*|merch|podcast|faq)\b"
SMALL = {"a", "an", "and", "the", "on", "of", "with", "in", "for", "to", "or", "at", "by", "from"}
CAPS = {"bbq": "BBQ", "ny": "NY", "nc": "NC", "kc": "KC", "st": "St", "diy": "DIY", "xl": "XL"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(3):
        try:
            body = urllib.request.urlopen(req, timeout=30).read()
            if body[:2] == b"\x1f\x8b":
                body = gzip.decompress(body)
            return body.decode("utf-8", "ignore")
        except Exception as e:  # noqa: BLE001 — retry then give up on this source
            if attempt == 2:
                print(f"  ! {url}: {e}", file=sys.stderr)
                return ""
            time.sleep(2)


def title_from(url):
    slug = url.rstrip("/").split("/")[-1]
    slug = re.sub(r"^\d+-", "", slug)                       # Shopify numeric prefix
    slug = re.sub(r"-\d$", "", slug)                        # duplicate-page suffix: "steak-fajitas-1"
    slug = re.sub(r"-(heath-riles|bbq-pit-boys|meat-church)(-bbq)?$", "", slug)
    words = [w for w in slug.split("-") if w]
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if lw in CAPS:
            out.append(CAPS[lw])
        elif i and lw in SMALL:
            out.append(lw)
        else:
            out.append(lw[:1].upper() + lw[1:])
    return " ".join(out)


def dish_for(title):
    """Tag by what the recipe *is*: how its name ends, before "on the Traeger", "with salsa" etc.
    So "Brisket Buffalo Sliders" isn't brisket and "Chili Pepper Relish" isn't chilli."""
    t = title.lower()
    if re.search(SKIP, t):
        return None
    head = re.split(r"\b(?:on|in|with|over|using|at|for) (?:the|a|an|my|your)\b|\b(?:with|over) (?=\w)", t)[0]
    head = re.sub(r"\b(recipes?|how to (make|smoke|cook|grill)|step by step.*)\b", " ", head)
    head = re.sub(r"[\s\d]+$", "", re.sub(r"\s+", " ", head)).strip()  # "junkyard steak 2" -> "junkyard steak"
    for key, pat in RULES:
        if re.search(pat, head):
            return key
    return None


def urls_for(src, pattern):
    urls = []
    for u in src.split():
        text = fetch(u)
        if u.endswith(".xml"):
            urls += re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text)
        else:  # a listing page (Chuds): collect its recipe links
            base = re.match(r"https?://[^/]+", u).group(0)
            urls += [base + p for p in re.findall(r'href="(/pages/recipe/[^"#?]+)"', text)]
        time.sleep(1)  # be polite
    return sorted({u for u in urls if re.search(pattern, u)})


def main():
    recipes = []
    for creator, (src, pattern) in SOURCES.items():
        found = urls_for(src, pattern)
        kept = 0
        for url in found:
            title = title_from(url)
            dish = dish_for(title)
            if dish:
                recipes.append({"t": title, "u": url, "c": creator, "d": dish})
                kept += 1
        print(f"{creator:11s} {len(found):4d} pages, {kept:4d} tagged")
    recipes.sort(key=lambda r: (r["d"], r["c"], r["t"]))
    with open("recipes.json", "w", encoding="utf-8") as f:
        json.dump({"built": time.strftime("%Y-%m-%d"), "recipes": recipes}, f, ensure_ascii=False, separators=(",", ":"))
    by = {}
    for r in recipes:
        by[r["d"]] = by.get(r["d"], 0) + 1
    print(f"\n{len(recipes)} recipes ->", ", ".join(f"{k}:{v}" for k, v in sorted(by.items())))


if __name__ == "__main__":
    main()
