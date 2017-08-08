Topic Modeling Congress Members' Tweets
================
August 07, 2017

I explore Congress members' tweets using the Latent Dirichlet Allocation (LDA) method, a probability-based approach to find clusters in documents. The objective is to identify topics and compare [polarity scores](proposal.md) by party affiliation, that is, to find topics in which writer's tone is different by party.

Using the data from the proposal, I run a LDA model with the `lda` package in R.

``` r
#+ load data and clean tweets
load("tweet_data.Rdata")
nrow(wdat)
```

    ## [1] 25857

``` r
text <- wdat$text

#char_to_remove <- c("m", "w", "t", "th", "c", "rd", "u", "s", "d", "en", "de", "la", "y", "el", "h")

text <- removeNumbers(text)
text <- removeWords(text, c(stopwords("en")))
text <- removePunctuation(text)

blank.removal <- function(x) {
  x <- unlist(strsplit(x, " "))
  x <- subset(x, nchar(x) > 0)
  x <- paste(x, collapse = " ")
}

text <- pblapply(text, blank.removal)
tweets <- lexicalize(text)

wc <- word.counts(tweets$documents, tweets$vocab)
tweet.length <-  document.lengths(tweets$documents)
```

I ran several topic models and found that a solution with 4 cluster seems reasonable after exploring word frequencies (`k = 4`). The plot below shows that the model reaches convergence after 200 iterations. However, the LDA algorithm provides rather unstable results. I have to look for alternative algorithms and specifications.

``` r
k <- 4
num.iter <- 500
alpha <- 0.02
eta <- 0.02

set.seed(12345678)
fit <- lda.collapsed.gibbs.sampler(documents = tweets$documents, K = k,
  vocab = tweets$vocab,
  num.iterations = num.iter,
  alpha = alpha,
  eta = eta,
  initial = NULL,
  burnin = 50,
  compute.log.likelihood = TRUE)

plot(fit$log.likelihoods[1,], ylab = "Log likelihood")
```

![](topic_modeling_files/figure-markdown_github-ascii_identifiers/unnamed-chunk-3-1.png)

``` r
top.topic.words(fit$topics, 10, by.score = TRUE)
```

    ##       [,1]      [,2]           [,3]            [,4]
    ##  [1,] "great"   "happy"        "bill"          "care"
    ##  [2,] "town"    "th"           "trump"         "health"
    ##  [3,] "hall"    "birthday"     "ndaa"          "trumpcare"
    ##  [4,] "discuss" "prayers"      "fy"            "medicaid"
    ##  [5,] "summer"  "family"       "netneutrality" "aca"
    ##  [6,] "office"  "july"         "must"          "repeal"
    ##  [7,] "tune"    "independence" "sanctions"     "gop"
    ##  [8,] "enjoyed" "wishing"      "russia"        "bill"
    ##  [9,] "pm"      "service"      "passed"        "healthcare"
    ## [10,] "tour"    "honor"        "internet"      "protectourcare"

``` r
top.topic.documents(fit$document_sums,1)
```

    ## [1]  2375 14073  6543 19423

The more frequent words by topic are shown below (both in a table and word cloud). The first topic is mainly about *town hall* and *summer*, the second one on the *Independence Day* celebration. The third and fourth are about the connection between Russia and Trump's administration , and *health care reform and Affordable Care Act (ACA)*.

``` r
theta <- t(pbapply(fit$document_sums + alpha, 2, function(x) x/sum(x)))
wdat[, topic := apply(theta,1,which.max)]
summary(wdat$topic)
```

    ##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    ##   1.000   1.000   3.000   2.615   4.000   4.000

``` r
table(wdat$topic)
```

    ##
    ##    1    2    3    4
    ## 6522 3954 8340 7041

``` r
# assign scores
ts <- wdat[party != "I", .(polarity = Mean(polarity)), .(topic, party)]
# compute absolute differences between parties
d <- ts[, .(d = abs(diff(polarity))), .(topic)]
setorder(d, -d); d
```

    ##    topic           d
    ## 1:     4 0.067550313
    ## 2:     3 0.038683959
    ## 3:     2 0.030305640
    ## 4:     1 0.005233338

``` r
ggplot(ts, aes(x = topic, y = polarity, group = party, fill = party, color = party)) + geom_point() + geom_line()
```

![](topic_modeling_files/figure-markdown_github-ascii_identifiers/unnamed-chunk-4-1.png)

``` r
createWordCloud <- function(data, title = "Title", groups) {
  corp <- list()
  for (i in 1:groups) {
   corp[[i]] <- paste(data[topic == i, text], collapse = " ")
  }

  all.terms <- unlist(corp)
  all.corpus <- VCorpus(VectorSource(all.terms))
  all.tdm <- TermDocumentMatrix(all.corpus,
                                control = list(weighting = weightSMART,
                                               removePunctuation = TRUE,
                                               removeNumbers = TRUE,
                                               stopwords = stopwords(kind = "en")))
  all.tdm.m <- as.matrix(all.tdm)
  colnames(all.tdm.m) <- as.character(1:groups)
  comparison.cloud(all.tdm.m, random.order = FALSE, max.words = 100)
  text(x=0.5, y=1.02, title)
}

createWordCloud(wdat, "Word Cloud by Topics", 4)
```

![](topic_modeling_files/figure-markdown_github-ascii_identifiers/unnamed-chunk-5-1.png)

Finally, we can see that differences in sentiment scores are higher in topics such *health care reform* and the *Russian meddling*, and tend to converge on positive topics such the *Independence Day*. This provide some face validity to the idea of using sentiment scores to create a polarization index. However, different topic modeling algorithms should be used to assess the robustness of the method.

References
==========

-   Kwartler, T. (2017). Text mining in practice with R.
-   Munzert, S. (2015). Automated data collection with R: a practical guide to Web scraping and text mining. Chichester, West Sussex, United Kingdom: John Wiley & Sons Inc.
