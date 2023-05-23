import ahocorasick

word_list_path = './app/utils/sensitive_words.txt'
class MessageProcessor:
    wordList = []
    replaceWord = "*屏蔽*"
    def __init__(self):
        # Initialize the sensitive word list
        with open(word_list_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 去除行尾的换行符和空白字符
                self.wordList.append(line)
        
        # Initialize the acTree
        self.acTree = ahocorasick.Automaton()
        for index, word in enumerate(self.wordList):
            self.acTree.add_word(word, (index, word))
        self.acTree.make_automaton()

    def process(self, message):
        ''' Process the message, replace the sensitive words with *屏蔽*
        :param message: the message to be processed
        '''
        processed_message = message
        for i in self.acTree.iter(message):
            processed_message = processed_message.replace(i[1][1], self.replaceWord)
        return processed_message
    

message_processor = MessageProcessor()
