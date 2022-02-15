from requests import get as webRequest
from bs4 import BeautifulSoup
from re import sub 
from string import punctuation, digits 

### Class ###

class WordCounter:
    charlist = punctuation.replace('\'','') + str(digits) + '\\n'

    """The main class of the module
    Will take a website URL and perform various statistically analysis
    Alternatively, can take a string of words
    """
    def __init__(self, content: str, url: bool=True) -> None:
        self.content: str = content
        self.isWebpage: str = url
        if self.isWebpage:
            self.url = content
            self.getWebPage()
        self.wordCounts: dict = None
    
    def getWebPage(self) -> None:
        """Parses the URL given to the class and sets up the content with the
        webpage content

        Raises:
            ConnectionError: Raised on failure to get a 200 status code from 
                             the web request
        """
        res = webRequest(self.url)
        if res.status_code == 200:
            self.soup = BeautifulSoup(res.content, 'html.parser')
            # Parse the soup
            text = self.soup.find_all(text=True)
            self.content = ""
            # Non-text sections to ignore
            blacklist = [
                '[document]','noscript','header','html',
                'meta','head','input','script','style'
            ]
            for content in text:
                if content.parent.name not in blacklist:
                    try:
                        self.content += " " + sub('['+self.charlist+']', '', content)
                    except:
                        continue
        
        else:
            raise ConnectionError(f"Webpage could not be retrieved: {res.status_code}")

    def computeWordCounts(self) -> None:
        """Computers the number of time each word appears in the content
        """
        # creates dictionary with number of words
        self.wordCounts = {}
        for text in self.content.split(" "):
            if text == '':
                continue
            if text in self.wordCounts:
                self.wordCounts[text] += 1
            else:
                self.wordCounts[text] = 1

    def getContents(self) -> str:
        """Returns the contents of the word counter

        Returns:
            str: string contents 
        """

    def getWordCounts(self) -> dict:
        """Returns the full count dictionary

        If not computed it will compute the numbers before returning

        Returns:
            dict: mapping of word to number of occurences in the content
        """
        if self.wordCounts == None:
            self.computeWordCounts()
        return self.wordCounts

    def getWordCount(self, word : str) -> int:
        """Returns the number of times a word appears in the content

        If not computed it will compute the numbers before returning

        Args:
            word (str): Word to check for.
        Returns:
            int: number of occurences of the given word in the content
        """
        if self.wordCounts == None:
            self.computeWordCounts()
        if word not in self.wordCounts:
            return 0
        return self.wordCounts[word]

    def getTopNWords(self, n: int = 10):
        """Returns the number of times the top n (default 10) words appear in the given content

        If not computed it will compute the numbers before returning

        Args:
            n (int, optional): number of words to return. Defaults to 10.
        Returns:
            int: number of occurences of the top n words in the content
        """
        if self.wordCounts == None:
            self.computeWordCounts()
        return dict(sorted(self.wordCounts.items(), key=lambda i: i[1],reverse=True)[:n])

    
### MAIN ###
# Example running
if __name__ == "__main__":
    exampleURL = 'http://example.com/'
    counter = WordCounter(exampleURL)

    print(f"Top 5 words in '{exampleURL}' are: {''.join([key + ':' + str(value) for key, value in counter.getTopNWords(5).items()])}.")
    print(f"The word 'example' appears in '{exampleURL}' {counter.getWordCount('example')} times.")
    
    stringContent = "Foo Bar FooBar Foo Bat Bob Ban Foop Foo Foobar Foop BarFoo"
    counter2 = WordCounter(stringContent,url=False)
    print(f"Top word in the given string is: {''.join(counter2.getTopNWords(1).keys())}.")
    print(f"The word 'Foo' appears in the given string {counter2.getWordCount('Foo')} times.")
    
#   ʕ •ᴥ•ʔ
