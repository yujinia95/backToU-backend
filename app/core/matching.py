import re

CATEGORY_MAX_POINTS = 30
LOCATION_MAX_POINTS = 20
COLOR_MAX_POINTS = 20
DATE_MAX_DAYS = 14
DATE_MAX_POINTS = 15
BRAND_MAX_POINTS = 10
KEYWORD_MAX_POINTS = 5
TITLE_WEIGHT = 0.7  # 나머지 0.3은 description


def overlap_ratio(textA: str, textB: str) -> float:
    wordsA = set(preprocessor(textA))
    wordsB = set(preprocessor(textB))
    if not wordsA or not wordsB:
        return 0
    return len(wordsA & wordsB) / min(len(wordsA), len(wordsB))

def preprocessor(string) -> list[str]:
    return re.findall(r"[a-z0-9]+", string.lower())
    
class MatchScore:
    def score_total(self, item, candidate):
        rules = [
            ("category", self.score_category),
            ("color", self.score_colors),
            ("location", self.score_location),
            ("date", self.score_date),
            ("brand", self.score_brand),
            (None, self.score_keywords),
        ]

        total = 0
        reasons = []
        for code, rule in rules:
            points = rule(item, candidate)
            total += points
            if points > 0 and code is not None:
                reasons.append(code)

        return round(total), reasons
    
    def score_category(self, item, candidate) -> float:
        if item["category"].lower() == candidate["category"].lower():
            return CATEGORY_MAX_POINTS
        return 0
    
    def score_colors(self, item, candidate) -> float:
        colorsA = set([c.lower() for c in item["colors"]])
        colorsB = set([c.lower() for c in candidate["colors"]])
        common = colorsA & colorsB
        numbers = colorsA | colorsB
        
        if len(numbers) == 0: return 0
        return (len(common) / len(numbers)) * COLOR_MAX_POINTS  
        
    def score_location(self, item, candidate) -> float:
        return overlap_ratio(item["location"], candidate["location"]) * LOCATION_MAX_POINTS
        
    def score_date(self, item, candidate) -> float:
        difference = abs((item["date"] - candidate["date"]).days)
        return max(0, 1 - difference / DATE_MAX_DAYS) * DATE_MAX_POINTS
        
    def score_brand(self, item, candidate) -> float:
        if (item["brand"] is None or candidate["brand"] is None): return 0
        if (item["brand"].lower() == candidate["brand"].lower()): return BRAND_MAX_POINTS
        return 0
        
    def score_keywords(self, item, candidate) -> float:
        title_ratio = overlap_ratio(item["title"], candidate["title"])

        desc_ratio = 0
        if item["description"] and candidate["description"]:
            desc_ratio = overlap_ratio(item["description"], candidate["description"])

        ratio = TITLE_WEIGHT * title_ratio + (1 - TITLE_WEIGHT) * desc_ratio
        return ratio * KEYWORD_MAX_POINTS
        
        
