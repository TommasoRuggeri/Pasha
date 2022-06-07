import hashlib as hl
import argparse as ap
import sys
from argparse import RawTextHelpFormatter
import textwrap

def LookForTheAlgorithm(algo:str, fileLines:str, hashedPass:str, algosThatNeedsLengthProp:list[str]) -> bool:
    for line in fileLines:
               h = hl.new(algo)
               h.update(line.strip("\n").encode())
               if algo in algosThatNeedsLengthProp:
                   passw = h.hexdigest(h.digest_size)
               else:
                    passw = h.hexdigest()
               if passw == hashedPass:
                   print(f"password found: {line}hash algorithm: {h.name}")
                   return True
    return False

def ReverseHash(filePath:str, passwordHashPath:str,interpreterMode=False, algorithmName= None):

    pass_found = False

    algos_that_needs_length = ["shake_128","shake_256"]
    try:
        words_file = open(filePath, 'r', encoding="utf-8")
    except:
        print("wordlist not found")
        sys.exit(1)
    try:
        passwordHash = open(passwordHashPath, 'r', encoding="utf-8").read()
    except:
        print("password file not found")
        sys.exit(1)
    lines = words_file.readlines()

    if(algorithmName != None):
        if algorithmName in hl.algorithms_available or algorithmName in hl.algorithms_guaranteed:
            pass_found = LookForTheAlgorithm(algorithmName, lines, passwordHash, algos_that_needs_length)
        else:
            print("{} is not recognized as an hashing algorithm. Type -h or --help to list all availables algorithms".format(algorithmName))
            sys.exit(1)

    else:
        if interpreterMode:
            print("trying with interpreter mode...\n")
            for algorithm in hl.algorithms_available:
                if pass_found == False:
                    pass_found = LookForTheAlgorithm(algorithm, lines, passwordHash, algos_that_needs_length)
                else:
                    break
        else:
            print("trying with guaranteed mode...\n")
            for algorithm in hl.algorithms_guaranteed:
                if pass_found == False:
                    pass_found = LookForTheAlgorithm(algorithm, lines, passwordHash, algos_that_needs_length)
                else:
                    break
    if pass_found == False:
            print("Password not found, try with another wordlist or try run with intepreter mode [-i]")

def GenerateAlgorithmsList():
    guaranteed = "defult Algorithms: "
    interp_depend = "interpreter dependens algorithms [-i]: "
    for element in hl.algorithms_guaranteed:
        guaranteed += element + " "
    for element in hl.algorithms_available:
        interp_depend += element + " "
    return "\n" + guaranteed + "\n \n" + interp_depend + "\n"
 
parser = ap.ArgumentParser(description="Pasha is a software created for trying to reverse an hash", usage='''python pasha.py -p [password file] -w [wordlist]
       type "python pasha.py -h" for help\n''',
 formatter_class=RawTextHelpFormatter,epilog=textwrap.dedent(GenerateAlgorithmsList()))
# parser.print_help()
parser.add_argument("-p", type=str, help="path to the file that contains the hash to reverse (required)", required=True)
parser.add_argument('-w', type=str, help="path to wordlist (required)", required=True)
parser.add_argument("-a", type=str, help="Algorithm of the hash",required=False)
parser.add_argument("-i", action="store_true",default=False, help="Algorthims that are supported by your python interpreter",required=False)

args = parser.parse_args()

if args.p != None and args.w != None:
        ReverseHash(args.w, args.p,args.i, args.a)