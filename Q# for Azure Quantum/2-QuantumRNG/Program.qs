/// # Can build & run the code via dotnet run first
/// then run via dotnet run --no-build to skip building phase
namespace qrng {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement; // Need this for measurement
    open Microsoft.Quantum.Math; // provides BitSizeI function
    open Microsoft.Quantum.Convert; // provides ResultArrayAsInt converts bit string to + integer
  
    operation GenerateRandomBit() : Result {
        // Allocating a qubit.
        use q = Qubit();
        // Hadamard gate puts qubit to superposition.
        H(q);
        // Measure
        return M(q);
    }
    // Generates random numbers with repeat until.
    operation RandomNumberInRange (max : Int) : Int{
        mutable output = 0; // Mutable variable means change during computation use set to change values.
        repeat{
            mutable bits = [Zero, size = 0];
            for idxBit in 1..BitSizeI(max){
                set bits +=[GenerateRandomBit()];
            }
            set output = ResultArrayAsInt(bits); // requires a QPU
        }until(output<=max);
        return output;
    }
      @EntryPoint()
      operation SampleRandomNumber() : Int{
          let max =50; // Let variable means doesn't change during computation.
          Message($"A random number between 0 and {max}: ");
          return RandomNumberInRange(max);
      }
}
