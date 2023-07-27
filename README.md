# NCBI基因组下载工具

该脚本便于从 NCBI Genank/Refseq 上批量下载基因组数据，可以根据需求选择下载格式，采用Rsync工具并行下载。

## 用法/示例
```bash
bash download.sh $1 $2 $3
#$1：IDtable.txt
#$2: Output file folder name
#$3: Database (GenBank--GB, Refseq--Ref)
```
```bash
#Example
bash download.sh IDtable.txt Test Ref
```
## 流程
### 1.预处理：从 NCBI 上下载得到 IDtable 文件
- 进入NCBI Assembly 网站 (https://www.ncbi.nlm.nih.gov/assembly/) 搜索需要批量下载的物种名称 (e.g. Escherichia coli，Viruses)
![](README_SCREENSHOTS/screenshot_1.jpeg)

- 选择左侧 **Status** 以及 **Assembly level** 选中数据范围
![](README_SCREENSHOTS/screenshot_2.jpeg)

- 点击中央上方**Send to**，勾选 **file**，**ID Table (text)**，点击 **Create File** 下载文件得到IDtable.txt(**建议：修改下载的文件名称**)
![](README_SCREENSHOTS/screenshot_3.jpeg)
![](README_SCREENSHOTS/screenshot_4.jpeg)

- 检查下载的数据(NA 表示没有对应的数据)

GenBank Assembly ID (Accession.version)	|GenBank release ID	|RefSeq Assembly ID (Accession.version)|RefSeq release ID
--|--|--|--| 	
GCA_000500165.1	|863668	|GCF_000500165.1	|863898
GCA_000500185.1	|863688	|GCF_000500185.1	|864078
GCA_000523875.1	|897338	|N/A	|N/A	
GCA_000280655.1	|401628	|GCF_000280655.1	|621018	

### 2.使用download.sh下载数据
```bash
bash download.sh IDtable.txt Test Ref
```
该脚本以**IDtable.txt**中的**Assembly ID**为输入对象(GCA_000500165.1)，采用 rsync 工具批量下载 NCBI FTP(https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/500/165/GCA_000500165.1_MAB_082312_2258/) 上对应的氨基酸序列(_genomic.fna.gz)以及基因组注释文件(_genomic.gbff.gz)
![](README_SCREENSHOTS/screenshot_5.jpeg)


## 输出文件
运行后会得到一个含有下载数据的文件夹，context 文本和 log 文本，其中 context 为 rsync 下载链接，log 记录NCBI数据库中对应物种的基因组是否含有相关数据类型文件，便于排查。

