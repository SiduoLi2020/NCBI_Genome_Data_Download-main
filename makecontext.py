### Function:create a context file for download genomic data from NCBI by rsync tool
### Usage: python3 makecontext.py -i IDtable.txt -n outputfilename -t GB/Ref
### NCBI data type: 
# 1. cds_from_genomic.fna,
# 2. genomic_fna,
# 3. genomic_gbff,
# 4. genomic_gff,
# 5. protein_faa,
# 6. protein_gpff,
# 7. rna_from_genomic.fna,
# 8. wgsmaster.gbff,
# 9. assembly_report.txt,
# 10. assembly_stats.txt,
# 11. feature_table.txt

import subprocess
import re
import argparse
import os.path
from time import sleep


class NameException(Exception): pass

# Check dependences
print("Check dependences: pandas, requests\n")
sleep(1)

try:
    import pandas as pd
    import requests

except ImportError:
    # Install pandas and requests
    print("Install pandas and requests")
    sleep(1)
    subprocess.call("pip3 install pandas",shell=True)
    subprocess.call("pip3 install requests",shell= True)

    import pandas as pd
    import requests


# Please download ID table(.txt) from NCBI Assembly: https://www.ncbi.nlm.nih.gov/assembly/
def loadIDtable(IDtable):
    SpeciesTable = pd.read_csv(IDtable,names=['GeneBnakAssemblyID','GenBankreleaseID','RefSeqAssemblyID','RefSeqreleaseID'],
    sep='\t',header=0,index_col=False)
    return SpeciesTable

# Choose the data type by user
def inputType():
    print("NCBI data type:\n"+ \
          "1. cds_from_genomic.fna,\n"+ \
          "2. genomic.fna,\n" + \
          "3. genomic.gbff,\n" + \
          "4. genomic.gff,\n" + \
          "5. protein.faa,\n" + \
          "6. protein.gpff,\n" + \
          "7. rna_from_genomic.fna,\n" + \
          "8. wgsmaster.gbff,\n" + \
          "9. assembly_report.txt,\n" + \
          "10. assembly_stats.txt,\n" + \
          "11. feature_table.txt\n" + \
          "12. ALL of above\n")

    typelist  = input("Please enter the data type you want to download, enter 0 to exit(eg: genomic_fna + genomic_gff = 2+4):")

    if type == '0':
        raise NameException("No data to download.Exit!")        

    return typelist

# Check the file of specific species is exist or not in NCBI, if exist, return True, else return False and delete the url
def filecheck(url):
    request = requests.get(url)
    if request.status_code == 200:
        return True
    else:
        return False
    

# Create a context file and check the file is exist or not in NCBI
def NCBIDataType(type,prefix):
        DataType = {"1":"cds_from_genomic.fna",\
                    "2":"genomic.fna",\
                    "3":"genomic.gbff",\
                    "4":"genomic.gff",\
                    "5":"protein.faa",\
                    "6":"protein.gpff",\
                    "7":"rna_from_genomic.fna",\
                    "8":"wgsmaster.gbff",\
                    "9":"assembly_report.txt",\
                    "10":"assembly_stats.txt",\
                    "11":"feature_table.txt"}
        
        datafile = prefix[:-1] + "_"+ DataType[type] +".gz"
        urlhttps = TestUrl + x + datafile
        # check the file is exist or not
        if filecheck(urlhttps):
            print("Exist:", DataType[type])
            urlrsync = urlhttps.replace("https","rsync")
            return urlrsync,DataType[type]
        else:
            print("Warning! Not exist:", DataType[type])
            return "",DataType[type]
        

if __name__ == "__main__":
    ap = argparse.ArgumentParser("Download genomic data from NCBI by rsync tool")
    ap.add_argument('-i', help="ID table(.txt) filename")
    ap.add_argument('-n', help='output file name')
    ap.add_argument('-t', help='database, if you want to download data from GenBank,please enter GB; Refseq -- Ref')

    opts = ap.parse_args()
    TableName = opts.i
    inputName = opts.n
    DataOrigin = opts.t

    # Check the context file
    ContextFilename = inputName + '_'+DataOrigin+'_Context.txt'
    if os.path.exists(ContextFilename):
        print("Warning: The context file already exists, please check it!")
        sleep(1)
        print("If you want to create a new context file, please delete the old one!")
        sleep(1)
        print("If you want to download data from the old context file, please run the command:\n \tpython3 NCBIdownload.py "+ContextFilename+"\n\n")
        sleep(2)
        raise NameException("Error: The context file already exists, please check it!")
    else:
        print("Create context file:",ContextFilename)
        sleep(1)

    # Create a log file
    LogFile = inputName + '_'+DataOrigin+'_Log.txt'
    print("Create log file:",LogFile)
    with open(LogFile, "w") as f:
        f.write("ID"+"\t"+"DataType"+"\t"+"Status"+"\n")
    sleep(1)


    
    # Load ID table and delete the empty data (NAN)
    if DataOrigin == 'GB':
        TableColumn = 0
    elif DataOrigin == "Ref":
        TableColumn = 2
    else:
        raise NameException("Error: please choose database: GB/Ref!")
    
    SpeciesTable = loadIDtable(TableName)
    SpeciesAssembly = SpeciesTable[SpeciesTable.columns[TableColumn]]
    SpeciesAssembly = SpeciesAssembly.dropna()
    print("Total species:",len(SpeciesAssembly),"\n")
    sleep(1)

    # Choose the data type by user
    typelist = inputType()
    if typelist == '12':
        typelist = "1+2+3+4+5+6+7+8+9+10+11"
    typelist = typelist.split('+')


    # Create a context file for download genomic data from NCBI by rsync tool
    print("Start search from NCBI :",inputName,DataOrigin,"\n")
    count = 0
    with open(ContextFilename, "w") as f:
        for i in SpeciesAssembly:
            
            try:
                print("Start search:",i)
                TestUrl = 'https://ftp.ncbi.nlm.nih.gov/genomes/all/'+ i[0:3] +'/'+ i[4:7] +'/'+ i[7:10] + '/'+ i[10:13] +'/'
                request = requests.get(TestUrl)
                raw_list = re.compile(r'<a.*?>(.*?)</a>').finditer(request.text.strip())

                for j in raw_list:
                    x = j.group(1)
                    if x[0:3] == 'GCF':
                        count = count + 1
                        for t in typelist:
                            Url_rsync,datatype = NCBIDataType(t,x)
                            if Url_rsync != "":
                                f.write(Url_rsync)
                                f.write("\n")
                                with open(LogFile, "a") as log:
                                    log.write(i+"\t"+datatype+"\t"+"Exist"+"\n")
                            else:
                                with open(LogFile, "a") as log:
                                    log.write(i+"\t"+datatype+"\t"+"NotExist"+"\n")
                                pass
                    else:
                        pass

                            
                    if x[0:3] == 'GCA':
                        count = count + 1
                        for t in typelist:
                            Url_rsync,datatype = NCBIDataType(t,x)
                            if Url_rsync != "":
                                f.write(Url_rsync)
                                f.write("\n")
                                with open(LogFile, "a") as log:
                                    log.write(i+"\t"+datatype+"\t"+"Exist"+"\n")
                            else:
                                with open(LogFile, "a") as log:
                                    log.write(i+"\t"+datatype+"\t"+"NotExist"+"\n")
                                pass
                    else:
                        pass
                
                print("Finish search:",i,"\n")


            except TypeError as E:
                pass
        
        f.close()
    print("\nFinish search from NCBI:",inputName,"\tToal:",count,"\n")
