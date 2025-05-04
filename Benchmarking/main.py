import CompilersLogic.HybridMapperMQT.HybridMapperRunner as HybridMapper


if __name__ == '__main__':
     result = HybridMapper.run(r"CircuitsQASM/dj_nativegates_rigetti_qiskit_opt3_10.qasm",r"CompilersLogic\HybridMapperMQT\architectures\example.json")
     print(result)
