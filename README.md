# Semantic Search

## The Task
The objective of this assignment is to engineer a novel wikipedia search engine using what we've learned about data collection, infrastructure, and natural language processing.

The task has two **required sections:**
- Data collection
- Search algorithm development

### Part 1 -- Collection

We will query the wikipedia API and collect all of the articles for a specified category. For the purposes of this project, we will look at two categories (however this can be applied to any specified category) 

* [Machine Learning](https://en.wikipedia.org/wiki/Category:Machine_learning)
* [Business Software](https://en.wikipedia.org/wiki/Category:Business_software)

The raw page text and its category information were written to a collection on a Mongo server running on a dedicated AWS instance.

The code can be run via the command line, the steps are as follows:

1. Work your way into the directory containing the script
2. Type ```bash
	$ python collect.py "some category" #nesting_level#```
e.g. ```bash $ python collect.py 'machine learning' 3```

The command line will output the category for every 10 pages collected to ensure that it is running correctly


### Part 2 -- Search

We used Latent Semantic Analysis to search the pages. For a given search query, we found the top 5 related articles to the search query using SVD and cosine similarity. 

This can also be run via the command line e.g.

```bash
$ python search.py "discriminant"
```

The command line will then output the top 5 related articles for the given search word

### Further Work

Ideally we would like to build a predictive model. More specifically, when a new article is published on Wikipedia, we would like to predict which category the article would fall under.

Also, the scripts could be cleaned up a bit to be less computationally expensive. Currently, it takes ~1-2 seconds to collect a single page's contents.


