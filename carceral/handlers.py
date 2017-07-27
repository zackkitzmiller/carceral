import json

from tornado.web import RequestHandler
from tornado_swagger import swagger

from carceral import words


class CarceralHandler(RequestHandler):

    @swagger.operation(nickname='generate')
    def get(self):
        """
            @param q: the query to generate a service name for
            @param num-words: number of words in the service name
            @param n: number of suggestions to return
            @type q: string
            @type num-words: int
            @type n: int
            @return 200: list or results
            @raise 400: invalid input
        """

        query = self.get_argument('q', None)
        num_suggestions = int(self.get_argument('n', 3))
        num_words_per_suggestion = int(self.get_argument('num-words', 1))
        suggestions = {
            'recommended': []
        }

        for n in xrange(0, num_suggestions):
            suggestions['recommended'].append(
                words.get_service_name(num_words_per_suggestion)
            )

        if query is not None:
            suggestions['not_recommended'] = ['jquery']
            suggestions['not_recommended']
            suggestions['not_recommended'].append(
                words.slugify(query)
            )

        resp = {
            'suggestions': suggestions
        }

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(resp))
