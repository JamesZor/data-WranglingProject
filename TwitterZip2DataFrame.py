import os, sys, gzip, json, tarfile, tempfile, shutil
import multiprocessing as mp
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.max_rows = 20
np.set_printoptions(precision=4, suppress=True)

userSelectPath = sys.argv[1]
userSavePath   = sys.argv[2]
userFileName   = sys.argv[3]

def getFileList(dir_path):
    files_list = []
    os.chdir(dir_path)
    files = os.listdir()
    [files_list.append(os.path.abspath(file)) for file in files ]
    return files_list

def printList(pList):
    [print(item) for item in pList]

def openGZip(file_path):
    with gzip.open(file_path, 'rb') as f:
        data = [json.loads(line) for line in f]
    f.close()
    return filterDataFrame(data) 

def multiProcessGZFiles(files):
    p =mp.Pool(processes=4)
    results = []
    for result in tqdm(p.imap(func=openGZip, iterable=files ), total=len(files),
                            desc="processing GZ"):
       results.append(result) 
    dataFrame= pd.concat(results)
    return dataFrame

def filterDataFrame(data):
    dataFrame = pd.DataFrame(data)
    dataFrame['created_at']= pd.to_datetime(dataFrame['created_at'])
    #return dataFrame[dataFrame.lang=='nl'][['created_at', 'id' ]]
    return dataFrame[['created_at', 'id','lang']].set_index('created_at')

def processTAR(path):
    tarFiles = []
    try:
        tarFiles = getFileList(path)
    except:
        print("Error in getting file list.")
    for (i, file) in tqdm(enumerate(tarFiles), total=len(tarFiles), desc="Processing TAR files.. "):
        try:
            dirTempPath = tempfile.mkdtemp()
            currentFile = tarfile.open(file)
            currentFile.extractall(dirTempPath)
            gzFiles = getFileList( getFileList(dirTempPath)[0] )
            if i==0:
                mainData = multiProcessGZFiles(gzFiles)
            else:
                mainData = pd.concat([mainData, multiProcessGZFiles(gzFiles)])
        finally:
            shutil.rmtree(dirTempPath)
    return mainData

# main
if len(sys.argv)!=4:
    print("Error with arguments.")

mainData = processTAR(userSelectPath)
mainData.to_csv(userSavePath+userFileName+".csv")
print(mainData)

