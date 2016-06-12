# diploma

* Подготовка исходных данных:
  1. Удаляем вставки и делеции (indel), а также экзомные семплы: bin/filterMutations.py
  2. Преобразуем .bigWig в .wig (см. полезрные ссылки)
  3. Преобразуем файлы генома с расширением .fa в последовательность нуклеотидов: bin/transformAllFa.sh
* Основная часть:
  1. Для каждого семпла исследуем зависимость от частоты мутаций от replication timing. Получаем наклон графика.
  2. Исследуем зависимость наклона графика от APOBEG enrichment

Полезные ссылки:
* [Breast canser mutations](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/somatic_mutation_data/Breast/Breast_clean_somatic_mutations_for_signature_analysis_apr15.txt)
* [Breast catalog](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/mutational_catalogs/genomes/Breast/Breast_genomes_mutational_catalog_192_subs_with_strand_bias.txt "Список геномных семплов")
* [Lung canser mutations](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/somatic_mutation_data/Lung%20Adeno/Lung%20Adeno_clean_somatic_mutations_for_signature_analysis.txt)
* [Lung catalog](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/mutational_catalogs/genomes/Lung%20Adeno/Lung%20Adeno_genomes_mutational_catalog_192_subs_with_strand_bias.txt "Список геномных семплов")
* [Последняя подверсия 37-й версии генома](ftp://ftp.ncbi.nlm.nih.gov/genomes/Homo_sapiens/ARCHIVE/BUILD.37.3/Assembled_chromosomes/seq/ "Берем файлы вида hs_ref_GRCh37.p5_chr*.fa.gz")
* [replication timing for IMR90](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeUwRepliSeq/wgEncodeUwRepliSeqImr90WaveSignalRep1.bigWig "lung replication timing")
* [replication timing for MCF-7](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeUwRepliSeq/wgEncodeUwRepliSeqMcf7WaveSignalRep1.bigWig "breast replication timing")
* [bigWigToWig](ftp://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/ "Преобразование .bigWig -> .wig")
* [APOBEG enrichment](www.cell.com/cms/attachment/2040452923/2053963817/mmc2.xlsx "Степень влияния APOBEG на каждый из семплов")