# ------------------------------------------------------------------- Installing modules -------------------------------------------------------------------
# This script extracts durations from all tiers of Mel's compound files

# ------------------------------------------------------------------- Installing modules -------------------------------------------------------------------
import shutil
import os, os.path
import fnmatch
import tgt
import csv
import datetime

# -------------------------------------------------------------------- Getting the date -------------------------------------------------------------------

today="{:%d_%m_%Y}".format(datetime.datetime.now())

# -------------------------------------------------------------------- Specifying the paths and directories -----------------------------------------------

TextGridPathWords = r"C:\Users\curly\Documents\Linguistics\completed_plosive_geminate_textgrids"
TextGridFilter = "*.TextGrid"
OutputPath = r"C:\Users\curly\Documents\Linguistics\completed_plosive_geminate_textgrids"
TemplatePath = r"C:\Users\curly\Documents\Linguistics\completed_plosive_geminate_textgrids\template_compound_duration.csv"

# -------------------------------------------------------------------- Preparing the necessary information -----------------------------------------------

# Let's first take care of the words: We make a list of all the textgrids which have to be analyzed

FileWalk = os.walk (TextGridPathWords)
FileList = []
for SourcePath, Folders, Files in FileWalk:
    for CurrentFile in Files:
        if fnmatch.fnmatch (CurrentFile, TextGridFilter):
            FileList.append ((SourcePath, CurrentFile))

print("There are " + str(len(FileList)) + " textgrids to be analyzed")

TierNames = ["sentence", "Compound", "Syllables", "Segments", "Detail", "Closures", "Releases"]
Tiers = {}

def ReadTiers (TextGrid, TierNames):
    D = {}
    for CurrentTierName in TierNames:
        try:
            D [CurrentTierName] = TextGrid.get_tier_by_name (CurrentTierName)
        except ValueError as e:
            print ("TextGrid does not contain a tier '%s'.") % (CurrentTierName)
            raise e

BoundaryAlignmentAccuracy = 0.01

# ------------------------------------------------------------------- Creating the output file and specifying what to read ---------------------------------

with open(OutputPath + str(today) + '.csv', 'w', newline='') as csvfile:
    OutputFile= csv.writer(csvfile, delimiter=',')
                            
    for Headers in csv.reader(open(TemplatePath, "r"), delimiter=","):
        OutputFile.writerow(Headers)
        break
   
    for (Path, Filename) in FileList:
        try:
                        CurrentTextGrid = tgt.read_textgrid (os.path.join(Path, Filename))
                        
                        # print(CurrentTextGrid)
                        ItemID=str(Filename)

                        SentenceTier=CurrentTextGrid.get_tier_by_name("sentence")
                        Sentence=SentenceTier.intervals[0].text
                        SentenceDur=SentenceTier.intervals[0].duration()

                        CompoundTier=CurrentTextGrid.get_tier_by_name("Compound")
                        Compound1=CompoundTier.intervals[0].text
                        Compound1Dur=CompoundTier.intervals[0].duration()
                        Compound2=CompoundTier.intervals[1].text
                        Compound2Dur=CompoundTier.intervals[1].duration()

                        SyllableTier=CurrentTextGrid.get_tier_by_name("Syllables")
                        SyllableNum=len(SyllableTier.intervals)
                        Syl1=SyllableTier.intervals[0].text
                        Syl1Dur=SyllableTier.intervals[0].duration()
                        Syl2=SyllableTier.intervals[1].text
                        Syl2Dur=SyllableTier.intervals[1].duration()

                        if SyllableNum > 2:
                            Syl3=SyllableTier.intervals[2].text
                            Syl3Dur=SyllableTier.intervals[2].duration()
                        else:
                            Syl3="NA"
                            Syl3Dur=0

                        if SyllableNum > 3:
                            Syl4=SyllableTier.intervals[3].text
                            Syl4Dur=SyllableTier.intervals[3].duration()
                        else:
                            Syl4="NA"
                            Syl4Dur=0

                        if SyllableNum > 4:
                            Syl5=SyllableTier.intervals[4].text
                            Syl5Dur=SyllableTier.intervals[4].duration()
                        else:
                            Syl5="NA"
                            Syl5Dur=0

                        if SyllableNum > 5:
                            Syl6=SyllableTier.intervals[5].text
                            Syl6Dur=SyllableTier.intervals[5].duration()
                        else:
                            Syl6="NA"
                            Syl6Dur=0
                        
                        if SyllableNum > 6:
                            Syl7=SyllableTier.intervals[6].text
                            Syl7Dur=SyllableTier.intervals[6].duration()
                        else:
                            Syl7="NA"
                            Syl7Dur=0

                        if SyllableNum > 7:
                            Syl8=SyllableTier.intervals[7].text
                            Syl8Dur=SyllableTier.intervals[7].duration()
                        else:
                            Syl8="NA"
                            Syl8Dur=0

                        SegmentTier=CurrentTextGrid.get_tier_by_name("Segments")
                        SegmentNum=len(SegmentTier.intervals)
                        Seg1=SegmentTier.intervals[0].text
                        Seg1Dur=SegmentTier.intervals[0].duration()
                        Seg2=SegmentTier.intervals[1].text
                        Seg2Dur=SegmentTier.intervals[1].duration()

                        if SegmentNum > 2:
                            Seg3=SegmentTier.intervals[2].text
                            Seg3Dur=SegmentTier.intervals[2].duration()
                        else:
                            Seg3="NA"
                            Seg3Dur=0

                        if SegmentNum > 3:
                            Seg4=SegmentTier.intervals[3].text
                            Seg4Dur=SegmentTier.intervals[3].duration()
                        else:
                            Seg4="NA"
                            Seg4Dur=0

                        if SegmentNum > 4:
                            Seg5=SegmentTier.intervals[4].text
                            Seg5Dur=SegmentTier.intervals[4].duration()
                        else:
                            Seg5="NA"
                            Seg5Dur=0

                        DetailTier=CurrentTextGrid.get_tier_by_name("Detail")
                        DetailNum=len(DetailTier.intervals)
                        Detail1=DetailTier.intervals[0].text
                        Detail1Dur=DetailTier.intervals[0].duration()

                        if DetailNum > 1:
                            Detail2 = DetailTier.intervals[1].text
                            Detail2Dur=DetailTier.intervals[1].duration()

                        else:
                            Detail2="NA"
                            Detail2Dur=0

                        if DetailNum > 2:
                            Detail3=DetailTier.intervals[2].text
                            Detail3Dur=DetailTier.intervals[2].duration()
                        else:
                            Detail3="NA"
                            Detail3Dur=0

                        if DetailNum > 3:
                            Detail4=DetailTier.intervals[3].text
                            Detail4Dur=DetailTier.intervals[3].duration()
                        else:
                            Detail4="NA"
                            Detail4Dur=0

                        if DetailNum > 4:
                            Detail5=DetailTier.intervals[4].text
                            Detail5Dur=DetailTier.intervals[4].duration()
                        else:
                            Detail5="NA"
                            Detail5Dur=0

                        OutputFile.writerow ([
                        # print([   
                            Filename,                            
                            Sentence, 
                            SentenceDur,
                            Compound1,
                            Compound1Dur,
                            Compound2,
                            Compound2Dur,
                            Syl1,
                            Syl1Dur,
                            Syl2,
                            Syl2Dur,
                            Syl3,
                            Syl3Dur,
                            Syl4,
                            Syl4Dur,
                            Syl5,
                            Syl5Dur,
                            Syl6,
                            Syl6Dur,
                            Syl7,
                            Syl7Dur,
                            Syl8,
                            Syl8Dur,
                            Seg1,
                            Seg1Dur,
                            Seg2,
                            Seg2Dur,
                            Seg3,
                            Seg3Dur,
                            Seg4,
                            Seg4Dur,
                            Seg5,
                            Seg5Dur,
                            Detail1,
                            Detail1Dur, 
                            Detail2,
                            Detail2Dur,
                            Detail3,
                            Detail3Dur,
                            Detail4,
                            Detail4Dur,
                            Detail5,
                            Detail5Dur
                            ])

        except Exception as e:
                     print (e)
                     print((Filename + " has a problem"))
                     # raise e
