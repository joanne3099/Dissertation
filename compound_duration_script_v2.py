# This script extracts durations from the forced-aligned files.

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

TextGridPathWords = r"C:\Users\curly\Documents\Linguistics\MAUS OUTPUTS_5103"
TextGridFilter = "*.TextGrid"
OutputPath = r"C:\Users\curly\Documents\Linguistics\MAUS_Python"
TemplatePath = r"C:\Users\curly\Documents\Linguistics\MAUS OUTPUTS_5103\template_compound_duration (2).csv"

# TextGridPathWords = "C:/Users/Stein/Dropbox/HHU/Promotionsstudium/Kurse/Python/Joanne Adeyinka/Forced alignment data"
# TextGridFilter = "*.TextGrid"
# OutputPath = "C:/Users/Stein/Dropbox/HHU/Promotionsstudium/Kurse/Python/Joanne Adeyinka/Forced alignment data/compound_duration_"
# TemplatePath = "C:/Users/Stein/Dropbox/HHU/Promotionsstudium/Kurse/Python/Joanne Adeyinka/Forced alignment data/template_compound_duration.csv"

# -------------------------------------------------------------------- Preparing the necessary information -----------------------------------------------

# Let's first take care of the words: We make a list of all the textgrids which have to be analyzed

FileWalk = os.walk (TextGridPathWords)
FileList = []
for SourcePath, Folders, Files in FileWalk:
    for CurrentFile in Files:
        if fnmatch.fnmatch (CurrentFile, TextGridFilter):
            FileList.append ((SourcePath, CurrentFile))

print("There are " + str(len(FileList)) + " textgrids to be analyzed")

# ------------------------------------------------------------------- Creating the output file and specifying what to read ---------------------------------

with open(OutputPath + str(today) + '.csv', 'w', newline = '') as csvfile:
    OutputFile = csv.writer(csvfile, delimiter = ',')
                            
    for Headers in csv.reader(open(TemplatePath, "r"), delimiter = ","):
        OutputFile.writerow(Headers)
        break
   
    for (Path, Filename) in FileList:
        try:
            CurrentTextGrid = tgt.read_textgrid (os.path.join(Path, Filename))
            ItemID = str(Filename)

# ------------------------------------------------------------------- SENTENCE DURATION --------------------------------------------------------------------

            SentenceTier = CurrentTextGrid.get_tier_by_name("ORT-MAU")
            SentenceDur = 0
            Sentence = ""
            for x in range(len(SentenceTier.intervals)):
                SentenceDur += SentenceTier.intervals[x].duration()
                Sentence += " " + SentenceTier.intervals[x].text
                Sentence = Sentence.lstrip(" ")

# ------------------------------------------------------------------- COMPOUND DURATIONS --------------------------------------------------------------------

            removeFileExtension = ItemID.split(".")
            separateFileName = removeFileExtension[0].split("_")

            CompoundTier = CurrentTextGrid.get_tier_by_name("ORT-MAU")
            Compound1 = separateFileName[2]
            Compound2 = separateFileName[3]

            for x in range(len(CompoundTier.intervals)):
                if (CompoundTier.intervals[x].text == Compound1):
                    Compound1Dur = CompoundTier.intervals[x].duration()
                    Compound1Idx = x
                elif (CompoundTier.intervals[x].text == Compound2):
                    Compound2Dur = CompoundTier.intervals[x].duration()
                    Compound2Idx = x
            ItemDur = Compound1Dur + Compound2Dur

                                

# ------------------------------------------------------------------- COMPOUND SEGMENT DURATIONS ----------------------------------------------------------------

            PhonTier = CurrentTextGrid.get_tier_by_name("KAN-MAU")
            PhonSeq1 = PhonTier.intervals[Compound1Idx].text.split()
            PhonSeq2 = PhonTier.intervals[Compound2Idx].text.split()
            PhonSeq3 = PhonSeq1+PhonSeq2
            SegNum = len(PhonSeq3)

            SoundTier = CurrentTextGrid.get_tier_by_name("MAU")  
          
            SegNumC1 = len(PhonSeq1)
            SegNumC2 = len(PhonSeq2)

            Compound1StartTime = CompoundTier.intervals[Compound1Idx].start_time
            Compound1EndTime = CompoundTier.intervals[Compound1Idx].end_time

            Compound2StartTime = CompoundTier.intervals[Compound2Idx].start_time
            Compound2EndTime = CompoundTier.intervals[Compound2Idx].end_time
             
            for x in range(len(SoundTier.intervals)):
                if (SoundTier.intervals[x].start_time == Compound1StartTime):

                    Seg1C1 = SoundTier.intervals[x].text
                    Seg1C1Dur = SoundTier.intervals[x].duration()
                    Seg1C1StartTime = SoundTier.intervals[x].start_time
                    Seg1C1EndTime = SoundTier.intervals[x].end_time

                    if SegNumC1 > 1:
                        Seg2C1Annotation = SoundTier.get_nearest_annotation(Seg1C1EndTime, boundary = "start")
                        Seg2C1Interval = Seg2C1Annotation[0]
                        Seg2C1 = Seg2C1Interval.text
                        Seg2C1Dur = Seg2C1Interval.duration()
                        Seg2C1StartTime = Seg2C1Interval.start_time
                        Seg2C1EndTime = Seg2C1Interval.end_time
                    else:
                        Seg2C1 = "NA"
                        Seg2C1Dur = "NA"
                        Seg2C1StartTime = "NA"
                        Seg2C1EndTime = "NA"
                    
                    if SegNumC1 > 2:
                        Seg3C1Annotation = SoundTier.get_nearest_annotation(Seg2C1EndTime, boundary = "start")
                        Seg3C1Interval = Seg3C1Annotation[0]
                        Seg3C1 = Seg3C1Interval.text
                        Seg3C1Dur = Seg3C1Interval.duration()
                        Seg3C1StartTime = Seg3C1Interval.start_time
                        Seg3C1EndTime = Seg3C1Interval.end_time
                    else:
                        Seg3C1 = "NA"
                        Seg3C1Dur = "NA"
                        Seg3C1StartTime = "NA"
                        Seg3C1EndTime = "NA"

                    if SegNumC1 > 3:
                        Seg4C1Annotation = SoundTier.get_nearest_annotation(Seg3C1EndTime, boundary = "start")
                        Seg4C1Interval = Seg4C1Annotation[0]
                        Seg4C1 = Seg4C1Interval.text
                        Seg4C1Dur = Seg4C1Interval.duration()
                        Seg4C1StartTime = Seg4C1Interval.start_time
                        Seg4C1EndTime = Seg4C1Interval.end_time
                    else:
                        Seg4C1 = "NA"
                        Seg4C1Dur = "NA"
                        Seg4C1StartTime = "NA"
                        Seg4C1EndTime = "NA"

                    if SegNumC1 > 4:
                        Seg5C1Annotation = SoundTier.get_nearest_annotation(Seg4C1EndTime, boundary = "start")
                        Seg5C1Interval = Seg5C1Annotation[0]
                        Seg5C1 = Seg5C1Interval.text
                        Seg5C1Dur = Seg5C1Interval.duration()
                        Seg5C1StartTime = Seg5C1Interval.start_time
                        Seg5C1EndTime = Seg5C1Interval.end_time
                    else:
                        Seg5C1 = "NA"
                        Seg5C1Dur = "NA"
                        Seg5C1StartTime = "NA"
                        Seg5C1EndTime = "NA"

                    if SegNumC1 > 5:
                        Seg6C1Annotation = SoundTier.get_nearest_annotation(Seg5C1EndTime, boundary = "start")
                        Seg6C1Interval = Seg6C1Annotation[0]
                        Seg6C1 = Seg6C1Interval.text
                        Seg6C1Dur = Seg6C1Interval.duration()
                        Seg6C1StartTime = Seg6C1Interval.start_time
                        Seg6C1EndTime = Seg6C1Interval.end_time
                    else:
                        Seg6C1 = "NA"
                        Seg6C1Dur = "NA"
                        Seg6C1StartTime = "NA"
                        Seg6C1EndTime = "NA"

                    if SegNumC1 > 6:
                        Seg7C1Annotation = SoundTier.get_nearest_annotation(Seg6C1EndTime, boundary = "start")
                        Seg7C1Interval = Seg7C1Annotation[0]
                        Seg7C1 = Seg7C1Interval.text
                        Seg7C1Dur = Seg7C1Interval.duration()
                        Seg7C1StartTime = Seg7C1Interval.start_time
                        Seg7C1EndTime = Seg7C1Interval.end_time
                    else:
                        Seg7C1 = "NA"
                        Seg7C1Dur = "NA"
                        Seg7C1StartTime = "NA"
                        Seg7C1EndTime = "NA"

                    if SegNumC1 > 7:
                        Seg8C1Annotation = SoundTier.get_nearest_annotation(Seg7C1EndTime, boundary = "start")
                        Seg8C1Interval = Seg8C1Annotation[0]
                        Seg8C1 = Seg8C1Interval.text
                        Seg8C1Dur = Seg8C1Interval.duration()
                        Seg8C1StartTime = Seg8C1Interval.start_time
                        Seg8C1EndTime = Seg8C1Interval.end_time
                    else:
                        Seg8C1 = "NA"
                        Seg8C1Dur = "NA"
                        Seg8C1StartTime = "NA"
                        Seg8C1EndTime = "NA"

                    if SegNumC1 > 8:
                        Seg9C1Annotation = SoundTier.get_nearest_annotation(Seg8C1EndTime, boundary = "start")
                        Seg9C1Interval = Seg9C1Annotation[0]
                        Seg9C1 = Seg9C1Interval.text
                        Seg9C1Dur = Seg9C1Interval.duration()
                        Seg9C1StartTime = Seg9C1Interval.start_time
                        Seg9C1EndTime = Seg9C1Interval.end_time
                    else:
                        Seg9C1 = "NA"
                        Seg9C1Dur = "NA"
                        Seg9C1StartTime = "NA"
                        Seg9C1EndTime = "NA"

                    if SegNumC1 > 9:
                        Seg10C1Annotation = SoundTier.get_nearest_annotation(Seg9C1EndTime, boundary = "start")
                        Seg10C1Interval = Seg10C1Annotation[0]
                        Seg10C1 = Seg10C1Interval.text
                        Seg10C1Dur = Seg10C1Interval.duration()
                        Seg10C1StartTime = Seg10C1Interval.start_time
                        Seg10C1EndTime = Seg10C1Interval.end_time
                    else:
                        Seg10C1 = "NA"
                        Seg10C1Dur = "NA"
                        Seg10C1StartTime = "NA"
                        Seg10C1EndTime = "NA"

                    if SegNumC1 > 10:
                        Seg11C1Annotation = SoundTier.get_nearest_annotation(Seg10C1EndTime, boundary = "start")
                        Seg11C1Interval = Seg11C1Annotation[0]
                        Seg11C1 = Seg11C1Interval.text
                        Seg11C1Dur = Seg11C1Interval.duration()
                        Seg11C1StartTime = Seg11C1Interval.start_time
                        Seg11C1EndTime = Seg11C1Interval.end_time
                    else:
                        Seg11C1 = "NA"
                        Seg11C1Dur = "NA"
                        Seg11C1StartTime = "NA"
                        Seg11C1EndTime = "NA"

                    if SegNumC1 > 11:
                        Seg12C1Annotation = SoundTier.get_nearest_annotation(Seg11C1EndTime, boundary = "start")
                        Seg12C1Interval = Seg12C1Annotation[0]
                        Seg12C1 = Seg12C1Interval.text
                        Seg12C1Dur = Seg12C1Interval.duration()
                        Seg12C1StartTime = Seg12C1Interval.start_time
                        Seg12C1EndTime = Seg12C1Interval.end_time
                    else:
                        Seg12C1 = "NA"
                        Seg12C1Dur = "NA"
                        Seg12C1StartTime = "NA"
                        Seg12C1EndTime = "NA"
                                                                                                                                                                                                                                                                                                                                                                       
            for x in range(len(SoundTier.intervals)):
                if (SoundTier.intervals[x].start_time == Compound2StartTime):

                    Seg1C2 = SoundTier.intervals[x].text
                    Seg1C2Dur = SoundTier.intervals[x].duration()
                    Seg1C2StartTime = SoundTier.intervals[x].start_time
                    Seg1C2EndTime = SoundTier.intervals[x].end_time

                    if SegNumC2 > 1:
                        Seg2C2Annotation = SoundTier.get_nearest_annotation(Seg1C2EndTime, boundary = "start")
                        Seg2C2Interval = Seg2C2Annotation[0]
                        Seg2C2 = Seg2C2Interval.text
                        Seg2C2Dur = Seg2C2Interval.duration()
                        Seg2C2StartTime = Seg2C2Interval.start_time
                        Seg2C2EndTime = Seg2C2Interval.end_time
                    else:
                        Seg2C2 = "NA"
                        Seg2C2Dur = "NA"
                        Seg2C2StartTime = "NA"
                        Seg2C2EndTime = "NA"
                    
                    if SegNumC2 > 2:
                        Seg3C2Annotation = SoundTier.get_nearest_annotation(Seg2C2EndTime, boundary = "start")
                        Seg3C2Interval = Seg3C2Annotation[0]
                        Seg3C2 = Seg3C2Interval.text
                        Seg3C2Dur = Seg3C2Interval.duration()
                        Seg3C2StartTime = Seg3C2Interval.start_time
                        Seg3C2EndTime = Seg3C2Interval.end_time
                    else:
                        Seg3C2 = "NA"
                        Seg3C2Dur = "NA"
                        Seg3C2StartTime = "NA"
                        Seg3C2EndTime = "NA"

                    if SegNumC2 > 3:
                        Seg4C2Annotation = SoundTier.get_nearest_annotation(Seg3C2EndTime, boundary = "start")
                        Seg4C2Interval = Seg4C2Annotation[0]
                        Seg4C2 = Seg4C2Interval.text
                        Seg4C2Dur = Seg4C2Interval.duration()
                        Seg4C2StartTime = Seg4C2Interval.start_time
                        Seg4C2EndTime = Seg4C2Interval.end_time
                    else:
                        Seg4C2 = "NA"
                        Seg4C2Dur = "NA"
                        Seg4C2StartTime = "NA"
                        Seg4C2EndTime = "NA"

                    if SegNumC2 > 4:
                        Seg5C2Annotation = SoundTier.get_nearest_annotation(Seg4C2EndTime, boundary = "start")
                        Seg5C2Interval = Seg5C2Annotation[0]
                        Seg5C2 = Seg5C2Interval.text
                        Seg5C2Dur = Seg5C2Interval.duration()
                        Seg5C2StartTime = Seg5C2Interval.start_time
                        Seg5C2EndTime = Seg5C2Interval.end_time
                    else:
                        Seg5C2 = "NA"
                        Seg5C2Dur = "NA"
                        Seg5C2StartTime = "NA"
                        Seg5C2EndTime = "NA"

                    if SegNumC2 > 5:
                        Seg6C2Annotation = SoundTier.get_nearest_annotation(Seg5C2EndTime, boundary = "start")
                        Seg6C2Interval = Seg6C2Annotation[0]
                        Seg6C2 = Seg6C2Interval.text
                        Seg6C2Dur = Seg6C2Interval.duration()
                        Seg6C2StartTime = Seg6C2Interval.start_time
                        Seg6C2EndTime = Seg6C2Interval.end_time
                    else:
                        Seg6C2 = "NA"
                        Seg6C2Dur = "NA"
                        Seg6C2StartTime = "NA"
                        Seg6C2EndTime = "NA"

                    if SegNumC2 > 6:
                        Seg7C2Annotation = SoundTier.get_nearest_annotation(Seg6C2EndTime, boundary = "start")
                        Seg7C2Interval = Seg7C2Annotation[0]
                        Seg7C2 = Seg7C2Interval.text
                        Seg7C2Dur = Seg7C2Interval.duration()
                        Seg7C2StartTime = Seg7C2Interval.start_time
                        Seg7C2EndTime = Seg7C2Interval.end_time
                    else:
                        Seg7C2 = "NA"
                        Seg7C2Dur = "NA"
                        Seg7C2StartTime = "NA"
                        Seg7C2EndTime = "NA"

                    if SegNumC2 > 7:
                        Seg8C2Annotation = SoundTier.get_nearest_annotation(Seg7C2EndTime, boundary = "start")
                        Seg8C2Interval = Seg8C2Annotation[0]
                        Seg8C2 = Seg8C2Interval.text
                        Seg8C2Dur = Seg8C2Interval.duration()
                        Seg8C2StartTime = Seg8C2Interval.start_time
                        Seg8C2EndTime = Seg8C2Interval.end_time
                    else:
                        Seg8C2 = "NA"
                        Seg8C2Dur = "NA"
                        Seg8C2StartTime = "NA"
                        Seg8C2EndTime = "NA"

                    if SegNumC2 > 8:
                        Seg9C2Annotation = SoundTier.get_nearest_annotation(Seg8C2EndTime, boundary = "start")
                        Seg9C2Interval = Seg9C2Annotation[0]
                        Seg9C2 = Seg9C2Interval.text
                        Seg9C2Dur = Seg9C2Interval.duration()
                        Seg9C2StartTime = Seg9C2Interval.start_time
                        Seg9C2EndTime = Seg9C2Interval.end_time
                    else:
                        Seg9C2 = "NA"
                        Seg9C2Dur = "NA"
                        Seg9C2StartTime = "NA"
                        Seg9C2EndTime = "NA"

                    if SegNumC2 > 9:
                        Seg10C2Annotation = SoundTier.get_nearest_annotation(Seg9C2EndTime, boundary = "start")
                        Seg10C2Interval = Seg10C2Annotation[0]
                        Seg10C2 = Seg10C2Interval.text
                        Seg10C2Dur = Seg10C2Interval.duration()
                        Seg10C2StartTime = Seg10C2Interval.start_time
                        Seg10C2EndTime = Seg10C2Interval.end_time
                    else:
                        Seg10C2 = "NA"
                        Seg10C2Dur = "NA"
                        Seg10C2StartTime = "NA"
                        Seg10C2EndTime = "NA"

                    if SegNumC2 > 10:
                        Seg11C2Annotation = SoundTier.get_nearest_annotation(Seg10C2EndTime, boundary = "start")
                        Seg11C2Interval = Seg11C2Annotation[0]
                        Seg11C2 = Seg11C2Interval.text
                        Seg11C2Dur = Seg11C2Interval.duration()
                        Seg11C2StartTime = Seg11C2Interval.start_time
                        Seg11C2EndTime = Seg11C2Interval.end_time
                    else:
                        Seg11C2 = "NA"
                        Seg11C2Dur = "NA"
                        Seg11C2StartTime = "NA"
                        Seg11C2EndTime = "NA"
                    
                    if SegNumC2 > 11:
                        Seg12C2Annotation = SoundTier.get_nearest_annotation(Seg11C2EndTime, boundary = "start")
                        Seg12C2Interval = Seg12C2Annotation[0]
                        Seg12C2 = Seg12C2Interval.text
                        Seg12C2Dur = Seg12C2Interval.duration()
                        Seg12C2StartTime = Seg12C2Interval.start_time
                        Seg12C2EndTime = Seg12C2Interval.end_time
                    else:
                        Seg12C2 = "NA"
                        Seg12C2Dur = "NA"
                        Seg12C2StartTime = "NA"
                        Seg12C2EndTime = "NA"
            
            
            
# ------------------------------------------------------------------- CONSONANT DURATION --------------------------------------------------------------------

            Consonants = ["p", "b", "t", "d", "k", "g", "tS", "dZ", "f", "v", "T", "D", "s", "z", "S", "Z", "h", "m", "n", "N", "r", "l", "w", "j", "?", "x"]
            Vowels = ["I", "e", "{", "Q", "V", "U", "@", "eI", "aI", "OI", "@U", "aU", "3", "3:", "A", "A:", "O", "O:", "I@", "e@", "U@", "i", "i:", "u", "u:", "E"]

            Compound1EndTime = CompoundTier.intervals[Compound1Idx].end_time
            for x in range(len(SoundTier.intervals)):
                if (SoundTier.intervals[x].end_time == Compound1EndTime):
                    FinalInterval = SoundTier.get_annotation_by_end_time(Compound1EndTime)
                    FinalSound = FinalInterval.text
                    if FinalSound in Consonants:
                        ConFinal = FinalSound
                        ConFinalDur = SoundTier.intervals[x].duration()
                    else:
                        ConFinal = "NA"
                        ConFinalDur = "NA"

            Compound2StartTime = CompoundTier.intervals[Compound2Idx].start_time
            for x in range(len(SoundTier.intervals)):
                if (SoundTier.intervals[x].start_time == Compound2StartTime):
                    InitialInterval = SoundTier.get_annotation_by_start_time(Compound2StartTime)
                    InitialSound = InitialInterval.text
                    if InitialSound in Consonants:
                        ConInitial = InitialSound
                        ConInitialDur = SoundTier.intervals[x].duration()
                    else:
                        ConInitial = "NA"
                        ConInitialDur = "NA"
            
            # Sum of boundary-adjacent consonant durations:
            if ConFinal != "NA":
                if ConInitial != "NA":
                    ConDur = ConFinalDur + ConInitialDur
                else:
                    ConDur = ConFinalDur
            else:
                if ConInitial != "NA":
                    ConDur = ConInitialDur
                else:
                    ConDur = "NA"

# ------------------------------------------------------------------- PRECEDING AND FOLLOWING SEGMENT DURATION ----------------------------------------------

            if ConFinal != "NA":
                PrecSegEndTime = FinalInterval.start_time
            else:
                PrecSegEndTime = FinalInterval.end_time

            for x in range(len(SoundTier.intervals)):
                if (SoundTier.intervals[x].end_time == PrecSegEndTime):
                    PrecSeg = SoundTier.intervals[x].text
                    PrecSegDur = SoundTier.intervals[x].duration()

            if ConInitial != "NA":
                FolSegStartTime = InitialInterval.end_time
            else:
                FolSegStartTime = InitialInterval.start_time

            for x in range(len(SoundTier.intervals)):
                if (SoundTier.intervals[x].start_time == FolSegStartTime):
                    FolSeg = SoundTier.intervals[x].text
                    FolSegDur = SoundTier.intervals[x].duration()

# ------------------------------------------------------------------- SYLLABLE DURATION? --------------------------------------------------------------------



# ------------------------------------------------------------------- WRITING RESULTS TO FILE ---------------------------------------------------------------

            OutputFile.writerow ([
                Filename,
                ItemDur,                            
                # sentence:
                Sentence, 
                SentenceDur,
                # compounds:
                Compound1,
                Compound1Dur,
                Compound2,
                Compound2Dur,
                Compound1StartTime,
                Compound2EndTime,
                # boundary consonants:
                ConFinal,
                ConFinalDur,
                ConInitial,
                ConInitialDur,
                ConDur,
                # adjacent segments:
                PrecSeg,
                PrecSegDur,
                FolSeg,
                FolSegDur,
                # number of segments:
                SegNum,
                # individual segments:
                Seg1C1,
                Seg1C1StartTime,
                Seg1C1EndTime,
                Seg2C1,
                Seg2C1StartTime,
                Seg2C1EndTime,
                Seg3C1,
                Seg3C1StartTime,
                Seg3C1EndTime,
                Seg4C1,
                Seg4C1StartTime,
                Seg4C1EndTime,
                Seg5C1,
                Seg5C1StartTime,
                Seg5C1EndTime,
                Seg6C1,
                Seg6C1StartTime,
                Seg6C1EndTime,
                Seg7C1,
                Seg7C1StartTime,
                Seg7C1EndTime,
                Seg8C1,
                Seg8C1StartTime,
                Seg8C1EndTime,
                Seg9C1,
                Seg9C1StartTime,
                Seg9C1EndTime,
                Seg10C1,
                Seg10C1StartTime,
                Seg10C1EndTime,
                Seg11C1,
                Seg11C1StartTime,
                Seg11C1EndTime,
                Seg12C1,
                Seg12C1StartTime,
                Seg12C1EndTime,
                # Second compound word
                Seg1C2,
                Seg1C2StartTime,
                Seg1C2EndTime,
                Seg2C2,
                Seg2C2StartTime,
                Seg2C2EndTime,
                Seg3C2,
                Seg3C2StartTime,
                Seg3C2EndTime,
                Seg4C2,
                Seg4C2StartTime,
                Seg4C2EndTime,
                Seg5C2,
                Seg5C2StartTime,
                Seg5C2EndTime,
                Seg6C2,
                Seg6C2StartTime,
                Seg6C2EndTime,
                Seg7C2,
                Seg7C2StartTime,
                Seg7C2EndTime,
                Seg8C2,
                Seg8C2StartTime,
                Seg8C2EndTime,
                Seg9C2,
                Seg9C2StartTime,
                Seg9C2EndTime,
                Seg10C2,
                Seg10C2StartTime,
                Seg10C2EndTime,
                Seg11C2,
                Seg11C2StartTime,
                Seg11C2EndTime,
                Seg12C2,
                Seg12C2StartTime,
                Seg12C2EndTime,
              #  Seg1C1Dur,
              #  Seg2C1Dur,
              #  Seg3C1Dur,
              #  Seg4C1Dur,
              #  Seg5C1Dur,
              #  Seg6C1Dur,
              #  Seg7C1Dur,
              #  Seg8C1Dur,
                
              #  Seg9C1Dur,
                
             #   Seg10C1Dur,
                
             #   Seg1C2Dur,
                
             #   Seg2C2Dur,
                
             #   Seg3C2Dur,
                
             #   Seg4C2Dur,
                
             #   Seg5C2Dur,
                
             #   Seg6C2Dur,
                
             #   Seg7C2Dur,
                
             #   Seg8C2Dur,
                
             #   Seg9C2Dur,
                
            ])    
             #   Seg10C2Dur,
                # xmin and xmax values:
              #  Compound1EndTime,
              #  Compound2StartTime,
                # Seg1C1StartTime,
                # Seg1C1EndTime,
                # Seg2C1StartTime,
                # Seg2C1EndTime,
                # Seg3C1StartTime,
                # Seg3C1EndTime,
                # Seg4C1StartTime,
                # Seg4C1EndTime,
                # Seg5C1StartTime,
                # Seg5C1EndTime,
                # Seg6C1StartTime,
                # Seg6C1EndTime,
                # Seg7C1StartTime,
                # Seg7C1EndTime,
                # Seg8C1StartTime,
                # Seg8C1EndTime,
                # Seg9C1StartTime,
                # Seg9C1EndTime,
                # Seg10C1StartTime,
                # Seg10C1EndTime,
                # Seg1C2StartTime,
                # Seg1C2EndTime,
                # Seg2C2StartTime,
                # Seg2C2EndTime,
                # Seg3C2StartTime,
                # Seg3C2EndTime,
                # Seg4C2StartTime,
                # Seg4C2EndTime,
                # Seg5C2StartTime,
                # Seg5C2EndTime,
                # Seg6C2StartTime,
                # Seg6C2EndTime,
                # Seg7C2StartTime,
                # Seg7C2EndTime,
                # Seg8C2StartTime,
                # Seg8C2EndTime,
                # Seg9C2StartTime,
                # Seg9C2EndTime,
                # Seg10C2StartTime,
                # Seg10C2EndTime,
            

        except Exception as e:
                    print (e)
                    print((Filename + " has a problem"))
                    # raise e