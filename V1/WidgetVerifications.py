entryObj = None

def limit_length(new_value, length):
    return len(new_value) <= length

def is_number(char):
    try:
        int(char)
        return True
    except ValueError:
        return False


def Verification_Processo(allText, char):
    return (char.isdigit() or is_number(char) or allText == "" or char == "") and limit_length(allText, 9)