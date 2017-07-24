
# Tracking Congress Tweets

American Politics has become polarized over the past quarter-century. Research has shown, using attraction-and-repulsion models adapted from physics and data on how senators vote, that American policy making has become more segregated and with little common voting, contrasting with what we observed decades ago where senators regularly crossed the aisle to get things done. This phenomenon is not only related to politicians but has also affected the public: according to data from the Pew Research Center, 45% of Republicans and 41% of Democrats think the other party is so dangerous that they consider it as a **threat to the nation**. Some commentators have also suggested that *media* and *new social platforms* exacerbate political polarization by spreading *fake news*.

A polarized political environment might have negative consequences, especially when the control of the executive and legislative branches are split among cohesive parties. Some of them include a reduction of the number of compromises that parties are willing to take, gridlock and **less legislative productivity**,  less policy innovation, and inhibition of majority rule. All these scenarios implied negative consequences for citizens and people directly or indirectly affected by the legislation.

In this project, I propose to create an index of polarization and political mood of Congress members by analyzing their tweets as a more fine-grained measure to track legislators' behavior and explore their consequences of the political environment on legislation practices and outcomes.

The goals of this project are:

1. To track the level of positivity and negativity of congress members tweets by day using **sentiment analysis** (i.e., extraction of *emotional intent* from text)
2. Create a index of polarization of congress tweets. After adjusting subjectivity lexicons and assess text classification, to define a method to classify tweets every day.
4. To explore the association between positivity and polarization indexes with outcomes such as congress approval ratings and proportion of bill passed.

### Data

I use data collected by the developer Alex Litel, who created a tool ([Congressional Tweet Automator](https://github.com/alexlitel/congresstweets)) that stores every Congress member’s tweets every day, as been highlighted in a recent [Washington Post article](https://www.washingtonpost.com/news/politics/wp/2017/06/26/how-congress-tweets-visualized/?utm_term=.6e80a8653a5f).

Daily tweet files and meta information on congress members is in JSON format.

### Preliminary analysis

1. A rather simple approach is to state whether a document is positive and negative, that is, the *polarity* of a document. Or in other words, the measure of positive or negative tweets?




I use the data provided by X.


Polarity calculation is a number that is negative to represent a negative, zero to represent neutral and positive to present positive tone.

Subjectivity lexicons: list of words associated with a particular emotional state.

Qdap's scoring function for positive and negative word choice

Sentiment analysis

In political field, it is used to keep track of political view, to detect consistency and inconsistency between statements and actions at the government level. It can be used to predict election results as well!


![](figures/hist_polarity.png)
![](figures/zhist_polarity.png)




### Next steps

The preliminary analysis shown in this proposal are very preliminary (e.g., this is my first time doing this kind of analysis.

1. T
2.