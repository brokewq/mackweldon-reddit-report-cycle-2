"""Cycle 02 source data for the Mack Weldon Reddit report.

Posts and insight numbers come from the Reddit Post Insights screenshots shared in chat.
Keyword rows come from the SERP crawler output in "SERP CAPTURE FOR MACKWELDON/data"
(captured 25 Oct 2026, US, desktop). Only the curated (kept) keywords go in the report.
"""

SERP_DIR = "/Users/aniket/Downloads/SERP CAPTURE FOR MACKWELDON"

# id = Reddit thread id. cycle = which cycle the thread was posted in.
POSTS = [
    dict(id="1xemfsg", cycle=2, sub="r/malefashionadvice",
         title="What's the best men's underwear brand? Boxer briefs, briefs or boxers",
         url="https://www.reddit.com/r/malefashionadvice/comments/1xemfsg/whats_the_best_mens_underwear_brand_boxer_briefs",
         views=404_000, vlabel="404K", rank=2, us=63.6, ins="1xemfsg"),
    dict(id="1x8j55g", cycle=2, sub="r/onebag",
         title="Comfortable sweatpants for travel that still look nice?",
         url="https://www.reddit.com/r/onebag/comments/1x8j55g/comfortable_sweatpants_for_travel_that_still_look",
         views=171_000, vlabel="171K", rank=None, us=55.8, ins="1x8j55g"),
    dict(id="1x99ick", cycle=2, sub="r/AskMenAdvice",
         title="Which underwear brand should I get for my husband?",
         url="https://www.reddit.com/r/AskMenAdvice/comments/1x99ick/which_underwear_brand_should_i_get_for_my_husband",
         views=98_700, vlabel="98.7K", rank=None, us=None, ins="1x99ick"),
    dict(id="1wydrfq", cycle=2, sub="r/capsulewardrobe",
         title="Brands for basics that actually hold up?",
         url="https://www.reddit.com/r/capsulewardrobe/comments/1wydrfq/brands_for_basics_that_actually_hold_up",
         views=44_800, vlabel="44.8K", rank=None, us=69.9, ins="1wydrfq"),
    dict(id="1xclz2u", cycle=2, sub="r/malefashionadvice",
         title="Best fabric for underwear? Modal vs cotton vs synthetic",
         url="https://www.reddit.com/r/malefashionadvice/comments/1xclz2u/best_fabric_for_underwear_modal_vs_cotton_vs",
         views=39_200, vlabel="39.2K", rank=16, us=65.7, ins="1xclz2u"),
    dict(id="1wzu2s3", cycle=2, sub="r/malefashionadvice",
         title="Looking for high quality sweatpants that keep their shape",
         url="https://www.reddit.com/r/malefashionadvice/comments/1wzu2s3/looking_for_high_quality_sweatpants_that_keep",
         views=23_800, vlabel="23.8K", rank=6, us=None, ins="1wzu2s3"),
    dict(id="1wv65xd", cycle=2, sub="r/malefashionadvice",
         title="What's the best undershirt you have bought?",
         url="https://www.reddit.com/r/malefashionadvice/comments/1wv65xd/whats_the_best_undershirt_you_have_brought",
         views=9_100, vlabel="9.1K", rank=None, us=62.6, ins="1wv65xd"),
    dict(id="1wwovun", cycle=2, sub="r/malefashionadvice",
         title="What does business casual or smart casual actually mean?",
         url="https://www.reddit.com/r/malefashionadvice/comments/1wwovun/what_does_business_casual_or_smart_casual",
         views=8_200, vlabel="8.2K", rank=None, us=68.5, ins="1wwovun"),
    # Cycle 01 threads that picked up new rankings this cycle (no new insights screenshots)
    dict(id="1wlm83t", cycle=1, sub="r/malefashionadvice",
         title="Most comfortable men's underwear you've ever worn?",
         url="https://www.reddit.com/r/malefashionadvice/comments/1wlm83t/most_comfortable_mens_underwear_youve_ever_worn/",
         views=None, vlabel=None, rank=None, us=None, ins=None),
    dict(id="1wpbbpz", cycle=1, sub="r/mensfashionadvice",
         title="Best boxer briefs for men?",
         url="https://www.reddit.com/r/mensfashionadvice/comments/1wpbbpz/best_boxer_briefs_for_men/",
         views=None, vlabel=None, rank=None, us=None, ins=None),
    dict(id="1wpf06y", cycle=1, sub="r/MensUnderwearGuide",
         title="What boxer brief brand do you guys actually swear by?",
         url="https://www.reddit.com/r/MensUnderwearGuide/comments/1wpf06y/what_boxer_brief_brand_do_you_guys_actually_swear/",
         views=None, vlabel=None, rank=None, us=None, ins=None),
]

TITLE_ECHO = "Restates the post title; not how people search"
CONTRIVED = "Too long or specific to be a real search"
NEAR_DUP = "Near-duplicate of a kept keyword"
INFO = "Informational, no shopping intent"

# (thread id, keyword) -> reason for cutting. Everything not listed is kept.
CUT = {
    # r/onebag comfortable sweatpants for travel
    ("1x8j55g", "comfortable sweatpants for travel that still look nice"): TITLE_ECHO,
    ("1x8j55g", "sweatpants for travel that still look nice"): TITLE_ECHO,
    ("1x8j55g", "comfortable pants for europe trip that look nice"): CONTRIVED,
    ("1x8j55g", "one pair of sweatpants for a two week trip"): CONTRIVED,
    ("1x8j55g", "one pair of sweatpants for travel"): CONTRIVED,
    ("1x8j55g", "replacing old gym sweatpants for travel"): CONTRIVED,
    ("1x8j55g", "sweatpants for a couple weeks of travel"): CONTRIVED,
    ("1x8j55g", "sweatpants for chill days traveling"): CONTRIVED,
    ("1x8j55g", "sweatpants for flights trains and walking around"): CONTRIVED,
    ("1x8j55g", "sweatpants that work for flights and walking around"): CONTRIVED,
    ("1x8j55g", "sweatpants for walking around the city"): CONTRIVED,
    ("1x8j55g", "sweatpants that aren't baggy for travel"): CONTRIVED,
    ("1x8j55g", "sweatpants that don't fade for travel"): CONTRIVED,
    ("1x8j55g", "sweatpants that still look nice after travel"): CONTRIVED,
    ("1x8j55g", "travel sweatpants that don't take up space"): NEAR_DUP,
    ("1x8j55g", "sweatpants for travel that look decent"): "Removed on review",

    # r/malefashionadvice best men's underwear brand
    ("1xemfsg", "best men's underwear brand boxer briefs briefs or boxers"): TITLE_ECHO,
    ("1xemfsg", "what's the best men's underwear brand boxer briefs briefs or boxers"): TITLE_ECHO,
    ("1xemfsg", "whats actually good mens underwear"): CONTRIVED,
    ("1xemfsg", "which underwear brand to get for my husband"): NEAR_DUP,

    # r/mensfashionadvice best boxer briefs (cycle 1 thread)
    ("1wpbbpz", "best men's underwear brand boxer briefs briefs or boxers"): TITLE_ECHO,
    ("1wpbbpz", "what's the best men's underwear brand boxer briefs briefs or boxers"): TITLE_ECHO,
    ("1wpbbpz", "whats actually good mens underwear"): CONTRIVED,

    # r/AskMenAdvice husband
    ("1x99ick", "buying underwear for husband what brand"): CONTRIVED,
    ("1x99ick", "underwear brand for my man"): CONTRIVED,
    ("1x99ick", "mens underwear brands wives recommend"): CONTRIVED,
    ("1x99ick", "which underwear brand to get for my husband"): NEAR_DUP,

    # r/malefashionadvice fabric
    ("1xclz2u", "best fabric for underwear modal vs cotton vs synthetic"): TITLE_ECHO,
    ("1xclz2u", "underwear fabric that holds its shape"): CONTRIVED,
    ("1xclz2u", "synthetic vs cotton underwear"): NEAR_DUP,
    ("1xclz2u", "modal underwear vs cotton underwear"): NEAR_DUP,
    ("1xclz2u", "modal or cotton underwear"): NEAR_DUP,

    # r/malefashionadvice most comfortable (cycle 1 thread)
    ("1wlm83t", "what do guys wear for underwear"): INFO,
    ("1wlm83t", "what underwear do men wear"): INFO,

    # r/malefashionadvice undershirt
    ("1wv65xd", "best undershirt you ever owned"): TITLE_ECHO,
    ("1wv65xd", "best undershirt you have bought"): TITLE_ECHO,
    ("1wv65xd", "best undershirt you've bought"): TITLE_ECHO,
    ("1wv65xd", "best undershirt you've ever bought"): TITLE_ECHO,
    ("1wv65xd", "what's the best undershirt you have bought"): TITLE_ECHO,

    # r/capsulewardrobe basics
    ("1wydrfq", "brands for basics that actually hold up"): TITLE_ECHO,
    ("1wydrfq", "basics that actually hold up"): NEAR_DUP,

    # r/malefashionadvice sweatpants keep their shape
    ("1wzu2s3", "looking for high quality sweatpants that keep their shape"): TITLE_ECHO,
    ("1wzu2s3", "sweatpants that look nice enough to wear out"): NEAR_DUP,

    # r/malefashionadvice business casual
    ("1wwovun", "what does business casual or smart casual actually mean"): INFO,
    ("1wwovun", "what does business casual or smart casual mean"): INFO,
}

# Manual corrections from recaptures shared in chat. Paths are relative to the project root.
# (thread id, keyword) -> (placement, screenshot)
OVERRIDE = {
    ("1x99ick", "underwear brand for husband"): ("Organic #2", "extra/underwear-brand-for-husband.png"),
}
# Pairs to drop entirely (thread no longer ranks for the keyword in the recapture)
DROP = {
    ("1xemfsg", "underwear brand for husband"),
}

THEMES = {
    "brands": ("Underwear brands & boxer briefs", "#f96a16"),
    "gift": ("Underwear as a gift", "#c2410c"),
    "travel": ("Sweatpants & travel", "#2e7d52"),
    "fabric": ("Fabrics & materials", "#d99a1e"),
    "basics": ("Basics & undershirts", "#1c1611"),
    "style": ("Style advice", "#9a8c7c"),
}
THEME_OF = {"1xemfsg": "brands", "1wlm83t": "brands", "1wpbbpz": "brands", "1wpf06y": "brands",
            "1x99ick": "gift", "1x8j55g": "travel", "1wzu2s3": "travel", "1xclz2u": "fabric",
            "1wydrfq": "basics", "1wv65xd": "basics", "1wwovun": "style"}
NICK = {"1xemfsg": "Best underwear brand", "1x8j55g": "Travel sweatpants", "1x99ick": "Underwear for husband",
        "1wydrfq": "Basics that hold up", "1xclz2u": "Modal vs cotton", "1wzu2s3": "Sweatpants that keep shape",
        "1wv65xd": "Best undershirt", "1wwovun": "Business casual", "1wlm83t": "Most comfortable underwear",
        "1wpbbpz": "Best boxer briefs", "1wpf06y": "Boxer brief brands"}

# Branded comments this cycle, from the two brand-cycle CSVs (01 Oct to 23 Oct 2026).
# The two 25 Sep comments in the CSV were already reported in cycle 01 and are left out.
FEED = [
    ("2026-10-23", "r/malefashionadvice", "https://www.reddit.com/r/malefashionadvice/comments/1xclz2u/comment/19rje2jynwitd"),
    ("2026-10-21", "r/malefashionadvice", "https://www.reddit.com/r/malefashionadvice/comments/1x9ayx6/comment/19rffykjwben8"),
    ("2026-10-20", "r/AskPinoyMen", "https://www.reddit.com/r/AskPinoyMen/comments/1x5oyp5/comment/19re6r96j8kqt"),
    ("2026-10-20", "r/MensUnderwearGuide", "https://www.reddit.com/r/MensUnderwearGuide/comments/1x2vo4s/comment/phx0pwm"),
    ("2026-10-20", "r/MensUnderwearGuide", "https://www.reddit.com/r/MensUnderwearGuide/comments/1x93ei8/comment/phwz6xu"),
    ("2026-10-19", "r/MensUnderwearGuide", "https://www.reddit.com/r/MensUnderwearGuide/comments/1x08sqk/comment/phnsrrl"),
    ("2026-10-18", "r/AustralianMFA", "https://www.reddit.com/r/AustralianMFA/comments/1wzuakl/comment/phkje4j"),
    ("2026-10-18", "r/AskMenAdvice", "https://www.reddit.com/r/AskMenAdvice/comments/1x99ick/comment/phjo9rv"),
    ("2026-10-18", "r/AskMenAdvice", "https://www.reddit.com/r/AskMenAdvice/comments/1x99ick/comment/phjiy5m"),
    ("2026-10-18", "r/onebag", "https://www.reddit.com/r/onebag/comments/1x8j55g/comment/pherlla"),
    ("2026-10-15", "r/MensUnderwearGuide", "https://www.reddit.com/r/MensUnderwearGuide/comments/1x6t7wm/comment/pgybu56"),
    ("2026-10-15", "r/malefashionadvice", "https://www.reddit.com/r/malefashionadvice/comments/1x476ko/comment/pgxkl7m"),
    ("2026-10-07", "r/bifl", "https://www.reddit.com/r/bifl/comments/1wz660w/comment/peh8iw3"),
    ("2026-10-07", "r/malefashionadvice", "https://www.reddit.com/r/malefashionadvice/comments/1wzu2s3/comment/peewa5g"),
    ("2026-10-07", "r/malefashionuk", "https://www.reddit.com/r/malefashionuk/comments/1wwmbeu/comment/pedxpwv"),
    ("2026-10-07", "r/Lululemen", "https://www.reddit.com/r/Lululemen/comments/1wxxq6o/comment/pedc2ge"),
    ("2026-10-05", "r/capsulewardrobe", "https://www.reddit.com/r/capsulewardrobe/comments/1wydrfq/comment/pe24ag4"),
    ("2026-10-03", "r/malefashionadvice", "https://www.reddit.com/r/malefashionadvice/comments/1wwovun/comment/pdmfphk"),
    ("2026-10-03", "r/malefashionadvice", "https://www.reddit.com/r/malefashionadvice/comments/1wvdzro/comment/pdkc4bb"),
    ("2026-10-02", "r/MensUnderwearGuide", "https://www.reddit.com/r/MensUnderwearGuide/comments/1wqvuk1/comment/pdg9az7"),
    ("2026-10-02", "r/GiftIdeas", "https://www.reddit.com/r/GiftIdeas/comments/1wthdvd/comment/pdg8uqk"),
    ("2026-10-02", "r/bigmenfashionadvice", "https://www.reddit.com/r/bigmenfashionadvice/comments/1wulz2f/comment/pdg7uzl"),
    ("2026-10-02", "r/MensUnderwearGuide", "https://www.reddit.com/r/MensUnderwearGuide/comments/1wr1lvf/comment/pdg7kuk"),
    ("2026-10-01", "r/malefashionadvice", "https://www.reddit.com/r/malefashionadvice/comments/1wv65xd/comment/pd942xf"),
]

# Purchase-intent score per keyword (10 = ready-to-buy head term, 1 = loosely related).
# Keyword lists in the report are ordered by this score, highest first.
INTENT = {
    # underwear brands & boxer briefs
    "best mens underwear brand": 10, "best men's underwear brand": 10, "best men's underwear brands": 10,
    "best underwear for men": 10, "best boxer briefs": 10, "best men's boxer briefs": 10,
    "best underwear brand men": 9, "best boxer brief brands": 9, "best mens underwear brand to buy": 10,
    "best male underwear brands": 9, "best underwear mens": 9, "best mens briefs": 9,
    "best underwear": 9, "which brand boxer briefs are best": 9, "boxer briefs brands": 8,
    "male underwear brands": 7, "best underwear for guys": 8, "men best underwear": 8,
    "what is the best men's underwear": 8, "what are the best men's underwear": 8,
    "what is the best underwear": 7, "what are the best underwear": 7, "popular boxer briefs": 7,
    "popular mens underwear": 7, "best type of underwear for men": 6, "boxer briefs or briefs": 5,
    "best underwear brand for men as a gift": 8,
    # comfort (cycle 1 thread)
    "most comfortable boxer briefs": 9, "most comfortable men's underwear": 9, "most comfortable mens underwear": 9,
    "most comfortable underwear for men": 9, "comfortable underwear for men": 8, "comfiest mens underwear": 8,
    "best mens underwear reddit": 8, "best underwear for men reddit": 8, "best underwear for husband": 8,
    "most comfortable underwear for husband": 7, "comfortable mens underwear for him": 7, "what underwear to get for him": 6,
    # gifts for husband / partner
    "best underwear brand for husband": 9, "best underwear to buy for husband": 9, "good underwear brand for husband": 8,
    "underwear brand for husband": 8, "comfortable underwear brand for husband": 8, "what brand of underwear to buy for husband": 8,
    "what underwear brand should i buy my husband": 8, "which underwear brand should i get for my husband": 8,
    "good underwear brand for boyfriend gift": 8, "underwear brand for boyfriend": 7, "underwear brand for partner": 7,
    "husband underwear recommendations": 7, "underwear recommendations for husband": 7, "underwear brands husbands actually like": 7,
    "what underwear should i buy my husband": 7, "what underwear should i get my husband": 7, "what underwear to buy for my husband": 7,
    "which underwear to buy for husband": 7, "good underwear to get my husband": 7, "nice underwear for husband": 6,
    "underwear for my husband": 6, "how to pick underwear for husband": 5,
    # sweatpants & travel
    "best sweatpants for travel": 10, "best sweatpants for traveling": 10, "sweatpants for travel": 9,
    "best sweatpants for long flights": 9, "comfortable sweatpants for travel": 9, "travel joggers that look nice": 8,
    "nice looking sweatpants for travel": 8, "comfy sweatpants for travel": 8, "packable sweatpants for travel": 8,
    "lightweight sweatpants for travel": 8, "versatile sweatpants for travel": 7, "elevated sweatpants for travel": 7,
    "sweatpants to wear on a long flight": 7, "sweatpants for one bag travel": 7, "one bag travel sweatpants that look nice": 6,
    "comfortable pants for travel that still look nice": 7, "most comfortable travel pants that look nice": 7,
    "sweatpants that don't look like sweatpants for travel": 6, "sweatpants that look put together for travel": 6,
    "comfy sweatpants for long travel days": 6, "sweatpants for train travel": 6, "sweatpants that look decent in public": 5,
    "best sweatpants that keep their shape": 9, "high quality sweatpants that keep their shape": 9,
    "heavyweight sweatpants that keep their shape": 8, "sweatpants that hold up": 8, "sweatpants that look good enough to wear out": 6,
    # fabrics
    "best underwear material": 9, "best underwear fabric for comfort": 9, "most comfortable underwear fabric": 8,
    "modal vs cotton underwear": 8, "cotton vs modal underwear": 8, "is modal or cotton better for underwear": 7,
    "cotton underwear vs modal which is better": 7, "modal underwear worth it": 7, "is modal good for underwear": 6,
    "modal vs cotton vs synthetic underwear": 7, "cotton vs synthetic underwear": 6, "modal vs synthetic underwear": 6,
    "modal vs cotton undershirt": 6,
    # basics & undershirts
    "what is the best undershirt": 9, "whats the best undershirt": 9, "undershirt recommendations": 8, "undershirts better than hanes": 8,
    "basics brands worth the money": 8, "basics brands worth it": 8, "basics brands that actually hold up": 8,
    "where to get good quality basics": 7, "basics brands better than h&m": 7, "clothing basics that hold up": 6,
}
