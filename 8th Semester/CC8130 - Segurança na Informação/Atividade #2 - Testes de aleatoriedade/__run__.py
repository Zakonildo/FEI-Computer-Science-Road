import monobit_test_eval as mt
import poker_test_eval as pt
import run_test_eval as rt
import long_run_test_eval as lrt
import getKeys as gk

def printApprovement(testName, testResult):
    if(testResult[-1] == True):
        print(testName + ": APROVADO.")
    else:
        print(testName + ": REPROVADO.")

def main():
    keys = gk.getKeysByLine("Chaves de Criptografia 2022.S1.txt")

    for i in range(0, len(keys)):
        print("---------------------------------------------")
        print("RESULTADO DA CHAVE", i+1)
        print()

        monobitResults = mt.solve(keys[i])
        printApprovement("THE MONOBIT TEST" , monobitResults)
        print("Contagem de Monobit: %d\n" % monobitResults[0])

        pokerResults = pt.solve(keys[i])
        printApprovement("THE POKER TEST" , pokerResults)
        for j in pokerResults[1].keys():
            print("Contagem de %s: %d" % (j, pokerResults[1][j]))
        print("Resultado Final: %.2f\n" % pokerResults[0])

        runResults = rt.solve(keys[i])
        printApprovement("THE RUN TEST" , runResults)
        for j in runResults[0].keys():
            if(j != 6):
                print("Sequência de tamanho %d:  0's = %5d | 1's = %5d" % (j, runResults[0][j], runResults[1][j]))
            else:
                print("Sequência de tamanho %d+: 0's = %5d | 1's = %5d" % (j, runResults[0][j], runResults[1][j]))
        print()

        longRunResults = lrt.solve(keys[i])
        printApprovement("THE LONG RUN TEST" , longRunResults)
        print("---------------------------------------------")

if(__name__ == "__main__"):
    main()