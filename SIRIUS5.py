#-------------------------------------------------------------------------------
#
# Sample Python script for FDR estimation
# 24/9/14 Fumio Matsuda@Osaka University
#-------------------------------------------------------------------------------

import glob,re, os, shutil, sys, csv
import subprocess, itertools
from pathlib import Path

#
# 1. Install SIRIUS5 and Describe the SIRIUS5 folder in your PC
#
sirius5path = 'C:/Program Files/sirius/sirius'
#
# 2. Choose query spetra folder.
#
querypath = 'C:/FDRestimation/MassBankCommonPos/target/'
#querypath = "D:\FDRestimation\MassBank CommonPos\decoy mirroring\"
#querypath = "D:\FDRestimation\MassBank CommonPos\decoy polarity switching\"
#querypath = "D:\FDRestimation\MassBank CommonPos\decoy spectral sampling\"
#
# 3. Describe output folder.
#
outputpath = 'C:/FDRestimation/MassBankCommonPos/output/'
#
# 4. Describe the email address of your SIRIUS5 account.
#
email = "fmatsuda@ist.osaka-u.ac.jp"
#
# 5. Choose compound database from YMDB, HMDB, and BIO
#
database = "YMDB"
#
# 6. Choose "POSITIVE" or "NEGATIVE" mode.
#
polarity = "POSITIVE"

#
# 7. Execute SIRIUS5 CI
#
#
#  Login
#

commonttext_orignal = '"C:/Program Files/sirius/sirius" login -u [email] -p'
commanttext = commonttext_orignal.replace("[email]", email)
subprocess.run(commanttext, shell=True)
#
# SetUp SIRIUS 5
#
siriusini_pos = '"C:\Program Files\sirius\sirius"  config --IsotopeSettings.filter=true --FormulaSearchDB=BIO --Timeout.secondsPerTree=0 --FormulaSettings.enforced=HCNOP --Timeout.secondsPerInstance=0 --AdductSettings.detectable=[[M+H]+,[M-H2O+H]+,[M-H4O2+H]+,[M+H3N+H]+] --UseHeuristic.mzToUseHeuristicOnly=650 --AlgorithmProfile=qtof --IsotopeMs2Settings=IGNORE --MS2MassDeviation.allowedMassDeviation=10.0ppm --NumberOfCandidatesPerIon=1 --UseHeuristic.mzToUseHeuristic=300 --FormulaSettings.detectable=B,Cl,Br,Se,S --NumberOfCandidates=20 --ZodiacNumberOfConsideredCandidatesAt300Mz=10 --ZodiacRunInTwoSteps=true --ZodiacEdgeFilterThresholds.minLocalConnections=10 --ZodiacEdgeFilterThresholds.thresholdFilter=0.95 --ZodiacEpochs.burnInPeriod=2000 --ZodiacEpochs.numberOfMarkovChains=10 --ZodiacNumberOfConsideredCandidatesAt800Mz=50 --ZodiacEpochs.iterations=20000 --AdductSettings.enforced=, --AdductSettings.fallback=[[M-H]-] --FormulaResultThreshold=true --InjectElGordoCompounds=true --StructureSearchDB=BIO --RecomputeResults=True'
siriusini_neg = '"C:\Program Files\sirius\sirius"  config --IsotopeSettings.filter=true --FormulaSearchDB=BIO --Timeout.secondsPerTree=0 --FormulaSettings.enforced=HCNOP --Timeout.secondsPerInstance=0 --AdductSettings.detectable=[[M-H]-,[M-H2O-H]-] --UseHeuristic.mzToUseHeuristicOnly=650 --AlgorithmProfile=qtof --IsotopeMs2Settings=IGNORE --MS2MassDeviation.allowedMassDeviation=10.0ppm --NumberOfCandidatesPerIon=1 --UseHeuristic.mzToUseHeuristic=300 --FormulaSettings.detectable=B,Cl,Br,Se,S --NumberOfCandidates=20 --ZodiacNumberOfConsideredCandidatesAt300Mz=10 --ZodiacRunInTwoSteps=true --ZodiacEdgeFilterThresholds.minLocalConnections=10 --ZodiacEdgeFilterThresholds.thresholdFilter=0.95 --ZodiacEpochs.burnInPeriod=2000 --ZodiacEpochs.numberOfMarkovChains=10 --ZodiacNumberOfConsideredCandidatesAt800Mz=50 --ZodiacEpochs.iterations=20000 --AdductSettings.enforced=, --AdductSettings.fallback=[[M-H]-] --FormulaResultThreshold=true --InjectElGordoCompounds=true --StructureSearchDB=BIO --RecomputeResults=True'
if polarity == "POSITIVE":
    siriusini = str(siriusini_pos)
else:
    siriusini = str(siriusini_neg)
subprocess.run(siriusini, shell=True)
#
# SetUp SIRIUS 5
#
exectext_orignal= '"C:\Program Files\sirius\sirius" --recompute --input [querypath] --output [outputpath] formula  --profile qtof --database [db] --candidates 10 zodiac fingerprint structure --database [db] canopus write-summaries -o [outputpath]'

exectext = exectext_orignal.replace("[querypath]", querypath)
exectext = exectext.replace("[outputpath]", outputpath)
exectext = exectext.replace("[db]", database)
subprocess.run(exectext, shell=True)

#
# Second-rand hits are summerized in secondrank.csv
#
paths = list(Path(outputpath).glob(r'*'))
outputlist = []
for path in paths:
    structure_candidates_path = str(path)+"/structure_candidates.tsv"
    if not os.path.isfile(structure_candidates_path):
        continue
    with open(structure_candidates_path,  encoding='UTF-8') as f:
        #print(structure_candidates_path)
        reader = csv.reader(f, delimiter='\t')

        for i, row in enumerate(reader):
            if row[0] == "2":

                outputlist.append([1,1,1] + row)

                continue
    with open("secondrank.csv", 'w',  encoding='UTF-8', newline='') as f:

        writer = csv.writer(f)
        writer.writerows(outputlist)

#
# 8. Please fine "compound_identifications.tsv" in the output folder. It includes top hits of queries.
# 9. Please copy "compound_identifications.tsv" or "secondrank.csv" of target and decoy query to the "target" and "decoy" sheet in FDRestimation.xlsx.
# 10. Please chech FDR sheet
#
