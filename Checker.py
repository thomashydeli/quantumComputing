from qiskit import *

class quantumMachineChecker: # status checker of a quantum machine, providing information including name, pending jobs, qubits, and version
    
    def __init__(self, simulator=False):
        self.simulator = simulator
                
    def __stringLookupMultiple(self, strings=[], target_string = ''): # perform the string comparisons in batch
        candidates = strings
        pointer = 0
        while (len(candidates) >= 1) & (pointer < len(target_string)):
            candidates = [c for c in candidates if c[pointer] == target_string[pointer]]
            pointer += 1
        return candidates
        
    def __printMachineInfo(self, backend, simulatorIndicator):
        qubits = 'simulated'
        version = ''
        prop = backend.properties()
        if not simulatorIndicator:
            qubits = len(prop.qubits)
            version = f' and version of {prop.backend_version}'
        print(f'{backend.name()}: {backend.status().pending_jobs} with {qubits} qubits' + version)
            
        
    def read_and_load(self, file=None):
        IBMQ.save_account(open(file).read(),overwrite=True) # save the account associated with an API key file
        IBMQ.load_account() # loading the account associated with the API key
        
        provider = IBMQ.ibmq.get_provider('ibm-q') # getting available actual quantum computers
        self.machine_backends = provider.backends()
        self.machines = [b.name().lower() for b in self.machine_backends] # getting all available quantum computers
        self.machines_split = [m.split('_') for m in self.machines] # splitting the codenames
        
        # following part performs algorithmic search for speeding up the lookups later
        # objective: save the places of simulators
        self.simulators = []
        for i,m in enumerate(self.machines_split):
            candidates = self.__stringLookupMultiple(m, 'simulator')
            if len(candidates) >= 1:
                self.simulators.append(i)
        
    def getInfo(self, name=None):
        simulatorIndicator = False
        if name is not None:
            name_split = name.split('_')
            candidates = self.__stringLookupMultiple(name_split, 'simulator')
            if len(candidates) >= 1:
                simulatorIndicator = True
                if not self.simulator:
                    raise ValueError('You are requesting info about a simulator, yet you turned display of simualtors off')
                    return
                
            candidates = [m+str(b) for b,m in enumerate(self.machines)]
            candidates = self.__stringLookupMultiple(candidates, name)
            if len(candidates) < 1:
                raise ValueError('No machine requested found, please check your spelling')
                return
            loc = int(candidates[0][-1]) # assuming machine names are unique
            requested_machine = self.machine_backends[loc]
            self.__printMachineInfo(requested_machine, simulatorIndicator)
            return
        
        simulator_pointer = 0
        for idx, mb in enumerate(self.machine_backends):
            simulatorIndicator = False
            if simulator_pointer < len(self.simulators):
                if idx == self.simulators[simulator_pointer]:
                    simulatorIndicator = True
                    simulator_pointer += 1
                    if not self.simulator:
                        continue
            self.__printMachineInfo(mb, simulatorIndicator)
        return