import json

from tornado.web import RequestHandler
from tornado_swagger import swagger

from carceral import words
from carceral.dzk import get_dzk_dictionary
from carceral.slugify import slugify
from carceral.wolf import get_wolfram_dictionary_multi_word

STD_MODE = "standard"
DZK_MODE = "drunkzackkitz"
WOLF_MODE = "wolframalpha"
VALID_MODES = [STD_MODE, DZK_MODE, WOLF_MODE]


class CarceralHandler(RequestHandler):

    @swagger.operation(nickname='generate')
    def get(self):
        """
            @param q: the query to generate a service name for
            @param num-words: number of words in the service name
            @param n: number of suggestions to return
            @param mode: which dict to use (one of drunkzackkitz or standard)
            @type mode: string
            @type q: string
            @type num-words: int
            @type n: int
            @return 200: list or results
            @raise 400: invalid input
        """
        mode = self.get_argument('mode', STD_MODE)
        if mode not in VALID_MODES:
            self.set_status(400)
            self.finish({
                "reason": 'invalid mode selected'
                ' mode must be one of drunkzackkitz, wolframalpha'
                ' or standard (default)'
                ' if you feel you have received this message in error'
                ' call 917-945-3487'
            })
            return

        query = self.get_argument('q', None)
        if query is None:
            self.set_status(400)
            self.finish({
                "reason": 'you didnt supply q. q is required'
                ' for processing this request.'
                ' if you feel you have received this message in error'
                ' call 917-945-3487'
            })
            return

        num_suggestions = int(self.get_argument('n', 3))
        num_words_per_suggestion = int(self.get_argument('num-words', 1))
        suggestions = {
            'recommended': []
        }

        if mode == STD_MODE:
            dictionary = words.get_standard_dictionary()
        elif mode == DZK_MODE:
            dictionary = get_dzk_dictionary()
        elif mode == WOLF_MODE:
            dictionary = get_wolfram_dictionary_multi_word(query)

        for n in xrange(0, num_suggestions):
            suggestions['recommended'].append(
                words.get_words_from_dictionary(
                    dictionary, num_words=num_words_per_suggestion
                )
            )
            suggestions['recommended'] = list(set(filter(
                lambda x: x != "", suggestions['recommended']
            )))

        if query is not None:
            suggestions['not_recommended'] = ['jquery']
            suggestions['not_recommended']
            suggestions['not_recommended'].append(
                slugify(query)
            )

        resp = {
            'suggestions': suggestions
        }

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(resp))
