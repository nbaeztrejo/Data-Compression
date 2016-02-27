CS181 - Lab 2
November Baez Trejo
2/26/16

Run as python script:
python entropy.py text_file.txt output_file

*For some reason, my algorithm worked best on very large files (>20MB where the compression was successful in smaller files, the "compressed" file was either larger or the same size. This might be due to not being able to export binary strings as actual binary)


1. Compression ratio:
	20000 Leagues: -600%
	Anna Karenina: -470%
	Crime and Punishment: -560%

   Entropy:
	20000 Leagues: 4.493
	Anna Karenina: 4.518
	Crime and Punishment: 4.518

2. Compression ratio:
	Random file 1: -1200%
	Random file 2: -708%
	Random file 3: -416%	

   Entropy:
	Random file 1: 8.00
	Random file 2: 6.23
	Random file 3: 4.25

3. It is clear that random files are harder to compress for compression relies on repetition which are statistically less likely in true random text. This can be seen in the entropy of the random files compared to actual books. When compared to gibberesh words, the compression was comparable to that of the books, which supports the results. 

4. Random files have a much higher entropy than regular text files, which is to be expected as written language is not random and thus has much repition. Thus, the lower the entropy the higher the compression rate, which can be a fairly good reason as to why modern compression algorithms perform further compressions after the first.