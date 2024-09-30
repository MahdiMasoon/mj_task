from pathlib import Path

import scrapy

valid_chars = [
    " ", "ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق",
    "ل", "م", "ن", "ه", "و", "پ", "چ", "ژ", "ک", "گ", "ی", ]

char_mappings = {
        "٥": "5",
        "А": "a",
        "В": "b",
        "Е": "e",
        "Н": "h",
        "Р": "P",
        "С": "C",
        "Т": "T",
        "а": "a",
        "г": "r",
        "е": "e",
        "к": "k",
        "м": "m",
        "о": "o",
        "р": "p",
        "ڈ": "د",
        "ڇ": "چ",
        # Persian numbers (will be raplaced by english one)
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        ".": ".",
        # Arabic numbers (will be raplaced by english one)
        "٠": "0",
        "١": "1",
        "٢": "2",
        "٣": "3",
        "٤": "4",
        "٥": "5",
        "٦": "6",
        "٧": "7",
        "٨": "8",
        "٩": "9",
        # Special Arabic Characters (will be replaced by persian one)
        "ك": "ک",
        "ى": "ی",
        "ي": "ی",
        "ؤ": "و",
        "ئ": "ی",
        "إ": "ا",
        "أ": "ا",
        "آ": "ا",
        "ة": "ه",
        "ء": "ی",
        # French alphabet (will be raplaced by english one)
        "à": "a",
        "ä": "a",
        "ç": "c",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "î": "i",
        "ï": "i",
        "ô": "o",
        "ù": "u",
        "û": "u",
        "ü": "u",
        # zero-width unicode
        "\u200c": "",
        "\u200b": "",
        "\ufe0f": "",
        "\ufeff": "",
        "\n": "",
        # Camma (will be replaced by dots for floating point numbers)
        ",": ".",
        # And (will be replaced by dots for floating point numbers)
        "&": " and ",
        # Vowels (will be removed)
        "ّ": "",  # tashdid
        "َ": "",  # a
        "ِ": "",  # e
        "ُ": "",  # o
        "ـ": "",  # tatvil
        # Spaces
        "‍": "",  # 0x9E -> ZERO WIDTH JOINER
        "‌": " ",  # 0x9D -> ZERO WIDTH NON-JOINER
        # Arabic Presentation Forms-A (will be replaced by persian one)
        "ﭐ": "ا",
        "ﭑ": "ا",
        "ﭖ": "پ",
        "ﭗ": "پ",
        "ﭘ": "پ",
        "ﭙ": "پ",
        "ﭞ": "ت",
        "ﭟ": "ت",
        "ﭠ": "ت",
        "ﭡ": "ت",
        "ﭺ": "چ",
        "ﭻ": "چ",
        "ﭼ": "چ",
        "ﭽ": "چ",
        "ﮊ": "ژ",
        "ﮋ": "ژ",
        "ﮎ": "ک",
        "ﮏ": "ک",
        "ﮐ": "ک",
        "ﮑ": "ک",
        "ﮒ": "گ",
        "ﮓ": "گ",
        "ﮔ": "گ",
        "ﮕ": "گ",
        "ﮤ": "ه",
        "ﮥ": "ه",
        "ﮦ": "ه",
        "ﮪ": "ه",
        "ﮫ": "ه",
        "ﮬ": "ه",
        "ﮭ": "ه",
        "ﮮ": "ی",
        "ﮯ": "ی",
        "ﮰ": "ی",
        "ﮱ": "ی",
        "ﯼ": "ی",
        "ﯽ": "ی",
        "ﯾ": "ی",
        "ﯿ": "ی",
        # Arabic Presentation Forms-B (will be removed)
        "ﹰ": "",
        "ﹱ": "",
        "ﹲ": "",
        "ﹳ": "",
        "ﹴ": "",
        "﹵": "",
        "ﹶ": "",
        "ﹷ": "",
        "ﹸ": "",
        "ﹹ": "",
        "ﹺ": "",
        "ﹻ": "",
        "ﹼ": "",
        "ﹽ": "",
        "ﹾ": "",
        "ﹿ": "",
        # Arabic Presentation Forms-B (will be replaced by persian one)
        "ﺀ": "ی",
        "ﺁ": "ا",
        "ﺂ": "ا",
        "ﺃ": "ا",
        "ﺄ": "ا",
        "ﺅ": "و",
        "ﺆ": "و",
        "ﺇ": "ا",
        "ﺈ": "ا",
        "ﺉ": "ی",
        "ﺊ": "ی",
        "ﺋ": "ی",
        "ﺌ": "ی",
        "ﺍ": "ا",
        "ﺎ": "ا",
        "ﺏ": "ب",
        "ﺐ": "ب",
        "ﺑ": "ب",
        "ﺒ": "ب",
        "ﺓ": "ه",
        "ﺔ": "ه",
        "ﺕ": "ت",
        "ﺖ": "ت",
        "ﺗ": "ت",
        "ﺘ": "ت",
        "ﺙ": "ث",
        "ﺚ": "ث",
        "ﺛ": "ث",
        "ﺜ": "ث",
        "ﺝ": "ج",
        "ﺞ": "ج",
        "ﺟ": "ج",
        "ﺠ": "ج",
        "ﺡ": "ح",
        "ﺢ": "ح",
        "ﺣ": "ح",
        "ﺤ": "ح",
        "ﺥ": "خ",
        "ﺦ": "خ",
        "ﺧ": "خ",
        "ﺨ": "خ",
        "ﺩ": "د",
        "ﺪ": "د",
        "ﺫ": "ذ",
        "ﺬ": "ذ",
        "ﺭ": "ر",
        "ﺮ": "ر",
        "ﺯ": "ز",
        "ﺰ": "ز",
        "ﺱ": "س",
        "ﺲ": "س",
        "ﺳ": "س",
        "ﺴ": "س",
        "ﺵ": "ش",
        "ﺶ": "ش",
        "ﺷ": "ش",
        "ﺸ": "ش",
        "ﺹ": "ص",
        "ﺺ": "ص",
        "ﺻ": "ص",
        "ﺼ": "ص",
        "ﺽ": "ض",
        "ﺾ": "ض",
        "ﺿ": "ض",
        "ﻀ": "ض",
        "ﻁ": "ط",
        "ﻂ": "ط",
        "ﻃ": "ط",
        "ﻄ": "ط",
        "ﻅ": "ظ",
        "ﻆ": "ظ",
        "ﻇ": "ظ",
        "ﻈ": "ظ",
        "ﻉ": "ع",
        "ﻊ": "ع",
        "ﻋ": "ع",
        "ﻌ": "ع",
        "ﻍ": "غ",
        "ﻎ": "غ",
        "ﻏ": "غ",
        "ﻐ": "غ",
        "ﻑ": "ف",
        "ﻒ": "ف",
        "ﻓ": "ف",
        "ﻔ": "ف",
        "ﻕ": "ق",
        "ﻖ": "ق",
        "ﻗ": "ق",
        "ﻘ": "ق",
        "ﻙ": "ک",
        "ﻚ": "ک",
        "ﻛ": "ک",
        "ﻜ": "ک",
        "ﻝ": "ل",
        "ﻞ": "ل",
        "ﻟ": "ل",
        "ﻠ": "ل",
        "ﻡ": "م",
        "ﻢ": "م",
        "ﻣ": "م",
        "ﻤ": "م",
        "ﻥ": "ن",
        "ﻦ": "ن",
        "ﻧ": "ن",
        "ﻨ": "ن",
        "ﻩ": "ه",
        "ﻪ": "ه",
        "ﻫ": "ه",
        "ﻬ": "ه",
        "ﻭ": "و",
        "ﻮ": "و",
        "ﻯ": "ی",
        "ﻰ": "ی",
        "ﻱ": "ی",
        "ﻲ": "ی",
        "ﻳ": "ی",
        "ﻴ": "ی",
        "ﻵ": "لا",
        "ﻶ": "لا",
        "ﻷ": "لا",
        "ﻸ": "لا",
        "ﻹ": "لا",
        "ﻺ": "لا",
        "ﻻ": "لا",
        "ﻼ": "لا",
        # sukun
        "\u0652": "",
    }

translation_table = dict((ord(a), b) for a, b in char_mappings.items())

def clean_persian_text(text: str) -> str:
    # Map invalid characters with replacement to valid characters.
    # apply the translation table to the text
    return text.translate(translation_table)

class ChatsSpider(scrapy.Spider):
    name = "chats"
    start_urls = [
        "https://doctor-yab.ir/faq/?page=1"
    ]

    def __init__(self, **kwargs):

            self.page_limit = int(kwargs.get('limit', 2))

            super().__init__(**kwargs)  # python3

    def parse(self, response):

        for chat in response.css("ul.questions li"):

            post_link = response.urljoin(chat.css("h3 a::attr(href)").get())
            answered = chat.css("i.fa-check").get() is not None

            if answered:
                yield scrapy.Request(post_link, callback=self.parse_chat)

        next_page = response.css("li.PagedList-skipToNext a::attr(href)").get()

        if next_page is not None and self.page_limit > 1:
                self.page_limit -= 1
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_chat(self, response):

        title = response.css("div>h1::text").get().strip()

        question = ' '.join(response.css("div.faq-text::text").getall()).strip()

        answers = []

        for answer in response.css("ul.ans li"):

            dr_name = answer.css("b.name-dr::text").get().strip()
            dr_exp = answer.css("span.dr-t::text").get().strip()
            answer_text = ' '.join(answer.css("p::text").getall()).strip()

            answers.append(
                {
                    'dr_name': clean_persian_text(dr_name),
                    'dr_exp': clean_persian_text(dr_exp),
                    'answer_text': clean_persian_text(answer_text),
                }
            )

        yield {
            'title': clean_persian_text(title),
            'question': clean_persian_text(question),
            'answers': answers,
        }

