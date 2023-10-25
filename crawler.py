import math
import os.path
import time

import webdev
import matmult


def create_directory(directory_name, url, URLtonum, numtoURL):
    URLtonum[url] = directory_name
    numtoURL[directory_name] = url

    precwd = os.getcwd()
    os.makedirs(directory_name)

    os.chdir(directory_name)

    os.makedirs('tf')
    os.makedirs('tf_idf')

    file = open('incoming-links.txt', 'w')
    file = open('outgoing-links.txt', 'w')
    file = open('page_rank.txt', 'w')
    file = open('title.txt', 'w')
    file.close()

    os.chdir(precwd)
    return URLtonum, numtoURL


def delete_directory(directory_name):
    if os.path.isdir(directory_name):
        files = os.listdir(directory_name)
        for file in files:
            os.remove(os.path.join(directory_name, file))
        os.rmdir(directory_name)
    else:
        print('Did not find directory to delete')


def add_to_queue(current_url, prev_url, queue, visited_url, URLtonum, numtoURL, directory_name):
    # if the url has already been visited (directory exists), then we add the link to the incoming-links of that url
    if current_url in visited_url:
        precwd = os.getcwd()
        os.chdir(str(URLtonum[current_url]))
        with open('incoming-links.txt', 'a') as file:
            file.write(prev_url + " ")
        os.chdir(precwd)

        return queue, visited_url, directory_name

    # if the url does not exist, we will add the incoming link in the create_directory function
    URLtonum, numtoURL = create_directory(str(directory_name), current_url, URLtonum, numtoURL)

    precwd = os.getcwd()
    os.chdir(str(URLtonum[current_url]))
    with open('incoming-links.txt', 'a') as file:
        if prev_url is not None:
            file.write(prev_url + " ")
    os.chdir(precwd)

    # add to url_map.txt
    with open('url_map.txt', 'a') as file:
        file.write(f'{current_url},{URLtonum[current_url]}\n')

    directory_name += 1
    visited_url[current_url] = True

    queue.append(current_url)
    return queue, visited_url, directory_name


def add_to_file(directory, title, contents):
    precwd = os.getcwd()
    os.chdir(directory)
    with open(f'{title}.txt', 'w') as file:
        file.write(contents)
    os.chdir(precwd)
    return


def extract_title(html_string):
    startindex = html_string.find('<title>') + 7
    endindex = html_string.find('</title>')
    return html_string[startindex:endindex]


def extract_links(html_string, url):
    url = str(url)
    last_slash_index = url.rfind('/')
    abs_url = url[:last_slash_index + 1]

    links = []
    html_string = html_string.split("\n")
    for line in html_string:
        if line.find('href'):
            startindex = line.find('href="') + 8
            endindex = line.rfind('"')
            if endindex > startindex:
                links.append(abs_url + line[startindex:endindex] + " ")
    return ''.join(links)


def extract_words(html_string):
    startindex = html_string.find('<p>') + 3
    endindex = html_string.rfind('</p>')
    return html_string[startindex:endindex]


def calculate_tfs(directory, words, word_in_url_freqs, current_url):
    freqs = {}
    words = words.split()
    total_num_of_words = len(words)
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
            if word not in word_in_url_freqs:
                word_in_url_freqs[word] = []
            freqs[word] = 0
        freqs[word] += 1

    precwd = os.getcwd()
    os.chdir(directory)
    for word in unique_words:
        word_in_url_freqs[word].append(current_url)

        add_to_file('tf', word, str(freqs[word] / total_num_of_words))

    os.chdir(precwd)
    return word_in_url_freqs


def calculate_idfs(num_urls, word_in_url_freqs):
    unique_words = list(word_in_url_freqs.keys())
    for word in unique_words:
        add_to_file('idf', word, str((math.log2(num_urls / (1 + len(word_in_url_freqs[word]))))))
    return


def calculate_tf_idfs(num_urls, word_in_url_freqs):
    unique_words = list(word_in_url_freqs.keys())

    for url in range(num_urls):
        precwd_base = os.getcwd()
        os.chdir(f'{url}')
        precwd_sub = os.getcwd()
        os.chdir('tf')
        for word in unique_words:
            if os.path.isfile(f'{word}.txt'):
                # grab tf value
                with open(f'{word}.txt', 'r') as file:
                    tf = float(file.read())

                # grab idf value
                os.chdir(precwd_base)
                os.chdir('idf')
                with open(f'{word}.txt', 'r') as file:
                    idf = float(file.read())
                    tf_idf = math.log2(1 + tf) * idf

                # write to tf_idf directory
                os.chdir(precwd_sub)
                os.chdir('tf_idf')
                with open(f'{word}.txt', 'w') as file:
                    file.write(str(tf_idf))
                    os.chdir(precwd_sub)
                    os.chdir('tf')

        os.chdir(precwd_base)
    return


def calculate_page_ranks(num_urls, URLtonum):

    # creating the adjacency matrix
    matrix = []
    for url_num in range(num_urls):
        precwd = os.getcwd()
        os.chdir(str(url_num))
        with open('incoming-links.txt', 'r') as file:
            lines = file.read().strip()
        urls = lines.split(' ')

        list = [0 for i in range(num_urls)]

        for url in urls:
            list[int(URLtonum[url])] = 1
        matrix.append(list)

        os.chdir(precwd)

    # transition probability matrix
    for list in range(len(matrix)):
        one_count = 0
        for index in matrix[list]:
            if index == 1:
                one_count += 1
        if one_count > 0:  # divide each 1 by the number of 1s
            for index in range(len(matrix[list])):
                if matrix[list][index] == 1:
                    matrix[list][index] = matrix[list][index] / one_count
        else:  # replace each element by 1/N
            for index in range(len(matrix[list])):
                matrix[list][index] = 1 / len(matrix)

    # Scaled Adjacency Matrix
    alpha_value = 0.1
    for list in range(len(matrix)):
        for index in range(len(matrix[list])):
            matrix[list][index] = (1 - alpha_value) * matrix[list][index]

    # Adding Alpha/N
    for list in range(len(matrix)):
        for index in range(len(matrix[list])):
            matrix[list][index] += alpha_value / len(matrix)

    # Power iteration
    t0 = [[1 / len(matrix) for i in range(len(matrix))]]
    t1 = matmult.mult_matrix(t0, matrix)
    euclidean_distance = matmult.euclidean_dist(t0, t1)

    while euclidean_distance > 0.0001:
        t0 = t1
        t1 = matmult.mult_matrix(t1, matrix)
        euclidean_distance = matmult.euclidean_dist(t0, t1)

    final_pr_vector = t1
    for i in range(len(final_pr_vector[0])):
        add_to_file(str(i), 'page_rank', str(final_pr_vector[0][i]))

    return


def crawl(seed):
    precwd = os.getcwd()
    URLtonum = {}
    numtoURL = {}
    visited_url = {}
    queue = []
    word_in_url_freqs = {}
    number_URL_visited = 0
    directory_name = 0

    if os.path.exists('crawl_data'):  # we delete the pre-existing data
        os.chdir('crawl_data')
        i = 0
        while True:
            if os.path.isdir(f'{i}'):
                precwd2 = os.getcwd()

                os.chdir(f'{i}')
                delete_directory('tf')
                delete_directory('tf_idf')
                os.chdir(precwd2)

                delete_directory(f'{i}')
                i += 1
            else:
                break

        delete_directory('idf')
        os.chdir(precwd)
        delete_directory('crawl_data')

    os.chdir(precwd)
    os.makedirs('crawl_data')
    os.chdir('crawl_data')
    os.makedirs('idf')
    file = open('url_map.txt', 'w')
    file.close()

    queue, visited_url, directory_name = add_to_queue(seed, None, queue, visited_url, URLtonum, numtoURL,
                                                      directory_name)

    while len(queue) > 0:
        current_url = queue.pop(0)

        # parse the current_url
        websitesourcecode = webdev.read_url(current_url)

        # extract title
        title = extract_title(websitesourcecode)
        add_to_file(str(number_URL_visited), 'title', title)

        # extract links
        links = extract_links(websitesourcecode, current_url)
        add_to_file(str(number_URL_visited), 'outgoing-links', links)
        links = links.split()
        for link in links:
            queue, visited_url, directory_name = add_to_queue(str(link), str(current_url), queue, visited_url,
                                                              URLtonum, numtoURL, directory_name)

        words = extract_words(websitesourcecode)
        word_in_url_freqs = calculate_tfs(str(number_URL_visited), words, word_in_url_freqs, current_url)

        number_URL_visited += 1

    calculate_idfs(number_URL_visited, word_in_url_freqs)

    calculate_tf_idfs(number_URL_visited, word_in_url_freqs)

    calculate_page_ranks(number_URL_visited, URLtonum)

    os.chdir(precwd)

    return number_URL_visited

with open('search-results.txt', 'w') as file:
    crawl(input('Enter seed url: '))
    file.write('Crawling Complete.')

