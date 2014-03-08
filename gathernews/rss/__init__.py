# improvements to be made:
# - multithreading
# - support for more RSS feeds
# - better organization of tables for large entries
# - support for databases other than SQLite3


# before you make improvements, get FindNews & News-Project working
# Here's the question you're trying to answer:
#  - How can I make it easier to find valuable news stories?
#
# Here's the answer that you have to the question:
#  - Track popular topics over time. Once you do that, then you can
#  - focus only on topics you care about. Topics can be extracted as
#  - named entities. Named entities are people, locations, or organizations.
#  -
#  - Topics can span across traditional sections like Sports or World News
#  -
#  - Currently, topics are understood as similar words with similar
#  - grammatical framing. Alternatively, topics are understood as entities
#  - which are in some way linked to other entities.
#  -
#  - My approach is different because it takes a much simpler approach.
#  - A story either involves a named entity or it does not. That named
#  - entity is the topic. This is a simplifying assumption but the neat
#  - thing about this assumption is that it gives us a definitive unit
#  - of analysis. When we have a definite unit of analysis, we are able
#  - to build things.
#
#  - For example, entities in the same document as other entities could be
#  - related topics. Like 'Canada' & 'Jack Dempsey' because of the citation.
#  - Related topics could be used to build 'meta topics' where often cited
#  - named entities become 'sections' in the newspaper or maybe just a way
#  - to organize top stories within a section. 

import duplicates
import io
import new_tables
import populate_tables
import threads
