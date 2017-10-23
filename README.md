
# Tracking Congress Political Polarization with Twitter

American Politics has become polarized over the past quarter-century. Research shows that American politics are more segregated and legislators have less common voting than decades ago, when senators regularly crossed the aisle to get things done. This phenomenon does not only affect politicians but also the public. According to data from the Pew Research Center, 45% of Republicans and 41% of Democrats think the other party is so dangerous that they consider it as a **threat to the nation**. Some commentators have also suggested that *media* and *new social platforms* exacerbate political polarization by spreading *fake news*.

A polarized political environment has negative consequences, especially when the control of the executive and legislative branches are split among cohesive parties. Some of its drawbacks include the reduction of the number of compromises parties are willing to take, **less legislative productivity**, gridlocks, less policy innovation, and inhibition of the majority rule. All these consequences affects people, so it is important to look for alternative measures that help us to track political polarization.

Using only legislative votes is rather limited because they only reflects the consolidation of polarization behavior and cannot be tracks in day by day. In this project, I propose to create an index of polarization and political mood analyzing Congress members' tweets. The goal is to provide an alternative and fine-grained measure - that supplements traditional ones - to track Congress polarization and explore their consequences on legislation practices and outcomes.

The goals of this project are:

1.  To track the level of positivity and negativity of daily Congress members tweets using **sentiment analysis**.
2.  To create an index of polarization from Congress tweets. After adjusting subjectivity lexicons and assess text classification, to define a method to classify tweets every day and create a polarization index.
3.  To explore the association between positivity and polarization indexes with outcomes such as Congress approval ratings and proportion of bills passed.

# Data

I use data collected by the developer Alex Litel through the app ([Congressional Tweet Automator](https://github.com/alexlitel/congresstweets)). This app stores Congress member’s tweets every day, and it was highlighted recently in a [Washington Post article](https://www.washingtonpost.com/news/politics/wp/2017/06/26/how-congress-tweets-visualized/?utm_term=.6e80a8653a5f).


# Preliminary app

https://sdaza-capstone.herokuapp.com/

# Next steps

<!-- This is my first time doing text analysis, and I am very excited about this project. Learning and applying data science techniques to get insights is exactly what I look for, that is why I applied to the Incubator. There is still a lot to do. I will follow these next steps: -->

1.  To use different subjectivity lexicons to assess the robustness of classifications, and adapt them accordingly to better capture the nature of tweets.
2.  To weight results by members rather than number of tweets.
3. To examine the relationship between polarity and actual votes.
