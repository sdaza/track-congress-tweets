---
title: "How Congress Political Polarization Evolves in Tweeter"
output: rmarkdown::github_document
date: "August 04, 2017"
---


{% highlight text %}
## Loading required package: methods
{% endhighlight %}



{% highlight text %}
## Loading required package: qdapDictionaries
{% endhighlight %}



{% highlight text %}
## Loading required package: qdapRegex
{% endhighlight %}



{% highlight text %}
## 
## Attaching package: 'qdapRegex'
{% endhighlight %}



{% highlight text %}
## The following object is masked from 'package:jsonlite':
## 
##     validate
{% endhighlight %}



{% highlight text %}
## Loading required package: qdapTools
{% endhighlight %}



{% highlight text %}
## Loading required package: RColorBrewer
{% endhighlight %}



{% highlight text %}
## Error: package or namespace load failed for 'qdap':
##  .onLoad failed in loadNamespace() for 'rJava', details:
##   call: dyn.load(file, DLLpath = DLLpath, ...)
##   error: unable to load shared object '/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so':
##   dlopen(/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so, 6): Library not loaded: @rpath/libjvm.dylib
##   Referenced from: /Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so
##   Reason: image not found
{% endhighlight %}



{% highlight text %}
## Loading required package: NLP
{% endhighlight %}



{% highlight text %}
## Loading required package: data.table
{% endhighlight %}



{% highlight text %}
## 
## Attaching package: 'data.table'
{% endhighlight %}



{% highlight text %}
## The following object is masked from 'package:qdapTools':
## 
##     shift
{% endhighlight %}



{% highlight text %}
## Loading required package: knitr
{% endhighlight %}



{% highlight text %}
## Loading required package: miceadds
{% endhighlight %}



{% highlight text %}
## Loading required package: mice
{% endhighlight %}



{% highlight text %}
## * miceadds 2.4-12 (2017-04-19 14:04:12)
{% endhighlight %}



{% highlight text %}
## 
## Attaching package: 'lubridate'
{% endhighlight %}



{% highlight text %}
## The following objects are masked from 'package:data.table':
## 
##     hour, isoweek, mday, minute, month, quarter, second, wday,
##     week, yday, year
{% endhighlight %}



{% highlight text %}
## The following object is masked from 'package:base':
## 
##     date
{% endhighlight %}



{% highlight text %}
## Error: package or namespace load failed for 'qdap':
##  .onLoad failed in loadNamespace() for 'rJava', details:
##   call: dyn.load(file, DLLpath = DLLpath, ...)
##   error: unable to load shared object '/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so':
##   dlopen(/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so, 6): Library not loaded: @rpath/libjvm.dylib
##   Referenced from: /Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so
##   Reason: image not found
{% endhighlight %}



{% highlight text %}
## 
## Attaching package: 'ggplot2'
{% endhighlight %}



{% highlight text %}
## The following object is masked from 'package:NLP':
## 
##     annotate
{% endhighlight %}



{% highlight text %}
## The following object is masked from 'package:qdapRegex':
## 
##     %+%
{% endhighlight %}



{% highlight text %}
## Error: package or namespace load failed for 'qdap':
##  .onLoad failed in loadNamespace() for 'rJava', details:
##   call: dyn.load(file, DLLpath = DLLpath, ...)
##   error: unable to load shared object '/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so':
##   dlopen(/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so, 6): Library not loaded: @rpath/libjvm.dylib
##   Referenced from: /Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so
##   Reason: image not found
{% endhighlight %}



{% highlight text %}
## Error: package or namespace load failed for 'qdap':
##  .onLoad failed in loadNamespace() for 'rJava', details:
##   call: dyn.load(file, DLLpath = DLLpath, ...)
##   error: unable to load shared object '/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so':
##   dlopen(/Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so, 6): Library not loaded: @rpath/libjvm.dylib
##   Referenced from: /Library/Frameworks/R.framework/Versions/3.4/Resources/library/rJava/libs/rJava.so
##   Reason: image not found
{% endhighlight %}


American Politics has become polarized over the past quarter-century. Research shows that American policy making has become more segregated and with little common voting, contrasting with what we observed decades ago where senators regularly crossed the aisle to get things done. This phenomenon is not only related to politicians but has also affected the public: according to data from the Pew Research Center, 45% of Republicans and 41% of Democrats think the other party is so dangerous that they consider it as a **threat to the nation**. Some commentators have also suggested that *media* and *new social platforms* exacerbate political polarization by spreading *fake news*.

A polarized political environment might have negative consequences, especially when the control of the executive and legislative branches are split among cohesive parties. Some of these consequences include a reduction of the number of compromises parties are willing to take, gridlock and **less legislative productivity**,  less policy innovation, and inhibition of the majority rule. All these scenarios implied negative consequences for citizens and people affected by laws.

Can we measure and track Congress polarization not only using legislative votes but alternative sources of information such as tweets? Are there sources from which we can gather information every day to measure Congress polarization? In this project, I propose to create an index of polarization and political mood of Congress members by analyzing their tweets. The goal is to provide an alternative and fine-grained measure - that supplements traditional ones - to track Congress polarization and explore their consequences on legislation practices and outcomes. This proposal only shows initial results.

The goals of the project are:

1. To track the level of positivity and negativity of daily Congress members tweets using **sentiment analysis**.
2. To create an index of polarization from Congress tweets. After adjusting subjectivity lexicons and assess text classification, to define a method to classify tweets every day and create a polarization index.
3. To explore the association between positivity and polarization indexes with outcomes such as Congress approval ratings and proportion of bill passed.

# Data

I use data collected by the developer Alex Litel through the app ([Congressional Tweet Automator](https://github.com/alexlitel/congresstweets)). This app stores Congress member’s tweets every day, and it was highlighted recently in a [Washington Post article](https://www.washingtonpost.com/news/politics/wp/2017/06/26/how-congress-tweets-visualized/?utm_term=.6e80a8653a5f).

Daily tweet files and meta information on Congress members are in JSON format.

# Preliminary analysis

This analysis uses Congress tweets from June 21 to July 21, 2017. The objective is to estimate the polarity of tweets, that is, the measure of positive or negative intent in a writer's tone. The aim is to examine their variability and describe the most frequent words used by polarity and political party. This is just a first step in defining a more complex polarization index.

After collecting tweets, I kept only those coming from accounts that match metadata for all the accounts the project follows for tweet collection (e.g., party affiliation, name). Then, I cleaned tweets by removing retweets (RT), URLs, usernames. Future versions of this analysis will process (punctuation based) emoticons and emojis.

I used the polarity function from package `qdap` to scan for positive and negative words within a list of terms associated with a particular emotional (i.e.,  subjectivity lexicon) and obtain polarity scores. Negative numbers represent a negative tone, zero represents a neutral tone, and positive numbers a positive tone. I used the lexicon developed by Bing Liu at the University of Illinois at Chicago.

I analyzed 32497 tweets, from Democrats and Republican members. Most of the tweets come from Democrats (62%), and the House of Representatives (72%). Below I show the distribution of the polarity scores:

![](figures/hist_polarity.png)

The average of the polarity score is 0.11. This means that on average each tweet is rather neutral, although they slightly incline towards more positive words. Democrats seem to have a higher proportion of *neutral* and negative words, what is confirmed by comparing the average polarity by party:  0.07 for Democrats, and 0.17 for Republicans.

The figure below shows the average polarity score by Political party and day.

![](figures/trend_polarity.png)

As can be seen, the scores vary considerably over time. Positivity reaches a pick during the Independence Day when both parties tend to coincide on their positive tone. The biggest difference between scores is observed on June 26th. Some of the most important headlines during that day was *Senate's version of Health Care Bill would increase the number of uninsured by 22 million by 2026*. This provides some initial face validity of the polarity score.

Finally, I show word clouds by party based on a scaled polarity score. In the case of Republicans, most of the positive words are related to *award*, *protection*, *gold*, *innovation*, and *success*, while among Democrats there are more messages related to the Independence Day. Regarding the negative words, both parties highlight the tragedy of US marines in Mississippi, although Democrats emphasize terms such as *reject*, *threaten*, *flawed*, *corruption*. Performing topic modeling and clustering will provide more insights on these patterns.


<!-- ![](figures/words_r.png)
![](figures/words_d.png)
 -->
### Next steps

This is my first time doing text analysis, and I am very excited about this project. Learning and applying data science techniques to get insights is exactly what I look for, that is why I applied to the Incubator. There is still a lot to do. I will follow these next steps:

1. To use different subjectivity lexicons to assess the robustness of classifications, and adapt them accordingly to better capture the nature of tweets.
2. To weight results by members rather than number of tweets.
3. To use clustering and topic modeling methods to get insights on the content tweets by party, and characterize polarity scores in a more systematic way.
4. Create a Shiny app to process these data automatically and deliver it in a friendly format by day and month.

### References

- Kwartler, T. (2017). Text mining in practice with R.
- Munzert, S. (2015). Automated data collection with R: a practical guide to Web scraping and text mining. Chichester, West Sussex, United Kingdom: John Wiley & Sons Inc.

