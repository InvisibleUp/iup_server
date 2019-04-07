''' Generate an atom feed from the root of the site '''
from flask import render_template
from flatten_dict import flatten, unflatten

def tab_reducer(k1, k2):
	if k1 is None:
		return k2
	else:
		return k1 + "\t" + k2

def tab_splitter(flat_key):
	return flat_key.split("\t")

def generate_atom(pages):
    # Reformat pages dict to be a list of every unique page that has a date,
    # sorted by date and capped to 10 entries
    a = flatten(pages, reducer=tab_reducer)
    a = {k.replace('\t', '_', k.count('\t') - 1): v for k, v in a.items() if k.count('\t') > 1}
    a = unflatten(a, splitter=tab_splitter)
    a = list(a.values())
    a = list(filter(lambda x: 'date' in x, a))
    a = sorted(a, key=lambda x: x['date'], reverse=True)
    a = a[:10]

    return render_template(
        'atom.xml',
        entries=a,
        lastupdated=a[0]['date']
    )