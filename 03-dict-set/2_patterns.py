from collections import OrderedDict


def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            print(f"{names}\n")
            return names
        case {'type': 'book', 'api': 1, 'author': name}:
            print(f"{name}\n")
            return [name]
        case {'type': 'book'}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:
            print(f"{name}\n")
            return [name]
        case _:
            raise ValueError(f'Invalid record: {record!r}')


b1 = dict(api=1, author='Douglas Hofstadter', type='book', title='Gödel, Escher, Bach')
get_creators(b1)

b2 = OrderedDict(api=2, type='book', title='Python in a Nutshell',
                 authors='Martelli Ravenscroft Holden'.split())
get_creators(b2)

get_creators({'type': 'book', 'pages': 770})

get_creators('Spam, spam, spam')
