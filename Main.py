
import simpy
import random

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
        env.process(process(env, f"P{i}", RAM, CPU, time))