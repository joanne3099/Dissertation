#Read in data
# MAUS output
JMAUS  <- read.csv("~/Linguistics/MAUS_Python/MAUS_Python04_05_2021.csv", header = T, stringsAsFactors = FALSE, na.strings=c("NA",""))

#SA segmentation of continuant compounds
SAcnt <- read.csv("~/Linguistics/MAUS_Python/correctedBBHPdata_14-09-19.csv", header = T, stringsAsFactors = FALSE, na.strings=c("NA",""))

# Check variable names in MAUS output
names(JMAUS)
# [1] "ItemID"  unique item ID     
# [2] "ItemDur" duration of compound     
# [3] "Sentence"     
# [4] "SentenceDur"  
# [5] "Compound1"    N1
# [6] "Compound1Dur" duration of N1
# [7] "Compound2"    N2
# [8] "Compound2Dur" duration of N2
# [9] "CompoundStart"
# [10] "CompoundEnd"  
# [11] "ConFinal"   ipa  
# [12] "ConFinalDur"  
# [13] "ConInitial"  ipa 
# [14] "ConInitialDur"
# [15] "ConDur"   total duration of both boundary consonants   
# [16] "PrecSeg"      
# [17] "PrecSegDur"   
# [18] "FolSeg"       
# [19] "FolSegDur"    
# [20] "SegNum"   

# look at first six rows
head(JMAUS[,1:20])

# We want to label the column so we know where the data came from
names(JMAUS)[names(JMAUS)=="ConDur"] <- "ConDurMAUS"

# Check variable names in SA output
names(SAcnt)

# [2] "n1"                            
# [3] "experimentalTokenCount"        
# [4] "nnHeadLemma"                   
# [5] "n2Lemma"                       
# [6] "transitionVowelN1.C"           
# [7] "FilenameID"                    
# [8] "Sentence"                      
# [9] "ItemDur"                       
# [10] "SyllNumAnnotated"              
# [11] "SegNum"                        
# [12] "Consonant"                     
# [13] "ConsonantDur"                  
# [14] "PrecSeg"                       
# [15] "PrecSegVC"                     
# [16] "PrecSegDur"                    
# [17] "FollSeg"                       
# [18] "FollSegVC"                     
# [19] "FollSegDur"                    
# [20] "PrePauseDur"                   
# [21] "PostPauseDur"                  
# [22] "SentenceDur"                   
# [23] "LocSpeech"                     
# [24] "Pause"                         
# [25] "PauseDur"                      
# [26] "SecondConsonant"               
# [27] "SecondConsonantDur"            
# [28] "Filename"                      
# [29] "lType"                         
# [30] "FilenameReduced"               
# [31] "item"                          
# [32] "participant"                   
# [33] "presentationOrderAllSentences" 
# [34] "presentationOrderCompoundsOnly"
# [35] "sentenceID"                    
# [36] "sentence"                      
# [37] "sentenceFinal"                 
# [38] "n2"                            
# [39] "soundFile"                     
# [40] "soundFileID"                   
# [41] "sound"                         
# [42] "geminate"                      
# [43] "type"                          
# [44] "class"                         
# [45] "expectedStress"                
# [46] "syllsN1"                       
# [47] "syllsN2"                       
# [48] "precedingSyllStrength"         
# [49] "vowelN1"                       
# [50] "vowelN2"                       
# [51] "SecondConsonantDurWoNA"        
# [52] "ConsonantDurTotal"             
# [106] "filename"                      
# [107] "annotator"   

# Ger rid of some columns we don't need
SAcnt <- SAcnt[,c(1:52,106:107)]

# Are ConsonantDurTotal and ConsonantDur the same thing?
identical(SAcnt$ConsonantDurTotal, SAcnt$ConsonantDur)
# [1] TRUE
# Yes they are

# We want to label the column so we know where the data came from
names(SAcnt)[names(SAcnt)=="ConsonantDur"] <- "ConDurSA"

# We need to be able to match items in the two files
# Look at SA "Filename"
# First six lines
head(SAcnt$FilenameID)

# Check structure
str(SAcnt$FilenameID)

# Check for duplicates

length(unique(SAcnt$FilenameID))
length(levels(as.factor(SAcnt$FilenameID)))
dim(SAcnt)
# No duplicates

# they need the same name so we can compare
names(SAcnt)[names(SAcnt)=="FilenameID"] <- "ItemID"

# Same thing for Maus data - ItemID
head(JMAUS$ItemID)
# Need to get rid of ".TextGrid"
JMAUS$ItemID <- gsub(".TextGrid","",JMAUS$ItemID)
head(JMAUS$ItemID)
# good

# Check structure - no longer has that extension
str(JMAUS$ItemID)

# Check for duplicates
length(unique(JMAUS$ItemID))
length(levels(as.factor(JMAUS$ItemID)))
dim(JMAUS)
# no duplicates

# merge datasets
data <- merge(SAcnt, JMAUS, by="ItemID")
dim(data)

# check for correlation between measurements
cor.test(data$ConDurSA,data$ConDurMAUS)

# inspect a scatter plot
dev.off()
plot(data$ConDurSA,data$ConDurMAUS)

# It looks as though there are outliers especially in the MAUS output
# Lets' trim the data, i.e. remove the outliers

densityplot(data$ConDurMAUS)
plot(sort(data$ConDurMAUS))
abline(0.4, 0)
data1 <- data[data$ConDurMAUS < 0.4, ]
dim(data1)
dim(data)
6/2063
# 0.002908386
# We lose less than 1% of the data

# Re-check the correlation
cor.test(data1$ConDurSA,data1$ConDurMAUS)
dev.off()
plot(data1$ConDurSA,data1$ConDurMAUS)
# Yes, it's stronger now

# How do the different consonants vary?

# How many lines do we have for each consonant?
table(data1$Consonant, useNA="always")
#   l   m   n   s 
# 507 477 471 594 

# Take m for example
str(data1$Consonant)
m <- data1[which(data1$Consonant=="m"),]
dim(m)
# [1] 477 145
#0.8932498 

# drawing a line of best fit lm = linear model
#Coefficients:
#(Intercept)  m$ConDurSA  
#0.006414     0.987920  
# lm(m$ConDurMAUS ~ m$ConDurSA)
# abline(0.006414, 0.987920)
# abline(lm(m$ConDurMAUS ~ m$ConDurSA))

cor.test(m$ConDurSA,m$ConDurMAUS)
dev.off()
plot(m$ConDurSA,m$ConDurMAUS)
#       cor 
# 0.8932498 
l <- data1[which(data1$Consonant=="l"),]
dim(l)
# [1] 507 145
# looking at the table of compounds with l. 
data1[which(data1$Consonant=="l"),]

cor.test(l$ConDurSA,l$ConDurMAUS)
dev.off()
plot(l$ConDurSA,l$ConDurMAUS)
# 0.5371978 
# lower correlation which may be because l is harder to segment manually.
# it looks like a vowel
# is it because of the nature of the consonants? 
# line of best fit
# lm(l$ConDurMAU ~ l$ConDurSA)
# #0.05425    0.80538  
# abline(0.05425, 0.80538)
# abline(lm(l$ConDurMAUS ~ l$ConDurSA))

# n
n <- data1[which(data1$Consonant=="n"),]
dim(n)
#[1] 471 145
cor.test(n$ConDurSA, n$ConDurMAUS)
dev.off()
plot(n$ConDurSA, n$ConDurMAUS)
#0.8669693
# higher correlation 
# s 
s <- data1[which(data1$Consonant=="s"),]
dim(s)
#[1] 594 145
cor.test(s$ConDurSA, s$ConDurMAUS)
dev.off()
plot(s$ConDurSA, s$ConDurMAUS)
# really high correlation! 0.9266539 
# best correlation, its a longer sound, a fricative and more clearer for maus to segment as well as humans
# L is has the worse correlation most likely because of the nature of the consonant. On spectrograms it can look like an L.

# Let's look at total compound duration
# change names for identity
names(data1)[names(data1)=="ItemDur.x"] <- "CompoundDurSA"
names(data1)[names(data1)=="ItemDur.y"] <- "CompoundDurMAUS"

cor.test(data1$CompoundDurSA,data1$CompoundDurMAUS)
dev.off()
plot(data1$CompoundDurSA,data1$CompoundDurMAUS)
# cor : 0.902007 
# very linear
# really high correlation with sentences in the CNT data.
#seems that maus had a better time with the continuants
# there's no obstruction with these consonants in comparisons to plosives where there is a build up & release
# continuants allow for continuous air flow. 


# Lastly sentence duration 
names(data1)[names(data1)=="SentenceDur.x"] <- "SentenceDurSA"
names(data1)[names(data1)=="SentenceDur.y"] <- "SentenceDurMAUS"

cor.test(data1$SentenceDurSA,data1$SentenceDurMAUS)
dev.off()
plot(data1$SentenceDurSA,data1$SentenceDurMAUS)
# 0.8185938 
# also high correlation which would be expected with this data
