#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct Instruction {
    public:
    char opcode;
    int A;
    int B;
    int C;

    Instruction(char opcode, int A, int B, int C): opcode(opcode), A(A), B(B), C(C) {}  
};

int main() {
    vector<Instruction> instructions = vector<Instruction>();
    instructions.push_back(Instruction(1, 2, 16, 2));
    instructions.push_back(Instruction(9, 1, 0, 1));
    instructions.push_back(Instruction(9, 1, 3, 3));
    instructions.push_back(Instruction(2, 1, 3, 5));
    instructions.push_back(Instruction(15, 5, 4, 5));
    instructions.push_back(Instruction(0, 5, 2, 2));
    instructions.push_back(Instruction(1, 2, 1, 2));
    instructions.push_back(Instruction(0, 1, 0, 0));
    instructions.push_back(Instruction(1, 3, 1, 3));
    instructions.push_back(Instruction(12, 3, 4, 5));
    instructions.push_back(Instruction(0, 2, 5, 2));
    instructions.push_back(Instruction(9, 2, 6, 2));
    instructions.push_back(Instruction(1, 1, 1, 1));
    instructions.push_back(Instruction(12, 1, 4, 5));
    instructions.push_back(Instruction(0, 5, 2, 2));
    instructions.push_back(Instruction(9, 1, 1, 2));
    instructions.push_back(Instruction(2, 2, 2, 2));
    instructions.push_back(Instruction(1, 4, 2, 4));
    instructions.push_back(Instruction(2, 4, 4, 4));
    instructions.push_back(Instruction(2, 2, 4, 4));
    instructions.push_back(Instruction(3, 4, 11, 4));
    instructions.push_back(Instruction(1, 5, 6, 5));
    instructions.push_back(Instruction(2, 5, 2, 5));
    instructions.push_back(Instruction(1, 5, 19, 5));
    instructions.push_back(Instruction(0, 4, 5, 4));
    instructions.push_back(Instruction(0, 2, 0, 2));
    instructions.push_back(Instruction(9, 0, 7, 2));
    instructions.push_back(Instruction(8, 2, 6, 5));
    instructions.push_back(Instruction(2, 5, 2, 5));
    instructions.push_back(Instruction(0, 2, 5, 5));
    instructions.push_back(Instruction(2, 2, 5, 5));
    instructions.push_back(Instruction(3, 5, 14, 5));
    instructions.push_back(Instruction(2, 5, 2, 5));
    instructions.push_back(Instruction(0, 4, 5, 4));
    instructions.push_back(Instruction(9, 0, 7, 0));
    instructions.push_back(Instruction(9, 0, 3, 2));
    long ipBoundRegister = 2;
    
    long ip = 0;
    
    long registers[6] = {1, 0, 0, 0, 0, 0};

    string instructionNames[16] = {
	"addr",
	"addi",
	"mulr",
	"muli",
	"banr",
	"bani",
	"borr",
	"bori",
	"setr",
	"seti",
	"gtir",
	"gtri",
	"gtrr",
	"eqir"
	"eqri",
	"eqrr"
    };

    long oldRegister0 = registers[0];
    long size = instructions.size();
    while (true) {
	if (ip < 0 || ip >= size) {
	    break;
	}
	
	char nextOpcode = instructions[ip].opcode;
	int A = instructions[ip].A;
	int B = instructions[ip].B;
	int C = instructions[ip].C;

	// Write ip to bound register
	registers[ipBoundRegister] = ip;

	// Execute instruction
	if (nextOpcode == 0) {
	    registers[C] = registers[A] + registers[B];
	} else if (nextOpcode == 1) {
	    registers[C] = registers[A] + B;
	} else if (nextOpcode == 2) {
	    registers[C] = registers[A] * registers[B];	    
	} else if (nextOpcode == 3) {
	    registers[C] = registers[A] * B;	    
	} else if (nextOpcode == 4) {
	    registers[C] = registers[A] & registers[B];
	} else if (nextOpcode == 5) {
	    registers[C] = registers[A] & B;
	} else if (nextOpcode == 6) {
	    registers[C] = registers[A] | registers[B];
	} else if (nextOpcode == 7) {
	    registers[C] = registers[A] | B;
	} else if (nextOpcode == 8) {
	    registers[C] = registers[A];
	} else if (nextOpcode == 9) {
	    registers[C] = A;
	} else if (nextOpcode == 10) {
	    registers[C] = A > registers[B] ? 1 : 0;
	} else if (nextOpcode == 11) {
	    registers[C] = registers[A] > B ? 1 : 0;
	} else if (nextOpcode == 12) {
	    registers[C] = registers[A] > registers[B] ? 1 : 0;
	} else if (nextOpcode == 13) {
	    registers[C] = A == registers[B] ? 1 : 0;
	} else if (nextOpcode == 14) {
	    registers[C] = registers[A] == B ? 1 : 0;
	} else if (nextOpcode == 15) {
	    registers[C] = registers[A] == registers[B] ? 1 : 0;
	}

	// Write bound register back to ip
	ip = registers[ipBoundRegister] + 1;	
    }

    cout << registers[0] << " " << ip << endl;

    return 0;
}
