MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "db_words"

RAW_DIR = "./RAW"
OUT_NAME = "wikipedia-mk"

UNWANTED_PAGES = ["корисник", "разговор", "разговор со корисник", 
                    "шаблон", "разговор за шаблон", 
                    "податотека", "разговор за податотека", 
                    "категорија", "разговор за категорија", "википедија", "разговор за википедија", "медијавики", "разговор за медијавики", 
                    "помош", "разговор за помош", "портал", "разговор за портал", "модул", "разговор за модул",
                    "gadget", "gadget talk", "gadget definition", "gadget definition talk", "вп", "кат"]

UNWANTED_KEYWORDS = ["(појаснување).+", "^\d{1,}$", "^(ngc).+", "^(предлошка).+", "^(ic).+", 
                    "^(Разговор за предлошка).+", "^(список).+", "^(космос).+", 
                    "^(iso ).+", "^(hd ).+", "^(hr ).+", "^(грб на ).+", "^(градови ).+"]
                    