import cirq
from cirq.circuits import circuit
import cirq_google
    # Qubits in Cirq
        # Naming qubits can be useful for algorithms.
q0 = cirq.NamedQubit('source')
q1 = cirq.NamedQubit('target')

        # Line qubits can be created individually.
q3 = cirq.LineQubit(3)

        # Line qubits can be created in a range.
q0, q1, q2 = cirq.LineQubit.range(3)

        # Grid qubits
q4_5 = cirq.GridQubit(4,5)

        # Or created in bulk in a square
        # This line will create 16 qubits from (0,0) to (3,3)
qubits = cirq.GridQubit.square(4)

print(cirq_google.Foxtail)
"""Output:
(0, 0)───(0, 1)───(0, 2)───(0, 3)───(0, 4)───(0, 5)───(0, 6)───(0, 7)───(0, 8)───(0, 9)───(0, 10)
│        │        │        │        │        │        │        │        │        │        │
│        │        │        │        │        │        │        │        │        │        │
(1, 0)───(1, 1)───(1, 2)───(1, 3)───(1, 4)───(1, 5)───(1, 6)───(1, 7)───(1, 8)───(1, 9)───(1, 10)
"""
    # Gates and operations in Cirq
"""
    A Gate is an effect that can be applied to set of qubits.
    An Operation is a gate applied to set of qubits.
"""
        # For example
not_gate = cirq.CNOT
pauli_z = cirq.Z
        # Square root of gates
sqrt_x_gate = cirq.X**0.5
        # Some gates can take parameters
sqrt_sqrt_y = cirq.YPowGate(exponent = 0.25)
        # Operations example
q0, q1 = cirq.LineQubit.range(2)
z_op = cirq.Z(q0)
not_op = cirq.CNOT(q0, q1)
sqrt_iswap_op = cirq.SQRT_ISWAP(q0, q1)

    # Circuits and moments
"""
Operation -- Moment -- Circuit

Cirq will attemp to slide your operation into earliest possible
moment when you insert it.
"""
circuit = cirq.Circuit()
        # Append to create a circuit with 3 qubits each have a hadamard gate.
circuit.append(cirq.H(q) for q in cirq.LineQubit.range(3))
print(circuit)
""" Output:
0: ───H───

1: ───H───

2: ───H───

"""
        # Creating a circuit directly
print(cirq.Circuit(cirq.SWAP(q, q+1) for q in cirq.LineQubit.range(3)))
"""Output:
0: ───x───────────
      │
1: ───x───x───────
          │
2: ───────x───x───
              │
3: ───────────x───

"""
        # Create a circuit with 3 hadamard gates no overlap
print(cirq.Circuit(cirq.Moment([cirq.H(q)]) for q in cirq.LineQubit.range(3)))
"""Output:
0: ───H───────────

1: ───────H───────

2: ───────────H───

"""
    # Circuits and devices
        # When using real quantum devices is that there are often 
        # hardware constraints on the circuit. Creating a circuit 
        # with a Device will allow you to capture some of these requirements.
q0 = cirq.GridQubit(0, 0)
q1 = cirq.GridQubit(0, 1)
q2 = cirq.GridQubit(0, 2)
adjacent_op = cirq.CZ(q0, q1)
nonadjacent_op = cirq.CZ(q0, q2)

free_circuit = cirq.Circuit() # Unconstrained circuit with no device
                              # Both operations are allowed.
free_circuit.append(adjacent_op)
free_circuit.append(nonadjacent_op)
print("Unconstrained device")
print(free_circuit)
"""Output
Unconstrained device
(0, 0): ───@───@───
           │   │
(0, 1): ───@───┼───
               │
(0, 2): ───────@───

"""
print("Foxtail device:")
foxtail_circuit = cirq.Circuit(device=cirq_google.Foxtail)
foxtail_circuit.append(adjacent_op)
try:
    #This is not allowed and going to throw exception
    foxtail_circuit.append(nonadjacent_op)
except ValueError as e:
    print('Not allowed %s' % e)
"""Output
Foxtail device:
Not allowed Non-local interaction: 
cirq.CZ(cirq.GridQubit(0, 0), cirq.GridQubit(0, 2)).

"""
    # Simulation
        # initialize via cirq.Simulator(). Can be used for 20 qubits.

# Circuit to generate a Bell State
# 1/sqrt(2) * ( |00⟩ + |11⟩ )
bell_circuit = cirq.Circuit()
q0, q1 = cirq.LineQubit.range(2)
bell_circuit.append(cirq.H(q0))
bell_circuit.append(cirq.CNOT(q0, q1))

simulator = cirq.Simulator()
print("Simulating the circuit:")
result = simulator.simulate(bell_circuit)
print(result)
print()
# We need to add measurement at the end
bell_circuit.append(cirq.measure(q0, q1, key='result'))

print('Sampling the circuit: ')
sample = simulator.run(bell_circuit, repetitions=1024)
print(sample.histogram(key='result'))
"""Output
Simulating the circuit:
measurements: (no measurements)
output vector: 0.707|00⟩ + 0.707|11⟩

Sampling the circuit:
Counter({3: 517, 0: 507})

"""