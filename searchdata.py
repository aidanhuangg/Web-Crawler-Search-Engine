import os

URLtonum = {}
numtoURL = {}


def import_URL_num_map():
    if not URLtonum:
        with open(os.path.join(os.getcwd(), 'crawl_data', 'url_map.txt'), 'r') as file:
            for line in file:
                x = (line.strip('\n').split(','))
                URLtonum[x[0]] = x[1]
                numtoURL[x[1]] = x[0]


def get_title(url):
    try:
        import_URL_num_map()
        with open(os.path.join(os.getcwd(), 'crawl_data', f'{URLtonum[url]}', 'title.txt'), 'r') as file:
            return file.read().strip()
    except:
        return None


def get_outgoing_links(url):
    try:
        import_URL_num_map()
        with open(os.path.join(os.getcwd(), 'crawl_data', f'{URLtonum[url]}', 'outgoing-links.txt'), 'r') as file:
            return file.read().strip().split()
    except:
        return None


def get_incoming_links(url):
    try:
        import_URL_num_map()
        with open(os.path.join(os.getcwd(), 'crawl_data', f'{URLtonum[url]}', 'incoming-links.txt'), 'r') as file:
            return file.read().strip().split()
    except:
        return None


def get_page_rank(url):
    try:
        import_URL_num_map()
        with open(os.path.join(os.getcwd(), 'crawl_data', f'{URLtonum[url]}', 'page_rank.txt'), 'r') as file:
            return float(file.read().strip())
    except:
        return -1


def get_idf(word):
    try:
        with open(os.path.join(os.getcwd(), 'crawl_data', 'idf', f'{word}.txt'), 'r') as file:
            return float(file.read().strip())
    except:
        return 0


def get_tf(url, word):
    try:
        import_URL_num_map()
        with open(os.path.join(os.getcwd(), 'crawl_data', f'{URLtonum[url]}', 'tf', f'{word}.txt'), 'r') as file:
            return float(file.read().strip())
    except:
        return 0


def get_tf_idf(url, word):
    try:
        import_URL_num_map()
        with open(os.path.join(os.getcwd(), 'crawl_data', f'{URLtonum[url]}', 'tf_idf', f'{word}.txt'), 'r') as file:
            return float(file.read().strip())
    except:
        return 0

