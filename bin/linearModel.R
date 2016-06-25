#!/usr/bin/Rscript
suppressMessages(library(lmtest))

## 1. Build linear regression: mutationProbability ~ replicationTiming
## 2. Build regression: coeff ~ APOBEC-enrichment,
## where coeff - regression coefficient from first part

args = commandArgs(trailingOnly = TRUE) # Command line arguments
if (length(args) != 3) {
    scriptName <- "./linearModel.R"
    sprintf("Usage: %s probabilityDir enrichment.txt outDir", scriptName)
} else {
    probabilityDir <- args[1]
    enrichmentFileName <- args[2]
    outDir <- args[3]
}

probabilityFiles <- list.files(probabilityDir)
coeffTable <- data.frame(Sample=character(), Coeff=integer())
for (fileName in probabilityFiles) {
    fullPath = file.path(probabilityDir, fileName)
    probabilityTable <- read.csv(fullPath, encoding="utf-8",
                                 header=T, sep='\t')
    model <- lm(probability ~ replicationTiming, data=probabilityTable)
    
    png(file.path(outDir, paste(fileName, "png", sep=".")))
    plot(probabilityTable$replicationTiming,
         probabilityTable$probability,
         main = paste("Sample", fileName),
         xlab = "replicationTiming",
         ylab = "APOBEC mutation probability")
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
mergedTable <- mergedTable[mergedTable$Sample != "PD4120a",]
write.table(mergedTable, file=file.path(outDir, "mergedTable"),
            sep='\t')
## finalModel <- lm(Coeff ~ APOBEC_enrich, data=mergedTable)
png(file.path(outDir, "!finalPlot.png"))
plot(mergedTable$Coeff,
     mergedTable$APOBEC_enrich,
     main = "final plot",
     xlab = "Coeff",
     ylab = "APOBEC-enrichment")
## abline(finalModel)
dev.off()
## mod <- lm(formula = mailing ~ orders + previous_mailing)
## previous <- mailing[length(mailing)]
## for (order_number in summer_orders) {
##     previous <- predict(mod, data.frame(orders = c(order_number), previous_mailing = c(previous)))
##     print(paste(order_number, previous, sep="\t"))
## }

