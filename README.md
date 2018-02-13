# donation-analytics

For solving the challenge Donation-Analytics, I took advantage of the input files provided by the example  (incont.txt) in the description of the challenge and I also used data downloaded from https://classic.fec.gov/finance/disclosure/ftpdet.shtml in the "Contributions by Individuals". Specifically, I used the itcont.txt files inside the indiv16.zip and indiv18.zip which correspond to data of individual contribution from the year 2015 until today's date. As the files obtained from the website are quite large, for simplicity a small dataset is found in the input file itcont.txt. The input file percentile.txt only has the value requested to preform the percentile calculation and can be changed for other percentile values calculations.

I used python to write the code, specifically pandas. When analyzing my code, please download the following dependencies:

#Dependencies
import math
from collections import Counter
import csv
import pandas as pd
import numpy as np
import os
import time
from scipy import stats
from datetime import datetime
import datetime as dt

The data was then cleaned using the following parameters:

-Consider only data with a date from the year 2015 until today's date since we know that the input file follows the data dictionary noted by the FEC for the 2015-current election years (https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).  In this same site, we can find the header with the corresponding labels for the data obtained and in this way, we can further analyze specific fields;

- As instructed, only the fields 'CMTE_ID', 'NAME', ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID' were selected;

-Empty or null entries were removed with the exception of 'OTHER_ID' entries where all should be NAN;

-The data was further cleaned by making sure that the above fields meet the FEC dictionary specifications in terms of length and data type;

-'ZIP_CODE' is represented by its first five characters and 'TRANSACTION_DT' is expressed by the year of transaction;

-Repeated donors were found by using both 'NAME', and ZIP_CODE' combined for data selection;

-According to the instructions, entries that are not chronologically ordered should be sorted out and therefore 2 condition statements were made in the code in order to select only chronologically ordered data from repeated donors;

-Having the data cleaned, the calculations required in the challenge were made and are presented in the code;

-This code is written to be able to deal both with streaming (chronologically in and out of order) data and also to analyze a  data at a specific time point from 2015 until today's date. The value of the percentile required can also be adjusted accordingly to the number provided by the percentile.txt file;

-The Output is printed in a .txt file;

