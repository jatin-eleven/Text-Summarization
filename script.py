
"""
EXTRACTIVE TEXT SUMMARIZATION 

How to do Text Summarization :
    - Text Cleaning
    - Sentance Tokenization
    - Word Tokenization
    - Word-Frequency Table
    - Summarization
"""


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from heapq import nlargest


text = """The Indian Space Research Organisation is the national space agency of India, headquartered in Bangalore. It operates under the Department of Space (DOS) which is directly overseen by the Prime Minister of India, while the Chairman of ISRO acts as the executive of DOS as well. ISRO is India's primary agency performing tasks related to space-based applications, space exploration and the development of related technologies. It is one of six government space agencies in the world which possess full launch capabilities, deploy cryogenic engines, launch extraterrestrial missions and operate large fleets of artificial satellites.
The Indian National Committee for Space Research (INCOSPAR) was established by Jawaharlal Nehru under the Department of Atomic Energy (DAE) in 1962, on the urging of scientist Vikram Sarabhai, recognising the need in space research. INCOSPAR grew and became ISRO in 1969, within DAE. In 1972, the government of India set up a Space Commission and DOS, bringing ISRO under it. The establishment of ISRO thus institutionalised space research activities in India. It since then has been managed by DOS, which governs various other institutions in India in the domain of astronomy and space technology.

ISRO built India's first satellite, Aryabhata, which was launched by the Soviet Union in 1975. In 1980, ISRO launched satellite RS-1 onboard its own SLV-3, making India the sixth country to be capable of undertaking orbital launches. SLV-3 was followed by ASLV, which was subsequently succeeded by development of many medium-lift launch vehicles, rocket engines, satellite systems and networks enabling the agency to launch hundreds of domestic and foreign satellites and various deep space missions for space exploration.

ISRO has the world's largest constellation of remote-sensing satellites and operates the GAGAN and NAVIC satellite navigation systems. It has sent two missions to the Moon and one to Mars.

The agency's goals for the near future include expanding its satellite fleet, landing a rover on Moon, sending humans into space, development of a semi-cryogenic engine, sending more uncrewed missions to the Moon, Mars, Venus and the Sun, and deployment of more space telescopes in orbit to observe cosmic phenomena and space beyond the Solar System. Long-term plans include development of reusable launchers, heavy and super heavy launch vehicles, deploying a space station, sending exploration missions to the outer planets and asteroids and crewed missions to moons and planets.

ISRO's programs have played a significant role in the socio-economic development of India and have supported both civilian and military domains in various aspects including disaster management, telemedicine and navigation and reconnaissance missions. ISRO's spinoff technologies also have found many crucial innovations for India's engineering and medical industries."""

# text = """
# Earth is our home planet. Scientists believe Earth and its moon formed around the same time as the rest of the solar system. They think that was about 4.5 billion years ago. Earth is the fifth-largest planet in the solar system. Its diameter is about 8,000 miles. And Earth is the third-closest planet to the sun. Its average distance from the sun is about 93 million miles. Only Mercury and Venus are closer. Earth has been called the "Goldilocks planet." In the story of "Goldilocks and the Three Bears," a little girl named Goldilocks liked everything just right. Her porridge couldn't be too hot or too cold. And her bed couldn't be too hard or too soft. On Earth, everything is just right for life to exist. It's warm, but not too warm. And it has water, but not too much water. Earth is the only planet known to have large amounts of liquid water. Liquid water is essential for life. Earth is the only planet where life is known to exist. From space, Earth looks like a blue marble with white swirls and areas of brown, yellow, green and white. The blue is water, which covers about 71 percent of Earth's surface. The white swirls are clouds. The areas of brown, yellow and green are land. And the areas of white are ice and snow.
# The equator is an imaginary circle that divides Earth into two halves. The northern half is called the Northern Hemisphere. The southern half is called the Southern Hemisphere. The northernmost point on Earth is called the North Pole. The southernmost point on Earth is called the South Pole. Humans have known that Earth is round for more than 2,000 years! The ancient Greeks measured shadows during summer solstice and also calculated Earth's circumference. They used positions of stars and constellations to estimate distances on Earth. They could even see the planet's round shadow on the moon during a lunar eclipse. (We still can see this during lunar eclipses.) Today, scientists use geodesy, which is the science of measuring Earth's shape, gravity and rotation. Geodesy provides accurate measurements that show Earth is round. With GPS and other satellites, scientists can measure Earth's size and shape to within a centimeter. Pictures from space also show Earth is round like the moon. Even though our planet is a sphere, it is not a perfect sphere. Because of the force caused when Earth rotates, the North and South Poles are slightly flat. Earth's rotation, wobbly motion and other forces are making the planet change shape very slowly, but it is still round. Earth is our home planet. Earth is our home planet. Earth is our home planet.
# """
print("\n\nORIGINAL TEXT : \n", text, "\n")


nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
stopwords = list(STOP_WORDS)

# formation of tokens from the text
tokens = [token.text for token in doc]


punctuation = punctuation + "\n"


word_frequency = {}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation and word.text.lower() not in "\n":
            if word.text not in word_frequency.keys():
                word_frequency[word.text] = 1
            else:
                word_frequency[word.text] += 1

max_frequency = max(word_frequency.values())


# # for getting the NORMALIZED FREQUENCY we will divide the each word frequency by max_frequency
for word in word_frequency.keys():
    word_frequency[word] = word_frequency[word]/max_frequency




# # # ---------------------------- SENTANCE TOKENIZATION -----------------------------------
sentance_tokens = [sent for sent in doc.sents]

sentance_scores = {}
for sent in sentance_tokens:
    for word in sent:
        if word.text in word_frequency.keys():
            # # here adding the normalized frequency of each word present in the sentances
            # # and store in the sentance_score dict....
            # # eg : NF(word1) + NF(word2) + NF(word3)
            if sent not in sentance_scores.keys():
                sentance_scores[sent] = word_frequency[word.text]
            else:
                sentance_scores[sent] += word_frequency[word.text]



# # getting the 30% of the sentance
select_length = int(len(sentance_tokens)*0.3)


# # finding the largest sentace_score sentance in the text...
summary = nlargest(select_length, sentance_scores, key=sentance_scores.get)


# # maintaining the order of the sentance
# # order will define meaning of the sentances in summary...
indexing = []
for i in summary:
    for j in range(len(sentance_tokens)):
        if str(i) == str(sentance_tokens[j]) and str(i) not in indexing:
            indexing.append(j)
            break 
# removing the repeated sentances...
indexing = set(indexing)


final_summary = []
for i in indexing:
    final_summary.append(str(sentance_tokens[i]))


summary = ' '.join(final_summary)
print("\n\nSUMMARY : ", summary, "\n\n")


