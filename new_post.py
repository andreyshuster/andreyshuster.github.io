#!/usr/bin/env python

import sys
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
f = open("_posts/{0}-{1}.md".format(current_date, sys.argv[1]), "w+")
contents = """---
layout: post
date: {1}
---
""".format(sys.argv[1], current_date)
f.write(contents)
f.close()

         

