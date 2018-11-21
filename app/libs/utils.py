def isbnOrKey(word):
    wordType = 'key'
    if len(word) == 13 and word.isdigit():
        wordType = 'isbn'
    shortWord = word.replace('-', '')
    if '-' in word and len(shortWord) == 10 and shortWord.isdigit():
        wordType = 'isbn'
    return wordType
