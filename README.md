# Web Crawler and Search Engine Program

### Created by: Aidan Huang

This project is implemented with search engine algorithms and computations to provide the user with a list of ranked webpages based on a query input. These include:
- PageRank Algorithm
- Vector Space Model and Cosine Similarity
- Term Frequencies and Inverse Document Frequencies

A PDF report of the project is included, detailing the program design, time complexities, and space complexities. 

## How to run

After downloading and extracting the zip file, enter 'cd downloads' into the command line/terminal and then enter 'cd project-master'.
To run the program, enter 'python3 crawler.py' into the command line/terminal.
Enter the seed url when prompted.
When program is finished crawling, enter 'python3 search.py' into the command line/terminal.
Enter the phrase.
Enter True or False for Boost.
Web Results will appear in 'search-results.txt'

----------------------------------------------------------------------

## Program Functionality
All parts of the program are complete and functional. The program passes all test cases in the testing-resources folder. 
File Structure
All of the crawled data is contained in a ‘crawl_data’ directory, which includes directories for each URL, the idf values of unique words, and a ‘url_map.txt’ file. I implemented my file structure this way so that all of the data can be retrieved from these files and eliminates the web crawling beyond the crawler module. The directories start from 0 to N, being the number of URLs. Each of these URL directories contain a ‘tf’ directory for tf-values, ‘tf_idf’ directory for tf-idf values. They also contain text files like ‘incoming-links.txt’, ‘outgoing-links.txt’, ‘page_rank.txt’, and ‘title.txt’. Outside of the URL directories, there is a ‘idf’ directory which stores the idf values of each word, as well as ‘url_map.txt’ to store the URL mappings.

## Program Efficiency

The downside of this file structure is that it would take up more space, but offers an upside in efficiency at finding the search results for queries. In a search engine, speed would be prioritized over space because users want fast results. In the crawl, we gather the data and calculate values like tf and idf so that it can be easily accessed in the other modules. If we were to crawl through every time for calculations, it would be time-consuming and inefficient. 

## Program Highlights

An issue I encountered was obtaining the incoming links of a URL without the need to crawl through the webpages a second time. When looking at outgoing links of an URL, those URLs may not exist yet (directory not yet created) so I could not add the current URL to the incoming-links.txt file of a nonexistent directory. I was able to find a solution by creating the directory whenever the program sees a new URL, and then adding the incoming link. If the directory already exists, we can ignore creating the directory. Another issue was that during testing in search.py, I discovered that the denominator for PageRank can sometimes be 0, which would cause an error because division by zero is not allowed. Therefore, I simply let the overall cosine value equal to 0. However, the original dictionary implementation only allowed for one url to be recognized with a value of 0. Therefore, I created a list inside of the dictionary with a key of 0.0 in case there are multiple urls with that cosine. 
