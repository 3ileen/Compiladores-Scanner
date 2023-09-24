#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_set>

using namespace std;

enum TokenType {
    LETTER,
    NUMBER,
    RESERVED_WORD,
    ASSIGN_OP,
    START_BLOCK,
    END_BLOCK,
    EOP,
    UNKNOWN,
    FUNCTION
};

bool isLetter(const string& token) {
    return isalpha(token[0]);
}

bool isNumber(const std::string& token) {
    return isdigit(token[0]);
}

bool isReservedWord(const string& token, const unordered_set<string>& reserved_words) {
    return reserved_words.find(token) != reserved_words.end();
}

void getTokenType(const std::string& token,
                           const unordered_set<string>& reserved_words,
                           const unordered_set<string>& assign_ops,
                           const unordered_set<string>& start_blocks,
                           const unordered_set<string>& end_blocks,
                           const unordered_set<string>& eops,
                           TokenType& type) {
    if (isReservedWord(token, reserved_words)) {
        type = RESERVED_WORD;}
    else if (isLetter(token)) {

        if (token == "function") {
            type = FUNCTION;
        } else {
            type = LETTER;
        }
    } else if (isNumber(token)) {
        type = NUMBER;
    } else if (assign_ops.find(token) != assign_ops.end()) {
        type = ASSIGN_OP;
    } else if (start_blocks.find(token) != start_blocks.end()) {
        type = START_BLOCK;
    } else if (end_blocks.find(token) != end_blocks.end()) {
        type = END_BLOCK;
    } else if (eops.find(token) != eops.end()) {
        type = EOP;
    } else {
        type = UNKNOWN;
    }
}

int main() {
    unordered_set<string> reserved_word = { "int", "char", "str", "bubble", "fifi", "blob" };
    unordered_set<string> assign_op = { "|" };
    unordered_set<string> start_block = { "(*", "{*" };
    unordered_set<string> end_block = { "*)", "*}" };
    unordered_set<string> eop = { "|*" };
    unordered_set<string> function = {"cosmos"};

    ifstream inputFile("C:\\Users\\len\\CLionProjects\\Scanner\\infinity.txt");
    if (!inputFile.is_open()) {
        cerr << "Error: No se pudo abrir el archivo de entrada." << endl;
        return 1;
    }

    string token;
    int line = 1;
    int position = 1;

    cout << "INFO SCAN - Start scanning. . ." << endl;

    while (inputFile >> token) {
        TokenType type = UNKNOWN;
        getTokenType(token, reserved_word, assign_op, start_block, end_block, eop, type);

        cout << "DEBUG SCAN - " << token << " [" << type << "] encontrado en (" << line << ":" << position << ")\n";

        switch (type) {
            case LETTER:
                cout << "Es una letra." << endl;
                break;
            case NUMBER:
                cout << "Es un número." << endl;
                break;
            case RESERVED_WORD:
                cout << "Es una palabra reservada." << endl;
                break;
            case ASSIGN_OP:
                cout << "Es un operador de asignación." << endl;
                break;
            case START_BLOCK:
                cout << "Es un bloque de inicio." << endl;
                break;
            case END_BLOCK:
                cout << "Es un bloque de fin." << endl;
                break;
            case EOP:
                cout << "Es el fin de programa." << endl;
                break;
            case FUNCTION:
                cout << "Es la palabra reservada 'function'." << endl;
                break;
            default:
                cout << "Token desconocido." << endl;
        }

        if (token == "\n") {
            line++;
            position = 1;
        } else {
            position += token.length() + 1;
        }
    }


    cout << "INFO SCAN - Completado sin errores" << endl;

    inputFile.close();
    return 0;
}
