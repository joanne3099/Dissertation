# Maus outputs 
JMAUS<- read.csv("~/Linguistics/MAUS_Python/MAUS_Python04_05_2021.csv", header = T, stringsAsFactors = FALSE, na.strings=c("NA",""))
#Student assisted data - Plosives
SApl <-read.csv("~/Linguistics/MAUS_Python/completed_plosive_geminate_textgrids28_04_2021.csv", header = T, stringsAsFactors = FALSE, na.strings=c("NA",""))
# all file names
# The encoding for this file is different
files <- read.csv("~/Linguistics/MAUS_Python/all_geminate_wav_files_list_excel_v8.csv",  fileEncoding="UTF-8-BOM", header= T)

head(files)
# get rid of empty columns
library(janitor)
files <- remove_empty(files, which = c("rows","cols"))
head(files)



JMAUS <- remove_empty(JMAUS, which = c("rows","cols"))
head(JMAUS)



SApl <- remove_empty(SApl, which = c("rows","cols"))
head(SApl)



head(JMAUS$ItemID)
# [1] "10_102_cabinet_table.TextGrid"
# [2] "10_104_back_corner.TextGrid"  



head(SApl$ItemID)
# ItemID
# 1 all_100_Man_22_75.TextGrid
# 2 all_103_Man_10_63.TextGrid



head(files)



names(SApl)[names(SApl)=="ItemID"] <- "original_wav_names"



names(files)
head(files)


head(SApl$original_wav_names)



# Need to get rid of "TextGrid" in SApl
SApl$original_wav_names <- gsub(".TextGrid","",SApl$original_wav_names)

SApl2<-merge(SApl, files, by = "original_wav_names")
names(SApl2)
# rename SApl2$updated_wav_names as SApl2$ItemID
head(SApl2$original_wav_names)





str(SApl2$updated_wav_names)
head(SApl2$updated_wav_names)
#[1] "15_46_traffic_policy" "2_36_benefit_agency" 
names(SApl2)[names(SApl2)=="updated_wav_names"] <-  "ItemID"



head(JMAUS$ItemID)
head(SApl2$ItemID)



# Need to get rid of ".TextGrid" again in JMAUS
JMAUS$ItemID <- gsub(".TextGrid","",JMAUS$ItemID)
head(JMAUS$ItemID)

#--------------------DATA CLEAN UP----------------------------#
# Before the merge we need to sort out the consonants.
# SAPL becomes SAPL2 because we had to change the original file names 

# identify which segments have the consonants in SA data
# remove suspect lines so that you end up with only the following values:
# segment1: v1
# segment2: c
# segment3: v2 or c
# segment4: v2 or NA
# segment5: NA

# Use NA to see the missing values 
table(SApl2$Seg1, useNA="always")
# b    d   v1   v2 <NA> 
# 1    2 2607   26    0 
table(SApl2$Seg2)
#  ?  ?d  ?p   b  b2  bb   d  d1  d2  db  dd  dk  dp  dt   k  k1  kb  kk  kp  kt   p  p1  p2  pb  pk  pp   t  t1  tb  td  tk  tp  tt  v2 
# 155   1   1 210   1 138 402   1   2  29 129   5  16  45 397   4  16  91  25   9 285   1   1  55  10 102 237   1  43  40  28  52 102   2 
table(SApl2$Seg3)
#    ?    b   b2    d   dp    k   k2    p   p2   rp    t   t2   v1   v2 
# 105  150    1   71    1  258    1  161    3    1  160    1    6 1707 
table(SApl2$Seg4)
#  ?   b  c2   d   k   p   t  v1  v2 
# 1   6   1   1   7   2  10   2 877 
table(SApl2$Seg5)
# v2 
# 27

# SEGMENT 1 : v1
# looks at the column/row where b is 
SApl2[which(SApl2$Seg1=="b"),]
# remove b, d, v2, as they are not v1
SAplclean0 <- SApl2[which(SApl2$Seg1!="b"&SApl2$Seg1!="d"&SApl2$Seg1!="v2"),]
dim(SApl2)
#[1] 2636   48
2636-1-2-26
dim(SAplclean0)
# [1] 2607    48
table(SAplclean0$Seg2,useNA="always")
# freq(b) = 210

# SEGMENT 2 : c
SAplclean0[which(SAplclean0$Seg2=="b2"),]
SAplclean0[which(SAplclean0$Seg2=="d1"),]
SAplclean0[which(SAplclean0$Seg2=="d2"),]
SAplclean0[which(SAplclean0$Seg2=="p1"),]
SAplclean0[which(SAplclean0$Seg2=="p2"),]
SAplclean0[which(SAplclean0$Seg2=="t1"),]
# remove the numbers and change to just letters
SAplclean0$Seg2[which(SAplclean0$Seg2=="b2")] <- "b"
table(SAplclean0$Seg2)
# freq(b) = 211 (b2) = 0 
SAplclean0[which(SAplclean0$Seg2=="b"),]
dim(SAplclean0)
table(SAplclean0$Seg2)
SAplclean0$Seg2[which(SAplclean0$Seg2=="d1")] <- "d"
table(SAplclean0$Seg2)
SAplclean0$Seg2[which(SAplclean0$Seg2=="d2")] <- "d"
SAplclean0$Seg2[which(SAplclean0$Seg2=="p1")] <- "p"
SAplclean0$Seg2[which(SAplclean0$Seg2=="p2")] <- "p"
SAplclean0$Seg2[which(SAplclean0$Seg2=="t1")] <- "t"

# check the updated segments.
table(SAplclean0$Seg2, useNA = "always")
# good.
#  ?  ?d  ?p   b  bb   d  db  dd  dk  dp  dt   k  k1  kb  kk  kp  kt   p  pb  pk  pp   t  tb  td  tk  tp  tt  v2 
# 149   1   1 211 137 402  29 128   5  16  45 391   4  16  90  24   9 282  55  10 101 236  43  39  28  52 102   1 

# Only should be consonants in seg 2, remove v2.
SAplclean1 <- SAplclean0[which(SAplclean0$Seg2!="v2"),]
table(SAplclean1$Seg2)

# ?  ?d  ?p   b  bb   d  db  dd  dk  dp  dt   k  k1  kb  kk  kp  kt   p  pb  pk  pp   t  tb  td  tk  tp  tt 
# 149   1   1 211 137 402  29 128   5  16  45 391   4  16  90  24   9 282  55  10 101 236  43  39  28  52 102 
dim(SAplclean1)
# 2606   48
149 +  1 + 1 + 211 + 137 + 402 + 29 + 128 +  5  + 16 + 45 + 391  + 4  + 16  + 90  + 24  + 9 + 282 +  55 +  10 + 101 + 236  + 43  + 39 + 28 + 52 + 102
# 2606.

#SEGMENT 3: v2 or c
table(SAplclean1$Seg3,useNA="always")
# ?    b   b2    d   dp    k   k2    p   p2   rp    t   t2   v1   v2 <NA> 
#103  148    1   69    1  254    1  158    3    1  159    1   6  1693    8 

SAplclean1[is.na(SAplclean1$Seg3),] # the rows with NA look OK
str(SAplclean1$Seg3) # check what type it is 
SAplclean1$Seg3 <- ifelse(is.na(SAplclean1$Seg3),"missing",SAplclean1$Seg3)

# but we don't want v1
SAplclean2 <- SAplclean1[SAplclean1$Seg3!="v1",]
dim(SAplclean2)
# [1] 2600   48
# good.

head(SAplclean2)
table(SAplclean2$Seg3,useNA="always")

# for some reason i can't remove the wrong segments but its fine, as not looking at these ones.
# SEGMENT 4: v2 or NA
table(SAplclean2$Seg4, useNA = "always")
# ?    b    d    k    p    t   v1   v2 <NA> 
# 1    6    1    7    2   10    2  864 1707 
SAplclean2[which(SAplclean2$Seg4=="v1"),]
table(SAplclean2$Seg4, useNA = "always")


# SEGMENT 5: NA
table(SAplclean2$Seg5, useNA = "always")
# v2 <NA> 
# 27 2573 

dim(SAplclean2)
# [1] 2600   48

# Eventually, you end up with:
# segment1: v1
# segment2: c
# segment3: v2 or c or "missing"
# segment4: v2 or NA
# segment5: NA

# Columns are renamed
SAplclean2$consDur2 <- ifelse((SAplclean2$Seg3=="v2"|SAplclean2$Seg3=="missing"),0,SAplclean2$Seg3Dur)
View(SAplclean2)

head(SAplclean2[,c("Seg3","Seg3Dur","consDur2")],20)

names(SAplclean2)[names(SAplclean2)=="Seg2Dur"] <- "consDur1"

head(SAplclean2[,c("Seg2", "consDur1")], 20)

# add together = total duration of the boundary consonants 
# and make a new column called ConDurSApl.
SAplclean2$ConDurSApl<-SAplclean2$consDur1 + SAplclean2$consDur2

# checking to see if it's done
head(SAplclean2$ConDurSApl)
head(SAplclean2[,c("Seg2", "consDur1","Seg3","Seg3Dur","consDur2", "ConDurSApl")], 20)
#looks good.


# Change the column name here so we can identify it in the correlations.
names(JMAUS)[names(JMAUS)=="ConDur"] <- "ConDurMAUS"

# merge data sets
PL_MAUS_data1 <- merge(SAplclean2, JMAUS, by="ItemID")
dim(PL_MAUS_data1)
# [1] [1] 2599  135
# check for correlation between measurements
cor.test(PL_MAUS_data1$ConDurSApl,PL_MAUS_data1$ConDurMAUS)
# 0.2861714
# inspect a scatter plot
dev.off()
plot(PL_MAUS_data1$ConDurSApl,PL_MAUS_data1$ConDurMAUS)
# cor : 0.2861714
# t = 15.194, df = 2588, p-value < 2.2e-16
# The relationship is not very linear
# Maus has a lot of the same values.
head(PL_MAUS_data1[,c("Seg2", "ConDurSApl", "ConDurMAUS")], 8)

# How do the different consonants vary?

# How many lines do we have for each consonant?
table(PL_MAUS_data1$Seg2, useNA= "always")
# ?   ?d   ?p    b   bb    d   db   dd   dk   dp   dt    k   k1   kb   kk   kp   kt    p   pb   pk   pp    t   tb   td   tk   tp   tt 
# 149    1    1  209  137  402   29  128    5   16   45  389    4   16   90   24    9  280   55   10  100  236   43   39   28   52  102 
# Take k for example
str(PL_MAUS_data1$Seg2)
k <- PL_MAUS_data1[which(PL_MAUS_data1$Seg2=="k"),]
dim(k)

cor.test(k$ConDurSApl,k$ConDurMAUS)
dev.off()
plot(k$ConDurSApl,k$ConDurMAUS)
# 0.3859063 
# low correlation 
# there's a lot of outliers and maus has lot of the same values, it's just all over the place.
head(PL_MAUS_data1[,c("Seg2" , "Seg3", "ConDurSApl", "ConDurMAUS")], 20)

# looking at p 
p <- PL_MAUS_data1[which(PL_MAUS_data1$Seg2=="p"),]
dim(p)
cor.test(p$ConDurSApl,p$ConDurMAUS)
dev.off()
plot(p$ConDurSApl,p$ConDurMAUS)
# 0.6830452 
# correlation with p is higher but because many of the values are the same, the graph has this line effect,
# this is probably because it has a longer sound
# unvoiced plosive but a higher correlation. 

# drawing a line of best fit lm = linear model
lm(p$ConDurMAUS ~ p$ConDurSA)
abline(0.6150710, 0.7409413)
abline(lm(p$ConDurMAUS ~ p$ConDurSA))
# there's still a positive correlation, as the line of best fit can be drawn. 
dev.off()

# Looking at d

d <- PL_MAUS_data1[which(PL_MAUS_data1$Seg2=="d"),]
dim(d)
cor.test(d$ConDurSApl,d$ConDurMAUS)
plot(d$ConDurSApl,d$ConDurMAUS)
# 0.5177005 
# the graphs look almost similar...
# voiced

# B
b <- PL_MAUS_data1[which(PL_MAUS_data1$Seg2=="b"),]
dim(b)
cor.test(b$ConDurSApl,b$ConDurMAUS)
dev.off()
plot(b$ConDurSApl,b$ConDurMAUS)
# cor 0.7254065 
# highest correlation
# voiced plosive

# GLOTTAL STOPS 
glottal <- PL_MAUS_data1[which(PL_MAUS_data1$Seg2=="?"),]
dim(glottal)
cor.test(glottal$ConDurSApl,glottal$ConDurMAUS)
dev.off()
plot(glottal$ConDurSApl,glottal$ConDurMAUS)
# cor. 0.197271 
# unvoiced
# as expected correlation is really low
# where the student assistants thought there are glottal stops, maus may not have put any
# thus the graph does not have those darker areas like the others
# it still has a similar structure though. 

# T
t <- PL_MAUS_data1[which(PL_MAUS_data1$Seg2=="t"),]
dim(t)
cor.test(t$ConDurSApl,t$ConDurMAUS)
dev.off()
plot(t$ConDurSApl,t$ConDurMAUS)
# 0.2328384 
# another low correlation.
# unvoiced plosive, difficult to hear? 

# COMPOUND WORDS 
# maybe maus works better with longer duration

# renaming them, so easier to tell which is which in the plot. 
names(PL_MAUS_data1)[names(PL_MAUS_data1)=="Compound1Dur.x"] <- "Compound1DurSA"
names(PL_MAUS_data1)[names(PL_MAUS_data1)=="Compound2Dur.x"] <- "Compound2DurSA"
names(PL_MAUS_data1)[names(PL_MAUS_data1)=="Compound1Dur.y"] <- "Compound1DurMAUS"
names(PL_MAUS_data1)[names(PL_MAUS_data1)=="Compound2Dur.y"] <- "Compound2DurMAUS"
# COMPOUND 1

cor.test(PL_MAUS_data1$Compound1DurSA,PL_MAUS_data1$Compound1DurMAUS)
dev.off()
plot(PL_MAUS_data1$Compound1DurSA,PL_MAUS_data1$Compound1DurMAUS)

# x = human annotated 
# y = maus annotated
head(PL_MAUS_data1[,c("Compound1.x" , "Compound1DurSA", "Compound1DurMAUS")], 20)

# cor: 0.3652228 
# correlation is just low, and some words maus thinks are 1 second long.

#   Compound1.x Compound1DurSA Compound1DurMAUS
#1       rabbit      0.3318703             0.24
#2          cot      0.2342593             0.06
#3         club      0.4359968             0.12
#4      cabinet      0.3898129             0.29
#5         site      0.2938843             1.41
#6        strip      0.5401965             1.97

# COMPOUND 2.
cor.test(PL_MAUS_data1$Compound2DurSA,PL_MAUS_data1$Compound2DurMAUS)
dev.off()
plot(PL_MAUS_data1$Compound2DurSA,PL_MAUS_data1$Compound2DurMAUS)
# cor: 0.5374629 
# higher correlation with the second compound word.
head(PL_MAUS_data1[,c("Compound2.x" , "Compound2DurSA", "Compound2DurMAUS")], 20)
head(PL_MAUS_data1[,c("Compound1.x", "Compound2.x","Compound1DurSA", "Compound2DurSA","Compound1DurMAUS", "Compound2DurMAUS")], 6)

# TOTAL COMPOUND. add them together as this isnt in the SA data 
PL_MAUS_data1$ItemDurSA<-PL_MAUS_data1$Compound1DurSA + PL_MAUS_data1$Compound2DurSA

# Change MAUS column name so more identifiable 
names(PL_MAUS_data1)[names(PL_MAUS_data1)=="ItemDur"] <- "ItemDurMAUS"

# look at them in scatter plot.

cor.test(PL_MAUS_data1$ItemDurSA,PL_MAUS_data1$ItemDurMAUS)
dev.off()
plot(PL_MAUS_data1$ItemDurSA,PL_MAUS_data1$ItemDurMAUS)
# cor 0.5955029 
#maus seems to have longer total duration because of its inaccuracies 

# Let's look at sentence duration lastly. 

names(PL_MAUS_data1)[names(PL_MAUS_data1)=="SentenceDur.x"] <- "SentenceDurSA"

names(PL_MAUS_data1)[names(PL_MAUS_data1)=="SentenceDur.y"] <- "SentenceDurMAUS"

cor.test(PL_MAUS_data1$SentenceDurSA,PL_MAUS_data1$SentenceDurMAUS)
dev.off()
plot(PL_MAUS_data1$SentenceDurSA,PL_MAUS_data1$SentenceDurMAUS)
# cor: 0.7228462 
# much higher correlation with sentence duration as expected
# maus is better with longer durations with its 10ms segment boundary.
# some sentences are considered four seconds long which is just terribly wrong. 

head(PL_MAUS_data1[,c("Sentence.x" , "SentenceDurSA", "SentenceDurMAUS")], 20)
# a lot of the durations of the words in the sentence are multiples of 10 and are the same. 