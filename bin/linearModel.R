#!/usr/bin/Rscript
suppressMessages(library(lmtest))

## 1. Build linear regression: mutationProbability ~ replicationTiming
## 2. Build regression: coeff ~ APOBEC-enrichment,
## where coeff - regression coefficient from first part

args = commandArgs(trailingOnly = TRUE) # Command line arguments
if (length(args) != 4) {
    scriptName <- "./linearModel.R"
    sprintf("Usage: %s frequencyDir enrichment.txt outDir motif", scriptName)
} else {
    frequencyDir <- args[1]
    enrichmentFileName <- args[2]
    outDir <- args[3]
    motif <- args[4]
}

probabilityFiles <- list.files(frequencyDir)
coeffTable <- data.frame(Sample=character(), Coeff=integer())
for (fileName in probabilityFiles) {
    fullPath = file.path(frequencyDir, fileName)
    frequencyTable <- read.csv(fullPath, encoding="utf-8",
                                 header=T, sep='\t')
    frequencyTable$bin_middle = (frequencyTable$bin_start + frequencyTable$bin_end) / 2
    model <- lm(frequency ~ bin_middle, data=frequencyTable)
    ## Use glm
    
    ## png(file.path(outDir, paste(fileName, "png", sep=".")))
    plot(as.table(setNames(frequencyTable$frequency, frequencyTable$bin_middle)),
         main=paste("Sample", fileName),
         xlab = "replication timing",
         ylab = "APOBEG mutation frequency",
         xaxt="n")
    axis(side=1, at=seq(10, 90, 10), labels=NULL)
    ## plot(frequencyTable$replicationTiming,
    ##      frequencyTable$frequency,
    ##      main = paste("Sample", fileName),
    ##      xlab = "replicationTiming",
    ##      ylab = "APOBEC mutation frequency")
    
    abline(model)
    dev.off()

    newData <- data.frame(Sample=fileName, Coeff=coef(model)[2])
    coeffTable <- rbind(coeffTable, newData)
}


enrichmentTable <- read.csv(enrichmentFileName, encoding="utf-8",
                            header=T, sep='\t')

mergedTable <- merge(enrichmentTable, coeffTable, by="Sample")
## write.csv(mergedTable, 'merged')
## Very strange sample
## TODO: check this sample
## mergedTable <- mergedTable[mergedTable$Sample != "PD4120a",]

finalModel <- lm(Coeff ~ APOBEC_enrich, data=mergedTable)
png(file.path(outDir, paste(motif, "png", sep=".")))
plot(as.numeric(as.character(mergedTable$APOBEC_enrich)),
     mergedTable$Coeff,
     main = motif,
     xlab = "APOBEC-enrichment",
     ylab = "Coeff")
abline(finalModel)
sprintf("motif: %s", motif)
summary(finalModel)$coef[,4][2]
summary(finalModel)$coef[,1][2]
## summary(finalModel)
error <- finalModel$residuals
sprintf("RMSE: %g", sqrt(mean(error^2)))
dev.off()
