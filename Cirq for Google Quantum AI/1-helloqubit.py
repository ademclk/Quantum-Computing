import cirq

# Picking a qubit 
qubit = cirq.GridQubit(0, 0)

# Creating a circuit
circuit = cirq.Circuit( 
    cirq.X(qubit), # example for NOT gate.
    cirq.measure(qubit, key='m1') # Measurement 
)
print("Circuit: \n",circuit)

# Simulator 

simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results from simulator: \n",result)

"""
Output of the file

Circuit:  
(0, 0): ───X───M('m1')───

Results from simulator:
m1=11111111111111111111

"""