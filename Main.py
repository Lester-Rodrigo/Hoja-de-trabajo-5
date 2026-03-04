
import simpy
import random
import statistics
import matplotlib.pyplot as plt

Seed = 30
AvailableRAM = 100
AvailableCPU = 1
InstructionsPerLoop = 3
CPUTimePerLoop = 1

random.seed(Seed)

def process(env, RAM, CPU, time):
    
    StartTime = env.now
    memory = random.randint(1, 10)
    instructions = random.randint(1, 10)

    yield RAM.get(memory)

    while instructions > 0:

        with CPU.request() as req:
            yield req
            yield env.timeout(CPUTimePerLoop)

            executeProcess = min(InstructionsPerLoop, instructions)
            instructions -= executeProcess

        if instructions > 0:
            numero = random.randint(1, 2)

            if numero == 1:
                yield env.timeout(1)

    yield RAM.put(memory)

    TotalTime = env.now - StartTime
    time.append(TotalTime)


def processGenerator(env, RAM, CPU, interval, numOfProcess, time):
    for i in range(numOfProcess):
        yield env.timeout(random.expovariate(1.0 / interval))
        env.process(process(env, RAM, CPU, time))
        
def runSimulation (numOfProcess, interval, RAM=100, availableCPU=1, instructionsPerLoop=3):

    global InstructionsPerLoop
    InstructionsPerLoop = instructionsPerLoop

    env = simpy.Environment()
    RAM = simpy.Container(env, init=RAM, capacity=RAM)
    CPU = simpy.Resource(env, capacity=availableCPU)

    time = []

    env.process(processGenerator(env, RAM, CPU, interval, numOfProcess, time))
    env.run()

    averageTime = statistics.mean(time)
    desviation = statistics.stdev(time)

    return averageTime, desviation

processList = [25, 50, 100, 150, 200]
interval = 10

averageTimeList = []

for n in processList:
    averageTime, desviation = runSimulation(n, interval)
    print(f"Procesos: {n}")
    print(f"Promedio: {averageTime:.2f}")
    print(f"Desviación estándar: {desviation:.2f}")
    print("-----------------------------")
    averageTimeList.append(averageTime)


# Gráfica
plt.plot(processList, averageTimeList)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio")
plt.title("Procesos vs Tiempo Promedio")
plt.show()