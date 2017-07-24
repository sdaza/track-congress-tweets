######################################################
# exploratory analysis congress tweets
######################################################

#+ clear working space
rm(list=ls(all=TRUE))
path <- "/Users/sdaza/Google Drive/github/i_proposal/figures"

#+ load libraries
library(jsonlite)
library(qdap)
library(tm)
library(sdazar)
library(stringdist)
library(lubridate)
library(stringr)
library(tm)
library(qdap)
library(wordcloud)
library(ggplot2)
library(ggthemes)
library(textcat)

#############################
#+ metadata
#############################

# for now to use only matched tweeter accounts!!!

# load metadata
url <- "https://raw.githubusercontent.com/alexlitel/congresstweets-automator/master/data/users-filtered.json"
meta <- jsonlite::fromJSON(url, simplifyDataFrame = FALSE)
length(meta)

# extract data of interest
dmeta <- list()
for (i in 1:length(meta)) {
  temp <- meta[[i]]
  temp
  dmeta[[i]] <- data.table(
  name =temp$name,
  chamber =temp$chamber,
  type = temp$type,
  party = ifelse(is.null(temp$party), NA, temp$party),
  sn1 = ifelse(length(temp$accounts$office) > 0 && !is.null(temp$accounts$office[[1]]$screen_name),
               temp$accounts$office[[1]]$screen_name, NA),
  sn2 = ifelse(length(temp$accounts$campaing) > 0 && !is.null(temp$accounts$campaign[[1]]$screen_name),
               emp$accounts$campaign[[1]]$screen_name, NA))
}

dmeta <- rbindlist(dmeta)
table(is.na(dmeta$sn1))

summary(dmeta)
prop.table(table(dmeta$chamber))
prop.table(table(dmeta$type))
anyDuplicated(dmeta[type == "member", name]) # duplicates among members

dmeta <- dmeta[type == "member"] # select only member

anyDuplicated(dmeta$sn1)
anyDuplicated(dmeta$sn2)

setkey(dmeta, sn1)
dmeta[, screen_name := ifelse(is.na(sn1), sn2, sn1)]
dmeta[is.na(screen_name)]
dmeta[!is.na(screen_name), N := .N, screen_name]
table(dmeta$N, useNA = "ifany") # okey, no duplicates excepts for missing cases

# congress member names in metadata
mnames <- unique(dmeta$screen_name)

#+ load tweeter data for month
dates <- seq(as.Date("2017-06-21"), as.Date("2017-07-21"), by = "day")

ldat <- list()
for (i in seq_along(dates)) {
      url <- paste0("https://alexlitel.github.io/congresstweets/data/", dates[i], ".json")
      ldat[[i]] <- jsonlite::fromJSON(url, simplifyDataFrame = TRUE)
}

length(ldat)
dat <- rbindlist(ldat)

names(dat)
table(dat$screen_name)

tnames <- unique(dat$screen_name)
tnames
mnames <- unique(dmeta$screen_name)
mnames

notthere <- !tnames %in% mnames
length(notthere) #
there <- tnames[!notthere]
length(there) # 507, okey, not that bad!

# TODO: figure a way to match more tweeter accounts to congress members (fuzzy matching)
# for instance, to use the amatch function
# deal with people who have more than one tweeter account

# merge data
setkey(dat, screen_name)
setkey(dmeta, screen_name)

dat <- dmeta[dat]
dat <- dat[!is.na(name)] # for now remove unmatched cases
nrow(dat) / 58778 # 70% of tweets

##################################
#+ clean tweets before analyzing
##################################

dat[, otext := text]

# remove RTs
dat[, rts := ifelse(grepl("^RT\\s", text), 1, 0)]
table(dat$rts, useNA = "ifany")
dat <- dat[rts == 0]
nrow(dat)

# some cleaning
dat[, text := gsub("&amp", "and", text)]
dat[, text := gsub("@\\w+", "", text)]
dat[, text := gsub("(f|ht)tp(s?)://\\S+", "", text, perl = TRUE)]
dat[, text := gsub("^\\s+|\\s+$", "", text)]
dat[, text := str_replace_all(text, "[[:punct:]]", " ")]
dat[, text := str_replace_all(text, "[[:digit:]]", " ")]
# dat[, text := iconv(text, "latin1", "UTF-8",sub='')]
dat[, text := tolower(text)]
dat[, text := gsub("^ *|(?<= ) | *$", "", text, perl = TRUE)]

dat <- dat[text != ""]
nrow(dat)

rows <- sample(1:nrow(dat), 10)
dat[rows, text, otext][1]

#+ identify language
dat[, lang := textcat(text, p = ECIMCI_profiles)]
table(dat$lang, useNA = "ifany")

# select only english tweets for now
# the textcat function is not always precise
dat <- dat[lang == "en"]
nrow(dat)

# change format of date
dat[, day := day(time)]
dat[, month := month(time)]
dat[, year := year(time)]
dat[, ymd := paste(year, month, day, sep = "-")]

table(dat$ymd, useNA = "ifany")

#######################
#+ explore polarity
#######################

tables() # 25 MB
pol <- polarity(dat$text)

dat[, polarity := pol$all$polarity]
dat[, zpolarity := scale(pol$all$polarity)]

summary(dat$polarity)
summary(dat$zpolarity)


png(file = paste0("/Users/sdaza/Google Drive/github/i_proposal/figures/" , "hist_polarity.png"),width=400, height=350)
ggplot(dat[party != "I"], aes(x = polarity, group = party, fill = party)) + theme_minimal() +
 geom_histogram(aes(y=..count../sum(..count..)), position = "identity",  binwidth = 0.25, alpha = 0.5) +
 labs(y = "Proportion", x = "Raw Polarity", title = "Histogram Raw Polarity Score by Party")
dev.off()

png(file = paste0("/Users/sdaza/Google Drive/github/i_proposal/figures/" , "hist_zpolarity.png"),width=400, height=350)
ggplot(dat[party != "I"], aes(x = zpolarity, group = party, fill = party)) + theme_minimal() +
 geom_histogram(aes(y=..count../sum(..count..)), position = "identity",  binwidth = 0.60, alpha = 0.5) +
 labs(y = "Proportion", x = "Z Polarity", title = "Histogram Standardized Polarity Score by Party")
dev.off()

dat[party != "I", .(avg_polarity = Mean(polarity)), party]
dat[party != "I", .(avg_zpolarity = Mean(zpolarity)), party]

# polarity by day
agg <- dat[party != "I", .(polarity = Mean(polarity), zpolarity = Mean(zpolarity)), .(party, ymd)]

png(file = paste0("/Users/sdaza/Google Drive/github/i_proposal/figures/" , "trend_polarity.png"), width = 400, height = 350)
ggplot(agg, aes(x = ymd, y = polarity, group = party, colour = party, fill = party)) + theme_minimal() +
      geom_line() +  geom_point() +
      theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
      labs(x = "", y = "Raw Polarization", title = "Polarization Score by Day and Party")
dev.off()

png(file = paste0("/Users/sdaza/Google Drive/github/i_proposal/figures/" , "trend_zpolarity.png"), width = 400, height = 350)
ggplot(agg, aes(x = ymd, y = zpolarity, group = party, colour = party, fill = party)) + theme_minimal() +
      geom_line() +  geom_point() +
      theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
      labs(x = "", y = "Z Polarization", title = "Standardized Polarization Score by Day and Party")
dev.off()

# some checks!
dat[polarity < 0 & party == "D" & ymd == "2017-6-26", .(text, polarity)][2]

test <- dat[ymd == "2017-6-26" & polarity < 0, .(party, text)]
test[sample(1:nrow(test), 10), text]
######################
#+ explore tweets
######################

createWordCloud <- function(dat) {

neg.tweets <- dat[zpolarity > 0, text]
pos.tweets <- dat[zpolarity < 0, text]
pos.terms <- paste(pos.tweets, collapse = " ")
neg.terms <- paste(neg.tweets, collapse = " ")
all.terms <- c(pos.terms, neg.terms)
all.corpus <- VCorpus(VectorSource(all.terms))

all.tdm <- TermDocumentMatrix(all.corpus,
                              control = list(weighting = weightTfIdf,
                                             removePunctuation = TRUE,
                                             stopwords = stopwords(kind = "en")))
all.tdm.m <- as.matrix(all.tdm)
colnames(all.tdm.m) <- c("negative", "positive")
comparison.cloud(all.tdm.m, max.words = 100, colors = c("darkred", "darkgreen"))

}

png(file = paste0("/Users/sdaza/Google Drive/github/i_proposal/figures/" , "words_r.png"), width = 400, height = 350)
createWordCloud(dat[party == "R"])
dev.off()

png(file = paste0("/Users/sdaza/Google Drive/github/i_proposal/figures/" , "words_d.png"), width = 400, height = 350)
createWordCloud(dat[party == "D"])
dev.off()

agg[ymd == "2017-6-25"]
agg[ymd == "2017-6-26"]
agg[ymd == "2017-6-27"]

createWordCloud(dat[party == "D" & ymd == "2017-6-26"])
createWordCloud(dat[party == "R" & ymd == "2017-6-26"])

####################
# end
###################

