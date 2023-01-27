# data-WranglingProject

## Introduction

Here are the files for the data wrangling course, for our group project.
The project goal is to use data wrangling skills learnt through the course and apply them
to a data set of our own interest.

In this project we look at the density of twitter tweets created in a specific time period 
to see if there is perhaps a correlation to world events/news.

Below details the various files and methods we used to obtain the data and also details of the
data sets themselves.


## Data set

Using the following website, the raw tweet data of a specific month can be downloaded via a torrent.
Link:  https://archive.org/search?query=collection%3Atwitterstream

The download file contains multiply .tar compressed files, which inside each one then contains
approximately 1440 .gz compressed json files. 

In order to process this information the python script "TwitterZip2DataFrame.py" was created.
Due to the sheer size of the files being process extra care is needed to process them.
Hence the python script unzips one of the .tar files into a temporary file, from which a
multiprocess function is called to process the .gz jsons files. 
This is to speed up the process. The json are convert in pandas data frames then the data frames
are stripped for the desired information, in this case 'created_at' and 'lang' (language )
which are then concatenated with the other json files and saved to the disk as .csv files.  
Once all json files are proccessed in the .tar file, the temporary file is cleared to allow space 
for the next .tar file, until all are done. The result is that approximately 100Gb of raw twitter 
data can be filtered to under 5gb of .csv files, which is more user friendly. 
