import matplotlib.pyplot as plt
import re
FidelityPattern = re.compile(r'Fidelity:\s*([0-9]+(?:\.[0-9]+)?)')
FidelityListHybridMapper1 = []
FidelityListHybridMapper2 = []
FidelityListHybridMapper3 = []
FidelityListEnola = []
FidelityListDasAtom = []

TotalTimePattern = re.compile(r'TotalTime:\s*([0-9]+(?:\.[0-9]+)?)')
TotalTimeListHybridMapper1 = []
TotalTimeListHybridMapper2 = []
TotalTimeListHybridMapper3 = []
TotalTimeListEnola = []
TotalTimeListDasAtom = []

AllGateCountPattern = re.compile(r'AllGateCount:\s*([0-9]+)')
AllGateCountListHybridMapper1 = []
AllGateCountListHybridMapper2 = []
AllGateCountListHybridMapper3 = []
AllGateCountListEnola = []
AllGateCountListDasAtom = []

CZGateCountPattern = re.compile(r'CZGateCount:\s*([0-9]+(?:\.[0-9]+)?)')
CZGateCountListHybridMapper1 = []
CZGateCountListHybridMapper2 = []
CZGateCountListHybridMapper3 = []
CZGateCountListEnola = []
CZGateCountListDasAtom = []

def fillLists(hybridMapperFile1, hybridMapperFile2, hybridMapperFile3, enolaFile, dasAtomFile):
    for line in hybridMapperFile1:
        if "FAILURE" in line:
            FidelityListHybridMapper1.append(None)
            TotalTimeListHybridMapper1.append(None)
            AllGateCountListHybridMapper1.append(None)
            CZGateCountListHybridMapper1.append(None)
            continue

        match = FidelityPattern.search(line)
        if match:
            value = float(match.group(1))
            FidelityListHybridMapper1.append(value)

        match = TotalTimePattern.search(line)
        if match:
            value = float(match.group(1))
            TotalTimeListHybridMapper1.append(value)

        match = AllGateCountPattern.search(line)
        if match:
            value = int(match.group(1))
            AllGateCountListHybridMapper1.append(value)

        match = CZGateCountPattern.search(line)
        if match:
            value = int(float(match.group(1)))
            CZGateCountListHybridMapper1.append(value)

    for line in hybridMapperFile2:
        if "FAILURE" in line:
            FidelityListHybridMapper2.append(None)
            TotalTimeListHybridMapper2.append(None)
            AllGateCountListHybridMapper2.append(None)
            CZGateCountListHybridMapper2.append(None)
            continue

        match = FidelityPattern.search(line)
        if match:
            value = float(match.group(1))
            FidelityListHybridMapper2.append(value)

        match = TotalTimePattern.search(line)
        if match:
            value = float(match.group(1))
            TotalTimeListHybridMapper2.append(value)

        match = AllGateCountPattern.search(line)
        if match:
            value = int(match.group(1))
            AllGateCountListHybridMapper2.append(value)

        match = CZGateCountPattern.search(line)
        if match:
            value = int(float(match.group(1)))
            CZGateCountListHybridMapper2.append(value)

    for line in hybridMapperFile3:
        if "FAILURE" in line:
            FidelityListHybridMapper3.append(None)
            TotalTimeListHybridMapper3.append(None)
            AllGateCountListHybridMapper3.append(None)
            CZGateCountListHybridMapper3.append(None)
            continue

        match = FidelityPattern.search(line)
        if match:
            value = float(match.group(1))
            FidelityListHybridMapper3.append(value)

        match = TotalTimePattern.search(line)
        if match:
            value = float(match.group(1))
            TotalTimeListHybridMapper3.append(value)

        match = AllGateCountPattern.search(line)
        if match:
            value = int(match.group(1))
            AllGateCountListHybridMapper3.append(value)

        match = CZGateCountPattern.search(line)
        if match:
            value = int(float(match.group(1)))
            CZGateCountListHybridMapper3.append(value)

    for line in enolaFile:
        if "FAILURE" in line:
            FidelityListEnola.append(None)
            TotalTimeListEnola.append(None)
            AllGateCountListEnola.append(None)
            CZGateCountListEnola.append(None)
            continue

        match = FidelityPattern.search(line)
        if match:
            value = float(match.group(1))
            FidelityListEnola.append(value)

        match = TotalTimePattern.search(line)
        if match:
            value = float(match.group(1))
            TotalTimeListEnola.append(value)

        match = AllGateCountPattern.search(line)
        if match:
            value = int(match.group(1))
            AllGateCountListEnola.append(value)

        match = CZGateCountPattern.search(line)
        if match:
            value = int(float(match.group(1)))
            CZGateCountListEnola.append(value)

    for line in dasAtomFile:
        if "FAILURE" in line:
            FidelityListDasAtom.append(None)
            TotalTimeListDasAtom.append(None)
            AllGateCountListDasAtom.append(None)
            CZGateCountListDasAtom.append(None)
            continue

        match = FidelityPattern.search(line)
        if match:
            value = float(match.group(1))
            FidelityListDasAtom.append(value)

        match = TotalTimePattern.search(line)
        if match:
            value = float(match.group(1))
            TotalTimeListDasAtom.append(value)

        match = AllGateCountPattern.search(line)
        if match:
            value = int(match.group(1))
            AllGateCountListDasAtom.append(value)

        match = CZGateCountPattern.search(line)
        if match:
            value = int(float(match.group(1)))
            CZGateCountListDasAtom.append(value)

def plotQFTAllGateCount():
    plt.figure()

    xHybridMapper1 = range(2, len(AllGateCountListHybridMapper1[:30]) + 2)
    yHybridMapper1 = AllGateCountListHybridMapper1[:30]
    plt.plot(xHybridMapper1, yHybridMapper1, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperOnlyShuttling')

    xHybridMapper2 = range(2, len(AllGateCountListHybridMapper2[:30]) + 2)
    yHybridMapper2 = AllGateCountListHybridMapper2[:30]
    plt.plot(xHybridMapper2, yHybridMapper2, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperMixed')

    xHybridMapper3 = range(2, len(AllGateCountListHybridMapper3[:30]) + 2)
    yHybridMapper3 = AllGateCountListHybridMapper3[:30]
    plt.plot(xHybridMapper3, yHybridMapper3, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperOnlySwaps')

    xEnola = range(2, len(AllGateCountListEnola) + 2)
    yEnola = AllGateCountListEnola
    plt.plot(xEnola, yEnola, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='Enola')

    # restrict dasAtom to 30
    AllGateCountListDasAtom30 = AllGateCountListDasAtom[:30]
    xDasAtom = range(2, len(AllGateCountListDasAtom30) + 2)
    yDasAtom = AllGateCountListDasAtom30
    plt.plot(xDasAtom, yDasAtom, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='DasAtom')

    #plt.yscale('log')
    plt.title('QFT - Architecture1')
    plt.xlabel('QubitAmount')
    plt.ylabel('AllGateCount')
    plt.grid(True)
    plt.legend()
    plt.savefig('Plots/AllGateCountArch2.png', dpi=300, bbox_inches='tight')

def plotQFTCZGateCount():
    plt.figure()

    xHybridMapper1 = range(2, len(CZGateCountListHybridMapper1[:30]) + 2)
    yHybridMapper1 = CZGateCountListHybridMapper1[:30]
    plt.plot(xHybridMapper1, yHybridMapper1, marker='o', markersize=1,linewidth=0.5, linestyle='-',
             label='HybridMapperOnlyShuttling')

    xHybridMapper2 = range(2, len(CZGateCountListHybridMapper2[:30]) + 2)
    yHybridMapper2 = CZGateCountListHybridMapper2[:30]
    plt.plot(xHybridMapper2, yHybridMapper2, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperMixed')

    xHybridMapper3 = range(2, len(CZGateCountListHybridMapper3[:30]) + 2)
    yHybridMapper3 = CZGateCountListHybridMapper3[:30]
    plt.plot(xHybridMapper3, yHybridMapper3, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperOnlySwaps')

    xEnola = range(2, len(CZGateCountListEnola) + 2)
    yEnola = CZGateCountListEnola
    plt.plot(xEnola, yEnola, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='Enola')

    # restrict dasAtom to 30
    CZGateCountListDasAtom30 = CZGateCountListDasAtom[:30]
    xDasAtom = range(2, len(CZGateCountListDasAtom30) + 2)
    yDasAtom = CZGateCountListDasAtom30
    plt.plot(xDasAtom, yDasAtom, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='DasAtom')

    #plt.yscale('log')
    plt.title('QFT - Architecture1')
    plt.xlabel('QubitAmount')
    plt.ylabel('CZGateCount')
    plt.grid(True)
    plt.legend()
    plt.savefig('Plots/CZGateCountArch2.png', dpi=300, bbox_inches='tight')

def plotQFTTotalTime():
    plt.figure()

    xHybridMapper1 = range(2, len(TotalTimeListHybridMapper1[:30]) + 2)
    yHybridMapper1 = TotalTimeListHybridMapper1[:30]
    plt.plot(xHybridMapper1, yHybridMapper1, marker='o', markersize=1,linewidth=0.5, linestyle='-',
             label='HybridMapperOnlyShuttling')

    xHybridMapper2 = range(2, len(TotalTimeListHybridMapper2[:30]) + 2)
    yHybridMapper2 = TotalTimeListHybridMapper2[:30]
    plt.plot(xHybridMapper2, yHybridMapper2, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperMixed')

    xHybridMapper3 = range(2, len(TotalTimeListHybridMapper3[:30]) + 2)
    yHybridMapper3 = TotalTimeListHybridMapper3[:30]
    plt.plot(xHybridMapper3, yHybridMapper3, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperOnlySwaps')

    xEnola = range(2, len(TotalTimeListEnola) + 2)
    yEnola = TotalTimeListEnola
    plt.plot(xEnola, yEnola, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='Enola')

    # restrict dasAtom to 30
    TotalTimeListDasAtom30 = TotalTimeListDasAtom[:30]
    xDasAtom = range(2, len(TotalTimeListDasAtom30) + 2)
    yDasAtom = TotalTimeListDasAtom30
    plt.plot(xDasAtom, yDasAtom, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='DasAtom')
    #plt.yscale('log')
    plt.title('QFT - Architecture1')
    plt.xlabel('QubitAmount')
    plt.ylabel('CompileTime s')
    plt.grid(True)
    plt.legend()
    plt.savefig('Plots/CompileTimeArch2.png', dpi=300, bbox_inches='tight')

def plotQFTFidelity():
    plt.figure()

    xHybridMapper1 = range(2, len(FidelityListHybridMapper1[:30]) + 2)
    yHybridMapper1 = FidelityListHybridMapper1[:30]
    plt.plot(xHybridMapper1, yHybridMapper1, marker='o', markersize=1,linewidth=0.5, linestyle='-',
             label='HybridMapperOnlyShuttling')

    xHybridMapper2 = range(2, len(FidelityListHybridMapper2[:30]) + 2)
    yHybridMapper2 = FidelityListHybridMapper2[:30]
    plt.plot(xHybridMapper2, yHybridMapper2, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperMixed')

    xHybridMapper3 = range(2, len(FidelityListHybridMapper3[:30]) + 2)
    yHybridMapper3 = FidelityListHybridMapper3[:30]
    plt.plot(xHybridMapper3, yHybridMapper3, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='HybridMapperOnlySwaps')

    xEnola = range(2, len(FidelityListEnola) + 2)
    yEnola = FidelityListEnola
    plt.plot(xEnola, yEnola, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='Enola')

    # restrict dasAtom to 30
    FidelityListDasAtom30 = FidelityListDasAtom[:30]
    xDasAtom = range(2, len(FidelityListDasAtom30) + 2)
    yDasAtom = FidelityListDasAtom30
    plt.plot(xDasAtom, yDasAtom, marker='o', markersize=1,linewidth=0.5, linestyle='-', label='DasAtom')

    #plt.yscale('log')
    plt.title('QFT - Architecture1')
    plt.xlabel('QubitAmount')
    plt.ylabel('Fidelity')
    plt.grid(True)
    plt.legend()
    plt.savefig('Plots/FidelityArch2.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    with open('RESULTS/HybridMapperResultsParameter1.txt', 'r', encoding='utf-8') as hybridMapperFile1, \
            open('RESULTS/HybridMapperResultsParameter2.txt', 'r', encoding='utf-8') as hybridMapperFile2, \
            open('RESULTS/HybridMapperResultsParameter3.txt', 'r', encoding='utf-8') as hybridMapperFile3, \
            open('RESULTS/EnolaResults.txt', 'r', encoding='utf-8') as enolaFile, \
            open('RESULTS/DasAtomResults.txt', 'r', encoding='utf-8') as dasAtomFile:

        hybridMapper1 = hybridMapperFile1.read()
        hybridMapper2 = hybridMapperFile2.read()
        hybridMapper3 = hybridMapperFile3.read()
        enola = enolaFile.read()
        dasAtom = dasAtomFile.read()
        hybridMapperFile1.seek(0)
        hybridMapperFile2.seek(0)
        hybridMapperFile3.seek(0)
        enolaFile.seek(0)
        dasAtomFile.seek(0)
        fillLists(hybridMapperFile1, hybridMapperFile2, hybridMapperFile3, enolaFile, dasAtomFile)

        #plot QFT
        if True:
            plotQFTAllGateCount()
            plotQFTCZGateCount()
            plotQFTTotalTime()
            plotQFTFidelity()