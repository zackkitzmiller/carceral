import json

from tornado.web import RequestHandler

from carceral import words


class CarceralHandler(RequestHandler):

    def get(self):
        query = self.get_argument('q', None)
        num_suggestions = int(self.get_argument('n', 3))
        suggestions = {
            'recommended': []
        }

        for n in xrange(0, num_suggestions):
            suggestions['recommended'].append(
                words.build_word(
                    words.get_service_name()
                )
            )

        if query is not None:
            suggestions['not_recommended'] = []
            suggestions['not_recommended'].append(
                {
                    'name': words.slugify(query),
                    'meta': {}
                }
            )

        resp = {
            'suggestions': suggestions
        }

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(resp))

