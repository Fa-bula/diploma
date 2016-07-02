#!/usr/bin/Rscript
suppressMessages(library(lmtest))

## 1. Build linear regression: mutationProbability ~ replicationTiming
## 2. Build regression: coeff ~ APOBEC-enrichment,
## where coeff - regression coefficient from first part

args = commandArgs(trailingOnly = TRUE) # Command line arguments
if (length(args) != 3) {
    scriptName <- "./linearModel.R"
    sprintf("Usage: %s frequencyDir enrichment.txt outDir", scriptName)
} else {
    frequencyDir <- args[1]
    enrichmentFileName <- args[2]
    outDir <- args[3]
}

probabilityFiles <- list.files(frequencyDir)
coeffTable <- data.frame(Sample=character(), Coeff=integer())
for (fileName in probabilityFiles) {
    fullPath = file.path(frequencyDir, fileName)
    frequencyTable <- read.csv(fullPath, encoding="utf-8",
                                 header=T, sep='\t')
    model <- lm(frequency ~ replicationTiming, data=frequencyTable)
    
    png(file.path(outDir, paste(fileName, "png", sep=".")))
    plot(frequencyTable$replicationTiming,
         frequencyTable$frequency,
         main = paste("Sample", fileName),
         xlab = "replicationTiming",
         ylab = "APOBEC mutation frequency")
    abline(model)
    dev.off()

    newData <- data.frame(Sample=fileName, Coeff=coef(model)[2])
    coeffTable <- rbind(coeffTable, newData)
}


enrichmentTable <- read.csv(enrichmentFileName, encoding="utf-8",
                            header=T, sep='\t')

mergedTable <- merge(enrichmentTable, coeffTable, by="Sample")
## Very strange sample
## TODO: check this sample
## mergedTable <- mergedTable[mergedTable$Sample != "PD4120a",]

## finalModel <- lm(Coeff ~ APOBEC_enrich, data=mergedTable)
png(file.path(outDir, "!finalPlot.png"))
plot(as.numeric(as.character(mergedTable$APOBEC_enrich)),
     mergedTable$Coeff,
     main = "final plot",
     xlab = "APOBEC-enrichment",
     ylab = "Coeff")
## abline(finalModel)
dev.off()
