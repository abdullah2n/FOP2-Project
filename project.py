# Muhammad Abdullah 
# CMS ID - 460901

import feedparser
from datetime import datetime
import string

# Problem 1
# Class for representing a news story.
# Stores information such as GUID, title, description, link, and publication date.
class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# Problem 2
# Abstract class for a trigger based on a phrase.
# Checks if a given phrase is present in the text.
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        words = text.lower().split()
        phrase_words = self.phrase.split()
        for i in range(len(words)):
            if words[i:i+len(phrase_words)] == phrase_words:
                return True
        return False


# Problem 3
# Subclass of PhraseTrigger.
# Fires when a news item's title contains a given phrase.
class TitleTrigger(PhraseTrigger):
    def evaluate(self, news_story):
        return self.is_phrase_in(news_story.get_title())


# Problem 4
# Subclass of PhraseTrigger.
# Fires when a news item's description contains a given phrase.
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, news_story):
        return self.is_phrase_in(news_story.get_description())


# Problem 5
# Abstract class for a trigger based on time.
# Represents a specific time point in EST.
class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")


# Problem 6
# Subclasses of TimeTrigger.
# BeforeTrigger fires when a story is published strictly before the trigger’s time,
# and AfterTrigger fires when a story is published strictly after the trigger’s time.
class BeforeTrigger(TimeTrigger):
    def evaluate(self, news_story):
        return news_story.get_pubdate() < self.time

class AfterTrigger(TimeTrigger):
    def evaluate(self, news_story):
        return news_story.get_pubdate() > self.time


# Problem 7
# Trigger that inverts the output of another trigger.
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, news_story):
        return not self.trigger.evaluate(news_story)


# Problem 8
# Trigger that fires if both inputted triggers would fire on that item.
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, news_story):
        return self.trigger1.evaluate(news_story) and self.trigger2.evaluate(news_story)


# Problem 9
# Trigger that fires if either one (or both) of its inputted triggers would fire on that item.
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, news_story):
        return self.trigger1.evaluate(news_story) or self.trigger2.evaluate(news_story)


# Problem 10
# Function to filter news stories based on triggers.
def filter_stories(stories, triggerlist):
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    return filtered_stories


# Problem 11
# Function to read trigger configurations from a file and create trigger objects.
# Modifies the main_thread to use the trigger list specified in the configuration file.
def read_trigger_config(filename):
    trigger_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            parts = line.split(',')
            if parts[0] == 'ADD':
                triggerlist = [trigger_dict[name] for name in parts[1:]]
            else:
                name, trigger_type = parts[0], parts[1]
                args = parts[2:]
                trigger = None
                if trigger_type == 'TITLE':
                    trigger = TitleTrigger(*args)
                elif trigger_type == 'DESCRIPTION':
                    trigger = DescriptionTrigger(*args)
                elif trigger_type == 'AFTER':
                    trigger = AfterTrigger(*args)
                elif trigger_type == 'BEFORE':
                    trigger = BeforeTrigger(*args)
                elif trigger_type == 'NOT':
                    trigger = NotTrigger(trigger_dict[args[0]])
                elif trigger_type == 'AND':
                    trigger = AndTrigger(trigger_dict[args[0]], trigger_dict[args[1]])
                elif trigger_type == 'OR':
                    trigger = OrTrigger(trigger_dict[args[0]], trigger_dict[args[1]])
                trigger_dict[name] = trigger
    return triggerlist
