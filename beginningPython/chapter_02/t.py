#!/usr/bin/python

screen_width = 100
sentence = raw_input("Sentence: ")
text_width = len(sentence)
box_width = text_width + 4
margin_width = (screen_width - text_width) / 2
print margin_width

print
print " " * margin_width + "+" + "-" * (box_width - 2) + "+"
print " " * margin_width + "| " + " " * text_width +  " |"
print " " * margin_width + "| " + sentence + " |"
