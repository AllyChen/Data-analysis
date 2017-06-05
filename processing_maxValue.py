import os
#get the max value of table
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ...
def exportTheBestChromosome():

    run = DataFrame()
    # Get input file
    for i in range(1, numRun + 1, 1):
        # Read file.
        fitnessScores = pd.read_csv(inputFolderName + "experiment_" + str(i) + ".csv")
        for ng in range(0, numGeneration, 1):
            locals()['fitnessScores_run' + str(i) + '_gen' + str(ng + 1)] = fitnessScores[ng * chromosomeCount : ng * chromosomeCount + chromosomeCount]
        # Create table that stores the best chromosome each generation.
        newColumns = list(fitnessScores)[0 : len(fitnessScores.columns)]
        newColumns.extend(['run'])
        bestChromosomes = DataFrame(columns = newColumns)
        # Get the max value from every Generations.
        # e.g. 100 numGeneration has 100 best chromosome each generation.
        for ng in range(0, numGeneration, 1):
            #Copy the fitnessScores each generation
            fitnessScoresInOneGeneration = locals()['fitnessScores_run' + str(i) + '_gen' + str(ng + 1)]
            #Get the index of max value from fitnessScores each generation
            indexOfMaxValue = fitnessScoresInOneGeneration['all'].argmax() # % chromosomeCount
            bestChromosome = fitnessScoresInOneGeneration.loc[[indexOfMaxValue]]
            bestChromosome['run'] = i
            bestChromosomes = bestChromosomes.append(bestChromosome)
        run = pd.concat([run, bestChromosomes])

    # output result table
    run.to_csv(outputFolderName + "bestChromosome.csv")

def plotGenerations():
    plt.figure()
    # Read file.
    data = pd.read_csv(outputFolderName + "bestChromosome.csv")
    # Get input file
    for i in range(1, numRun + 1, 1):
        bestChromosomes = data[data['run'] == i]['all']
        plt.plot(range(len(bestChromosomes)), bestChromosomes, 'b-')

    plt.legend(['generation'])
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.savefig(outputFolderName + 'result.png')

# Our program.
if __name__ == "__main__":
    # Number of file.
    numRun = 100
    # Num of generation.
    numGeneration = 101
    # Count of chromosome each generation.
    chromosomeCount = 100
    # The path of dataset.
    nameOfRun = "Export_100_100"
    inputFolderName  = "./CreVox/" + nameOfRun + "/"
    outputFolderName = "./CreVox/BestChromosome_" + nameOfRun + "/"

    if not os.path.exists(outputFolderName):
        os.makedirs(outputFolderName)
    else:
        for file in os.listdir(outputFolderName):
            os.remove(outputFolderName + file)
    # ...
    exportTheBestChromosome()
    # ...
    plotGenerations()
