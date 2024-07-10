# Student names: Khadidja Manaa, Xiaoyao Ren, Sarah Binte Tariq

# Exploring Themes and Sentiment in English Rap

This project aims to carry out both sentiment analysis and topic modelling to find trends or patterns in the lyrics of 40 rappers from the Billboard Top 50 list.

# Introduction

This report delves into the unique world of rap music, a culturally and linguistically distinctive genre that artfully explores a range of emotions and sentiments through its lyrical content. The main focus of this project is to comprehensively examine the sentiments and topics conveyed in rap lyrics. Through the utilization of sentiment analysis and topic modeling, the objective is to uncover the linguistic, emotional, and cultural implications embedded within these lyrics. This combined approach enables a deeper understanding of the affective emotions, attitudes, recurring themes, and thematic patterns that permeate rap music. 

# Part One: Lyrics scraper 

The lyrics_scraper.py was implemented such that it automatically crawls www.genius.com in order to extract and store lyrics. We had some issues with it, such as incorrectly storing the metadata (we had an issue with years specifically), or timing out on specific rappers. Sometimes, we even had to run it many times to get results. Eventually, we stored our data in .csv files for sentiment analysis, and .json files for topic modelling.

# Part Two: Formatting

The formatting.py script was used to clean the lyrics, in the sense that sometimes other unnecessary data was extracted, such as the number of contributers that assembled the lyrics on the website, or even terms that are specifically used to divide songs into parts, like 'Chorus' and 'Outro'. 

# Part Three: Preprocessing

The preprocessing.py script is crucial, as it tokenizes, lemmatizes, and removes the punctuation, stop words, and non English words in the lyrics column of the .csv file. Additionally, another version of the dataset was created, in which the profanity library in python was used to remove profanity. Our dataset is now ready!

# Part Four: Sentiment analysis

We chose Jupyter Notebook for both sentiment analysis and topic modelling, as we think it visualizes the results better than a python script. In sentiment_analysis.ipynb, VADER was imported from the NLTK library and used to get the sentiment scores. Additionally, Seaborn and Matplotlib are two python libraries we used to visualize our results. We looked at four main analyses:
    1. Sentiment scores
    2. Compound sentiment scores
    3. Standard deviation per rapper
    4. Chronological analyses of sentiment scores

# Part Five: Topic modelling

In the topic_modelling.ipynb script, we worked with the Gensim library to generate bigrams and trigrams, and build a model. Using the coherence value measurement, we arrive at the optimal number of topics, which is 7. We use this number to generate topics and WordClouds using the wordcloud and Matplotlib libraries. 

# Conclusion

This project has taught us a lot, and offered valuable opportunities for us to put what we learned into practice. We give special thanks to Gerold Schneider and Ahmet Yavuz Uluslu for their help and guidance throughout the duration of this project. 