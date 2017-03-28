# diploma

* Подготовка исходных данных:
  1. Удаляем вставки и делеции (indel), а также экзомные семплы:
  bin/filter.py
  2. Преобразуем файлы генома с расширением .fa в последовательность
  нуклеотидов: bin/genome.py
  3. Проверяем, соответствуют ли мутации геному: bin/check.py
  4. Преобразуем .bigWig в .wig (см. полезные ссылки)
  5. Преобразуем .wig в .csv: bin/replication.py
  6. Переводим enrichment.xlsx в текстовый вид посредством copy-paste. При этом:
    * Не забываем скопировать заголовок
    * Переводим все числа в формат с разделителем дробной части 
    — точкой (НЕ запятой!)
  7. Генерируем комплиментарные пары мутационных сигнатур (в текущей версии -- все 96
     трехбуквенных пар сигнатур): bin/generate.py

* Для каждого семпла исследуем зависимость частоты мутаций от replication timing:
  1. Для каждого семпла находим replication timing всех мутировавших (согласно выбранной сигнатуре)
  нуклеотидов: bin/mutations.py
  2. Для каждого семпла находим replication timing всех позиций нуклеотидов в геноме,
  входящих в мотивы текущей пары комплиментарных сигнатур: bin/motif.py
  3. Делим массив replication timing'ов, найденных в предыдущем пункте, на равные бины:
  bin/split.py
  4. Делим весь интервал значений replication timing на несколько бинов.
  (BIN_START = [10 * i for i in range(9)]). Затем, вычисляем частоту мутаций
  в каждом бине (Делим количество мутаций в бине на количество APOBEC-мотивов):
  bin/frequency.py
  
* Исследуем зависимость наклона графика частоны мутаций от APOBEC-enrichment: bin/linearModel.R
  1. Строим линейную регрессию частоты APOGEC-мутаций от replication timing
  и для каждого семпла сохраняем коэффициент наклона регрессионной прямой
  2. Строим линейную регрессию коэффициента наклона, найденного в предыдущем
  пункте от APOBEC-enrichment

* Повторям последние два шага для всех сгеерированных комплиментарных пар сигнатур

Полезные ссылки (ссылки на ftp гитхаб не отображает, но их можно посмотреть в [сыром виде этого файла](https://raw.githubusercontent.com/Fa-bula/diploma/master/README.md?token=AJHajQHKS2BXy2uASf3yPNw8L5Hnk6dVks5XaFz1wA%3D%3D)):
* [Breast canser mutations](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/somatic_mutation_data/Breast/Breast_clean_somatic_mutations_for_signature_analysis_apr15.txt)
* [Breast catalog](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/mutational_catalogs/genomes/Breast/Breast_genomes_mutational_catalog_192_subs_with_strand_bias.txt "Список геномных семплов")
* [Lung canser mutations](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/somatic_mutation_data/Lung%20Adeno/Lung%20Adeno_clean_somatic_mutations_for_signature_analysis.txt)
* [Lung catalog](ftp://ftp.sanger.ac.uk/pub/cancer/AlexandrovEtAl/mutational_catalogs/genomes/Lung%20Adeno/Lung%20Adeno_genomes_mutational_catalog_192_subs_with_strand_bias.txt "Список геномных семплов")
* [Последняя подверсия 37-й версии генома](ftp://ftp.ncbi.nlm.nih.gov/genomes/Homo_sapiens/ARCHIVE/BUILD.37.3/Assembled_chromosomes/seq/ "Берем файлы вида hs_ref_GRCh37.p5_chr*.fa.gz")
* [replication timing for MCF-7 (breast)](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeUwRepliSeq/wgEncodeUwRepliSeqMcf7WaveSignalRep1.bigWig "breast replication timing")
* [replication timing for IMR90 (lung)](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeUwRepliSeq/wgEncodeUwRepliSeqImr90WaveSignalRep1.bigWig "lung replication timing")
* [bigWigToWig](ftp://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/ "Преобразование .bigWig -> .wig")
* [APOBEC enrichment](www.cell.com/cms/attachment/2040452923/2053963817/mmc2.xlsx "Степень влияния APOBEC на каждый из семплов")
