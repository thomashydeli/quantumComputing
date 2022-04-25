# checker example
from Checker import quantumMachineChecker

# check all machine
checker = quantumMachineChecker(simulator = True)
checker.read_and_load('apikey')
checker.getInfo()

# check a specific machine defined by user
simulator = input('Please input whehter you want to check simulator or not:')
machine_name = input('Please input the desired machine name for status checking:')
checker = quantumMachineChecker(simulator = simulator)
checker.read_and_load('apikey')
checker.getInfo(machine_name)