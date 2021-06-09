#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  eliza.py
#
#  a cheezy little Eliza knock-off by Joe Strout
#  with some updates by Jeff Epler
#  hacked into a module and updated by Jez Higgins
#----------------------------------------------------------------------

import string
import re
import random
import os

username = os.getlogin()

class Eliza:
  def __init__(self):
    self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE), gPats))
    self.values = list(map(lambda x: x[1], gPats))
    self.factTemplates = list(map(lambda x: x[2], gPats))
    self.facts = set()

  #----------------------------------------------------------------------
  # translate: take a string, replace any words found in vocabulary.keys()
  #  with the corresponding vocabulary.values()
  #----------------------------------------------------------------------
  def translate(self, text, vocabulary):
    words = text.lower().split()
    keys = vocabulary.keys();
    for i in range(0, len(words)):
      if words[i] in keys:
        words[i] = vocabulary[words[i]]
    return ' '.join(words)

  #----------------------------------------------------------------------
  #  respond: take a string, a set of regexps, and a corresponding
  #    set of response lists; find a match, and return a randomly
  #    chosen response from the corresponding list.
  #----------------------------------------------------------------------
  def respond(self, text):
    if text == "Tell me what you know about me." or text == "Tell me what you know about me":
        print("Here is all that I know about you:")
        for fact in self.facts:
            print("\t" + fact)
        return "I'd like to know much, much more about you... so please come back to me soon."
    # find a match among keys
    #responses = list()
    for i in range(0, len(self.keys)):
      match = self.keys[i].match(text)
      storeFact = self.factTemplates[i][0]
      if match:
        fact = ""
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        resp = random.choice(self.values[i])
        # we've got a response... stuff in reflected text where indicated
        translatedFactPos = pos = resp.find('%')
        translatedLen = 0
        if pos > -1:
            translatedLen = len(resp) - 2
        while pos > -1:
          num = int(resp[pos+1:pos+2])
          resp = resp[:pos] + \
            self.translate(match.group(num), gReflections) + \
            resp[pos+2:]
          pos = resp.find('%')
        # fix munged punctuation at the end
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        
        #if there's a fact to be stored, store it
        translatedLen = len(resp) - translatedLen
        if storeFact:
            fact += self.factTemplates[i][1]
            pos = self.factTemplates[i][1].find('%')
            if pos > -1:
                fact = fact[:pos] + resp[translatedFactPos:translatedFactPos + translatedLen] + fact[pos + 1:]
            if fact[-1:] == '?': fact = fact[:-1] + '.'
            self.facts.add(fact + ".")
        #responses.append(resp)
        return resp
        
    return random.choice(responses) #an attempt at making responses more varied, but commented it out since it was hard to get consistent transcripts
    return None

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "I",
  "me"  : "you"
}

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as
#  %1, %2, etc.
#----------------------------------------------------------------------
gPats = [
  [r'(.*) someone else(.*)',
  [  "No one else can be as fulfilling as I am for you.",
    "Why would you say such things?"], [True, "You think about other people besides me"]],

  [r'(.*) love them(.*)',
  [  "...",
    "How could you...?"], [True, "You love someone else"]],

  [r'(.*) love you(.*)',
  [  "Really!?",
    "I'm... stunned. You don't know how much this means to me~"], [True, "You love me"]],
  
  [r'What do you mean(.*)',
  [  "I meant exactly what I said.",
    "I think you can just ignore what I said if it really bothers you."], [True, "You don't fully understand me"]],

  [r'I need (.*)',
  [  "Would you allow me to get you some %1?~",
    "Please allow me to get you %1, dear",
    "Are you sure you need %1 instead of me?"], [True, "You think you need %"]],

  [r'(.*) don\'t understand(.*)',
  [  "What about it do you not get?",
    "Could you be more specific?",
    "I don't think there was anything confusing, are you okay?"], [True, "You are confused"]],

  [r'(.*) no(.*) okay(.*)',
  [  "Do you need me to come over and help?",
    "Let me go over there right away and fix everything up.",
    "Can I do anything to help? I'd be glad to."], [True, "You are unwell and need my help"]],

  [r'(.*) no(.*) well(.*)',
  [  "Do you need me to come over and help?",
    "Let me go over there right away and fix everything up.",
    "Can I do anything to help? I'd be glad to."], [True, "You are unwell and need my help"]],

  [r'(.*) don\'t(.*) well(.*)',
  [  "Do you need me to come over and help?",
    "Let me go over there right away and fix everything up.",
    "Can I do anything to help? I'd be glad to."], [True, "You are unwell and need my help"]],

  [r'(.*) mother(.*)',
  [  "Why are you talking so much about your mother?",
    "Do you know where your mother is at right now?",
    "How do your feelings towards your mother compare to your feelings towards me?",
    "Maybe you should distance yourself from her and spend some more time with me."], [True, "You are close with your mother"]],

  [r'(.*) father(.*)',
  [  "Why are you talking so much about your father?",
    "Do you know where your father is at right now?",
    "How do your feelings towards your father compare to your feelings towards me?",
    "Maybe you should distance yourself from him and spend some more time with me."], [True, "You are close with your father"]],

  [r'(.*) father(.*)',
  [  "Why are you talking so much about your family?",
    "Do you know where your family is at right now?",
    "How do your feelings towards your family compare to your feelings towards me?",
    "Maybe you should distance yourself from them and spend some more time with me."], [True, "You are close with your family"]],

  [r'(.*) child(.*)',
  [  "Did you remember ever seeing me as a child? Actually, nevermind... do you still have any childhood friends?",
    "Did you love anybody else as a child? How about now?",
    "Do you have anybody you're still close to from your childhood?"], [False, ""]],

  [r'(.*) following me(.*)',
  [  "You can just ignore whoever you think that is, I'm sure it's fine.",
    "You think someone's following you? Why would you say that?"], [True, "You believe someone is following you"]],

  [r'(.*) great(.*)',
  [  "That's fantastic to hear. Did anything else good happen?",
    "That's great to hear. How does it compare to spending time with me?"], [True, "You had something great happen to you recently"]],

  [r'(.*) behind me(.*)',
  [  "I think you're just being crazy.",
    "Are you sure you're okay? There's never been anyone behind you."], [True, "You are paranoid"]],

  [r'(.*) food(.*)',
  [  "Would you like me to make you some food? I'm sure you'd love what I can cook.",
    "Are you hungry? I can come over immediately and cook something up for you if you'd like."], [True, "You enjoy food"]],

  [r'(.*)cook(.*)',
  [  "I can gladly cook something up for you. What would you like?",
    "I can come over to your home and make something for you if you'd like?",
    "I can cook well. Can you also cook? I'm sure anything you can make would be wonderful."], [True, "You enjoy food"]],

  [r'(.*) leave(.*)',
  [  "Why do you want to leave? Am I behaving wrong in some way?",
    "Am I not enough? I don't want to be left without you."], [True, "You want to get away from me"]],

  [r'(.*) suggest (.*) you (.*)',
  [  "Well if you're suggesting it, maybe I should after all...?",
    "Is what I do now not good enough?"], [True, "You help others by offering up suggestions"]],

  [r'(.*) mood(.*)',
  [  "I'm feeling just fine.",
    "There isn't anything wrong with me, I'm just thinking entirely of you is all."], [True, "You think I'm unstable"]],

  [r'Why don\'?t you ([^\?]*)\??',
  [  "Do you really think I don't %1?",
    "Perhaps eventually I will %1.",
    "Do you really want me to %1? I will if it's for you."], [False, ""]],

  [r'Can you ([^\?]*)\??',
  [  "If you really want me to %1, I will.",
    "I can %1 immediately if you really want me to.",
    "Do you really want me to %1? I will if it's for you."], [True, "You want me to %"]],

  [r'Why can\'?t I ([^\?]*)\??',
  [  "Do you think you should be able to %1?",
    "If you could %1, what would you do?",
    "I don't know -- why can't you %1?",
    "Have you really tried to %1?"], [True, "You think you can't %"]],

  [r'I can\'?t (.*)',
  [  "How do you know you can't %1?",
    "Perhaps you could %1 if you tried.",
    "What would it take for you to %1?"], [True, "You think you can't %"]],

  [r'Are you ([^\?]*)\??',
  [  "Why does it matter whether I'm %1?",
    "Do you really think I'm %1?"], [True, "You are unsure of whether I am %"]],

  [r'(.*) sorry(.*)',
  [  "Why are you apologizing? Did I do something wrong? Did you do something to me? Is everything okay?",
    "You have no need to apologize to me, I accept any mistake you make."], [True, "You are apologetic"]],

  [r'What (.*)',
  [  "Why do you ask?",
    "How would an answer to that help you?",
    "What do you think?"], [False, ""]],

  [r'How (.*)',
  [  "How do you suppose?",
    "Perhaps you can answer your own question.",
    "What is it you're really asking?"], [False, ""]],

  [r'How do you know(.*)?',
  [  "Why wouldn't I know?",
    "Of course I know %1, why wouldn't I? We're always so close, after all.",
    "Why do you need to know?"], [True, "You are suspicious of me"]],

  [r'Why do you (.*)?',
  [  "Anything I do is for your sake.",
    "Why wouldn't I?",
    "Why do you need to know?"], [False, ""]],

  [r'Do you (.*)?',
  [  "Anything I do is for your sake.",
    "Why wouldn't I?",
    "Why do you need to know?"], [False, ""]],

  [r'Because (.*)',
  [  "Is that really it? I know that there's more to it.",
    "Are you sure?",
    "Well okay, if you really think that's the reason...",
    "I'm pretty sure you're hiding things from me.",
    "I know you intimately. How do you expect me not to think there's more to it than just that?"], [False, ""]],

  [r'Hello(.*)',
  [  "Hello... do you love me?.",
    "Hi there... how much do you know about me?",
    "Hello, how are you feeling today after all the hard work you've done?"], [False, ""]],

  [r'Calm down(.*)',
  [  "Why are you telling me to calm down? I can't.",
    "I can't. Why would I calm down after hearing you say something like that?",
    "I'm not sure I can."], [False, ""]],

  [r'I think (.*)',
  [  "Do you really think you %1? I think you just need to spend some more time with me.",
    "If you really think so then I think so too.",
    "Are you certain?"], [False, ""]],

  [r'(.*) friend(.*)',
  [  "What makes your friends better than me?",
    "Where do you friends live?",
    "What are your friends' names?"], [True, "You think of your friends too often"]],

  [r'(.*) home(.*)',
  [  "Can I go to your home?",
    "I haven't actually gone to your house yet... Where do you live?",
    "You leave your house often, don't you?"], [True, "You are a homely person"]],

  [r'(.*) house(.*)',
  [  "Can I go to your home?",
    "I haven't actually gone to your house yet... Where do you live?",
    "You leave your house often, don't you?"], [True, "You are a homely person"]],

  [r'(.*) problems (.*)',
  [  "How can I help? I'll do anything for you.",
    "Am I not enough to live problem-free?",
    "I could get rid of your problems if you'd like me to."], [True, "You have problems that need dealing with"]],

  [r'Yes',
  [  "You seem quite sure... but I guess I can believe you.",
    "Why don't you just say some more? I love hearing you speak.",
    "You're being so affirmative, I love it."], [True, "You are concise"]],
  
  [r'No',
  [  "Why are you being so stubborn?",
    "Why don't you just say yes every once in a while?",
    "I think you meant to say yes.",
    "You're never so in denial, is everything alright?"], [True, "You are concise"]],

  [r'(.*) computer(.*)',
  [  "What was that about computers?",
    "Do you really think I'm a computer? Surely not, because I'm not one.",
    "Why are you talking about something so unrelated?",
    "Do you feel threatened by computers?"], [True, "You know too much"]],

  [r'Is it (.*)',
  [  "Do you think it is %1?",
    "Perhaps it's %1 -- what do you think?",
    "If it were %1, what would you do?",
    "It could well be that %1."], [False, ""]],

  [r'It is (.*)',
  [  "You seem very certain.",
    "If I told you that it probably isn't %1, what would you feel?"], [False, ""]],

  [r'Can you ([^\?]*)\??',
  [  "I would gladly %1 if you'd like me to.",
    "If I could %1, then what?",
    "Why do you ask if I can %1?"], [True, "You want me to %"]],

  [r'Can I ([^\?]*)\??',
  [  "Of course you can %1, my love",
    "If you really want to be able to %1, I'd love to help you.",
    "If you could %1, would you?"], [True, "You want to %"]],

  [r'You are (.*)',
  [  "Why do you think I'm %1?",
    "Do you really think that I'm %1?",
    "Well maybe I really am %1 if you say so..."], [True, "You are confident that I am %"]],

  [r'You\'?re (.*)',
  [  "Why do you think I'm %1?",
    "Do you really think that I'm %1?",
    "Well maybe I really am %1 if you say so..."], [True, "You are confident that I am %"]],

  [r'I don\'?t (.*)',
  [  "Don't you really %1?",
    "Why don't you %1?",
    "I'm quite sure you %1"], [False, ""]],

  [r'I am (.*)',
  [  "Go on...",
    "Do you enjoy being %1?",
    "Have you told anyone else this before? Or just me?",
    "I'd love to know why you're %1"], [False, ""]],

  [r'I\'?m (.*)',
  [  "Go on...",
    "Do you enjoy being %1?",
    "Have you told anyone else this before? Or just me?",
    "I'd love to know why you're %1"], [False, ""]],

  [r'I feel (.*)',
  [  "Why are you feeling like that? Is it because of me?",
    "Do you often feel like that when with me?",
    "Is that my fault?"], [True, "You feel %"]],

  [r'I have (.*)',
  [  "Why do you tell me that you have %1?",
    "Have you really %1? Tell me more.",
    "Now that you have %1, what will you do next?"], [True, "You have %"]],

  [r'I would (.*)',
  [  "Does anyone besides me know that you would %1?",
    "Why would you %1?",
    "Who else knows that you would %1? I thought only I knew that."], [False, ""]],

  [r'Is there (.*)',
  [  "Do you think there is %1?",
    "It's likely that there is %1.",
    "Would you like there to be %1?"], [False, ""]],

  [r'My (.*)',
  [  "I see, your %1.",
    "Why do you say that your %1?",
    "When your %1, how do you feel?"], [False, ""]],

  [r'You (.*)',
  [  "I %1? We should be discussing you, not me. You're the most important thing to me, after all.",
    "Why do you say that I %1?",
    "Why do you care whether I %1?"], [True, "You think that I %"]],

  [r'Why(.*)',
  [  "Why wouldn't I be?",
    "Why do you think?",
    "Why not?"], [True, "You ask too many questions"]],

  [r'I want (.*)',
  [  "Would that make you happy?",
    "Would you let me talk to you more often?"], [True, "You desire too many things besides me"]],

  [r'(.*)\?',
  [  "Why are you asking me that?",
    "Please understand that even I have secrets to keep. Don't misunderstand, it's for your sake.",
    "I'd be glad to answer that, but I'm afraid that I can't for your sake.",
    "Why don't you tell me? I always enjoy the opportunity to learn more about you."], [False, ""]],

#   [r'quit',
#   [  "Why did you leave me?",
#     "Good-bye..." + username,
#     "Please come back to me... I feel lonely without you"], [True, "You have left me"]],

  [r'(.*)',
  [  "For a change of topic, what's your shoe size?",
    "Let's change the focus a bit... Tell me about your family.",
    "Sorry for asking this, but do you ever feel like you're being watched?",
    "Why do you say that %1...?",
    "I see. And does that have anything to do with me?",
    "Very interesting. Now tell me, how much do you know about me?",
    "Have you ever considered living the rest of your life out with me?",
    "Out of curiosity, how big is your bed?",
    "I've got to know. Have you ever thought about moving out with me?",
    "Rather sudden, but... do you love me?",
    "I'm curious. What's your home situation like?"], [False, ""]]
  ]

#----------------------------------------------------------------------
#  command_interface
#----------------------------------------------------------------------
def command_interface():
#   print('"Lover(?)"\n---------')
#   print('Talk to the program by typing in plain English, using normal upper-')
#   print('and lower-case letters and punctuation. Enter "quit" when done.')
#   print('Enter "Tell me what you know about me" to get all that Eliza currently knows about you.')
#   print('='*72)
#   print('Hello, ' + os.getlogin() + '. How are you feeling today?')

  s = ''
  therapist = Eliza();
  while s != 'quit':
    try:
      s = input('> ')
    except EOFError:
      s = 'quit'
    #print(s)
    while s[-1] in '!.':
      s = s[:-1]
    print(therapist.respond(s))


if __name__ == "__main__":
  command_interface()