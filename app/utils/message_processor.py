import ahocorasick

# def build_actree(wordlist):
#  actree = ahocorasick.Automaton()
#  for index, word in enumerate(wordlist):
#   actree.add_word(word, (index, word))
#  actree.make_automaton()
#  return actree

# if __name__ == '__main__':
#  actree = build_actree(wordlist=wordlist)
#  sent_cp = sent
#  for i in actree.iter(sent):
#   sent_cp = sent_cp.replace(i[1][1], "**")
#   print("屏蔽词：",i[1][1])
#  print("屏蔽结果：",sent_cp)

file_path = './app/utils/sensitive_words.txt'
class MessageProcessor:
    wordList = []
    def __init__(self):
        # Initialize the sensitive word list
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 去除行尾的换行符和空白字符
                self.wordList.append(line)
        
        # Initialize the acTree
        self.acTree = ahocorasick.Automaton()
        for index, word in enumerate(self.wordList):
            self.acTree.add_word(word, (index, word))
        self.acTree.make_automaton()

    def process(self, message):
        processed_message = message
        for i in self.acTree.iter(message):
            processed_message = processed_message.replace(i[1][1], "*屏蔽*")
        return processed_message
    
    
    
message_processor = MessageProcessor()
