## Nazli Uzgur

from __future__ import with_statement # for Python 2.5 and 2.6
import urllib
# import PyPDF2
import re, collections
import os
import tokenize
import pdftotextmaybe
import getCategory
import difflib

def init():

    ########################################################
    ### Convert pdf to txt with pdf miner 
    ########################################################

    # input the file name
    filename = raw_input("File name: ")
    
    # need this to work in case no input
    if filename == " ":
        return ("", "")
    # is .pdf; need to convert to .txt
    elif filename.endswith(".pdf"):
        resume = pdftotextmaybe.convert(filename)
    else: 
        resume = readFile(filename).lower()
    # return resume as a string with different sections
    # good enough for the demo, lol
    return resume

def category(resume):
    # Return the category that appears the most
    (cat, score) = getCategory.mainCategoryAndScore(resume)
    return (cat, score)

def overall(resume):
    overall = getCategory.getCategoriesAverage(resume)
    return overall

def programmingScore(resume):
    proScore = getCategory.programmingScore(resume)
    return proScore

def gpaScoreCalculator(gpa):
    gpa_unweighted = gpa / 4.00
    gpa_scaled = gpa_unweighted * 10
    return gpa_scaled

def gpaScore(word_tokens):
    score = 0
    gpaFound = False
    for token in word_tokens:
        if "gpa" in token.lower():
            index = word_tokens.index(token)
            try:
                if "/" in word_tokens[index + 1]:
                    words = word_tokens[index + 1].split("/")
                    gpa = float(words[0])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True
                else:
                    gpa = float(word_tokens[index + 1])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True
            except:
                if "/" in word_tokens[index - 1]:
                    words = word_tokens[index - 1].split("/")
                    gpa = float(words[0])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True
                else:
                    gpa = float(word_tokens[index - 1])
                    score = gpaScoreCalculator(gpa)
                    gpaFound = True

    # a resume with a GPA might indicate a lower GPA
    if gpaFound == False: score = gpaScoreCalculator(2.5)
    return score

def collegeScore(word_tokens):
    university = ["Carnegie Mellon University", "Princeton University",
    "Harvard University", "Yale University", "Columbia University",
    "Stanford University", "University of Chicago",
    "Massachusetts Institute of Technology", "Duke University",
    "University of Pennsylvania", "California Institute of Technology",
    "Johns Hopkins University", "Dartmouth College", "Northwestern University",
    "Brown University", "Cornell University", "Vanderbilt University",
    "Washington University in St. Louis", "Rice University",
    "University of Notre Dame", "University of California-Berkeley",
    "Emory University", "Georgetown University",
    "University of California-Los Angeles", "University of Southern California",
    "University of Virginia", "Tufts University", "Wake Forest University",
    "University of Michigan-Ann Arbor", "Boston College",
    "University of North Carolina-Chapel Hill", "New York University", "University of Rochester",
    "Brandeis University", "College of William and Mary", "Georgia Institute of Technology",
    "Case Western Reserve University", "University of California-Santa Barbara",
    "University of California-San Diego", "Boston University", "Rensselaer Polytechnic Institute",
    "Tulane University", "University of California-Davis", "University of Illinois-Urbana-Champaign",
    "University of Wisconsin-Madison", "Lehigh University", "Northeastern University",
    "Pennsylvania State University-University Park", "University of Florida", "University of Miami",
    "Ohio State University-Columbus", "Pepperdine University", "University of Texas-Austin",
    "University of Washington", "Yeshiva University", "George Washington University",
    "University of Connecticut", "University of Maryland-College Park",
    "Worchester Polytechnic Institute", "Clemson University", "Purdue University-West Lafayette",
    "Southern Methodist University", "Syracuse University", "University of Georgia",
    "Brigham Young University-Provo", "Fordham University", "University of Pittsburgh",
    "University of Minnesota-Twin Cities", "Texas A&M University-College Station", "Virginia Tech",
    "American University", "Baylor University", "Rutgers, The State University of New Jersey-New Brunswick",
    "Clark University", "Colorado School of Mines", "Indiana University-Bloomington",
    "Michigan State University", "Stevens Institute of Technology", "University of Delaware",
    "University of Massachusetts-Amherst", "Miami University-Oxford", "Texas Christian University",
    "University of California-Santa Cruz", "University of Iowa", "Marquette University",
    "University of Denver", "University of Tulsa", "Binghamton University-SUNY",
    "North Carolina State University-Raleigh", "Stony Brook University-SUNY",
    "SUNY College of Environmental Science and Forestry", "University of Colorado-Boulder",
    "University of San Diego", "University of Vermont", "Florida State University", "Saint Louis University",
    "University of Alabama", "Drexel University", "Loyola University Chicago", "University at Buffalo-SUNY",
    "Auburn University", "University of Missouri", "University of Nebraska-Lincoln",
    "University of New Hampshire", "University of Oregon", "University of Tennessee",
    "Illinois Institute of Technology", "Iowa State University", "University of Dayton",
    "University of Oklahoma", "University of San Francisco", "University of South Carolina",
    "University of the Pacific", "Clarkson University", "Duquesne University", "Temple University",
    "University of Kansas", "University of St. Thomas", "University of Utah", "University of Arizona",
    "University of California-Riverside", "The Catholic University of America", "DePaul University",
    "Michigan Technological University", "Seton Hall University", "Colorado State University", "New School",
    "Arizona State University-Tempe", "Louisiana State University-Baton Rouge", "University at Albany-SUNY",
    "University of Arkansas", "University of Illinois-Chicago", "University of Kentucky",
    "George Mason University", "Hofstra University", "Howard University", "Ohio University",
    "Oregon State University", "New Jersey Institute of Technology",
    "Rutgers, The State University of New Jersey-Newark", "University of Cincinnati",
    "University of Mississippi", "University of Texas-Dallas", "Washington State University",
    "Kansas State University", "Missouri University of Science & Technology", "St. John Fisher College",
    "Illinois State University", "Oklahoma State University", "San Diego State University",
    "University of Alabama-Birmingham", "Adelphi University", "Southern Illinois University-Carbondale",
    "St. John's University", "University of Maryland-Baltimore County", "University of Massachusetts-Lowell",
    "University of South Florida", "Virginia Commonwealth University", "University of La Verne",
    "Biola University", "Florida Institute of Technology", "Immaculata University",
    "Maryville University of St. Louis", "Mississippi State University", "University of Hawaii-Manoa",
    "University of Rhode Island", "Ball State University", "Texas Tech University",
    "University of Central Florida", "University of Idaho", "University of Louisville", "University of Maine",
    "University of Wyoming", "Andrews University", "Azusa Pacific University", "Edgewood College",
    "Kent State University", "West Virginia University", "Pace University",
    "St. Mary's University of Minnesota", "University of New Mexico", "University of North Dakota",
    "University of South Dakota", "Bowling Green State University", "North Dakota State University",
    "South Dakota State University", "University of Alabama-Huntsville", "University of Houston",
    "University of Nevada-Reno", "University of North Carolina-Greensboro", "Western Michigan University",
    "Widener University", "Central Michigan University", "East Carolina University",
    "South Carolina State University", "University of Missouri-Kansas City",
    "University of North Carolina-Charlotte", "Ashland University",
    "Indiana University-Purdue University-Indianapolis", "Louisiana Tech University",
    "New Mexico State University", "University of Colorado-Denver"]
    i = 0
    score = 15
    for college in university:
        for word in word_tokens:
            if(word != "University"):
                if(word in college):
                    i = university.index(college)
                    i = i + 1
                    break   
        if(i != 0):
            break
    if(i < 20):
        score -= 0
    if(i == 0): # if the university isn't here
        score -= 13
    return score

def wordCountScore(tokens):
    score = 10
    # number of words
    count = 0
    # word count
    for tok in tokens:
        if tok != "":
            count += 1
    # 475 words -> average amount of words on one page
    if count == 400: score -= 0
    # accounts for resumes too short and too long
    else:
        score -= min(abs(400 - count) / 20, 5)
    return score

def degreeScore(word_tokens):
    score = 10
    desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
    word_tokens_lower = [x.lower() for x in word_tokens]
    # searches for similar words
    degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
    close_match_fail = False
    close_match = ""
    if degree == []:
        for word in word_tokens_lower:
            if (desiredDegree.lower() in word):
                close_match_fail = True
                close_match = word
                break
    stop_search = False
    while (not stop_search):
        if degree == [] and close_match_fail == False: 
            answer2 = raw_input("There are no matches. Search again? (Y/N) \n")
            if answer2 == "Y" or answer2 == "y" or answer2 == "yes" or answer2 == "Yes":
                desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
                degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
            else:
                stop_search = True
        else:
            if close_match_fail == True:
                print("Closest match to " + desiredDegree + " is " +
                close_match + ".")
                stop_search = True
            else:
                print("Closest match to " + desiredDegree + " is " +
                    degree[0] + ".")
                stop_search = True
    close_match_fail = False
    close_match = ""
    stop_search = False
    while (not stop_search):
        answer1 = raw_input("Would you like to search for another degree? (Y/N)\n")
        if answer1 == "Y" or answer1 == "y" or answer1 == "yes" or answer1 == "Yes":
            desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
            degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
            if degree == []:
                for word in word_tokens_lower:
                    if (desiredDegree.lower() in word):
                        close_match_fail = True
                        close_match = word
                        break
            if degree == [] and close_match_fail == False:
                answer3 = raw_input("There are no matches. Search again? (Y/N) \n")
                if answer3 == "Y" or answer3 == "y" or answer3 == "yes" or answer3 == "Yes":
                    desiredDegree = raw_input("Degree level needed (i.e. 'phd', 'ba', 'bachelor'): ")
                    degree = difflib.get_close_matches(desiredDegree.lower(), word_tokens_lower)
                else:
                    stop_search = True
            else:  
                if close_match_fail == True:
                    print("Closest match to " + desiredDegree + " is " +
                        close_match + ".")
                else:
                    print("Closest match to " + desiredDegree + " is " +
                            degree[0] + ".")
        else:
            stop_search = True
    degreeFound = False
    answer4 = raw_input("Would you like to search the word 'degree'? (Y/N) \n")
    if answer4 == "Y" or answer4 == "y" or answer4 == "yes" or answer4 == "Yes":
        print("Searching 'degree' and returning adjacent words...") 
        for word in word_tokens_lower:
            if ("degree" in word):
                index = word_tokens_lower.index(word)
                if index - 1 >= 0 and index + 1 < len(word_tokens_lower):
                    prev_word = word_tokens_lower[index - 1]
                    after_word = word_tokens_lower[index + 1]
                    print("Word before 'degree': " + prev_word)
                    print("Word after 'degree': " + after_word)
                    degreeFound = True
                    break
                elif index - 1 >= 0 and index + 1 >= len(word_tokens_lower):
                    prev_word = word_tokens_lower[index - 1]
                    print("Word before 'degree': " + prev_word + "\n")
                    print("No word found after 'degree'.")
                    degreeFound = True
                    break
                elif index - 1 < 0 and index + 1 < len(word_tokens_lower):
                    after_word = word_tokens_lower[index + 1]
                    print("Word after 'degree': " + after_word + "\n")
                    print("No word found before 'degree'.")
                    degreeFound = True
                    break
                else:
                    # should not happen
                    print("The only word in the resume is 'degree'.")
                    degreeFound = True
                    break
        if degreeFound == False:
            print("The word 'degree' does not appear in the resume.")
    else:
        pass
    answer = raw_input("Is this what you are looking for? (Y/N)\n")
    # yes if desired degree found else degree not attained or present
    if answer == "yes" or answer == "Y" or answer == "y" or answer == "Yes": score -= 0
    else: score -= 10
    return score

def sectionScore(resume):
    section_tokens = tokenize.input_file_words(resume,[])
    currentIndex = -1
    wordCount = [0,0,0]
    for x in section_tokens: 
        x = x.lower()
        if(x.strip("!@#$%^&*()_+|}{:?") in ["work experience", "employment", "experience"] and currentIndex != 0):
            currentIndex = 0
        elif(x.strip("!@#$%^&*()_+|}{:?") in ["publications", "projects", "research"] and currentIndex != 1):
            currentIndex = 1
        elif(x.strip("!@#$%^&*()_+|}{:?") in ["leadership","leadership experience"] and currentIndex != 2):
            currentIndex = 2    
        elif(x.strip("!@#$%^&*()_+|}{:?") in ["education","activites","skils", "interests", "extracurricular", "honors", "references", "awards", "acheivements"]):
            currentIndex = -1
        else:
            wordCount[currentIndex] += 1

        print(wordCount)

    return  min(((sum(wordCount) - min(wordCount))) / 450.0, 1.0) * 10

def main(resume):
    # initialize variables 
    # have the words as tokens in a list
    tokens = tokenize.input_file_lines(resume,[])
    word_tokens = tokenize.input_file_words(resume,[])
    score = 0
    
    # get email
    email = ""
    for token in word_tokens:
        if "@" in token:
            email = token
            break

    # category score
    (cat, category_score) = category(resume)
    print category_score

    # overall score
    overall_score = overall(resume)
    print overall_score

    # programming languages score
    programming_score = programmingScore(resume)
    print programming_score

    # GPA score
    gpa_score = gpaScore(word_tokens)
    print gpa_score

    # university score
    college_score = collegeScore(word_tokens)
    print college_score

    # word count score
    word_count_score = wordCountScore(tokens)
    print word_count_score

    # degree score
    degree_score = degreeScore(word_tokens)
    print degree_score

    # sectional score
    section_score = sectionScore(resume)
    print section_score

    print "finished parsing"
    score = category_score + overall_score + programming_score + \
            gpa_score + college_score + word_count_score + \
            degree_score + section_score

    return (cat, score, email)

def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

resume = init()
if resume != "":
    print main(resume)
