'''
    Author: Bhavya Budania
    Following script is written to scrape all the GK & Current Affairs Q&A for a given month
    from the site: www.gktoday.in
    You just need to provide the link where links for the Q&A for that month are given.
    E.G. Suppose you want to get all Q&A for March, 2016 then you can just given
        www.gktoday.in/gk/current-affairs-questions-answers/page/... (whatever page has March,2016 links)
'''
# Importing required libraries
#!/usr/bin/env python
import urllib, re
import bs4
from random import shuffle
from threading import Thread

'''
    Function: This function is responsible for fetching the questions and
              corresponding answers from the given link.
'''
def getQA(link, finalLST):
    print 'Fetching Q&A from: ', link
    html = urllib.urlopen(link).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')

    aws  = soup.find_all(attrs={'class': 'lesson-content'})[0].find_all(attrs={'class': 'answer'})
    flst = []               # Final result

    for ans in aws:
        qlst = []           # Question and Options
        tmplst = []         # Temporary List that we will use

        sflg = False        # Whether Show Answer has come
        oflg = False        # Whether options have been shown

        for child in ans.parent.parent.descendants:

            if type(child) == bs4.NavigableString and len(child) > 1:
                if sflg == False and oflg == False:

                    if child.startswith('[A]'):
                        oflg = True                 # Now we know options have started

                        qstmt = ' '.join(tmplst)    # We have got our question statement
                        qlst.append(qstmt)

                        tmplst = []                 # Re-initialise
                        tmplst.append(child)

                    else:                           # Simply add to the temp list
                        tmplst.append(child)

                elif sflg == False and oflg == True:

                        if child.startswith('Show Answer'):
                            sflg = True
                            opD = ' '.join(tmplst)  # Option-D is done
                            tmplst = []             # Re-initialise

                            # Now we have got all our options
                            qlst.append([opA, opB, opC, opD])

                        elif child.startswith('[B]'):
                            opA = ' '.join(tmplst)  # Option-A is done
                            tmplst = []             # Re-initialise
                            tmplst.append(child)
                        elif child.startswith('[C]'):
                            opB = ' '.join(tmplst)  # Option-B is done
                            tmplst = []             # Re-initialise
                            tmplst.append(child)
                        elif child.startswith('[D]'):
                            opC = ' '.join(tmplst)  # Option-C is done
                            tmplst = []             # Re-initialise
                            tmplst.append(child)
                        else:
                            tmplst.append(child)

                elif sflg == True and oflg == True:
                    tmplst.append(child)

        answer = ','.join(tmplst)       # Now we have got our full answer
        flst.append([qlst, answer])     # Add this question and answer to the final list

    for item in flst:
        finalLST.append(item)

def main():
    mth = raw_input('Please enter the month you require: ').lower()
    cnt = int(raw_input('How many links are there ? : '))

    flnk  = []
    for i in range(0, cnt):
        url = raw_input('Please enter link #%d: ' % (i+1))

        html = urllib.urlopen(url).read()           # Now it's a

        soup = bs4.BeautifulSoup(html, 'html.parser')

        lnks  = soup.find_all(attrs={'class': "inside_post column content_width"})[0].find_all(attrs={'class': "widget widget_archive"})[0].find_all('a')


        for link in lnks:
            idx = link.get('href', None).find(mth)
            if idx != -1 :
                flnk.append(link.get('href', None))

    # Now we will scrape the questions and corresponding answers from these links
    finalLST = []
    threadList = []

    # Making threads
    for link in flnk:
        th = Thread(target=getQA, args=(link,finalLST))
        th.start()
        threadList.append(th)

    for th in threadList:
        th.join()           # Wait for all the threads to finish

    tempLST = [finalLST[i] for i in range(len(finalLST))]
    shuffle(tempLST)
    finalLST = tempLST

    print 'All Q&A for the month',mth.capitalize(),'have been fetched.'

    qfname = raw_input('Please enter the file name to store questions: ')
    afname = raw_input('Please enter the file name to store answers: ')

    qfhandle = open(qfname, 'wb')
    afhandle = open(afname, 'wb')

    cnt = 0
    for item in finalLST:
        try:
            qfhandle.write(u' '.join(['Q%d.' % (cnt+1), item[0][0]]).encode('utf-8').strip())
            qfhandle.write('\n')
            for opt in item[0][1]:
                qfhandle.write(opt.encode('utf-8').strip())
                qfhandle.write('\n')
            qfhandle.write('\n')

            afhandle.write(u' '.join(['Ans %d.' % (cnt+1), item[1]]).encode('utf-8').strip())
            afhandle.write('\n\n')
            cnt = cnt + 1
        except IndexError:
            pass

    qfhandle.close()
    afhandle.close()


if __name__ == '__main__':
    main()
