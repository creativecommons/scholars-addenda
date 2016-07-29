import noembargo
import embargo
import retaincc
import mit

handlers = {'noembargo': noembargo.NoEmbargo,
            'embargo': embargo.Embargo,
            'retaincc': retaincc.RetainCC,
            'mit': mit.MIT,
            }
