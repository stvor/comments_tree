import calendar
import random
import datetime

from django.core.management import BaseCommand

from core.models import Comment


class Command(BaseCommand):
    START_CNT = 10
    MAX_LEVELS = 3
    MAX_CHILDREN = 5

    def create_comment(self, parent, level):
        now = datetime.datetime.now()
        one_year_ago = now - datetime.timedelta(days=365)
        comment = Comment.objects.create(text=random_text(), is_deleted=False, parent=parent)
        comment.created = random_datetime(one_year_ago, now)
        comment.save(update_fields=['created'])

        if level < self.MAX_LEVELS and random.randint(0, 100) < 40:
            children_cnt = random.randint(0, self.MAX_CHILDREN)
            children = []
            for j in range(children_cnt):
                child = self.create_comment(comment, level + 1)
                children.append(child)
            setattr(comment, 'children', children)
        return comment

    def show_tree(self, comments, level):
        for comment in comments:
            if hasattr(comment, 'children'):
                print(' + ' * level, comment, len(comment.children))
                if comment.children:
                    self.show_tree(comment.children, level + 1)
            else:
                print(' ' * level, comment, 0)

    def handle(self, *args, **options):
        tree = []
        for i in range(self.START_CNT):
            comment = self.create_comment(None, level=0)
            tree.append(comment)
        self.show_tree(tree, 0)

def random_letter(is_vowel):
    if is_vowel:
        letters = en_vowel_frequency
        num = random.randint(1, 401)
    else:
        letters = en_consonant_frequency
        num = random.randint(1, 598)

    counter = 0
    for letter in letters:
        if counter <= num <= counter + letter[1]:
            return letter[0]
        counter += letter[1]
    return '*'


def random_syllable():
    case = random.randint(0, 2)
    syllable = ""
    if case == 0:
        syllable = random_letter(True) + random_letter(False)
    if case == 1:
        syllable = random_letter(False) + random_letter(True)
    if case == 2:
        syllable = random_letter(False) + random_letter(True) + random_letter(False)
    return syllable


def random_word():
    word = ""
    length = random.randint(3, 8)
    for i in range(length):
        word += random_syllable()
    return word


def random_sentence(capitalize=True, ending="."):
    sentence = ""

    length = random.randint(3, 12)
    if ending == "?":
        length = random.randint(2, 5)

    for i in range(length):
        sentence = sentence + random_word()
        if i < length - 1:
            sentence += " "

    if capitalize:
        sentence = sentence.capitalize()
    sentence += ending
    return sentence


def random_text():
    text = random_sentence()
    length = random.randint(2, 5)
    for i in range(length):
        text += random_sentence()
        if i < length - 1:
            text += " "
    return text


en_vowel_frequency = [
    ('a', 82), ('e', 127), ('i', 70), ('o', 75), ('u', 27), ('y', 20),
]
en_consonant_frequency = [
    ('b', 15), ('c', 28), ('d', 43), ('f', 22), ('g', 20), ('h', 61), ('j', 1), ('k', 7), ('l', 40),
    ('m', 24), ('n', 68), ('p', 19), ('q', 1), ('r', 60), ('s', 63), ('t', 90), ('v', 10), ('w', 24),
    ('x', 1), ('z', 1),
]


def convert_datetime(dt):
    return calendar.timegm(dt.timetuple())


def random_datetime(start, end):
    unix_start = convert_datetime(start)
    unix_end = convert_datetime(end)
    ts = random.randint(unix_start, unix_end)
    return datetime.datetime.utcfromtimestamp(ts)
