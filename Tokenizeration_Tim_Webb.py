# Tim Webb
# Tokenizer Lab

filename = "Main"

file = open(f'{filename}.jack', 'r')
Lines = file.readlines()

keyword_list = ['class','constructor','method','function','int','boolean','char','void','var','static','field','let','do','if','else','while','return','true','false','null','this']
symbol_list = ['(',')','[',']','{','}',',',';','=','.','+','-','*','/','&','|','~','<','>']
###alphabet = ["_","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

with open(f'{filename}t.txt', 'a') as f:
    f.write('<tokens>')
    f.close()

def isSymbol(x):
    if x in symbol_list:
        return True
    else:
        return False
def isKeyword(x):
    if x in keyword_list:
        return True
    else:
        return False



# Flags for knowing if we're in a multi-line comment or constant string
mlc = False
constStr = False

# For each line in all the lines in the input program
for line in Lines:
    buff = ''
    # For each n (character) in a line, increment i
    for i, n in enumerate(line):
        next_char = line[min((i+1, len(line)-1))]
        # n = current character
        prev_char = line[min((i-1, len(line)-1))]
        
        # Once we see a '//' comment, we can break, there is no code after this,
        # break to new line
        if n == '/' and next_char == '/':
            break
        
        # Once we see a '/', then '*' we must go through the entire
        # comment until we find a '*', then '/' because there could 
        # still be valid code after this. None of this is recorded however,
        # its comment.
        
        # /* HELLO */ int a = 9;
        if n == '/' and next_char == '*':
            mlc = True
            continue # Continuing here, skipping over comment.
        elif n == '/' and prev_char == '*':
             mlc = False
             continue # Continuing here, skipping over last comment.
        elif mlc == True:
            continue # Continuing here, skipping over comment.
 
        # Constant String Logic. If we're in a quotation, we're going to
        # continue and keep adding each letter until we find the last quotation.
        if constStr == True and n == "\"":
            constStr = False
            with open(f'{filename}t.txt', 'a') as f:
                    f.write('\n\t<stringConstant> ' + buff + ' </stringConstant>')
                    f.close()
            buff = ''
            continue              
        elif n == "\"":
            constStr = True
            continue
        elif constStr == True:
            buff += n
            continue
          
        # Basic adding of letters or numbers to generate each word, number,
        # or symbol to save to the output
        if n in alphabet or n.isdigit():
            buff += n
            if next_char.isalpha() or next_char.isdigit():
                continue

        # Checking word after a terminator space or symbol is found
        if (next_char == ' ') or (next_char == '\n') or (isSymbol(next_char) 
                                                         or isSymbol(n)):
            # If the character we're on is a symbol, write as symbol
            if isSymbol(n):
                #write to output as symbol
                with open(f'{filename}t.txt', 'a') as f:
                    f.write('\n\t<symbol> ' + n + ' </symbol>')
                buff = ''
                continue
            # If the buff is in the keywords, write as keyword
            elif isKeyword(buff):
                #write to output as keyword
                with open(f'{filename}t.txt', 'a') as f:
                    f.write('\n\t<keyword> ' + buff + ' </keyword>')
                    f.close()
                buff = ''
                continue
            # If buff is a digit, it's an integerConstant
            elif buff.isdigit():
                #write to output as intConst
                with open(f'{filename}t.txt', 'a') as f:
                    f.write('\n\t<integerConstant> ' + buff + ' </integerConstant>')
                    f.close()
                    continue
            # Finally, if word begins with '_' or an alphabet
            elif buff[:1] in alphabet:
                #write to output as identifier
                with open(f'{filename}t.txt', 'a') as f:
                    f.write('\n\t<identifier> ' + buff + ' </identifier>')
                    f.close()
                buff = ''
                continue
            
with open(f'{filename}t.txt', 'a') as f:
    f.write('\n</tokens>')
    f.close()