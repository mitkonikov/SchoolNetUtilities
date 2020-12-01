import re

def clearCurlyBrackets(text: str) -> str:
    i = 1
    startPos = -1
    while i < len(text):
        if (text[i-1] == '{' and text[i] == '{' and startPos == -1):
            startPos = i-1
        elif (text[i-1] == '}' and text[i] == '}' and startPos != -1):
            leftText = text[:startPos]
            rightText = text[(i+1):]
            text = leftText + rightText
            i = startPos - 1
            startPos = -1
        
        i += 1
    
    # clean some leftovers
    text = re.sub("(\{\{)|(\}\})", "", text)

    return text

def clearLinks(text):
    i = 1
    startPos = -1
    while i < len(text):
        if (text[i-1] == '[' and text[i] == '[' and startPos == -1):
            startPos = i-1
        elif (text[i-1] == ']' and text[i] == ']' and startPos != -1):
            startPos = -1
        elif text[i] == '|' and startPos != -1:
            leftText = text[:startPos]
            rightText = text[(i+1):]
            text = leftText + rightText
            i = startPos - 1
            startPos = -1
        
        i += 1
    
    # clean some leftovers
    text = re.sub("(\[\[)|(\]\])", "", text)

    return text