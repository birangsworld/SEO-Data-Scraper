import pandas as pd
import requests
from bs4 import BeautifulSoup


def sheetToDataFrame(filePath):
    inputCSV = pd.read_csv(filePath)
    return inputCSV


def requestPage(pageRoute):
    requestResponse = requests.get(pageRoute)

    if requestResponse.status_code == 200:
        pageContent = requestResponse.text
        return pageContent
    else:
        print(
            f"Failed to Retrieve Page Content, Status Code: {requestResponse.status_code}"
        )
        return None


def makeSoup(pageContent):
    soup = BeautifulSoup(pageContent, "html.parser")
    return soup


def extractTitle(soup):
    pageTitle = str(soup.title.string)
    print(pageTitle)
    return pageTitle


def extractDescription(soup):
    metaDescription = soup.find("meta", {"name": "description"})
    if metaDescription:
        return metaDescription["content"]
    else:
        return "None"
    
def extractHeadings(soup):
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    allHeadings = []

    for heading in headings:
        headingContent = heading.string
        allHeadings.append(headingContent)

    allHeadings = ', '.join(map(str, allHeadings))

    return allHeadings


def extractTextContent(soup):
    allContentTags = soup.find_all("p")

    allContents = []

    for contentTag in allContentTags:
        content = contentTag.string
        allContents.append(content)

    allContents = ', '.join(map(str, allContents))

    return allContents


def extractImageAlts(soup):
    allImages = soup.find_all("img", alt=True)

    allImageAlts = []
    
    for image in allImages:
        altText = image["alt"]
        allImageAlts.append(altText)

    allImageAlts = ', '.join(map(str, allImageAlts))

    return allImageAlts

def extractLinks(soup):
    allLinks = soup.find_all("a")
    linkAnchors = []
    linkDestinations = []

    for link in allLinks:
        linkAnchor = link.string
        linkAnchors.append(linkAnchor)

    for link in allLinks:
        linkDestination = link["href"]
        linkDestinations.append(linkDestination)

    return linkAnchors, linkDestinations


def mergeLinks(linkAnchors, linkDestinations):
    anchorDestPairs = []
    for i, anchor in enumerate(linkAnchors):
        for j, destination in enumerate(linkDestinations):
            if i == j:
                anchorDestPair = f"{linkAnchors[i]}| {linkDestinations[j]}"
                anchorDestPairs.append(anchorDestPair)

    anchorDestPairs = ', '.join(map(str, anchorDestPairs))

    return anchorDestPairs


def scrapeWebPage(pageURL):
    pageContent = requestPage(pageURL)
    soup = makeSoup(pageContent)
    title = extractTitle(soup)
    metaDescription = extractDescription(soup)
    headings = extractHeadings(soup)
    contents = extractTextContent(soup)
    imageAlts = extractImageAlts(soup)
    anchorTexts, linkDestinations = extractLinks(soup)
    linkPairs = mergeLinks(anchorTexts, linkDestinations)

    pageData = [title, pageURL, metaDescription, headings, contents, imageAlts, linkPairs]

    return pageData


def exportFinalResults(pageDataFrame):
    pageDataFrame.to_csv("output.csv", index= False)

    return None



def main():
    finalExport = []
    filePath = "./input.csv"    
    dataFrame = sheetToDataFrame(filePath)
    urls = dataFrame["URLs"]
    urlsArray = urls.values.tolist()
    for url in urlsArray:
        tempData = scrapeWebPage(url)
        export = f"'Title': {tempData[0]}, 'URL': {tempData[1]}, 'Meta_Description': {tempData[2]}, 'Headings': {tempData[3]}, 'Content': {tempData[4]}, 'imageAlts': {tempData[5]}, 'Links': {tempData[6]}"
        finalExport.append(export)

    with open("output.txt", "w") as file:
        file.write(str(finalExport))
    

        

main()
